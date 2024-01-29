import smtk_draco as draco
import pathlib

test_resource_directory = pathlib.Path(__file__).parent.joinpath("resources/")
testfile = test_resource_directory / "test.drc"

def read_test_file():
    with open(testfile, "rb") as f:
        return f.read()

def get_and_check_attribute(decoder, attribute_id, attribute_name, component_type, data_type, expected_buffer_length, expect_normalized_data ):
    assert decoder.read_attribute(attribute_id, component_type, data_type), f'Expected the attribute {attribute_name} (ID {attribute_id}) to be read'

    # Get the position buffer byte length
    buffer_length = decoder.get_attribute_byte_length(attribute_id)
    assert buffer_length == expected_buffer_length, f"Invalid {attribute_name} buffer size. Expected {expected_buffer_length}, got {buffer_length}"

    # Create a buffer and copy the data
    decoded_buffer_data = bytes(buffer_length)
    decoder.copy_attribute(attribute_id, decoded_buffer_data)

    attribute_is_normalized = decoder.attribute_is_normalized(attribute_id)
    assert expect_normalized_data == attribute_is_normalized, f"Expected attribute_is_normalized to return {expect_normalized_data}, got {not attribute_is_normalized}"

    return decoded_buffer_data

def decode_test_data(test_data: input):
    """ 
    Helper method to decode a Draco data and check the result
    Currently hard-coded for the example file (both raw and encoded).
    """
    decoder = draco.Decoder()

    # Decode the file
    assert decoder.decode(test_data), f"Failed to decode test data"

    # Get vertex count
    vertex_count = decoder.get_vertex_count()
    expected_vertex_count = 6697
    assert vertex_count == expected_vertex_count, f"Invalid vertex count. Expected {expected_vertex_count}, got {vertex_count}"
    
    # Get index count
    index_count = decoder.get_index_count()
    expected_index_count = 12783
    assert index_count == expected_index_count, f"Invalid index count. Expected {expected_index_count}, got {index_count}"
    
    # Read the index data
    assert decoder.read_indices(5123), 'Expected indices to be read'

    # Get the index buffer byte length
    index_buffer_byte_length = decoder.get_index_byte_length()
    expected_index_buffer_byte_length = 25566
    assert index_count == expected_index_count, f"Invalid index buffer size. Expected {expected_index_buffer_byte_length}, got {index_buffer_byte_length}"

    # Create a buffer and copy the data
    index_data = bytes(index_buffer_byte_length)
    decoder.copy_indices(index_data)
    
    # POSITION (attribute 0)
    expected_position_attribute_id = 0
    position_data = get_and_check_attribute(decoder, expected_position_attribute_id, "POSITION", 5126, "VEC3", 80364, False)
    # TODO: validate the data

    # TEXCOORD_0 (attribute 1)
    expected_texcoord_0_attribute_id = 1
    texcoord_0_data = get_and_check_attribute(decoder, expected_texcoord_0_attribute_id, "TEXCOORD_0", 5126, "VEC2", 53576, False)
    # TODO: validate the data

    # NORMAL attribute
    expected_normal_attribute_id = 2
    normal_data = get_and_check_attribute(decoder, expected_normal_attribute_id, "NORMAL", 5126, "VEC3", 80364, False)    
    # TODO: validate the data

    # TANGENT attribute
    expected_tangent_attribute_id = 3
    tangent_data = get_and_check_attribute(decoder, expected_tangent_attribute_id, "TANGENT", 5126, "VEC4", 107152, False)
    # TODO: validate the data

    return vertex_count, index_count, index_data, position_data, texcoord_0_data, normal_data, tangent_data

