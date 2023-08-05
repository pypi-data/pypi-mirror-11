# cython: boundscheck=False, wraparound=False, cdivision=True

cdef bint is_revcomp(int refid) nogil:
    """Return True if refid belongs to a reverse complement."""
    return refid % 2  # every second ref is the reverse complement


cdef int pos_to_bam_pos(int reference_size, int reference_offset, int refid, int pos, int query_size) nogil:
    """Adjust internal position for bam output."""
    return reference_size - pos - 1 if not is_revcomp(refid) else pos - query_size - reference_offset + 1


cdef int bam_pos_to_pos(int reference_size, int reference_offset, int refid, int pos, int query_size) nogil:
    """Adjust a bam position to internal coordinates."""
    return reference_size - pos - 1 if not is_revcomp(refid) else pos + query_size + reference_offset - 1
