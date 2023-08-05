# -*- coding: utf-8 -*-
# distutils: language = c++
# cython: boundscheck=False, wraparound=False, cdivision=True


__author__ = "Johannes Köster"
__license__ = "MIT"


import numpy as np
cimport numpy as np

import logging

from libc.stdlib cimport malloc, free
from libc.stdio cimport printf

import peanut
from peanut.bitencoding import COMPLEMENT


cimport peanut.common as common


cdef char** stringarray(strings):
    """Create a pointer array for a list of strings."""
    cdef:
        int i
        char** ret = <char **>malloc(len(strings) * sizeof(char *))

    for i in range(len(strings)):
        ret[i] = strings[i]
    return ret


DEF FLAG_PRIMARY = 0x0
DEF FLAG_MULTIPLE_SEGMENTS = 0x1
DEF FLAG_SEGMENTS_PROPERLY_ALIGNED = 0x2
DEF FLAG_UNMAPPED = 0x4
DEF FLAG_REVCOMP = 0x10
DEF FLAG_SECONDARY = 0x100
DEF FLAG_FIRST_IN_PAIR = 0x40
DEF FLAG_SECOND_IN_PAIR = 0x80
DEF FLAG_MATE_UNMAPPED = 0x8
DEF FLAG_MATE_REVCOMP = 0x20

cdef char SAM_HEADER_PREFIX = "@"


DEF CIGAR_M = 0
DEF CIGAR_I = 1
DEF CIGAR_D = 2
DEF CIGAR_S = 4
cdef char[:] TRANSLATE_CIGAR = np.fromstring(b"MIDNSHP=X", dtype=np.uint8)
cdef int[:,:] EMPTY_CIGAR = np.empty((0,0), dtype=np.int32)


cdef int COL_REFID = 0
cdef int COL_POS = 1
cdef int COL_SCORE = 2
cdef int COL_PAIR_SCORE = 3
cdef int COL_MAPQ = 4


cdef int get_alignment_length(int[:,:] cigar) nogil:
    """Calculate the length of an alignment given a cigar."""
    cdef:
        int i
        int alen = 0

    for i in range(cigar.shape[0]):
        if cigar[i, 0] == CIGAR_D:
            alen -= cigar[i, 1]
        else:
            alen += cigar[i, 1]
    return alen


cdef inline int get_tid(int refid) nogil:
    """Calculate a SAM compatible tid from a refid."""
    return (refid - refid % 2) / 2


# deprecated
cdef inline bint is_revcomp(int refid) nogil:
    """Return True if refid belongs to a reverse complement."""
    return refid % 2  # every second ref is the reverse complement


cdef inline int adjust_pos(int pos) nogil:
    """Adjust position to being one-based."""
    return pos + 1


cdef inline int get_tlen(int alen, int tid, int pos, int mate_tid, int mate_pos, int mate_alen) nogil:
    """Calculate template length."""
    cdef:
        int tlen = 0

    if mate_tid == tid:
        # calculate tlen
        if mate_pos < pos:
            tlen = - (pos + alen - mate_pos)
        else:
            tlen = mate_pos + mate_alen - pos
    return tlen


cdef inline void _print_sam_record_end() nogil:
    """Print the end of a sam record."""
    printf(b"%s", b"\n")


cdef inline void _print_cigar(int[:,:] cigar) nogil:
    """Print a cigar string."""
    cdef:
        int i

    if cigar.shape[0] == 0:
        printf(b"%s", b"*")
    else:
        for i in range(cigar.shape[0]):
            printf(b"%i%c", cigar[i, 1], TRANSLATE_CIGAR[cigar[i, 0]])


cdef void _print_sam_record(char* qname, int flag, char* rname, int pos, int mapq, int[:,:] cigar, char* rnext, int pnext, int tlen, char* seq, char* qual) nogil:
    """Print a sam record."""
    printf(b"%s\t%i\t%s\t%i\t%i\t", qname, flag, rname, adjust_pos(pos), mapq)
    _print_cigar(cigar)
    printf(b"\t%s\t%i\t%i\t%s\t%s", rnext, adjust_pos(pnext), tlen, seq, qual)


cdef inline void _print_sam_as(int score) nogil:
    """Print an AS tag."""
    printf(b"\tAS:i:%i", score)


cdef inline void _print_sam_xa() nogil:
    """Print prefix of an XA tag."""
    printf(b"\t%s", b"XA:Z:")


cdef void _print_sam_xa_record(char* rname, int pos, int mapq, int[:,:] cigar) nogil:
    """Print an XA record."""
    printf(b"%s,%i,", rname, pos)
    _print_cigar(cigar)
    printf(b",%i;", mapq)