def encode_test_data( vertex_count, index_count, index_data, position_data, texcoord_0_data, normal_data, tangent_data ): 
    """ 
    Helper method to encode mesh data and check the result
    Currently hard-coded for the example file ()
    """
    encoder = draco.Encoder(vertex_count)

    ## Set the attributes first

    # Set POSITION
    position_attribute_id = encoder.set_attribute("POSITION", 5126, "VEC3", position_data )
    expected_position_attribute_id = 0
    assert position_attribute_id == expected_position_attribute_id, f"Expected POSITION attribute ID to be {expected_position_attribute_id}, got {position_attribute_id}"

    # Set TEXCOORD_0
    texcoord_0_attribute_id = encoder.set_attribute("TEXCOORD_0", 5126, "VEC2", texcoord_0_data )
    expected_texcoord_0_attribute_id = 1
    assert texcoord_0_attribute_id == expected_texcoord_0_attribute_id, f"Expected TEXCOORD_0 attribute ID to be {expected_texcoord_0_attribute_id}, got {texcoord_0_attribute_id}"

    # Set NORMAL
    normal_attribute_id = encoder.set_attribute("NORMAL", 5126, "VEC3", normal_data )
    expected_normal_attribute_id = 2
    assert normal_attribute_id == expected_normal_attribute_id, f"Expected NORMAL attribute ID to be {expected_normal_attribute_id}, got {normal_attribute_id}"
    
    # Set TANGENT
    tangent_attribute_id = encoder.set_attribute("TANGENT", 5126, "VEC4", tangent_data )
    expected_tangent_attribute_id = 3
    assert tangent_attribute_id == expected_tangent_attribute_id, f"Expected TANGENT attribute ID to be {expected_tangent_attribute_id}, got {tangent_attribute_id}"
    
    ## Set the indices
    encoder.set_indices(5123, index_count, index_data)
   
    # Set the compression level
    encoder.set_compression_level(0) # 0 - worst/speediest compression

    # Set the quantization bits
    encoder.set_quantization_bits(position=0, normal=0, uv=0, color=0, generic=0) # 0 = no quantization
    
    ## Encode the the data

    assert encoder.encode(True), "Expected encoding to succeed" # True = Preserve triangle order

    ## Check the encoded data
    encoded_index_count = encoder.get_encoded_index_count()
    assert encoded_index_count == index_count, f"Expected encoded index count {index_count}, got {encoded_index_count}"

    encoded_vertex_count = encoder.get_encoded_vertex_count()
    assert encoded_vertex_count == vertex_count, f"Expected encoded vertex count {vertex_count}, got {encoded_vertex_count}"

    # TODO: decode a model with known encoding settings
    encoded_data_length = encoder.get_byte_length()
    expected_data_length = 347064 # This is bigger than the original. We should really use a sample with known settings
    assert encoded_data_length == expected_data_length, f"Expected encoded data length {expected_data_length}, got {encoded_data_length}"
    
    ## Copy the encoded data
    output_data = bytes(encoded_data_length)
    encoder.copy(output_data)

    del encoder    # Delete the encoder to make sure the __dealloc__ works (just for the purposes of this test)

    return output_data

def test_decoder():
    decode_test_data(read_test_file())

def test_encoder():
    """ 
    Decode a file and then encode it using the encoder.
    Currently, the encoded data is not validated - we basically just check that the methods can be called without a crash.
    """

    # Decode the test file
    (
        initial_vertex_count, 
        initial_index_count, 
        initial_index_data, 
        initial_position_data, 
        initial_texcoord_0_data, 
        initial_normal_data, 
        initial_tangent_data 
    ) = decode_test_data( read_test_file() )
    
    # Encode the data
    encode_test_data(
        initial_vertex_count, 
        initial_index_count, 
        initial_index_data, 
        initial_position_data, 
        initial_texcoord_0_data, 
        initial_normal_data, 
        initial_tangent_data
    )
    # TODO: validate the data
   
