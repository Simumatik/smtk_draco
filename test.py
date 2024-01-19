import smtk_draco as draco

dir( draco )

# region common
assert draco.getNumberOfComponents("SCALAR") == 1
assert draco.getNumberOfComponents("VEC2") == 2
assert draco.getNumberOfComponents("VEC3") == 3
assert draco.getNumberOfComponents("VEC4") == 4
assert draco.getNumberOfComponents("MAT2") == 4
assert draco.getNumberOfComponents("MAT3") == 9
assert draco.getNumberOfComponents("MAT4") ==  16
assert draco.getNumberOfComponents("") == 0 # invalid case (return 0)

# Find a way to expose component type enum properly
assert draco.getComponentByteLength(5120) == 1  # Byte
assert draco.getComponentByteLength(5121) == 1  # Unsigned Byte
assert draco.getComponentByteLength(5122) == 2  # Short
assert draco.getComponentByteLength(5123) == 2  # Unsigned Short
assert draco.getComponentByteLength(5125) == 4  # Unsigned Int
assert draco.getComponentByteLength(5126) == 4  # Unsigned Float
assert draco.getComponentByteLength(0) == 0    # invalid case (return 0)

# Find a way to expose the component type enum properly
assert draco.getAttributeStride(5120, "SCALAR") == 1 # Scalar Byte component
assert draco.getAttributeStride(5121, "SCALAR") == 1 # Scalar Unsigned Byte component
assert draco.getAttributeStride(5122, "SCALAR") == 2 # Scalar Short component
assert draco.getAttributeStride(5123, "SCALAR") == 2 # Scalar Unsigned Short component
assert draco.getAttributeStride(5125, "SCALAR") == 4 # Scalar Unsigned Int component
assert draco.getAttributeStride(5126, "SCALAR") == 4 # Scalar Unsigned Float component

assert draco.getAttributeStride(5120, "VEC2") == 2   # Vector with 2 Byte components
assert draco.getAttributeStride(5121, "VEC2") == 2   # Vector with 2 Unsigned Byte components
assert draco.getAttributeStride(5122, "VEC2") == 4   # Vector with 2 Short components
assert draco.getAttributeStride(5123, "VEC2") == 4   # Vector with 2 Unsigned Short components
assert draco.getAttributeStride(5125, "VEC2") == 8   # Vector with 2 Unsigned Int components
assert draco.getAttributeStride(5126, "VEC2") == 8   # Vector with 2 Unsigned Float components

assert draco.getAttributeStride(5120, "VEC3") == 3   # Vector with 3 Byte components
assert draco.getAttributeStride(5121, "VEC3") == 3   # Vector with 3 Unsigned Byte components
assert draco.getAttributeStride(5122, "VEC3") == 6   # Vector with 3 Short components
assert draco.getAttributeStride(5123, "VEC3") == 6   # Vector with 3 Unsigned Short components
assert draco.getAttributeStride(5125, "VEC3") == 12  # Vector with 3 Unsigned Int components
assert draco.getAttributeStride(5126, "VEC3") == 12  # Vector with 3 Unsigned Float components

assert draco.getAttributeStride(5120, "VEC4") == 4   # Vector with 4 Byte components
assert draco.getAttributeStride(5121, "VEC4") == 4   # Vector with 4 Unsigned Byte components
assert draco.getAttributeStride(5122, "VEC4") == 8   # Vector with 4 Short components
assert draco.getAttributeStride(5123, "VEC4") == 8   # Vector with 4 Unsigned Short components
assert draco.getAttributeStride(5125, "VEC4") == 16  # Vector with 4 Unsigned Int components
assert draco.getAttributeStride(5126, "VEC4") == 16  # Vector with 4 Unsigned Float components

