#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
import re
from setuptools import setup

dirname = os.path.dirname(__file__)

def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()

with codecs.open(os.path.join(dirname, "pytest_bdd_web.py"), encoding="utf-8") as fd:
    VERSION = re.compile(r".*__version__ = ['\"](.*?)['\"]", re.S).match(fd.read()).group(1)

setup(
    name='pytest-bdd-web',
    version=VERSION,
    author='Ed J',
    author_email='mohawk2@users.noreply.github.com',
    maintainer='Ed J',
    maintainer_email='mohawk2@users.noreply.github.com',
    license='MIT',
    url='https://github.com/mohawk2/pytest-bdd-web',
    description='A simple plugin to use with pytest',
    long_description=read('README.rst'),
    py_modules=['pytest_bdd_web'],
    python_requires='>=3.5',
    install_requires=[
        'pytest>=3.5.0',
        'pytest_bdd>=3.2',
        'mechanize>=0.4.5',
        'pyquery>=1.4.1',
    ],
    tests_require=["Flask>=1.1.1"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
    + [("Programming Language :: Python :: %s" % x) for x in "3.6 3.7 3.8".split()],
    entry_points={
        'pytest11': [
            'pytest-bdd-web = pytest_bdd_web',
        ],
    },
)
