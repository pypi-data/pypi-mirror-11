# -*- coding: utf-8 -*-
# distutils: language = c++
# cython: boundscheck=False, wraparound=False, cdivision=True


__author__ = "Johannes Köster"
__license__ = "MIT"


import math
from collections import namedtuple
from functools import partial
import numpy as np
cimport numpy as np
from cython cimport view
from cpython.exc cimport PyErr_CheckSignals
from cython.operator cimport dereference as deref, preincrement as inc
from libc.math cimport log10, exp, log, log1p
cimport libcpp.map
cimport libcpp.pair
cimport libcpp.set
from libc.stdlib cimport malloc, free
from libc.math cimport fabs
from concurrent.futures import ThreadPoolExecutor

import logging

cimport peanut.common as common
cimport peanut.alignment as alignment
cimport peanut.rescue as rescue
from peanut.stats import stats


cdef extern from "limits.h":
    int INT_MAX


ctypedef int (*get_best_hits_type)(int[:,:], int, int, int[:], int[:,:], double, int, bint) nogil
ctypedef void (*rescue_apply_type)(int[:,:], int[:], int, double, double, int, int, int, int, bint) nogil


PostprocessedHits = namedtuple("PostprocessedHits", "hits cigar_address cigars cigar_sizes hits_address offset window_size")

cdef int COL_REFID = 0
cdef int COL_POS = 1
cdef int COL_SCORE = 2
cdef int COL_PAIR_SCORE = 3
cdef int COL_MAPQ = 4

DEF MAX_MAPQ = 60
cdef double LOG_TO_PHRED = -10 / log(10)

cdef void delete_hits(hits):
    """Delete hits explicity to free memory."""
    hits.positions.clear()
    hits.scores.clear()
    hits.query_hits_pos.clear()


cdef unsigned int** get_reference_sequences(references):
    """Create pointer array to reference sequences."""
    cdef:
        list encoded_refs = references.encoded
        unsigned int[:] encoded
        int i
        unsigned int** ret = <unsigned int**>malloc(len(encoded_refs) * sizeof(unsigned int*))

    for i in range(len(encoded_refs)):
        encoded = encoded_refs[i]
        ret[i] = &encoded[0]
    return ret


cdef inline int get_mate(int query) nogil:
    """Get the mate of a query."""
    return query + (1 - query % 2 * 2)


cdef inline int get_revcomp(int refid) nogil:
    """Get the reverse complement refid."""
    return refid + (1 - refid % 2 * 2)


# deprecated
cdef inline int adjust_pos(int reference_size, int reference_offset, int refid, int pos, int query_size) nogil:
    """Adjust the position for bam output."""
    return reference_size - pos - 1 if not common.is_revcomp(refid) else pos - query_size - reference_offset + 1


ctypedef int (*get_max_alignment_score_type)(int, int[:]) nogil


cdef int get_max_alignment_score(int query, int[:] queries_sizes) nogil:
    return queries_sizes[query]


cdef int get_max_alignment_score_paired(int query, int[:] queries_sizes) nogil:
    return queries_sizes[query] + queries_sizes[get_mate(query)]


