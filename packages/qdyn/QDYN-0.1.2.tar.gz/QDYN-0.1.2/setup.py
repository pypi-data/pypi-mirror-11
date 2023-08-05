#!/usr/bin/env python
from setuptools import setup
from QDYN import __version__

setup(name='QDYN',
      version=__version__,
      description='Package providing some Python modules for working with ' \
                  'the QDYN Fortran library',
      author='Michael Goerz',
      author_email='goerz@physik.uni-kassel.de',
      url='https://github.com/goerz/qdynpylib',
      license='GPL',
      install_requires=[
          'numpy>=1.9',
          'matplotlib>=1.3',
          'scipy>=0.15',
          'sympy>=0.7',
          'bokeh>=0.8',
      ],
      packages=['QDYN', 'QDYN.prop'],
      scripts=[],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Natural Language :: English',
          'Topic :: Scientific/Engineering',
          'Programming Language :: Python :: 2.7',
      ]
     )
