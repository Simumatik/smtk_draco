"""
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
 
       http://www.apache.org/licenses/LICENSE-2.0
 
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

#cython: language_level=3
from libc.stdint cimport uint8_t, uint32_t

cdef extern from "common.cpp":
    pass

cdef extern from "common.h": 

    cdef enum ComponentType:
        Byte = 5120,
        UnsignedByte = 5121,
        Short = 5122,
        UnsignedShort = 5123,
        UnsignedInt = 5125,
        Float = 5126,

    size_t getNumberOfComponents(char* dataType)

    size_t getComponentByteLength(size_t componentType)

    size_t getAttributeStride(size_t componentType, char* dataType)
