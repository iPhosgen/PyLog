#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import re
import os
from setuptools import setup, find_packages


def find_version(*file_paths):
    with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *file_paths), 'r') as init:
        result = re.search(r"^__version__ = \((\d+), ?(\d+), ?(\d+)\)", init.read(), re.M)
        if result:
            return "{}.{}.{}".format(*result.groups())
        raise RuntimeError("Unable to find the package version")


VERSION = find_version("PyLog", "__init__.py")

setup(
    name='PyLog',
    version=VERSION,
    description="Just another one Python logging package.",
    keywords='logging',
    author='Alexey Morozov',
    author_email='iphosgen@gmail.com',
    url='https://github.com/iPhosgen/PyLog',
    license='MIT License',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: System :: Logging',
    ]
)