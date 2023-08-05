# -*- coding: utf-8 -*-
#cython: boundscheck=False, cdivision=True


__author__ = "Johannes Köster"
__license__ = "MIT"


import os
import io
import gzip
import logging
from itertools import repeat, cycle, islice
from collections import namedtuple

import h5py
import numpy as np
cimport numpy as np

from peanut.utils import PeanutError


def open_hdf5(path, write=False):
    """Open an HDF5 file."""
    if os.path.exists(path):
        if write:
            os.remove(path)
    else:
        if not write:
            raise PeanutError("Error opening HDF5 index. File {} does not exist.".format(path))
    try:
        return h5py.File(path, mode="w" if write else "r")
    except OSError as e:
        raise PeanutError("Error opening HDF5 index. ".format(str(e)))


def open_text(path, mode="rb"):
    """Open a (gzipped) text file."""
    return io.BufferedReader(gzip.open(path, mode), buffer_size=io.DEFAULT_BUFFER_SIZE * 64) if path.endswith(".gz") else open(path, mode, buffering=-1)


SequenceRecord = namedtuple("SequenceRecord", "name seq")


def read_fastq_buffered(fq1, fq2, int buffersize):
    """Read fastq into a numpy buffer."""
    cdef:
        int recordline, query_size, maxquerysize
        bytes l
        char* _l
        char identifier = b"@"
        int buffer = 0
        int[:] query_sizes = np.empty(buffersize, dtype=np.int32)
        object[:] query_names = np.empty(buffersize, dtype=object)
        object[:] query_sequences = np.empty(buffersize, dtype=object)
        object[:] query_qualities = np.empty(buffersize, dtype=object)

    fqs = cycle([iter(fq1), iter(fq2)]) if fq2 is not None else repeat(iter(fq1))

    for fq in fqs:
        try:
            name, seq, _, qual = islice(fq, 4)
        except ValueError:
            break

        if not name[0] == identifier:
            raise IOError("Expected sequence identifier.")
        name = name[1:].split()[0]
        seq = seq[:-1]
        qual = qual[:-1]

        query_sizes[buffer] = len(seq)
        query_names[buffer] = name
        query_sequences[buffer] = seq
        query_qualities[buffer] = qual
        buffer += 1

        if buffer == buffersize:
            yield query_names, query_sizes, query_sequences, query_qualities

            # init buffer again
            buffer = 0
            query_sizes = np.empty(buffersize, dtype=np.int32)
            query_names = np.empty(buffersize, dtype=object)
            query_sequences = np.empty(buffersize, dtype=object)
            query_qualities = np.empty(buffersize, dtype=object)

    if buffer > 0:
        yield query_names[:buffer], query_sizes[:buffer], query_sequences[:buffer], query_qualities[:buffer]


def read_fasta(path, identifier=ord(b">")):
    """Read a fasta file."""
    with open_text(path) as fa:
        for i, l in enumerate(fa):
            if l[0] == identifier:
                if i:
                    yield SequenceRecord(name=name, seq=bytes(seq))
                name = l[1:-1]
                seq = bytearray()
            else:
                seq.extend(l[:-1])
        yield SequenceRecord(name=name, seq=bytes(seq))
