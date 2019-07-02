#!/usr/bin/env python
"""Define the setup options."""
import os
import re
import setuptools

with open('README.rst', 'r') as f:
    readme = f.read()


setuptools.setup(
    name='kaiterra-client',
    version='0.1',
    description="Kaiterra API Client",
    long_description=readme,
    long_description_content_type="text/x-rst",
    url='https://github.com/kaiterra/api-python',
    license='MIT License',
    packages=setuptools.find_packages(exclude=['tests']),
    test_suite='kaiterra.tests',
    tests_require=[
        'requests-mock',
    ],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
