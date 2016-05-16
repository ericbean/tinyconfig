#!/usr/bin/env python3
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import tinyconfig

setup(
    name="tinyconfig",
    version=tinyconfig.__version__,
    author=tinyconfig.__author__,
    description=("The config file parser no one asked for."),
    license="MIT",
    keywords="config",
    py_modules=['tinyconfig']
)
