#cython: language_level=3
cimport encoder
from libc.stdint cimport uint8_t

cdef class Encoder():
    cdef encoder.Encoder* thisptr

    def __cinit__(self, vertex_count: int):
        self.thisptr = encoder.encoderCreate(vertex_count)
 
    def __dealloc__(self):
        encoder.encoderRelease( self.thisptr )

    def set_compression_level(self, compressionLevel: int):
        encoder.encoderSetCompressionLevel(self.thisptr, compressionLevel)

    def set_quantization_bits(self, position: int, normal: int, uv: int, color: int, generic: int):
        encoder.encoderSetQuantizationBits(self.thisptr, position, normal, uv, color, generic)

    def encode(self, preserveTriangleOrder: bool = True):
        return encoder.encoderEncode(self.thisptr, preserveTriangleOrder)
    
    def get_byte_length(self):
        return encoder.encoderGetByteLength(self.thisptr)

    def copy(self, output: bytes):
        cdef uint8_t* output_buffer = <uint8_t*>output
        encoder.encoderCopy(self.thisptr, output_buffer)

    def set_indices(self, indexComponentType: int, indexCount: int, indices: bytes):
        cdef void* index_buffer = <void*>indices
        encoder.encoderSetIndices(self.thisptr, indexComponentType, indexCount, index_buffer)

    def set_attribute(self, attributeName: str, componentType: int, dataType: str, data: bytes):
        cdef void* attribute_buffer = <void*><uint8_t*>data
        return encoder.encoderSetAttribute(self.thisptr, attributeName.encode("utf-8"), componentType, dataType.encode("utf-8"), attribute_buffer)

    def get_encoded_vertex_count(self):
        return encoder.encoderGetEncodedVertexCount(self.thisptr)

    def get_encoded_index_count(self):
        return encoder.encoderGetEncodedIndexCount(self.thisptr)