cdef int[:,:] get_unique_hits(hits, int reference_count, int[:] reference_sizes, int[:] reference_offsets, int[:] queries_sizes, int query_count, int[:] ref_hits_address, int[:,:] hits_query_start, int offset, int window):
    """Collect hits and remove duplicates."""

    cdef:
        int refid, reference_size, reference_offset, x
        int[:] positions, scores, query_start
        int[:,:] ref_hits
        # variables for inner loop
        int query, pos, score, hmin, hmax, i, j, qsize, ref_hits_count
        libcpp.map.map[int, int] qhits
        libcpp.map.map[int, int].iterator qhits_iterator
        libcpp.pair.pair[int, int] hit
        int total_hits_count = 0

    # count total hits
    for refid in range(reference_count):
        positions = hits.positions[refid]
        scores = hits.scores[refid]
        query_start = hits.query_hits_pos[refid]
        with nogil:
            for query in range(offset, offset + window):
                hmin = query_start[query]
                hmax = query_start[query+1]
                collect_unique_query_reference_hits(
                    hmin, hmax, qhits, positions, scores
                )
                total_hits_count += qhits.size()

    cdef:
        int[:,:] hits_unique = np.empty((total_hits_count, 4), dtype=np.int32)

    ref_hits_address[0] = 0

    for refid in range(reference_count):
        positions = hits.positions[refid]
        scores = hits.scores[refid]
        ref_hits_count = positions.shape[0]
        query_start = hits.query_hits_pos[refid]

        with nogil:
            ref_hits = hits_unique[ref_hits_address[refid]:ref_hits_address[refid] + ref_hits_count, :]
            reference_size = reference_sizes[refid]
            reference_offset = reference_offsets[refid]

            ref_hits[:, COL_REFID] = refid

            i = 0
            for query in range(offset, offset + window):
                # retreive interval
                hmin = query_start[query]
                hmax = query_start[query+1]
                qsize = queries_sizes[query]
                # adjust start to elements written so far
                hits_query_start[refid, query - offset] = i
                collect_unique_query_reference_hits(
                    hmin, hmax, qhits, positions, scores
                )

                qhits_iterator = qhits.begin()
                while qhits_iterator != qhits.end():
                    hit = deref(qhits_iterator)
                    pos = hit.first
                    score = hit.second
                    ref_hits[i, COL_POS] = common.pos_to_bam_pos(reference_size, reference_offset, refid, pos, qsize)
                    ref_hits[i, COL_SCORE] = score
                    ref_hits[i, COL_PAIR_SCORE] = score
                    i += 1
                    inc(qhits_iterator)

            # record the end for the last query
            hits_query_start[refid,query - offset + 1] = i
            # record the start address for the next ref_hits
            ref_hits_address[refid + 1] = ref_hits_address[refid] + i
        ###########
    return hits_unique


cdef void collect_unique_query_reference_hits(int hmin, int hmax, libcpp.map.map[int, int]& qhits, int[:] positions, int[:] scores) nogil:
    cdef:
        int j, pos, score

    qhits.clear()
    for j in range(hmin, hmax):
        pos = positions[j]
        score = scores[j]
        if qhits.count(pos) == 0:
            qhits[pos] = score

cdef int estimate_template_length(int pos, int mate_pos, int qsize, int mate_qsize) nogil:
    if mate_pos < pos:
        return pos + qsize - mate_pos
    else:
        return mate_pos + mate_qsize - pos


cdef void score_mates(int reference_count, int insert_size, int insert_size_error, int[:,:] hits_unique, int[:] ref_hits_address, int[:,:] hits_query_start, int[:] queries_sizes, int window, int offset) nogil:
    """Adjust scores considering mate pairing."""

    cdef:
        int refid, revcomp_refid, query, hmin, hmax, mate_hmin, mate_hmax, pos, mate_pos, mate_score, mate, best_mate_score, qsize, mate_qsize
        int isize_min = insert_size - insert_size_error
        int isize_max = insert_size + insert_size_error
        int dist
        int[:,:] rhits
        int[:,:] revcomp_rhits
        int[:] query_start
        int[:] revcomp_query_start

    for refid in range(reference_count):
        rhits = hits_unique[ref_hits_address[refid]:ref_hits_address[refid + 1]]
        revcomp_refid = get_revcomp(refid)
        revcomp_rhits = hits_unique[ref_hits_address[revcomp_refid]:ref_hits_address[revcomp_refid + 1]]
        query_start = hits_query_start[refid]
        revcomp_query_start = hits_query_start[revcomp_refid]
        for query in range(offset, offset + window):
            hmin = query_start[query - offset]
            hmax = query_start[query - offset + 1]
            mate = get_mate(query)
            mate_hmin = revcomp_query_start[mate - offset]
            mate_hmax = revcomp_query_start[mate - offset + 1]
            qsize = queries_sizes[query]
            mate_qsize = queries_sizes[mate]
            for i in range(hmin, hmax):
                pos = rhits[i, COL_POS]
                best_mate_score = 0
                for j in range(mate_hmin, mate_hmax):
                    mate_pos = revcomp_rhits[j, COL_POS]
                    mate_score = revcomp_rhits[j, COL_SCORE]
                    dist = estimate_template_length(pos, mate_pos, qsize, mate_qsize)
                    # TODO make use of hits being sorted by position?
                    if isize_min <= dist and dist <= isize_max and mate_score > best_mate_score:
                        best_mate_score = mate_score
                rhits[i, COL_PAIR_SCORE] = best_mate_score + rhits[i, COL_SCORE]


