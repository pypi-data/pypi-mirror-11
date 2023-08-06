#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'path.py==5.2'
]

test_requirements = [
    'path.py==5.2'
]

setup(
    name='python-perforce',
    version='0.2.0',
    description='Pure python Perforce API',
    long_description=readme + '\n\n' + history,
    author='Brett Dixon',
    author_email='theiviaxx@gmail.com',
    url='https://github.com/theiviaxx/python-perforce',
    packages=[
        'perforce',
    ],
    package_dir={'python-perforce':
                 'python-perforce'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='python-perforce',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)