#cython: language_level=3
#distutils: language = c++
cimport common
cimport decoder
cimport encoder

cimport cpython.pycapsule
cimport cpython.object

from libc.stdint cimport uint8_t

__version__ = "0.0.0"

# common
def get_number_of_components(dataType: str):
     return common.getNumberOfComponents(dataType.encode("utf-8"))

# TODO: expose ComponentType enum
def get_component_byte_length(componentType):
    return common.getComponentByteLength(componentType)

# TODO: expose ComponentType enum
def get_attribute_stride(componentType, dataType: str):
    return common.getAttributeStride(componentType, dataType.encode("utf-8"))

# decoder
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

# encoder

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
