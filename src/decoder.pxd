#cython: language_level=3
from libc.stdint cimport uint8_t, uint32_t
from libcpp cimport bool

cdef extern from "decoder.cpp":
    pass

cdef extern from "decoder.h": 

    ctypedef struct Decoder:
        pass

    Decoder* decoderCreate()

    void decoderRelease(Decoder* decoder) except *

    bool decoderDecode(Decoder* decoder, void* data, size_t byteLength)

    uint32_t decoderGetVertexCount(Decoder* decoder)

    uint32_t decoderGetIndexCount(Decoder* decoder)

    bool decoderAttributeIsNormalized(Decoder* decoder, uint32_t id)

    bool decoderReadAttribute(Decoder* decoder, uint32_t id, size_t componentType, char* dataType)

    size_t decoderGetAttributeByteLength(Decoder* decoder, size_t id)

    void decoderCopyAttribute(Decoder* decoder, size_t id, void* output)

    bool decoderReadIndices(Decoder* decoder, size_t indexComponentType)

    size_t decoderGetIndicesByteLength(Decoder* decoder)

    void decoderCopyIndices(Decoder* decoder, void* output)