cdef int[:] get_query_hits_count(int[:,:] hits_query_start, int query_count, int reference_count):
    """Calculate the number of hits per query."""

    cdef:
        int[:] query_hits_count
        int[:] query_start
        int i

    query_hits_count = np.zeros(query_count, dtype=np.int32)

    with nogil:
        for refid in range(reference_count):
            query_start = hits_query_start[refid]

            for i in range(query_count):
                query_hits_count[i] += query_start[i + 1] - query_start[i]
        return query_hits_count
    ###########


cdef void get_query_hit_properties(int k, int reference_count, int max_strata, int[:,:] hits_unique, int[:] ref_hits_address, int[:,:] hits_query_start, int* min_score, double* weighted_score_sum, int max_score) nogil:
    """Calculate the minimum score of a query given a maximum number of strata."""

    cdef:
        int hmin, hmax, i, refid, score
        double _weighted_score_sum = 0
        int[:] query_start
        int[:,:] rhits
        libcpp.set.set[int] strata
        libcpp.set.set[int].iterator min_stratum

    for refid in range(reference_count):
        rhits = hits_unique[ref_hits_address[refid]:ref_hits_address[refid + 1]]
        query_start = hits_query_start[refid]
        hmin = query_start[k]
        hmax = query_start[k+1]
        for i in range(hmin, hmax):
            score = rhits[i, COL_PAIR_SCORE]
            _weighted_score_sum += weight_score(score, max_score)
            min_stratum = strata.begin()

            if strata.size() < max_strata:
                # maximum number of strata not yet reached
                strata.insert(score)
            elif score > deref(min_stratum):
                # the strata tree is full and the score is better than the minimum
                # hence the so far minimum has to be discarded
                strata.erase(min_stratum)
                strata.insert(score)
    min_score[0] = deref(strata.begin())
    weighted_score_sum[0] = _weighted_score_sum


cdef int[:,:] get_query_hits(int k, int reference_count, int min_score, int[:,:] hits_unique, int[:] ref_hits_address, int[:,:] hits_query_start, int[:,:] temp_hits) nogil:
    """Collect the hits of a query given a minimum score."""

    cdef:
        int hmin, hmax, j, refid, hit_count
        int[:] query_start
        int[:,:] rhits
        int i = 0

    for refid in range(reference_count):
        rhits = hits_unique[ref_hits_address[refid]:ref_hits_address[refid + 1]]
        query_start = hits_query_start[refid]
        hmin = query_start[k]
        hmax = query_start[k+1]
        for j in range(hmin, hmax):
            if rhits[j, COL_PAIR_SCORE] >= min_score:
                temp_hits[i, :4] = rhits[j, :]
                i += 1
    return temp_hits[:i]


cdef inline double weight_score(int score, int max_score) nogil:
    return exp(score - max_score)


cdef inline int calc_mapq(int score, double weighted_score_sum, int max_score) nogil:
    """Calculate a single mapping quality in phred scale."""
    cdef:
        double weighted_score = weight_score(score, max_score)
    if weighted_score != weighted_score_sum:
        #return min(MAX_MAPQ, <int> (-10 * log10(1 - weighted_score / weighted_score_sum)))
        return min(
            MAX_MAPQ,
            <int> (
                LOG_TO_PHRED *
                log1p(-exp(log(weighted_score) - log(weighted_score_sum)))
            )
        )
    return MAX_MAPQ


cdef void calc_mapqs(int best_hit_count, int strata_count, double weighted_score_sum, int max_score, int[:,:] strata_qhits, int[:] strata) nogil:
    """Calculate mapping qualities for the given strata."""
    cdef:
        int j, s, mapq
        int i = 0

    # record mapping quality for each hit
    for s in range(strata_count):
        mapq = calc_mapq(strata_qhits[strata[s], COL_PAIR_SCORE], weighted_score_sum, max_score) 
        for j in range(strata[s + 1] - strata[s]):
            strata_qhits[i, COL_MAPQ] = mapq
            i += 1


