cmake_minimum_required(VERSION 3.18...3.28)

if (NOT SKBUILD_PROJECT_VERSION)
  message(WARNING "SKBUILD_PROJECT_VERSION is not set. Running CMake manually may not work as intended.")
endif()

project(
  ${SKBUILD_PROJECT_NAME} 
  VERSION ${SKBUILD_PROJECT_VERSION}
  LANGUAGES CXX 
)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_CXX_STANDARD 17)

set(PACKAGE_SOURCE_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/src")
set(PACKAGE_BINARY_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}")
set(DRACO_SOURCE_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/draco/src")
set(DRACO_BINARY_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/draco") # Created by draco's CMake configuration

find_package(
  Python3
  COMPONENTS Interpreter Development.Module
  REQUIRED
)

# TODO: unless scikit env vars are set, check if scikit-build-core is installed by importing it
# See: https://stackoverflow.com/questions/62553007/cmake-check-python3-and-python-packages-presence

find_program(CYTHON "cython")
if(NOT CYTHON OR NOT EXISTS ${CYTHON})
  message(FATAL_ERROR "Cython is required. See build system requirements in pyproject.toml.")
endif()

# Add the DRACO library files
set(DRACO_FAST ON CACHE BOOL "") # Optimize for speed if possible
set(DRACO_GLTF_BITSTREAM ON CACHE BOOL "") # We don't need the whole DRACO library (not yet anyway)
add_subdirectory(draco EXCLUDE_FROM_ALL)

# Generate the extension C++ code from the Cython source
add_custom_command(
  OUTPUT smtk_draco.cpp
  COMMAND "${CYTHON}" 
    --cplus ${PACKAGE_SOURCE_DIRECTORY}/smtk_draco.pyx
    --output-file ${PACKAGE_BINARY_DIRECTORY}/smtk_draco.cpp
  VERBATIM
)

# Prepare the module
Python3_add_library (smtk_draco
  MODULE
  WITH_SOABI
  "${PACKAGE_BINARY_DIRECTORY}/smtk_draco.cpp"
)

# Add module dependencies
target_include_directories(smtk_draco
  PRIVATE
  ${PACKAGE_BINARY_DIRECTORY}
  ${PACKAGE_SOURCE_DIRECTORY}
  ${DRACO_SOURCE_DIRECTORY}
  ${DRACO_BINARY_DIRECTORY}
)

# DRACOs configuration for non-MSVC builds use another name 
if(MSVC)
  target_link_libraries(smtk_draco PRIVATE draco)
else()
  target_link_libraries(smtk_draco PRIVATE draco_static)
endif()

install(TARGETS smtk_draco DESTINATION .)
