# -*- coding: utf-8 -*-
# distutils: language = c++
# cython: cdivision=True, wraparound=False, boundscheck=False


__author__ = "Johannes Köster"
__license__ = "MIT"


import numpy as np
cimport numpy as np
from libcpp.vector cimport vector
from libc.stdio cimport printf
from libc.math cimport ceil

import logging

cimport peanut.common as common

DEF BANDED = True
DEF CIGAR_M = 0
DEF CIGAR_I = 1
DEF CIGAR_D = 2
DEF CIGAR_S = 4

DEF CONTEXT = 10


cdef extern from "limits.h":
    int INT_MAX


cdef int COL_REFID = 0
cdef int COL_POS = 1
cdef int COL_SCORE = 2
cdef int COL_PAIR_SCORE = 3
cdef int COL_MAPQ = 4


# we encode the traceback in a single byte: 0=(i,j), 1=(i-1,j-1), 2=(i-1,j), 3=(i,j-1)
cdef char TRACEBACK_START = 0
cdef char TRACEBACK_SUBSTITUTION = 1
cdef char TRACEBACK_DELETION = 2
cdef char TRACEBACK_INSERTION = 3
# the following matrix allows to restore i and j from the code (first row=i, second row=j)
cdef char[:,:] TRACEBACK = np.array([
    [0, -1, -1, 0],
    [0, -1, 0, -1]
], dtype=np.int8)


cdef int get_max_cigar_size(int query_size, int score) nogil:
    """Calculate the maximum size of a cigar string given a levenshtein score."""
    cdef:
        int max_edit_ops = get_expected_errors(query_size, score)

    if max_edit_ops == 0:
        return 1
    return max_edit_ops * 2 + 4 + CONTEXT  # maximum edit ops times 2 (for matches in between) plus 2 matches at the sides and at most 2 soft clippings at the side

# deprecated
cdef inline bint is_revcomp(int refid) nogil:
    """Return True if refid belongs to a reverse complement."""
    return refid % 2  # every second ref is the reverse complement


# deprecated
cdef inline int adjust_pos(int reference_size, int reference_offset, int refid, int pos, int query_size) nogil:
    """Adjust a hit position."""
    return reference_size - pos - 1 if not common.is_revcomp(refid) else pos + query_size + reference_offset - 1


cdef inline void init_scores(int[:,:] S, int[:,:] I, int[:,:] D) nogil:
    """Initialize dynamic programming matrix."""
    S[:,:] = 0
    I[:,:] = -INT_MAX
    D[:,:] = -INT_MAX


cdef inline void init_traceback(char[:,:] T) nogil:
    """Initialize traceback matrix."""
    cdef:
        int i, j

    for i in range(T.shape[0]):
        for j in range(T.shape[1]):
            T[i, j] = TRACEBACK_START


cdef inline char decode_char(unsigned int* encoded_sequence, int pos) nogil:
    """Decode a bitencoded sequence into characters."""
    return (encoded_sequence[pos / 16] >> ((pos % 16) * 2)) & 3


cdef int traceback(
    int[:,:] qhits,
    int hit,
    char[:,:] T,
    int[:,:] cigar,
    int i,
    int j,
    int query_size,
    int window_size,
    int suffix,
    int prefix,
    bint revcomp=False) nogil:
    """Calculate cigar from traceback."""

    cdef:
        char tbcode
        int ii, jj
        int acode, alen, ilen, jlen
        int acount = 0
        int alast = -1
        int cigarlen = 0
        int besti = i

    if j < query_size:
        cigar[0, 0] = CIGAR_S  # soft clip
        cigar[0, 1] = query_size - j
        cigarlen += 1
    if j > 0:
        while True:
            tbcode = T[i,j]
            ii = i + TRACEBACK[0,tbcode]
            jj = j + TRACEBACK[1,tbcode]
            if ii == i and jj == j:
                cigar[cigarlen, 0] = alast
                cigar[cigarlen, 1] = acount
                cigarlen += 1
                break
            ilen = i - ii
            jlen = j - jj
            if ilen == jlen:
                acode = CIGAR_M  # match or substitution
                alen = ilen
            elif ilen < jlen:
                acode = CIGAR_I  # insertion
                alen = jlen
            else:
                acode = CIGAR_D  # deletion
                alen = ilen

            if alast == -1:
                alast = acode

            if acode == alast:
                acount += alen
            else:
                cigar[cigarlen, 0] = alast
                cigar[cigarlen, 1] = acount
                alast = acode
                acount = alen
                cigarlen += 1
            i = ii
            j = jj
    if j > 0:
        # soft clip the missing prefix
        cigar[cigarlen, 0] = CIGAR_S
        cigar[cigarlen, 1] = j
        cigarlen += 1

    if not revcomp:
        qhits[hit, COL_POS] += i - prefix
        cigar[:cigarlen,:] = cigar[:cigarlen,:][::-1,:]
    else:
        qhits[hit, COL_POS] += window_size - suffix - besti
    return cigarlen