cdef int get_best_hits_first_stratum(int[:,:] qhits, int strata_count, int max_hits, int[:] strata, int[:,:] strata_qhits, double weighted_score_sum, int max_score, bint accurate_mapq) nogil:
    """Collect the best hits in case only the best stratum shall be provided."""

    cdef:
        int qhits_count = qhits.shape[0]
        # default mapq is zero if accurate mapq is not selected since we have then a best stratum of size more than 1 here
        int mapq = 0

    if qhits_count == 1:
        strata_qhits[0, :] = qhits[0, :]
        strata_qhits[0, COL_MAPQ] = calc_mapq(qhits[0, COL_PAIR_SCORE], weighted_score_sum, max_score)
        return 1
    if qhits_count == 0:
        return 0

    # if only one stratum is present, mapq is easy...
    if accurate_mapq:
        mapq = calc_mapq(qhits[0, COL_PAIR_SCORE], weighted_score_sum, max_score)

    qhits_count = min(max_hits, qhits_count)
    strata_qhits[:qhits_count, :] = qhits[:qhits_count,:]
    strata_qhits[:qhits_count, COL_MAPQ] = mapq

    return qhits_count


cdef int get_best_hits(int[:,:] qhits, int strata_count, int max_hits, int[:] strata, int[:,:] strata_qhits, double weighted_score_sum, int max_score, bint accurate_mapq) nogil:
    """Get the best hits for a query.

    Args:
        qhits (int[:,:]): the collected query hits
        strata_count (int): number of strata to be reported for each read
        max_hits (int): independently of strata, number of hits to be reported for each read
        strata (int[:]): an array for storing the strata addresses
        mapq (int[:]): an array for storing the mapping qualities
        strata_qhits (int[:,:]): an array for storing the resulting sorted and combined hits of the query

    Returns:
        int: the number of remaining hits
    """

    cdef:
        int qhits_count = qhits.shape[0]

    if qhits_count == 1:
        strata_qhits[0, :] = qhits[0, :]
        strata_qhits[0, COL_MAPQ] = calc_mapq(qhits[0, COL_PAIR_SCORE], weighted_score_sum, max_score)
        return 1
    if qhits_count == 0:
        return 0

    max_hits = min(qhits_count, max_hits)

    cdef long[:] best_index
    with gil:
        best_index = np.argsort(qhits[:, COL_PAIR_SCORE])[::-1]
    strata[:] = 0

    cdef int i=1, s=0
    cdef int j, k
    cdef int best_hit_count

    # find strata breakpoints
    while s < strata_count and i < qhits_count and i < max_hits:
        if qhits[best_index[i], COL_PAIR_SCORE] < qhits[best_index[i - 1], COL_PAIR_SCORE]:
            s += 1
            strata[s] = i
        i += 1

    if s < strata_count and i >= max_hits:
        strata[s + 1] = max_hits
        strata_count = s + 1
    best_hit_count = strata[strata_count]

    # trim to given strata
    best_index = best_index[:best_hit_count]
    # copy best hits to start of qhits
    for j in range(best_hit_count):
        k = best_index[j]
        strata_qhits[j, :] = qhits[k, :]

    if not accurate_mapq and strata[0] > 1:
        strata_qhits[:, COL_MAPQ] = 0
    else:
        calc_mapqs(best_hit_count, strata_count, weighted_score_sum, max_score, strata_qhits, strata)
    return best_hit_count


