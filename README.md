# Python wrapper of Blenders Draco bridging library

This repository contains a Cython-based wrapper for Python (>= 3.7) of the Blender bridging library for [Draco](https://github.com/google/draco) encoding/decoding (See [extern/draco](https://github.com/blender/blender/extern/draco) in the [Blender](https://github.com/blender/blender) Github mirror repository).

It was initially forked from [ux3d/blender_extern_draco](https://github.com/ux3d/blender_extern_draco) (commit [35e1595](https://github.com/ux3d/blender_extern_draco/commit/35e1595c0ab1fa627aeaeff0247890763f993865)) which is a repo containing a copy of the extern/draco folder and a git submodule with the Draco library (v1.5.2).

The original bridging library is used by the Blender glTF 2.0 Importer and Exporter (see [KhronosGroup/glTF-Blender-IO](https://github.com/KhronosGroup/glTF-Blender-IO)) via the CTypes library (rather than Cython).

## Purpose

The main reason this repository was created was to implement the [KHR_draco_mesh_compression](https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Khronos/KHR_draco_mesh_compression/README.md) extension to the glTF 2.0 specification (see [KhronosGroup/glTF](https://github.com/KhronosGroup/glTF/blob/main/README.md)) in order to be able to add support for the extension to the glTF loaders we use. 

Since we only require the parts of the Draco library used by the glTF extension, the Blender bridging library served as an excellent starting point that serves our need. 


Be aware that we leave no guarantees regarding the quality or reliability of the code in this repository. Use it at your own risk! 

Beside trying to fix any eventual issues with the current implementation, we may or may not add new functionality or improvements, either to the existing bridge code or by wrapping other parts of the Draco library to suit our needs.

## Changes

* CTypes-related functionality (macros etc.) has been removed from headers and source files
* Cython sources for the bridging library has been added (.pyd, .pyx)
* Added a Python-based build system that uses CMake (scikit-build-core, see pyproject.toml) and setup the project for packaging and distribution to PyPi
* Added a Decoder and Encoder class that wrap the C-style free-standing functions

## Installation

### From source

```
pip install .
```

### From PyPi

```
pip install smtk_draco
```

## Usage

For now, refer to the basic test script tests/test.py.


# TODO

* Add a Github Actions workflow for [cibuildwheel](https://github.com/pypa/cibuildwheel) to create wheels for more platforms and Python versions
* Add proper unit tests
* Add an enum for the glTF helper functions (see common.pxi)
