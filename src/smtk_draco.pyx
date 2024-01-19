#cython: language_level=3
# distutils: language = c++
cimport common
cimport decoder
cimport encoder

cimport cpython.pycapsule
cimport cpython.object

from libc.stdint cimport uint8_t

__version__ = "1.0.0"

# print("Byte: ", common.ComponentType.Byte)

# common
def getNumberOfComponents(dataType: str):
     return common.getNumberOfComponents(dataType.encode("utf-8"))

# TODO: expose ComponentType enum
def getComponentByteLength(componentType):
    return common.getComponentByteLength(componentType)

# TODO: expose ComponentType enum
def getAttributeStride(componentType, dataType: str):
    return common.getAttributeStride(componentType, dataType.encode("utf-8"))

# decoder
cdef void decoderDestructor(object decoderObject) noexcept:
    handle = cpython.pycapsule.PyCapsule_GetPointer(decoderObject, "decoder")
    decoder.decoderRelease(<decoder.Decoder*>handle)

def decoderCreate():
    handle = decoder.decoderCreate()
    if not handle: 
        raise MemoryError("Failed to create decoder")

    return cpython.pycapsule.PyCapsule_New(handle, "decoder", decoderDestructor)

def decoderRelease(decoderObject: object):
    decoderDestructor(decoderObject)

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
cdef void encoderDestructor(object encoderObject) noexcept:
    handle = cpython.pycapsule.PyCapsule_GetPointer(encoderObject, "encoder")
    encoder.encoderRelease(<encoder.Encoder*>handle)

def encoderCreate(vertexCount: int):
    handle = encoder.encoderCreate(vertexCount)
    if not handle: 
        raise MemoryError("Failed to create encoder")

    return cpython.pycapsule.PyCapsule_New(handle, "encoder", encoderDestructor)

def encoderRelease(encoderObject: object):
    encoderDestructor(encoderObject)

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