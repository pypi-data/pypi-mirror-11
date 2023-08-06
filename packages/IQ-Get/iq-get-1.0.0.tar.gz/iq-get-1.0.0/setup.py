#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requirements = ['qds_sdk == 1.3.4']

setup(
    name='iq-get',
    version='1.0.0',
    author='MediaMath',
    author_email='rsawyer@mediamath.com',
    description=('Python script to download Hive command results from Qubole Data Service (QDS)'),
    keywords='mediamath qubole sdk iq',
    install_requires=requirements,
    scripts=['bin/iq-get'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Natural Language :: English',
        'Operating System :: OS Independent'
    ]
)