cdef int align_hit(
    unsigned int* reference,
    int reference_size,
    int reference_offset,
    unsigned int* query,
    int[:,:] qhits,
    int hit,
    int query_size,
    int expected_errors,
    int[:,:] S,
    int[:,:] I,
    int[:,:] D,
    char[:,:] T,
    int[:,:] cigar,
    int[:,:] score_matrix,
    int gap_open=6,
    int gap_extend=1,
    bint semiglobal=False,
    bint score_only=False) nogil:
    """Align a hit with Smith-Waterman/Needleman-Wunsch."""

    cdef:
        int i, j, q, curr_col, prev_col, jmin, jmax
        int refid = qhits[hit, COL_REFID]

        # adjust pos to reverse reference storage
        int pos = common.bam_pos_to_pos(reference_size, reference_offset, refid, qhits[hit, COL_POS], query_size)

        int prefix = min(CONTEXT, reference_size - pos)
        int suffix = min(CONTEXT, max(pos - query_size, 0))
        int window_size = query_size + prefix + suffix
        char c_ref, c_query
        int best = 0, besti = 0, bestj = 0
        int curr_score
        char curr_tb
        int band = expected_errors + prefix + 1
        int bound_penalty = -INT_MAX + gap_open

    pos = pos + prefix  # TODO what about the offset??

    # fill score matrices
    init_scores(S, I, D)
    # fill traceback
    init_traceback(T)

    for i in range(1, window_size + 1):

        curr_col = i % 2
        prev_col = 1 - curr_col
        # allow to begin anywhere in the text
        S[curr_col, 0] = 0
        # set the boundary scores such that the alignment does not exit the band
        IF BANDED:
            jmin = min(i, query_size) - band
            jmax = i + band
            if jmin > 1:
                S[curr_col, jmin - 1] = bound_penalty
                I[curr_col, jmin - 1] = bound_penalty
            else:
                jmin = 1
            if jmax < query_size:
                S[prev_col, jmax] = bound_penalty
                D[prev_col, jmax] = bound_penalty
            else:
                jmax = query_size
        ELSE:
            jmin = 1
            jmax = query_size

        c_ref = decode_char(reference, pos)
        for j in range(jmin, jmax + 1):
            c_query = decode_char(query, query_size - j)

            D[curr_col, j] = max(S[prev_col, j] - gap_open, D[prev_col, j] - gap_extend)
            I[curr_col, j] = max(S[curr_col, j - 1] - gap_open, I[curr_col, j - 1] - gap_extend)

            curr_score = S[prev_col, j - 1] + score_matrix[c_ref, c_query]
            curr_tb = TRACEBACK_SUBSTITUTION
            if D[curr_col, j] > curr_score:
                curr_score = D[curr_col, j]
                curr_tb = TRACEBACK_DELETION
            if I[curr_col, j] > curr_score:
                curr_score = I[curr_col, j]
                curr_tb = TRACEBACK_INSERTION

            if not semiglobal:
                if curr_score < 0:
                    curr_score = 0
                    curr_tb = TRACEBACK_START
                elif curr_score > best:
                    best = curr_score
                    besti = i
                    bestj = j

            S[curr_col, j] = curr_score
            T[i,j] = curr_tb

        if semiglobal and S[curr_col, j] > best:
            best = S[curr_col, j]
            besti = i
            bestj = j
        pos -= 1

    if score_only:
        return best
    return traceback(qhits, hit, T, cigar, besti, bestj, query_size, window_size, suffix, prefix, revcomp=common.is_revcomp(refid))