cdef void print_sam_mapped(int qsize, char* qname, char* seq, char* qual, char* seq_revcomp, char* qual_revcomp, int[:,:] hits, int[:] cigar_address, int[:,:] cigars, int[:] cigar_sizes, int i, char* mate_rname, int mate_tid, int mate_pos, int mate_alen, short flags, char** rnames, const bint no_cigars) nogil:
    """Print a collection of hits."""

    cdef:
        int refid = hits[i, COL_REFID]
        int pos = hits[i, COL_POS]
        int mapq = hits[i, COL_MAPQ]
        int score = hits[i, COL_SCORE]
        int cigar_size, tlen, alen
        int[:,:] cigar = EMPTY_CIGAR
        int tid = get_tid(refid)

    if not no_cigars:
        cigar_size = cigar_sizes[i]
        cigar = cigars[cigar_address[i]:cigar_address[i] + cigar_size, :]
        alen = get_alignment_length(cigar)
    else:
        alen = qsize
    tlen = get_tlen(alen, tid, pos, mate_tid, mate_pos, mate_alen)

    if common.is_revcomp(refid):
        flags |= 0x10
        seq = seq_revcomp
        qual = qual_revcomp

    _print_sam_record(qname, flags, rnames[tid], pos, mapq, cigar, mate_rname, mate_pos, tlen, seq, qual)

    _print_sam_as(score)
    _print_sam_record_end()


cdef void print_sam_mapped_xa(int qsize, char* qname, char* seq, char* qual, char* seq_revcomp, char* qual_revcomp, int[:,:] hits, int[:] cigar_address, int[:,:] cigars, int[:] cigar_sizes, char* mate_rname, int mate_tid, int mate_pos, int mate_alen, short flags, char** rnames, const bint no_cigars) nogil:
    """Print a collection of hits, using XA tags."""

    cdef:
        int hit_count = hits.shape[0]
        int i, refid, pos, mapq, score, cigar_size, tid, tlen, alen
        char* rname
        int[:,:] cigar = EMPTY_CIGAR

    refid = hits[0, COL_REFID]
    pos = hits[0, COL_POS]
    mapq = hits[0, COL_MAPQ]
    score = hits[0, COL_SCORE]
    
    if not no_cigars:
        cigar_size = cigar_sizes[0]
        cigar = cigars[cigar_address[0]:cigar_address[0] + cigar_size, :]
        alen = get_alignment_length(cigar)
    else:
        alen = qsize

    tid = get_tid(refid)
    tlen = get_tlen(alen, tid, pos, mate_tid, mate_pos, mate_alen)
    rname = rnames[tid]

    if common.is_revcomp(refid):
        flags |= 0x10
        seq = seq_revcomp
        qual = qual_revcomp

    _print_sam_record(qname, flags, rname, pos, mapq, cigar, mate_rname, mate_pos, tlen, seq, qual)

    _print_sam_as(score)
    if hit_count > 1:
        _print_sam_xa()

    for i in range(1, hit_count):
        refid = hits[i, COL_REFID]
        pos = hits[i, COL_POS]
        mapq = hits[i, COL_MAPQ]

        if not no_cigars:
            cigar_size = cigar_sizes[i]
            cigar = cigars[cigar_address[i]:cigar_address[i] + cigar_size, :]

        tid = get_tid(refid)
        rname = rnames[tid]

        _print_sam_xa_record(rname, pos, mapq, cigar)
    _print_sam_record_end()


cdef void print_sam_unmapped(char* qname, char* seq, char* qual, char* mate_rname, int mate_pos, short flags, char** rnames) nogil:
    """Print unmapped queries."""
    _print_sam_record(qname, flags | FLAG_UNMAPPED, b"*", -1, 0, EMPTY_CIGAR, mate_rname, mate_pos, 0, seq, qual)
    _print_sam_record_end()


cdef void print_sam_records(int size, char* name, char* seq, char* qual, char* seq_revcomp, char* qual_revcomp, int[:,:] hits, int[:] cigar_address, int[:,:] cigars, int[:] cigar_sizes, char* mate_rname, int mate_tid, int mate_pos, int mate_alen, short flags, char** rnames, const bint use_xa, const bint no_cigars) nogil:
    """Print given queries and their hits."""

    cdef:
        int hit_count = hits.shape[0]
        int i

    if hit_count == 0:
        print_sam_unmapped(name, seq, qual, mate_rname, mate_pos, flags, rnames)
    else:
        if use_xa:
            print_sam_mapped_xa(size, name, seq, qual, seq_revcomp, qual_revcomp, hits, cigar_address, cigars, cigar_sizes, mate_rname, mate_tid, mate_pos, mate_alen, flags, rnames, no_cigars)
        else:
            print_sam_mapped(size, name, seq, qual, seq_revcomp, qual_revcomp, hits, cigar_address, cigars, cigar_sizes, 0, mate_rname, mate_tid, mate_pos, mate_alen, flags | FLAG_PRIMARY, rnames, no_cigars)  # use primary flag
            for i in range(1, hit_count):
                print_sam_mapped(size, name, seq, qual, seq_revcomp, qual_revcomp, hits, cigar_address, cigars, cigar_sizes, i, mate_rname, mate_tid, mate_pos, mate_alen, flags | FLAG_SECONDARY, rnames, no_cigars)  # use secondary flag


