#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-bdd-web',
    version='0.1.0',
    author='Ed J',
    author_email='mohawk2@users.noreply.github.com',
    maintainer='Ed J',
    maintainer_email='mohawk2@users.noreply.github.com',
    license='MIT',
    url='https://github.com/mohawk2/pytest-bdd-web',
    description='A simple plugin to use with pytest',
    long_description=read('README.rst'),
    py_modules=['pytest_bdd_web'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
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
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'pytest-bdd-web = pytest_bdd_web',
        ],
    },
)
