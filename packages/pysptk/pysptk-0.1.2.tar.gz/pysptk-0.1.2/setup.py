# coding: utf-8

from __future__ import with_statement, print_function, absolute_import

from setuptools import setup, find_packages, Extension
from distutils.version import LooseVersion

import numpy as np
import os
from glob import glob
from os.path import join


min_cython_ver = '0.19.0'
try:
    import Cython
    ver = Cython.__version__
    _CYTHON_INSTALLED = ver >= LooseVersion(min_cython_ver)
except ImportError:
    _CYTHON_INSTALLED = False

try:
    if not _CYTHON_INSTALLED:
        raise ImportError('No supported version of Cython installed.')
    from Cython.Distutils import build_ext
    cython = True
except ImportError:
    cython = False

if cython:
    ext = '.pyx'
    cmdclass = {'build_ext': build_ext}
else:
    ext = '.c'
    cmdclass = {}
    if not os.path.exists("pysptk/sptk" + ext):
        raise RuntimeError("Cython is required to generate C codes.")

# SPTK sources
src_top = "lib/SPTK"
swipe_src = [
    join(src_top, 'bin/pitch/swipe/swipe.c'),
    join(src_top, 'bin/pitch/swipe/vector.c'),
]
hts_engine_src = glob(join(src_top, 'bin/vc/hts_engine_API/*.c'))
sptklib_src = glob(join(src_top, 'lib/*.c'))
sptk_src = glob(join(src_top, 'bin/*/_*.c'))

# collect all sources
sptk_all_src = sptk_src + sptklib_src + swipe_src + hts_engine_src

# define core cython module
ext_modules = [Extension(
    name="pysptk.sptk",
    sources=["pysptk/sptk" + ext] + sptk_all_src,
    include_dirs=[np.get_include(), join(os.getcwd(), 'lib/SPTK/include')],
    language="c",
)]

setup(
    name='pysptk',
    version='0.1.2',
    description='A python wrapper for Speech Signal Processing Toolkit (SPTK)',
    author='Ryuichi Yamamoto',
    author_email='zryuichi@gmail.com',
    url='https://github.com/r9y9/pysptk',
    license='MIT',
    packages=find_packages(),
    ext_modules=ext_modules,
    cmdclass=cmdclass,
    install_requires=[
        'numpy >= 1.8.0',
        'six'
    ],
    tests_require=['nose', 'coverage'],
    extras_require={
        'docs': ['numpydoc', 'sphinx_rtd_theme', 'seaborn']
    },
    classifiers=[
        "Programming Language :: Cython",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering"
    ],
    keywords=["SPTK"]
)