def print_sam(queries, postprocessed_hits, bint paired, object[:] reference_names, bint use_xa, bint no_cigars=False):
    """Print postprocessed hits and given queries."""

    cdef:
        int mate, query, k, k_mate, hmin, hmax, window, mate_refid, size
        int j = 0
        bytes temp_name, temp_seq, temp_qual, temp_seq_revcomp, temp_qual_revcomp
        char* name
        short flags
        char* seq
        char* qual
        char* seq_revcomp
        char* qual_revcomp
        int[:,:] qhits
        int[:,:] mhits
        int[:] qcigar_address = None
        int[:] qcigar_sizes = None
        np.ndarray names = queries.names
        np.ndarray sequences = queries.sequences
        np.ndarray qualities = queries.qualities
        int[:] queries_sizes = queries.sizes
        int[:,:] hits = postprocessed_hits.hits
        int[:] cigar_address = postprocessed_hits.cigar_address
        int[:,:] cigars = postprocessed_hits.cigars
        int[:] cigar_sizes = postprocessed_hits.cigar_sizes
        int[:] hits_address = postprocessed_hits.hits_address
        int offset = postprocessed_hits.offset
        int window_size = postprocessed_hits.window_size  # we have one address for each query in the window
        char* no_mate_rname = b"*"
        char* mate_rname = no_mate_rname
        int mate_tid = -1, mate_pos = -1, mate_alen = 0
        _rnames = [strip_fasta_comment(rname) for rname in reference_names]
        char** rnames = stringarray(_rnames)

    for k in range(window_size):
        query = k + offset
        hmin = hits_address[k]
        hmax = hits_address[k + 1]

        temp_name = bytes(names[query])
        temp_seq = bytes(sequences[query])
        temp_qual = bytes(qualities[query])
        temp_seq_revcomp = temp_seq[::-1].translate(COMPLEMENT)
        temp_qual_revcomp = temp_qual[::-1]

        size = queries_sizes[query]
        name = temp_name
        seq = temp_seq
        qual = temp_qual
        seq_revcomp = temp_seq_revcomp
        qual_revcomp = temp_qual_revcomp

        with nogil:
            # TODO maybe skip hits with 100% soft clip!
            qhits = hits[hmin:hmax, :]
            if not no_cigars:
                qcigar_sizes = cigar_sizes[hmin:hmax]
                qcigar_address = cigar_address[hmin:hmax]
            flags = 0
            if paired:
                k_mate = k - k % 2 + (k + 1) % 2
                mate = k_mate + offset
                hmin = hits_address[k_mate]
                hmax = hits_address[k_mate + 1]
                flags |= FLAG_MULTIPLE_SEGMENTS
                if k % 2:
                    flags |= FLAG_SECOND_IN_PAIR
                else:
                    flags |= FLAG_FIRST_IN_PAIR
                if hmax - hmin == 0:
                    mate_rname = no_mate_rname
                    mate_tid = -1
                    mate_pos = -1
                    mate_alen = 0
                    flags |= FLAG_MATE_UNMAPPED
                else:
                    mate_refid = hits[hmin, COL_REFID]
                    mate_tid = get_tid(mate_refid)
                    mate_rname = rnames[mate_tid]
                    mate_pos = hits[hmin, COL_POS]
                    if no_cigars:
                        mate_alen = queries_sizes[mate]
                    else:
                        mate_alen = get_alignment_length(cigars[cigar_address[hmin]:cigar_address[hmin] + cigar_sizes[hmin], :])
                    flags |= FLAG_SEGMENTS_PROPERLY_ALIGNED
                    if common.is_revcomp(mate_refid):
                        flags |= FLAG_MATE_REVCOMP
            print_sam_records(size, name, seq, qual, seq_revcomp, qual_revcomp, qhits, qcigar_address, cigars, qcigar_sizes, mate_rname, mate_tid, mate_pos, mate_alen, flags, rnames, use_xa, no_cigars)
        #################
    free(rnames)
    #free(no_mate_rname)


def strip_fasta_comment(name):
    return name.split(None, 1)[0]


def print_sam_header_line(*items):
    """Print a SAM header line."""
    cdef:
        bytes t = b"\t".join(map(str.encode, items))
        char* out = t
    printf(b"%s\n", out)


def print_sam_header(references, list read_group):
    """Print a sam header."""
    print_sam_header_line("@HD", "VN:1.4", "SO:queryname")
    for rname, rsize in zip(references.names, references.sizes):
        print_sam_header_line("@SQ", "SN:{}".format(strip_fasta_comment(rname).decode()), "LN:{}".format(rsize))
    if read_group:
        print_sam_header_line("@RG", *read_group)
    print_sam_header_line("@PG", "ID:peanut", "PN:peanut", "VN:{}".format(peanut.__version__))
