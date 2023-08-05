# cython: boundscheck=False, wraparound=False, cdivision=True

import numpy as np
cimport numpy as np
from cython.operator cimport dereference as deref
cimport peanut.common as common


cdef inline char decode_char(unsigned int* encoded_sequence, int pos) nogil:
    """Decode a bitencoded sequence into characters."""
    return (encoded_sequence[pos / 16] >> ((pos % 16) * 2)) & 3


cdef void rescue(
    int refid,
    unsigned int* reference,
    int reference_size,
    int reference_offset,
    unsigned int* query,
    int query_size,
    int pos,
    int insert_size,
    int insert_size_error,
    int* best_pos,
    int* best_score
    ) nogil:
    """ Search for the start position with the highest percent identity by calculating the edit distance."""
    pos = common.bam_pos_to_pos(reference_size, reference_offset, refid, pos, query_size)
    pos -= insert_size + insert_size_error

    cdef:
        int[:,:] D
        int i, j
        int curr_col, prev_col, curr_dist
        int curr_pos = pos
        int best_dist = query_size
        int best_i = -1
        int window_size = min(reference_size - pos, (insert_size + insert_size_error) * 2)
        char c_ref, c_query
    with gil:
        D = np.empty((2, query_size + 1), dtype=np.int32)

    D[0,:] = 0
    # init distance matrix
    for j in range(query_size + 1):
        D[1,j] = j # TODO verify

    for i in range(window_size):
        curr_col = i % 2
        prev_col = 1 - curr_col
        # allow to begin anywhere in the text
        D[curr_col, 0] = 0

        c_ref = decode_char(reference, pos + i)

        for j in range(1, query_size + 1):
            c_query = decode_char(query, j)
            D[curr_col, j] = min(
                D[prev_col, j - 1] + (c_ref != c_query),
                D[prev_col, j] + 1,
                D[curr_col, j - 1] + 1
            )

        if D[curr_col, j] < best_dist:
            best_dist = D[curr_col, j]
            best_i = i
        curr_pos -= 1

    best_pos[0] = common.pos_to_bam_pos(reference_size, reference_offset, refid, pos + best_i, query_size)
    best_score[0] = <int> (100.0 * (query_size - best_dist) / query_size)
