#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='gmag',
      version='1.0.0',
      description='Data I/O for ground-base magnetometers',
      author='Kyle Murphy',
      author_email='kylemurphy.spacephys@gmail.com',
      license='MIT License',
      license_file = 'LICENSE.md',
      url='https://github.com/kylermurphy/gmag/',
      install_requires=['pandas','numpy','wget','requests','cdflib','heliopy'],
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages(),
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'Intended Audience :: Science/Research',
                   'Topic :: Scientific/Engineering :: Atmospheric Science',
                   'Topic :: Scientific/Engineering :: Physics',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.7',
                   ],
     )