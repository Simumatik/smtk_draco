#cython: language_level=3
from libc.stdint cimport uint8_t, uint32_t

cdef extern from "common.cpp":
    pass

cdef extern from "common.h": 

    cdef enum ComponentType:
        Byte = 5120,
        UnsignedByte = 5121,
        Short = 5122,
        UnsignedShort = 5123,
        UnsignedInt = 5125,
        Float = 5126,

    size_t getNumberOfComponents(char* dataType)

    size_t getComponentByteLength(size_t componentType)

    size_t getAttributeStride(size_t componentType, char* dataType)