assert draco.getAttributeStride(5120, "MAT2") == 4   # Matrix (2x2) with 4 Byte components
assert draco.getAttributeStride(5121, "MAT2") == 4   # Matrix (2x2) with 4 Unsigned Byte components
assert draco.getAttributeStride(5122, "MAT2") == 8   # Matrix (2x2) with 4 Short components
assert draco.getAttributeStride(5123, "MAT2") == 8   # Matrix (2x2) with 4 Unsigned Short components
assert draco.getAttributeStride(5125, "MAT2") == 16  # Matrix (2x2) with 4 Unsigned Int components
assert draco.getAttributeStride(5126, "MAT2") == 16  # Matrix (2x2) with 4 Unsigned Float components

assert draco.getAttributeStride(5120, "MAT3") == 9   # Matrix (3x3) with 9 Byte components
assert draco.getAttributeStride(5121, "MAT3") == 9   # Matrix (3x3) with 9 Unsigned Byte components
assert draco.getAttributeStride(5122, "MAT3") == 18  # Matrix (3x3) with 9 Short components
assert draco.getAttributeStride(5123, "MAT3") == 18  # Matrix (3x3) with 9 Unsigned Short components
assert draco.getAttributeStride(5125, "MAT3") == 36  # Matrix (3x3) with 9 Unsigned Int components
assert draco.getAttributeStride(5126, "MAT3") == 36  # Matrix (3x3) with 9 Unsigned Float components

assert draco.getAttributeStride(5120, "MAT4") == 16  # Matrix (4x4) with 16 Byte components
assert draco.getAttributeStride(5121, "MAT4") == 16  # Matrix (4x4) with 16 Unsigned Byte components
assert draco.getAttributeStride(5122, "MAT4") == 32  # Matrix (4x4) with 16 Short components
assert draco.getAttributeStride(5123, "MAT4") == 32  # Matrix (4x4) with 16 Unsigned Short components
assert draco.getAttributeStride(5125, "MAT4") == 64  # Matrix (4x4) with 16 Unsigned Int components
assert draco.getAttributeStride(5126, "MAT4") == 64  # Matrix (4x4) with 16 Unsigned Float components

# endregion 

# region decoder

# Create a decoder
decoder = draco.decoderCreate()

assert decoder is not None
assert type(decoder).__name__ == 'PyCapsule'

import pathlib
testfile = pathlib.Path(__file__).parent.joinpath("test.drc")
with open(testfile, "rb") as f:
    data = f.read()
    if not draco.decoderDecode(decoder, data, len(data)):
        print(f"Failed to decode {testfile}")
        exit()

vertex_count = draco.decoderGetVertexCount(decoder)
print("Vertices: ", vertex_count)

index_count = draco.decoderGetIndexCount(decoder)
print("Indices: ", index_count)

if not draco.decoderReadIndices(decoder, 5123):
    print('ERROR', 'Draco Decoder: Unable to decode indices. Skipping primitive')
    exit()

print("Index byte length: ", draco.decoderGetIndicesByteLength(decoder))

index_buffer_byte_length = draco.decoderGetIndicesByteLength(decoder)
decoded_index_buffer = bytes(index_buffer_byte_length)
draco.decoderCopyIndices(decoder, decoded_index_buffer)
print(f"Loaded index buffer containing {index_buffer_byte_length} bytes")

print(f"Reading attribute POSITION")
if not draco.decoderReadAttribute(decoder, 0, 5126, "VEC3"):
    print('ERROR', f'Draco Decoder: Could not decode attribute POSITION. Skipping primitive')
    exit()

position_buffer_length = draco.decoderGetAttributeByteLength(decoder, 0)
print("POSITION byte length: ", position_buffer_length)
decoded_position_buffer = bytes(position_buffer_length)
draco.decoderCopyAttribute(decoder, 0, decoded_position_buffer)
print("POSITION attribute normalized: ", draco.decoderAttributeIsNormalized(decoder, 0))

print(f"Reading attribute TEXCOORD_0")
if not draco.decoderReadAttribute(decoder, 1, 5126, "VEC2"):
    print('ERROR', f'Draco Decoder: Could not decode attribute TEXCOORD_0. Skipping primitive')
    exit()

