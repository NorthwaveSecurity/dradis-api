#!/usr/bin/env python

from distutils.core import setup

with open("README.md") as f:
    long_description = f.read()

setup(name='dradis-api',
      version='1.1',
      description='Dradis API',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Northwave B.V.',
      url="https://github.com/NorthwaveSecurity/dradis-api",
      license='LGPL',
      py_modules=['dradis'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: LGPL License',
          'Programming Language :: Python :: 3',
      ],
      keywords='dradis api',
      python_requires='>=3',
      )
