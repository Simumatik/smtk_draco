# Borrowed from github seung-lab/DracoPy@9caf1aaf219700b93994122e1f267ba7c71233ce
# Intended to be rewritten from scratch

import setuptools
import os
import platform
import sys

from skbuild import setup
from skbuild.constants import CMAKE_INSTALL_DIR, skbuild_plat_name
from skbuild.exceptions import SKBuildError
from skbuild.cmaker import get_cmake_version

import multiprocessing as mp

if not "CMAKE_BUILD_PARALLEL_LEVEL" in os.environ:
    os.environ["CMAKE_BUILD_PARALLEL_LEVEL"] = str(mp.cpu_count())

def read(fname):
  with open(os.path.join(os.path.dirname(__file__), fname), 'rt') as f:
    return f.read()

# Add CMake as a build requirement if cmake is not installed or is too low a version
#setup_requires = ['cython']
#setup_requires.append('cmake<3.15')

# If you want to re-build the cython cpp file (DracoPy.cpp), run:
# cython --cplus -3 -I./_skbuild/linux-x86_64-3.6/cmake-install/include/draco/ ./src/DracoPy.pyx
# Replace "linux-x86_64-3.6" with the directory under _skbuild in your system
# Draco must already be built/setup.py already be run before running the above command

src_dir = './src'
lib_dirs = [os.path.abspath(os.path.join(CMAKE_INSTALL_DIR(), 'lib/')),
            os.path.abspath(os.path.join(CMAKE_INSTALL_DIR(), 'lib64/'))]
cmake_args = []

operating_system = platform.system().lower()

is_macos = sys.platform == 'darwin' or operating_system == "darwin"
is_windows = sys.platform == 'win32' or operating_system == "windows"

if is_macos:
    raise RuntimeError("MacOS is not supported right now")
    plat_name = skbuild_plat_name()
    sep = [pos for pos, char in enumerate(plat_name) if char == '-']
    assert len(sep) == 2
    cmake_args = [
        '-DCMAKE_OSX_DEPLOYMENT_TARGET:STRING='+plat_name[sep[0]+1:sep[1]],
        '-DCMAKE_OSX_ARCHITECTURES:STRING='+plat_name[sep[1]+1:]
    ]
    library_link_args = [
        f'-l{lib}' for lib in ('draco',)
    ]
elif is_windows:
    library_link_args = [
        lib for lib in ('draco.lib',)
    ]
else: # linux
    library_link_args = [
        f'-l:{lib}' for lib in ('libdraco.a',)
    ]

cmake_args.append("-DCMAKE_POSITION_INDEPENDENT_CODE=ON") # make -fPIC code

# TODO: make optional
cmake_args.append("-DDRACO_TESTS=ON") # enable draco tests


if is_windows:
    extra_link_args = ['/LIBPATH:{0}'.format(lib_dir) for lib_dir in lib_dirs] + library_link_args
    extra_compile_args = [
      '/std:c++17', '/O2',
      "/DWITH_LOGGING" # TODO: make optional
    ]
else:
    extra_link_args = ['-L{0}'.format(lib_dir) for lib_dir in lib_dirs] + library_link_args
    extra_compile_args = [
      '-std=c++17','-O3',
      "-DWITH_LOGGING" # TODO: make optional
    ]

setup(
    name='smtk_draco',
    version='1.0.0',
    description = 'Simple Python wrapper for Blenders minimal DRACO decoder/encoder using Google\'s Draco Mesh Compression Library',
    author = 'Manuel Castro, William Silversmith :: Contributors :: Fatih Erol, Faru Nuri Sonmez, Zeyu Zhao, Denis Riviere',
    author_email = 'macastro@princeton.edu, ws9@princeton.edu',
    url = 'https://github.com/Simumatik/smtk_draco',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    license = "License :: OSI Approved :: Apache Software License",
    cmake_source_dir='./draco',
    cmake_args=cmake_args,
    #setup_requires=setup_requires,
    ext_modules=[
        setuptools.Extension(
            'smtk_draco',
            sources=[ 
                os.path.join(src_dir, 'smtk_draco.pyx'),
            ],
            language='c++',
            include_dirs = [
                os.path.join(CMAKE_INSTALL_DIR(), 'include/'),
            ],
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args
        )
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Topic :: Utilities",
  ]
)
