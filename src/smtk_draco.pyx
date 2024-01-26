#cython: language_level=3
#distutils: language = c++
cimport common
cimport decoder
cimport encoder

cimport cpython.pycapsule
cimport cpython.object

from libc.stdint cimport uint8_t

from _version import version

__version__ = version

# print("Byte: ", common.ComponentType.Byte)

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
        print("Creating decoder")
        self.thisptr = decoder.decoderCreate()
 
    def __dealloc__(self):
        print("Releasing decoder")
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

def decoderCreate():
    handle = decoder.decoderCreate()
    if not handle: 
        raise MemoryError("Failed to create decoder")

    return cpython.pycapsule.PyCapsule_New(handle, "decoder", NULL)

def decoderRelease(decoderObject: object):
    handle = cpython.pycapsule.PyCapsule_GetPointer(decoderObject, "decoder")
    decoder.decoderRelease(<decoder.Decoder*>handle)

def decoderDecode(decoderObject: object, data: bytes, byteLength: int ):
    if len(data) != byteLength:
        raise ValueError("Data length mismatch")

    handle = <decoder.Decoder*>cpython.pycapsule.PyCapsule_GetPointer(decoderObject, "decoder")

    cdef void* byteBuffer = <void*><char*>data
    return decoder.decoderDecode(handle, byteBuffer, byteLength)

def decoderGetVertexCount(decoderObject: object):
    handle = <decoder.Decoder*>cpython.pycapsule.PyCapsule_GetPointer(decoderObject, "decoder")
    return decoder.decoderGetVertexCount(handle)

def decoderGetIndexCount(decoderObject: object):
    handle = <decoder.Decoder*>cpython.pycapsule.PyCapsule_GetPointer(decoderObject, "decoder")
    return decoder.decoderGetIndexCount(handle)

def decoderAttributeIsNormalized(decoderObject: object, id: int):
    handle = <decoder.Decoder*>cpython.pycapsule.PyCapsule_GetPointer(decoderObject, "decoder")
    return decoder.decoderAttributeIsNormalized(handle, id)

def decoderReadAttribute(decoderObject: object, id: int, componentType: int, dataType: str):
    handle = <decoder.Decoder*>cpython.pycapsule.PyCapsule_GetPointer(decoderObject, "decoder")
    return decoder.decoderReadAttribute(handle, id, componentType, dataType.encode("utf-8"))

def decoderGetAttributeByteLength(decoderObject: object, id: int ):
    handle = <decoder.Decoder*>cpython.pycapsule.PyCapsule_GetPointer(decoderObject, "decoder")
    return decoder.decoderGetAttributeByteLength(handle, id)

def decoderCopyAttribute(decoderObject: object, id: int, output: bytes):
    handle = <decoder.Decoder*>cpython.pycapsule.PyCapsule_GetPointer(decoderObject, "decoder")
    cdef void* byteBuffer = <void*><char*>output
    return decoder.decoderCopyAttribute(handle, id, byteBuffer)

def decoderReadIndices(decoderObject: object, indexComponentType):
    handle = <decoder.Decoder*>cpython.pycapsule.PyCapsule_GetPointer(decoderObject, "decoder")
    return decoder.decoderReadIndices(handle, indexComponentType)

def decoderGetIndicesByteLength(decoderObject: object):
    handle = <decoder.Decoder*>cpython.pycapsule.PyCapsule_GetPointer(decoderObject, "decoder")
    return decoder.decoderGetIndicesByteLength(handle)

def decoderCopyIndices(decoderObject: object, output: bytes):
    handle = <decoder.Decoder*>cpython.pycapsule.PyCapsule_GetPointer(decoderObject, "decoder")
    cdef void* byteBuffer = <void*><char*>output
    decoder.decoderCopyIndices(handle, byteBuffer)

# encoder

cdef class Encoder():
    cdef encoder.Encoder* thisptr

    def __cinit__(self, vertex_count: int):
        print("Creating encoder")
        self.thisptr = encoder.encoderCreate(vertex_count)
 
    def __dealloc__(self):
        print("Releasing encoder")
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

def encoderCreate(vertexCount: int):
    handle = encoder.encoderCreate(vertexCount)
    if not handle: 
        raise MemoryError("Failed to create encoder")

    return cpython.pycapsule.PyCapsule_New(handle, "encoder", NULL)

def encoderRelease(encoderObject: object):
    handle = cpython.pycapsule.PyCapsule_GetPointer(encoderObject, "encoder")
    encoder.encoderRelease(<encoder.Encoder*>handle)

def encoderSetCompressionLevel(encoderObject: object, compressionLevel: int):
    handle = <encoder.Encoder*>cpython.pycapsule.PyCapsule_GetPointer(encoderObject, "encoder")
    encoder.encoderSetCompressionLevel(handle, compressionLevel)

def encoderSetQuantizationBits(encoderObject: object, position: int, normal: int, uv: int, color: int, generic: int):
    handle = <encoder.Encoder*>cpython.pycapsule.PyCapsule_GetPointer(encoderObject, "encoder")
    encoder.encoderSetQuantizationBits(handle, position, normal, uv, color, generic)

def encoderEncode(encoderObject: object, preserveTriangleOrder: bool):
    handle = <encoder.Encoder*>cpython.pycapsule.PyCapsule_GetPointer(encoderObject, "encoder")
    return encoder.encoderEncode(handle, preserveTriangleOrder)

def encoderGetByteLength(encoderObject: object):
    handle = <encoder.Encoder*>cpython.pycapsule.PyCapsule_GetPointer(encoderObject, "encoder")
    return encoder.encoderGetByteLength(handle)

def encoderCopy(encoderObject: object, data: bytes):
    handle = <encoder.Encoder*>cpython.pycapsule.PyCapsule_GetPointer(encoderObject, "encoder")
    cdef uint8_t* byteBuffer = <uint8_t*>data
    encoder.encoderCopy(handle, byteBuffer)

def encoderSetIndices(encoderObject: object, indexComponentType: int, indexCount: int, indices: bytes):
    handle = <encoder.Encoder*>cpython.pycapsule.PyCapsule_GetPointer(encoderObject, "encoder")
    cdef void* byteBuffer = <void*>indices
    encoder.encoderSetIndices(handle, indexComponentType, indexCount, byteBuffer)

def encoderSetAttribute(encoderObject: object, attributeName: str, componentType: int, dataType: str, data: bytes):
    handle = <encoder.Encoder*>cpython.pycapsule.PyCapsule_GetPointer(encoderObject, "encoder")
    cdef void* byteBuffer = <void*><uint8_t*>data
    return encoder.encoderSetAttribute(handle, attributeName.encode("utf-8"), componentType, dataType.encode("utf-8"), byteBuffer)

def encoderGetEncodedVertexCount(encoderObject: object):
    handle = <encoder.Encoder*>cpython.pycapsule.PyCapsule_GetPointer(encoderObject, "encoder")
    return encoder.encoderGetEncodedVertexCount(handle)

def encoderGetEncodedIndexCount(encoderObject: object):
    handle = <encoder.Encoder*>cpython.pycapsule.PyCapsule_GetPointer(encoderObject, "encoder")
    return encoder.encoderGetEncodedIndexCount(handle)