def test_decoder_encoder_roundtrip():
    """ 
    Decode a file and then encode it using the encoder, and then decode the result 
    """
    # Decode the test file
    ( 
        initial_vertex_count, 
        initial_index_count, 
        initial_index_data, 
        initial_position_data, 
        initial_texcoord_0_data, 
        initial_normal_data, 
        initial_tangent_data
    ) = decode_test_data( read_test_file() )
    
    # Encode the data
    encoded_data = encode_test_data(
        initial_vertex_count, 
        initial_index_count, 
        initial_index_data, 
        initial_position_data, 
        initial_texcoord_0_data, 
        initial_normal_data, 
        initial_tangent_data
    )

    # Decode the encoded data again and compare the result with the initial decoding result
    (
        decoded_vertex_count, 
        decoded_index_count, 
        decoded_index_data, 
        decoded_position_data, 
        decoded_texcoord_0_data, 
        decoded_normal_data, 
        decoded_tangent_data 
    ) = decode_test_data( encoded_data )

    # Check the decoded vertex and index counts
    assert decoded_vertex_count == initial_vertex_count, f"Expected vertex count {initial_vertex_count}, got {decoded_vertex_count}"
    assert decoded_index_count == initial_index_count, f"Expected vertex count {initial_index_count}, got {decoded_index_count}"
    
    # Check the index data buffer length
    initial_index_byte_count = len(initial_index_data)
    decoded_index_byte_count = len(decoded_index_data)
    assert decoded_index_byte_count == initial_index_byte_count, f"Expected index byte count {initial_index_byte_count}, got {decoded_index_byte_count}"
    # TODO: validate the data
    
    # Check the position data buffer length
    initial_position_byte_count = len(initial_position_data)
    decoded_position_byte_count = len(decoded_position_data)
    assert decoded_position_byte_count == initial_position_byte_count, f"Expected position byte count {initial_position_byte_count}, got {decoded_position_byte_count}"
    # TODO: validate the data

    # Check the texcoord_0 data buffer length
    initial_texcoord_0_byte_count = len(initial_texcoord_0_data)
    decoded_texcoord_0_byte_count = len(decoded_texcoord_0_data)
    assert decoded_texcoord_0_byte_count == initial_texcoord_0_byte_count, f"Expected texcoord_0 byte count {initial_texcoord_0_byte_count}, got {decoded_texcoord_0_byte_count}"
    # TODO: validate the data

    # Check the normal data buffer length
    initial_normal_byte_count = len(initial_normal_data)
    decoded_normal_byte_count = len(decoded_normal_data)
    assert decoded_normal_byte_count == initial_normal_byte_count, f"Expected normal byte count {initial_normal_byte_count}, got {decoded_normal_byte_count}"
    # TODO: validate the data

    # Check the tangent data buffer length
    initial_tangent_byte_count = len(initial_tangent_data)
    decoded_tangent_byte_count = len(decoded_tangent_data)
    assert decoded_tangent_byte_count == initial_tangent_byte_count, f"Expected tangent byte count {initial_tangent_byte_count}, got {decoded_tangent_byte_count}"
    # TODO: validate the data

def test_get_number_of_components():
    assert draco.get_number_of_components("SCALAR") == 1
    assert draco.get_number_of_components("VEC2") == 2
    assert draco.get_number_of_components("VEC3") == 3
    assert draco.get_number_of_components("VEC4") == 4
    assert draco.get_number_of_components("MAT2") == 4
    assert draco.get_number_of_components("MAT3") == 9
    assert draco.get_number_of_components("MAT4") ==  16
    assert draco.get_number_of_components("") == 0 # invalid case (return 0)

def test_get_component_byte_length():
    assert draco.get_component_byte_length(5120) == 1  # Byte
    assert draco.get_component_byte_length(5121) == 1  # Unsigned Byte
    assert draco.get_component_byte_length(5122) == 2  # Short
    assert draco.get_component_byte_length(5123) == 2  # Unsigned Short
    assert draco.get_component_byte_length(5125) == 4  # Unsigned Int
    assert draco.get_component_byte_length(5126) == 4  # Unsigned Float
    assert draco.get_component_byte_length(0) == 0    # invalid case (return 0)

