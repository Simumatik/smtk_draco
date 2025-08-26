# Python wrapper of Blenders Draco bridging library

This repository contains a Cython-based wrapper for Python (>= 3.8) of the Blender bridging library for [Draco](https://github.com/google/draco) encoding/decoding (See [extern/draco](https://github.com/blender/blender/extern/draco) in the [Blender](https://github.com/blender/blender) Github mirror repository).

It was initially forked from [ux3d/blender_extern_draco](https://github.com/ux3d/blender_extern_draco) (commit [35e1595](https://github.com/ux3d/blender_extern_draco/commit/35e1595c0ab1fa627aeaeff0247890763f993865)) which is a repo containing a copy of the extern/draco folder and a git submodule with the Draco library (v1.5.2).

The original bridging library is used by the Blender glTF 2.0 Importer and Exporter (see [KhronosGroup/glTF-Blender-IO](https://github.com/KhronosGroup/glTF-Blender-IO)) via the CTypes library (rather than Cython).

## Purpose

The main reason this repository was created was to implement the [KHR_draco_mesh_compression](https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Khronos/KHR_draco_mesh_compression/README.md) extension to the glTF 2.0 specification (see [KhronosGroup/glTF](https://github.com/KhronosGroup/glTF/blob/main/README.md)) in order to be able to add support for the extension to the glTF loaders we use. 

Since we only require the parts of the Draco library used by the glTF extension, the Blender bridging library served as an excellent starting point that serves our need. 

Beside trying to fix any eventual issues with the current implementation, we may or may not add new functionality or improvements, either to the existing bridge code or by wrapping other parts of the Draco library to suit our needs. Use the Python package and the code at your own risk!

## Changes

* CTypes-related functionality (macros etc.) has been removed from headers and source files
* Cython sources for the bridging library has been added (.pyd, .pyx)
* Added a Python-based build system that uses CMake (scikit-build-core, see pyproject.toml) and setup the project for packaging and distribution to PyPi
* Added a Decoder and Encoder class that wrap the C-style free-standing functions
* Added a basic Github action workflow for managing building, packaging and releasing.

### TODO

* Add proper unit tests
* Add an enum for the glTF helper functions (see common.pxi)
* Improve build process: avoid building Draco every time the project is built (cache the build for each platform)
* Improve build process: find a way to build and use Dracos tests when Draco is built (the build breaks unless the full library is built)

## Installation

### From source

```
pip install .
```

### From PyPi

```
pip install smtk_draco
```

### For development

Create a virtual environment (e.g. `python -m venv .venv`) and make sure
to activate it.

Install the prerequisites for an editable install:

```
pip install scikit-build-core scikit-build-core[pyproject] "cython>=3.0.8" 
```

Then, from the repository root execute the following command to create an editable install:
```
pip install --no-build-isolation -C build-dir=build --editable  .
```

NOTE: When changing the package source files you need to rebuild (i.e. rerun the install command above). This is because Cython needs to generate a new C++ source file for the 
extension, which then needs to be rebuilt and linked with Draco. However, the Draco library will not have to be rebuilt, so the process is relatively quick. If the `build-dir` setting is omitted, the build system uses a temporary directory for each build which _will_ build Draco as well.

## Build and release

The repository uses a Github Action workflow to build, package and (conditionally) release the Python package by
uploading it to the [Python Package Index](https://pypi.org).

[cibuildwheel](https://github.com/pypa/cibuildwheel) is used to build wheels for Python 3.8-3.14 for several versions of Linux, Windows and macOS.

Source distributions are built using `pipx`.

The final release steps are only executed when a release is published. As a final test, the wheels and the source distribution are first uploaded to [Test PyPI](https://test.pypi.org) and then, if all goes well, the release is uploaded to PyPI.

## Usage

For now, refer to the basic test script tests/test.py.