cdef void rescue_apply_first_stratum(
    int[:,:] postprocessed_hits,
    int[:] postprocessed_hits_address,
    int k,
    double query_weighted_score_sum,
    double mate_weighted_score_sum,
    int rescued_refid,
    int rescued_pos,
    int rescued_score,
    int max_score,
    bint rescued_mate) nogil:
    cdef:
        int[:] rescued_hit, mate_hit
        double rescued_weighted_score_sum
    if rescued_mate:
        rescued_hit = postprocessed_hits[postprocessed_hits_address[k - 1]]
        # move the mate
        postprocessed_hits[postprocessed_hits_address[k - 1] + 1, :] = postprocessed_hits[postprocessed_hits_address[k]]
        # select the new mate at the corrected address
        mate_hit = postprocessed_hits[postprocessed_hits_address[k - 1] + 1]
        rescued_weighted_score_sum = mate_weighted_score_sum
        mate_weighted_score_sum = query_weighted_score_sum
    else:
        rescued_hit = postprocessed_hits[postprocessed_hits_address[k - 1] + 1]
        mate_hit = postprocessed_hits[postprocessed_hits_address[k - 1]]
        rescued_weighted_score_sum = query_weighted_score_sum

    # update intervals
    postprocessed_hits_address[k] = postprocessed_hits_address[k - 1] + 1
    postprocessed_hits_address[k + 1] = postprocessed_hits_address[k] + 1

    rescue_set_hits(
        rescued_hit, mate_hit,
        rescued_weighted_score_sum,
        mate_weighted_score_sum,
        rescued_refid, rescued_pos, rescued_score, max_score)


cdef void rescue_apply(
    int[:,:] postprocessed_hits,
    int[:] postprocessed_hits_address,
    int k,
    double query_weighted_score_sum,
    double mate_weighted_score_sum,
    int rescued_refid,
    int rescued_pos,
    int rescued_score,
    int max_score,
    bint rescued_mate) nogil:
    cdef:
        int i
        int j = postprocessed_hits_address[k + 1]
        double rescued_weighted_score_sum
    if rescued_mate:
        i = postprocessed_hits_address[k - 1]
    else:
        i = postprocessed_hits_address[k]
    postprocessed_hits[i + 1:j + 1] = postprocessed_hits[i:j]
    postprocessed_hits_address[k + 1] += 1

    cdef:
        int[:] rescued_hit
        int[:] mate_hit
    if rescued_mate:
        postprocessed_hits_address[k] += 1
        mate_hit = postprocessed_hits[postprocessed_hits_address[k]]
        rescued_hit = postprocessed_hits[postprocessed_hits_address[k - 1]]
        rescued_weighted_score_sum = mate_weighted_score_sum
        mate_weighted_score_sum = query_weighted_score_sum
    else:
        mate_hit = postprocessed_hits[postprocessed_hits_address[k - 1]]
        rescued_hit = postprocessed_hits[postprocessed_hits_address[k]]
        rescued_weighted_score_sum = query_weighted_score_sum

    rescue_set_hits(
        rescued_hit, mate_hit,
        rescued_weighted_score_sum,
        mate_weighted_score_sum,
        rescued_refid, rescued_pos, rescued_score, max_score)


cdef void rescue_set_hits(
    int[:] rescued_hit,
    int[:] mate_hit,
    double rescued_weighted_score_sum,
    double mate_weighted_score_sum,
    int rescued_refid,
    int rescued_pos,
    int rescued_score,
    int max_score) nogil:
    rescued_hit[COL_REFID] = rescued_refid
    rescued_hit[COL_POS] = rescued_pos
    rescued_hit[COL_SCORE] = rescued_score
    rescued_hit[COL_PAIR_SCORE] = rescued_score + mate_hit[COL_SCORE]
    mate_hit[COL_PAIR_SCORE] = rescued_hit[COL_PAIR_SCORE]

    # update score sums
    rescued_weighted_score_sum += weight_score(rescued_hit[COL_PAIR_SCORE], max_score)
    mate_weighted_score_sum -= weight_score(mate_hit[COL_SCORE], max_score)
    mate_weighted_score_sum += weight_score(mate_hit[COL_PAIR_SCORE], max_score)

    rescued_hit[COL_MAPQ] = calc_mapq(
        rescued_hit[COL_PAIR_SCORE], rescued_weighted_score_sum, max_score)
    mate_hit[COL_MAPQ] = calc_mapq(
        mate_hit[COL_PAIR_SCORE], mate_weighted_score_sum, max_score)


