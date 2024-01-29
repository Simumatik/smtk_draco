#cython: language_level=3
from libc.stdint cimport uint8_t, uint32_t, uint64_t
from libcpp cimport bool

cdef extern from "encoder.cpp":
    pass

cdef extern from "encoder.h": 

    ctypedef struct Encoder:
        pass

    Encoder* encoderCreate(uint32_t vertexCount)

    void encoderRelease(Encoder *encoder) except *

    void encoderSetCompressionLevel(Encoder* encoder, uint32_t compressionLevel)

    void encoderSetQuantizationBits(Encoder* encoder, uint32_t position, uint32_t normal, uint32_t uv, uint32_t color, uint32_t generic)

    bool encoderEncode(Encoder* encoder, uint8_t preserveTriangleOrder)

    uint64_t encoderGetByteLength(Encoder* encoder)

    void encoderCopy(Encoder*encoder, uint8_t* data)

    void encoderSetIndices(Encoder* encoder, size_t indexComponentType, uint32_t indexCount, void* indices)

    uint32_t encoderSetAttribute(Encoder* encoder, char* attributeName, size_t componentType, char* dataType, void* data)

    uint32_t encoderGetEncodedVertexCount(Encoder* encoder)

    uint32_t encoderGetEncodedIndexCount(Encoder* encoder)