texcoord_0_buffer_length = draco.decoderGetAttributeByteLength(decoder, 1)
print("TEXCOORD_0 byte length: ", texcoord_0_buffer_length)
decoded_texcoord_0_buffer = bytes(texcoord_0_buffer_length)
draco.decoderCopyAttribute(decoder, 1, decoded_texcoord_0_buffer)
print("TEXCOORD_0 attribute normalized: ", draco.decoderAttributeIsNormalized(decoder, 1))

print(f"Reading attribute NORMAL")
if not draco.decoderReadAttribute(decoder, 2, 5126, "VEC3"):
    print('ERROR', f'Draco Decoder: Could not decode attribute NORMAL. Skipping primitive')
    exit()

normal_buffer_length = draco.decoderGetAttributeByteLength(decoder, 2)
print("NORMAL byte length: ", normal_buffer_length)
decoded_normal_buffer = bytes(normal_buffer_length)
draco.decoderCopyAttribute(decoder, 2, decoded_normal_buffer)
print("NORMAL attribute normalized: ", draco.decoderAttributeIsNormalized(decoder, 2))

print(f"Reading attribute TANGENT")
if not draco.decoderReadAttribute(decoder, 3, 5126, "VEC4"):
    print('ERROR', f'Draco Decoder: Could not decode attribute TANGENT. Skipping primitive')
    exit()

tangent_buffer_length = draco.decoderGetAttributeByteLength(decoder, 3)
print("TANGENT byte length: ", tangent_buffer_length)
decoded_tangent_buffer = bytes(tangent_buffer_length)
draco.decoderCopyAttribute(decoder, 3, decoded_tangent_buffer)
print("TANGENT attribute normalized: ", draco.decoderAttributeIsNormalized(decoder, 3))

# Release a decoder
draco.decoderRelease(decoder)

# endregion

# region encoder

# Create a encoder
encoder = draco.encoderCreate(vertex_count)

draco.encoderSetCompressionLevel(encoder, 0)

# Set indices
draco.encoderSetIndices(encoder, 5123, index_count, decoded_index_buffer)
if not draco.encoderEncode(encoder, True): # preserve triangle order
    print("Failed to encode data")

# Set POSITION
position_id = draco.encoderSetAttribute(encoder, "POSITION", 5126, "VEC3", decoded_position_buffer )
print("POSITION attribute ID: ", position_id)
if not draco.encoderEncode(encoder, True): # preserve triangle order
    print("Failed to encode data")

# Set TEXCOORD_0
texcoord_0_id = draco.encoderSetAttribute(encoder, "TEXCOORD_0", 5126, "VEC2", decoded_texcoord_0_buffer )
print("TEXCOORD_0 attribute ID: ", texcoord_0_id)
if not draco.encoderEncode(encoder, True): # preserve triangle order
    print("Failed to encode data")

# Set NORMAL
normal_id = draco.encoderSetAttribute(encoder, "NORMAL", 5126, "VEC3", decoded_normal_buffer )
print("NORMAL attribute ID: ", normal_id)
if not draco.encoderEncode(encoder, True): # preserve triangle order
    print("Failed to encode data")

# Set TANGENT
tangent_id = draco.encoderSetAttribute(encoder, "TANGENT", 5126, "VEC4", decoded_tangent_buffer )
print("TANGENT attribute ID: ", tangent_id)

# Encode the the data
if not draco.encoderEncode(encoder, True): # preserve triangle order
    print("Failed to encode data")

encoded_index_count = draco.encoderGetEncodedIndexCount(encoder)
assert encoded_index_count == index_count
print( "Encoded index count: ", encoded_index_count)

encoded_vertex_count = draco.encoderGetEncodedVertexCount(encoder)
assert encoded_vertex_count == vertex_count
print("Encoded vertex count: ", encoded_vertex_count)

encoded_byte_length = draco.encoderGetByteLength(encoder)
print("Encoded byte length: ", encoded_byte_length)

outputBuffer = bytes(encoded_byte_length)
draco.encoderCopy(encoder, outputBuffer)

# Release a encoder
draco.encoderRelease(encoder)

# endergion