def _postprocess_hits(
    references,
    int[:] reference_sizes,
    int[:] reference_offsets,
    int query_count,
    int reference_count,
    unsigned int[:,:] queries_sequences,
    int[:] queries_sizes,
    int queries_maxsize,
    hits,
    int[:,:] score_matrix,
    int gap_open,
    int gap_extend,
    bint semiglobal_alignment,
    int strata_count,
    int max_hits,
    int min_score,
    bint accurate_mapq,
    bint paired,
    int insert_size,
    int insert_size_error,
    bint skip_alignment,
    int window, int offset,
    ):
    """Perform the final postprocessing of hits.

    Args:
        references (peanut.reference.References): the loaded references
        reference_sizes (int[:]): the reference sizes
        reference_offsets (int[:]): the reference offsets
        query_count (int): the number of queries
        reference_count (int): the number of references
        queries_sequences (int[:,:]): the query sequences
        queries_sizes (int[:,:]): the query sizes
        queries_maxsize (int): the maximum query size
        hits_unique (int[:,:]): unique hits
        ref_hits_address (int[:]): reference hits addresses
        hits_query_start (int[:]): per query hits addresses inside one reference hits region
        query_hits_count (int[:]): per query hits count
        score_matrix (int[:,:]): a score matrix (smith-waterman alignment)
        gap_open (int): gap open penalty (smith-waterman alignment)
        gap_extend (int): gap extend penalty (smith-waterman alignment)
        semiglobal_alignment (bint): perform a semiglobal alignment instead of local
        strata_count (int): number of strata to be reported for each read (-1 means all)
        max_hits (int): independently of strata, number of hits to be reported for each read
        min_score (int): minimum score for a hit (hits with lower scores were removed in validation step)
        accurate_mapq (bool): whether to report an accurate mapping quality or set it to zero in case of ambiguity
        paired (bint): pair corresponding reads (if two reads are properly paired, use the sum of their scores as new score)
        insert_size (int): expected insert size
        insert_size_error (int): maximum insert size error
        skip_alignment (bool): do not calculate the concrete alignments
        window (int): size of the window to process
        offset (int): start of the window to process

    Returns:
        tuple: tuple of postprocessed hits (including new column COL_MAPQ), cigars, cigar_sizes, postprocessed_hits_addresses and the used offset and window parameters.
    """
    window = min(query_count - offset, window)

    # remove duplicate hits
    cdef:
        int[:] ref_hits_address = np.empty(reference_count + 1, dtype=np.int32)
        int[:,:] hits_query_start = np.empty(
            (reference_count, window + 1), dtype=np.int32
        )
        int[:,:] hits_unique = get_unique_hits(
            hits, reference_count, reference_sizes, reference_offsets,
            queries_sizes, query_count, ref_hits_address, hits_query_start,
            offset, window
        )

    # count hits
    cdef:
        int[:] hit_counts = get_query_hits_count(
            hits_query_start, window, reference_count
        )

    cdef:
        unsigned int** reference_sequences = get_reference_sequences(references)
        # the maximum score is a percent identity
        # of 100 or 2*100 for paired reads
        int max_score = 200 if paired else 100

    if paired:
        with nogil:
            score_mates(
                reference_count, insert_size, insert_size_error, hits_unique,
                ref_hits_address, hits_query_start, queries_sizes, window,
                offset
            )

    cdef:
        int max_hit_count = np.max(hit_counts)
        int postprocessed_hits_count = np.sum(np.minimum(max_hits, hit_counts))

    if paired:
        # plan at least one additional hit for each read pair in case of rescue mode
        postprocessed_hits_count += window / 2

    cdef:
        int[:,:] postprocessed_hits = np.empty(
            (postprocessed_hits_count, 5), dtype=np.int32
        )
        int[:] postprocessed_hits_address = np.empty(
            window + 1, dtype=np.int32
        )

        # allocate per-query data structures for get_query_hits
        # (one column more for the MAPQ)
        int[:,:] temp_qhits = np.empty((max_hit_count, 5), dtype=np.int32)
        int[:,:] qhits
        int query, i, hit_count, k, query_min_score
        double query_weighted_score_sum, mate_weighted_score_sum

        get_best_hits_type _get_best_hits = get_best_hits
        get_max_alignment_score_type _get_max_alignment_score = get_max_alignment_score
        rescue_apply_type _rescue_apply = rescue_apply

    if strata_count < 0:
        strata_count = min(max_hit_count, max_hits)
    elif strata_count == 1:
        # use a shortcut if only the first stratum is required
        _get_best_hits = get_best_hits_first_stratum
        _rescue_apply = rescue_apply_first_stratum
    if paired:
        _get_max_alignment_score = get_max_alignment_score_paired

    # allocate per-query data structures for get_best_hits
    cdef:
        int[:] strata = np.empty(strata_count + 1, dtype=np.int32)
        int[:,:] temp_strata_qhits = np.empty_like(temp_qhits)
        int rescued_refid, rescued_mate_refid, rescued_pos, rescued_score, rescued_mate_pos, rescued_mate_score, hit_score, mate_score
        bint rescue_mate
        int[:] hit
        int[:] mate_hit
        int _i
        int rescue_count = 0

    postprocessed_hits_address[0] = 0

    with nogil:
        for k in range(window):
            query = k + offset

            i = postprocessed_hits_address[k]
            get_query_hit_properties(
                k, reference_count, strata_count, hits_unique,
                ref_hits_address, hits_query_start, &query_min_score,
                &query_weighted_score_sum, max_score
            )
            qhits = get_query_hits(
                k, reference_count, query_min_score, hits_unique,
                ref_hits_address, hits_query_start, temp_qhits
            )
            hit_count = _get_best_hits(
                qhits, strata_count, max_hits, strata,
                postprocessed_hits[i:, :], query_weighted_score_sum, max_score,
                accurate_mapq
            )
            postprocessed_hits_address[k + 1] = i + hit_count

            if paired and k % 2:
                hit = postprocessed_hits[i]
                if hit[COL_SCORE] == hit[COL_PAIR_SCORE]:
                    rescued_mate_score = 0
                    rescued_score = 0
                    hit_score = 0
                    mate_score = 0
                    if hit_count:
                        # use this as anchor
                        rescued_mate_refid = get_revcomp(hit[COL_REFID])
                        hit_score = hit[COL_SCORE]
                        rescue.rescue(
                            rescued_mate_refid,
                            reference_sequences[rescued_mate_refid],
                            reference_sizes[rescued_mate_refid],
                            reference_offsets[rescued_mate_refid],
                            &queries_sequences[query - 1, 0],
                            queries_sizes[query - 1],
                            hit[COL_POS],
                            insert_size,
                            insert_size_error,
                            &rescued_mate_pos,
                            &rescued_mate_score
                        )

                    if i - postprocessed_hits_address[k - 1]:
                        # use mate as anchor
                        mate_hit = postprocessed_hits[postprocessed_hits_address[k - 1]]
                        rescued_refid = get_revcomp(mate_hit[COL_REFID])
                        mate_score = mate_hit[COL_SCORE]
                        rescue.rescue(
                            rescued_refid,
                            reference_sequences[rescued_refid],
                            reference_sizes[rescued_refid],
                            reference_offsets[rescued_refid],
                            &queries_sequences[query, 0],
                            queries_sizes[query],
                            mate_hit[COL_POS],
                            insert_size,
                            insert_size_error,
                            &rescued_pos,
                            &rescued_score
                        )

                    rescue_mate = (
                        rescued_mate_score > min_score and
                        hit_score + rescued_mate_score > mate_score + rescued_score
                    )
                    if rescue_mate:
                        _rescue_apply(
                            postprocessed_hits,
                            postprocessed_hits_address,
                            k, query_weighted_score_sum,
                            mate_weighted_score_sum,
                            rescued_mate_refid, rescued_mate_pos,
                            rescued_mate_score, max_score, True
                        )
                        rescue_count += 1
                    elif rescued_score > min_score:
                        _rescue_apply(
                            postprocessed_hits,
                            postprocessed_hits_address,
                            k, query_weighted_score_sum,
                            mate_weighted_score_sum,
                            rescued_refid, rescued_pos, rescued_score,
                            max_score, False
                        )
                        rescue_count += 1

            mate_weighted_score_sum = query_weighted_score_sum

    ###########
    # adjust the hit count after strata calculations
    postprocessed_hits_count = postprocessed_hits_address[window]

    cdef:
        int[:] cigar_address = None
        int[:,:] cigars = None
        int[:] cigar_sizes = None

    if not skip_alignment:
        cigar_address = alignment.calc_cigar_address(
            postprocessed_hits, postprocessed_hits_address, queries_sizes,
            window, offset, postprocessed_hits_count
        )
        cigars = np.empty(
            (cigar_address[postprocessed_hits_count], 2), dtype=np.int32
        )
        cigar_sizes = np.empty(postprocessed_hits_count, dtype=np.int32)

        alignment.alignment(
            reference_sequences, reference_sizes, reference_offsets,
            queries_sequences, queries_sizes, queries_maxsize,
            postprocessed_hits, postprocessed_hits_address, score_matrix,
            gap_open, gap_extend, semiglobal_alignment, cigar_address,
            cigars, cigar_sizes, window, offset
        )
    free(reference_sequences)
    return (
        postprocessed_hits, cigar_address, cigars, cigar_sizes,
        postprocessed_hits_address, offset, window, rescue_count
    )


