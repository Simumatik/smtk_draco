#cython: language_level=3
#distutils: language = c++
cimport common

def get_number_of_components(dataType: str):
    """ 
        Return the number of components in the specified glTF accessor type
        See https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#accessor-data-types
    """
    return common.getNumberOfComponents(dataType.encode("utf-8"))

# TODO: expose ComponentType enum
def get_component_byte_length(componentType):
    """ 
        Return the size in bytes for a value of the specified componentType
        See https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#accessor-data-types
    """
    return common.getComponentByteLength(componentType)

# TODO: expose ComponentType enum
def get_attribute_stride(componentType, dataType: str):
    """ 
        Return the size in bytes of a dataType value consisting of components of componentType.
        
        E.g. the attribute stride of type VEC3 (-> a vector with three components) 
        with unsigned short components (-> 2 bytes) is 6 bytes. For a data buffer containing
        a series of VEC3 values, this simply represents the amount of bytes from the start of
        one VEC3 to the start of the next VEC3.

        See https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#accessor-data-types
    """
    return common.getAttributeStride(componentType, dataType.encode("utf-8"))