def test_get_attribute_stride():
    # Just some bruteforce testing 😅
    assert draco.get_attribute_stride(5120, "SCALAR") == 1 # Scalar Byte component
    assert draco.get_attribute_stride(5121, "SCALAR") == 1 # Scalar Unsigned Byte component
    assert draco.get_attribute_stride(5122, "SCALAR") == 2 # Scalar Short component
    assert draco.get_attribute_stride(5123, "SCALAR") == 2 # Scalar Unsigned Short component
    assert draco.get_attribute_stride(5125, "SCALAR") == 4 # Scalar Unsigned Int component
    assert draco.get_attribute_stride(5126, "SCALAR") == 4 # Scalar Unsigned Float component

    assert draco.get_attribute_stride(5120, "VEC2") == 2   # Vector with 2 Byte components
    assert draco.get_attribute_stride(5121, "VEC2") == 2   # Vector with 2 Unsigned Byte components
    assert draco.get_attribute_stride(5122, "VEC2") == 4   # Vector with 2 Short components
    assert draco.get_attribute_stride(5123, "VEC2") == 4   # Vector with 2 Unsigned Short components
    assert draco.get_attribute_stride(5125, "VEC2") == 8   # Vector with 2 Unsigned Int components
    assert draco.get_attribute_stride(5126, "VEC2") == 8   # Vector with 2 Unsigned Float components

    assert draco.get_attribute_stride(5120, "VEC3") == 3   # Vector with 3 Byte components
    assert draco.get_attribute_stride(5121, "VEC3") == 3   # Vector with 3 Unsigned Byte components
    assert draco.get_attribute_stride(5122, "VEC3") == 6   # Vector with 3 Short components
    assert draco.get_attribute_stride(5123, "VEC3") == 6   # Vector with 3 Unsigned Short components
    assert draco.get_attribute_stride(5125, "VEC3") == 12  # Vector with 3 Unsigned Int components
    assert draco.get_attribute_stride(5126, "VEC3") == 12  # Vector with 3 Unsigned Float components

    assert draco.get_attribute_stride(5120, "VEC4") == 4   # Vector with 4 Byte components
    assert draco.get_attribute_stride(5121, "VEC4") == 4   # Vector with 4 Unsigned Byte components
    assert draco.get_attribute_stride(5122, "VEC4") == 8   # Vector with 4 Short components
    assert draco.get_attribute_stride(5123, "VEC4") == 8   # Vector with 4 Unsigned Short components
    assert draco.get_attribute_stride(5125, "VEC4") == 16  # Vector with 4 Unsigned Int components
    assert draco.get_attribute_stride(5126, "VEC4") == 16  # Vector with 4 Unsigned Float components

    assert draco.get_attribute_stride(5120, "MAT2") == 4   # Matrix (2x2) with 4 Byte components
    assert draco.get_attribute_stride(5121, "MAT2") == 4   # Matrix (2x2) with 4 Unsigned Byte components
    assert draco.get_attribute_stride(5122, "MAT2") == 8   # Matrix (2x2) with 4 Short components
    assert draco.get_attribute_stride(5123, "MAT2") == 8   # Matrix (2x2) with 4 Unsigned Short components
    assert draco.get_attribute_stride(5125, "MAT2") == 16  # Matrix (2x2) with 4 Unsigned Int components
    assert draco.get_attribute_stride(5126, "MAT2") == 16  # Matrix (2x2) with 4 Unsigned Float components

    assert draco.get_attribute_stride(5120, "MAT3") == 9   # Matrix (3x3) with 9 Byte components
    assert draco.get_attribute_stride(5121, "MAT3") == 9   # Matrix (3x3) with 9 Unsigned Byte components
    assert draco.get_attribute_stride(5122, "MAT3") == 18  # Matrix (3x3) with 9 Short components
    assert draco.get_attribute_stride(5123, "MAT3") == 18  # Matrix (3x3) with 9 Unsigned Short components
    assert draco.get_attribute_stride(5125, "MAT3") == 36  # Matrix (3x3) with 9 Unsigned Int components
    assert draco.get_attribute_stride(5126, "MAT3") == 36  # Matrix (3x3) with 9 Unsigned Float components

    assert draco.get_attribute_stride(5120, "MAT4") == 16  # Matrix (4x4) with 16 Byte components
    assert draco.get_attribute_stride(5121, "MAT4") == 16  # Matrix (4x4) with 16 Unsigned Byte components
    assert draco.get_attribute_stride(5122, "MAT4") == 32  # Matrix (4x4) with 16 Short components
    assert draco.get_attribute_stride(5123, "MAT4") == 32  # Matrix (4x4) with 16 Unsigned Short components
    assert draco.get_attribute_stride(5125, "MAT4") == 64  # Matrix (4x4) with 16 Unsigned Int components
    assert draco.get_attribute_stride(5126, "MAT4") == 64  # Matrix (4x4) with 16 Unsigned Float components

if __name__ == "__main__":
    test_decoder()
    test_encoder()
    test_decoder_encoder_roundtrip()
    test_get_number_of_components()
    test_get_component_byte_length()
    test_get_attribute_stride()
    print("Tests finished")