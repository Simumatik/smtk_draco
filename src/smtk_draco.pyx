#cython: language_level=3
#distutils: language = c++

__version__ = "0.0.1"

# Include the implementation files to compile all the code into one extension
include "common.pxi"
include "decoder.pxi"
include "encoder.pxi"