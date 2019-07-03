#!/usr/bin/env python3
"""Define the setup options."""
import os
import re
import setuptools

with open('README.rst', 'r') as f:
    readme = f.read()


setuptools.setup(
    name='kaiterra-client-kaiterramike',
    version='0.2a6',
    description="Kaiterra API Client",
    long_description=readme,
    long_description_content_type="text/x-rst",
    url='https://github.com/kaiterra/api-python',
    license='MIT License',
    packages=setuptools.find_packages(exclude=['tests']),
    test_suite='kaiterra_client.tests',
    tests_require=[
        'requests-mock',
    ],
    install_requires=[
        # Require new ISRG root certificates
        'requests>=2.16.0',
    ],
    # Uses enums (3.4) and type hints (3.5), though reducing this to >=3.4
    # by importing the typing package is a possibility
    python_requires='>=3.5',
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