cdef int[:] calc_cigar_address(int[:,:] postprocessed_hits, int[:] postprocessed_hits_address, int[:] queries_sizes, int window, int offset, int postprocessed_hits_count):
    cdef:
        int i, k, query, hmin, hmax, qhits_count, query_size, score
        int[:,:] qhits
        int j = 0
        int[:] cigar_address = np.empty(postprocessed_hits_count + 1, dtype=np.int32)
    with nogil:
        cigar_address[0] = 0
        for k in range(window):
            query = k + offset
            hmin = postprocessed_hits_address[k]
            hmax = postprocessed_hits_address[k + 1]
            qhits_count = hmax - hmin

            qhits = postprocessed_hits[hmin:hmax, :]
            query_size = queries_sizes[query]

            for i in range(qhits_count):
                score = qhits[i, COL_SCORE]
                cigar_address[j + 1] = cigar_address[j] + get_max_cigar_size(query_size, score)
                j += 1
    return cigar_address


cdef void alignment(
    unsigned int** reference_sequences, int[:] reference_sizes, int[:] reference_offsets,
    unsigned int[:,:] queries_sequences, int[:] queries_sizes, int queries_maxsize,
    int[:,:] postprocessed_hits, int[:] postprocessed_hits_address,
    int[:,:] score_matrix, int gap_open, int gap_extend, bint semiglobal, int[:] cigar_address, int[:,:] cigars, int[:] cigar_sizes,
    int window, int offset):
    """Calculate hit alignments."""

    cdef:
        int[:,:] S = np.empty((2, queries_maxsize + 1), dtype=np.int32)
        int[:,:] I = np.empty((2, queries_maxsize + 1), dtype=np.int32)
        int[:,:] D = np.empty((2, queries_maxsize + 1), dtype=np.int32)
        char[:,:] T = np.empty((queries_maxsize * 2 + 1, queries_maxsize + 1), dtype=np.int8)
        int query_count = queries_sequences.shape[0]
        int i, k, refid, qhits_count, query_size, query, expected_errors, hmin, hmax

        unsigned int* query_sequence
        unsigned int* reference_sequence
        int[:,:] qhits
        int[:,:] cigar
        int[:] qcigar_sizes
        int[:] qcigar_address

    with nogil:
        for k in range(window):
            query = k + offset
            hmin = postprocessed_hits_address[k]
            hmax = postprocessed_hits_address[k + 1]
            qhits_count = hmax - hmin

            qhits = postprocessed_hits[hmin:hmax, :]
            query_size = queries_sizes[query]
            qcigar_sizes = cigar_sizes[hmin:hmax]
            qcigar_address = cigar_address[hmin:hmax + 1]
            query_sequence = &queries_sequences[query, 0]

            for i in range(qhits_count):
                refid = qhits[i, COL_REFID]
                reference_sequence = reference_sequences[refid]
                cigar = cigars[qcigar_address[i]:qcigar_address[i + 1], :]

                # calculate the expected errors from percent identity (see validation.cl)
                expected_errors = get_expected_errors(query_size, qhits[i, COL_SCORE])
                if expected_errors == 0:
                    cigar[0, 0] = CIGAR_M
                    cigar[0, 1] = query_size
                    qcigar_sizes[i] = 1
                else:
                    qcigar_sizes[i] = align_hit(
                        reference_sequence,
                        reference_sizes[refid],
                        reference_offsets[refid],
                        query_sequence,
                        qhits, i, query_size, expected_errors,
                        S, I, D, T,
                        cigar, score_matrix,
                        gap_open, gap_extend, semiglobal=semiglobal,
                        score_only=False)
    #############


cdef int get_expected_errors(int query_size, int score) nogil:
    return <int>ceil(query_size * (1 - score / 100.0))