def postprocess_hits(
    queries,
    references,
    hits,
    int min_score,
    int[:,:] score_matrix,
    int gap_open=6,
    int gap_extend=1,
    bint semiglobal_alignment=False,
    int strata=-1,
    int max_hits=100,
    int threads=1,
    int buffersize=100000,
    bint paired=False,
    int insert_size=220,
    int insert_size_error=50,
    bint accurate_mapq=False,
    bint skip_alignment=False):
    """Postprocess hits.
    
    Args:
        queries (peanut.query.Queries): the buffered queries
        references (peanut.reference.References): the loaded references
        hits (peanut.Hits): the validated hits
        min_score (int): minimum score for a hit (hits with lower scores were removed in validation step)
        score_matrix (int[:,:]): a score matrix (smith-waterman alignment)
        gap_open (int): gap open penalty (smith-waterman alignment)
        gap_extend (int): gap extend penalty (smith-waterman alignment)
        semiglobal_alignment (bint): perform a semiglobal alignment instead of local
        strata (int): number of strata to be reported for each read (-1 means all)
        max_hits (int): independently of strata, number of hits to be reported for each read
        threads (int): number of threads to use
        buffersize (int): number of hits to align in one iteration
        paired (bint): pair corresponding reads (if two reads are properly paired, use the sum of their scores as new score)
        insert_size (int): expected insert size
        insert_size_error (int): maximum insert size error
        accurate_mapq (bool): whether to report an accurate mapping quality or set it to zero in case of ambiguity
        skip_alignment (bool): do not calculate the concrete alignments

    Yields:
        PostprocessedHits: a buffer of postprocessed hits
    """

    cdef:
        int query_count = queries.count
        int[:] queries_sizes = queries.sizes
        int queries_maxsize = queries.maxsize
        unsigned int[:,:] queries_sequences = queries.encoded

        int reference_count = references.count

        int[:] reference_sizes = references.strand_sizes
        int[:] reference_offsets = references.offsets

        int i
        int window = buffersize / threads

    window += window % 2  # ensure that the window size can be divided by 2 (in order to always include the mate)

    with ThreadPoolExecutor(max_workers=threads) as pool:
        for i, (hits, cigar_address, cigars, cigar_sizes, hits_address, offset, effective_window_size, rescue_count) in enumerate(pool.map(
            partial(
                _postprocess_hits,
                references, reference_sizes, reference_offsets,
                query_count, reference_count,
                queries_sequences, queries_sizes, queries_maxsize,
                hits,
                score_matrix, gap_open, gap_extend, semiglobal_alignment,
                strata, max_hits, min_score, accurate_mapq,
                paired, insert_size,
                insert_size_error,
                skip_alignment, window
            ),
            range(0, query_count, window))):
            PyErr_CheckSignals()
            if rescue_count:
                logging.info("Rescued {} alignments using the mate.".format(rescue_count))
            yield PostprocessedHits(hits=hits, cigar_address=cigar_address, cigars=cigars, cigar_sizes=cigar_sizes, hits_address=hits_address, offset=offset, window_size=effective_window_size)
