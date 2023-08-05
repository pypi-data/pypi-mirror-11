# -*- coding: utf-8 -*-
#cython: boundscheck=False, wraparound=False, cdivision=True


__author__ = "Johannes Köster"
__license__ = "MIT"


import struct
import math
import random
import re
from itertools import chain
from functools import partial
import numpy as np
cimport numpy as np
import logging

from peanut.utils import to_multiple


ALPHABET = b"ACGT"
ALPHABET_LOWER = b"acgt"
WILDCARD = b"N"
WILDCARDS_REGEX = re.compile(b"[RYMKWSBDHVN]")
WILDCARDS = {
    ord("R"): [b"A", b"G"],
    ord("Y"): [b"C", b"T"],
    ord("M"): [b"C", b"A"],
    ord("K"): [b"T",b"G"],
    ord("W"): [b"T",b"A"],
    ord("S"): [b"C",b"G"],
    ord("B"): [b"C",b"T",b"G"],
    ord("D"): [b"A",b"T",b"G"],
    ord("H"): [b"A",b"T",b"C"],
    ord("V"): [b"A",b"C",b"G"],
    ord("N"): [b"A",b"C",b"G",b"T"]}
ALPHABET_BITENCODED = b"\x00\x01\x02\x03"
BITENCODE = bytes.maketrans(ALPHABET + ALPHABET_LOWER, ALPHABET_BITENCODED * 2)
BITENCODE_COMPLEMENT = bytes.maketrans(ALPHABET + ALPHABET_LOWER, ALPHABET_BITENCODED[::-1] * 2)
BITDECODE = bytes.maketrans(ALPHABET_BITENCODED, ALPHABET)
COMPLEMENT = bytes.maketrans(ALPHABET + ALPHABET_LOWER + b"N", ALPHABET[::-1] + ALPHABET_LOWER[::-1] + b"N")

replace_wildcard = lambda c: random.choice(WILDCARDS[ord(c.group())])


cdef char UPPERCASE_OFFSET = <char>'a' - <char>'A'


def preprocess_query_sequences(object[:] sequences, int maxquerysize):
    """Preprocess query sequences, converting lowercase and Ns."""

    cdef:
        int k, i, query_size
        bytes _seq
        char* seq
        char s
        char* bitencode = BITENCODE
        char[:,:] processed = np.zeros((sequences.shape[0], maxquerysize), dtype=np.uint8)

    for k in range(sequences.shape[0]):
        _seq = sequences[k]
        query_size = len(_seq)
        seq = _seq
        with nogil:
            for i in range(query_size):
                s = seq[i]
                if s >= 'a' and s <= 'z':
                    s -= UPPERCASE_OFFSET
                if s != 'A' and s != 'C' and s != 'G' and s != 'T':
                    with gil:
                        s = random.choice(WILDCARDS[s])[0]
                processed[k, query_size - i - 1] = bitencode[s]  # reversed sequence since we map reverse
    return np.asarray(processed, dtype=np.uint8)


def preprocess_bases(sequence):
    """
    Preprocess the given sequence such that all characters are in ACGT.
    Note, this should be called immediately before the bitencode.
    """
    return WILDCARDS_REGEX.sub(replace_wildcard, sequence)


def preprocess_length(sequence):
    """
    Preprocess the given sequence such that it is a multiple of 16.
    """
    return sequence.ljust(math.ceil(len(sequence) / 16.0) * 16, WILDCARD)


def get_not_n_pos(sequence, bytes nstretch=b"N" * 16):
    """Return positions not containing an N homopolymer."""
    cdef:
        int i

    return np.array(
        [i for i in range(0, len(sequence), 16) 
            if sequence[i:i+16] != nstretch], dtype=np.int32)


def bitencode(sequence):
    """Bitencode a sequence."""
    return np.fromstring(sequence.translate(BITENCODE), dtype=np.uint8)


def bitencode_comp(sequence):
    """Bitencode a sequence into its complement."""
    return np.fromstring(sequence.translate(BITENCODE_COMPLEMENT), dtype=np.uint8)


cdef inline void _pack_sequence(char[:] bitencoded_sequence, unsigned int[:] packed_sequence) nogil:
    """Pack a bitencoded sequence into 32-bit words."""
    cdef:
        int qgram, i, j
        int sequence_size = bitencoded_sequence.shape[0]
        int packed_width = packed_sequence.shape[0]
        int jmin = 0

    for i in range(packed_width):
        qgram = 0
        for j in range(min(jmin + 15, sequence_size - 1), jmin - 1, -1):
            qgram <<= 2
            qgram |= bitencoded_sequence[j]
        packed_sequence[i] = qgram
        jmin += 16


def pack_sequence(char[:] bitencoded_sequence):
    """Pack a bitencoded sequence."""
    packed_size = math.ceil(len(bitencoded_sequence) / 16.0)
    packed_sequence = np.empty(packed_size, dtype=np.uint32)
    _pack_sequence(bitencoded_sequence, packed_sequence)
    return packed_sequence


def pack_sequences(char[:,:] bitencoded_sequences):
    """Pack many bitencoded sequences."""
    cdef:
        int k
        int sequences_size = bitencoded_sequences.shape[0]
        int sequences_width = bitencoded_sequences.shape[1]
        int packed_width = math.ceil(sequences_width / 16.0)
        unsigned int[:,:] packed_sequences = np.zeros((sequences_size, packed_width), dtype=np.uint32)

    with nogil:
        for k in range(sequences_size):
            _pack_sequence(bitencoded_sequences[k, :], packed_sequences[k, :])
    return np.asarray(packed_sequences, dtype=np.uint32)


def bitdecode(bitencoded_sequence):
    """Use for testing only."""
    def chars(seq):
        three = np.uint32(3)
        for _ in range(16):
            yield seq & three
            seq >>= 2
    return struct.pack(
        "<16B", *chars(bitencoded_sequence)).translate(BITDECODE)


def bitdecode_packed(packed_sequence):
    """Use for testing only."""
    return b"".join(map(bitdecode, packed_sequence))
