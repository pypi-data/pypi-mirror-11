#!/usr/bin/env python
# Copyright 2015 Paul Schwendenman. All Rights Reserved.

from setuptools import setup

setup(name='twintrimmer',
      version='0.6',
      description='tool for removing duplicate files',
      author='Paul Schwendenman',
      author_email='schwendenman.paul+twintrim@gmail.com',
      license='MIT',
      url='https://github.com/paul-schwendenman/twintrim',
      py_modules=['twintrimmer'],
      classifiers=['Environment :: Console',
                   'Intended Audience :: Developers',
                   'Intended Audience :: End Users/Desktop',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4',
                   'Operating System :: POSIX :: Linux',
                   'Topic :: Utilities', ],
      entry_points={'console_scripts': ['twintrim = twintrimmer:main'], }, )
