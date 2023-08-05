from murmurhash.mrmr cimport hash64
from preshed.maps cimport PreshMap
from libc.stdint cimport uint64_t


def sequential_inserts(n):
    cdef PreshMap table = PreshMap(n)

    cdef uint64_t i
    cdef uint64_t key
    for i in range(n):
        key = hash64(&i, sizeof(i), 0)
        table.set(key, <void*>i)
    return table


def py_sequential_inserts(n):
    table = {}

    cdef uint64_t i
    cdef uint64_t key
    for i in range(n):
        key = hash64(&i, sizeof(i), 0)
        table[key] = i
    return table


def sequential_retrieve(table, start, stop):
    cdef uint64_t i
    cdef uint64_t key
    cdef uint64_t value = 0
    for i in range(start, stop):
        key = hash64(&i, sizeof(i), 0)
        value += table[key]
    return value


from sparsehash.dense_hash_map cimport dense_hash_map


cdef class DenseHashMap64:
    cdef dense_hash_map[uint64_t, uint64_t] c

    def __init__(self):
        self.c.set_empty_key(0)

    def __getitem__(self, uint64_t key):
        return self.c[key]

    def __setitem__(self, uint64_t key, uint64_t value):
        self.c[key] = value
