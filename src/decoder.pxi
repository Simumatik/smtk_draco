#cython: language_level=3
#distutils: language = c++
cimport decoder

cdef class Decoder():
    cdef decoder.Decoder* thisptr

    def __cinit__(self):
        self.thisptr = decoder.decoderCreate()
 
    def __dealloc__(self):
        decoder.decoderRelease( self.thisptr )

    def decode(self, data: bytes):
        cdef void* data_pointer = <void*><char*>data
        cdef size_t data_length = len(data)
        return decoder.decoderDecode(self.thisptr, data_pointer, data_length)

    def get_vertex_count(self):
        return decoder.decoderGetVertexCount(self.thisptr)

    def get_index_count(self):
        return decoder.decoderGetIndexCount(self.thisptr)

    def attribute_is_normalized(self, id: int):
        return decoder.decoderAttributeIsNormalized(self.thisptr, id)

    def read_attribute(self, id: int, componentType: int, dataType: str):
        return decoder.decoderReadAttribute(self.thisptr, id, componentType, dataType.encode("utf-8"))

    def get_attribute_byte_length(self, id: int ):
        return decoder.decoderGetAttributeByteLength(self.thisptr, id)

    def copy_attribute(self, id: int, output: bytes):
        cdef void* output_buffer = <void*><char*>output
        decoder.decoderCopyAttribute(self.thisptr, id, output_buffer)

    def read_indices(self, indexComponentType):
        return decoder.decoderReadIndices(self.thisptr, indexComponentType)

    def get_index_byte_length(self):
        return decoder.decoderGetIndicesByteLength(self.thisptr)

    def copy_indices(self, output: bytes):
        cdef void* output_buffer = <void*><char*>output
        decoder.decoderCopyIndices(self.thisptr, output_buffer)