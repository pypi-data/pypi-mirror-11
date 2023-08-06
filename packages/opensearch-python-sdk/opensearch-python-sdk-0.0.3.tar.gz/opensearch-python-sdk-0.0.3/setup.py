#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='opensearch-python-sdk',
    version='0.0.3',
    description='Python unofficial sdk of aliyun open search',
    author='Kaiyuan Li, Jingping Yi',
    author_email='me@defool.me, jingping.yi@gmail.com',
    py_modules=['opensearch', ],
    url='https://github.com/bowenpay/opensearch-python-sdk',
    license="MIT",
    long_description=open('README.md').read(),
    install_requires=[
        "requests>=2.4.0",
    ],
    classifiers=[
        "Topic :: Software Development",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ])
