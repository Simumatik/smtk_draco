# A fork of https://github.com/ux3d/blender_extern_draco@35e1595c0ab1fa627aeaeff0247890763f993865 (used as a starting point) for a Python wrapper package
# Also inspired by https://github.com/seung-lab/DracoPy@9caf1aaf219700b93994122e1f267ba7c71233ce

# Draco Mesh Compression for Python

[Draco](https://github.com/google/draco) encoding and decoding for Python 3.x

## Changes

Blender does not need to be built locally to test changes in Draco or the bridging code.

- Build the target `extern_draco`
- Set the environment variable `BLENDER_EXTERN_DRACO_LIBRARY_PATH` to the built dynamic library
- Launch Blender and export with compression enabled or inspect the console output if compression options are missing

## Release

- Checkout the Blender source code repository
- Copy all changed files to `<blender-root>/extern/draco`
- Open a new Blender Differential
