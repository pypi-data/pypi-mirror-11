#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import io

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

description = "Manage and load dataprotocols.org Data Packages"
with io.open('README.rst') as readme:
    long_description = ''.join(
        filter(lambda x: 'https://travis-ci.org/' not in x,
               readme.readlines()))

setup(
    name = 'datapackage',
    version = '0.5.4',
    url = 'https://github.com/trickvi/datapackage',
    license = 'GPLv3',
    description = description,
    long_description = long_description,
    maintainer = 'Tryggvi Björgvinsson',
    maintainer_email = 'tryggvi.bjorgvinsson@okfn.org',
    packages = ['datapackage'],
    package_dir={'datapackage': 'datapackage'},
    package_data={'datapackage': ['data/*.json']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
