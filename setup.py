# encoding: utf-8
from __future__ import absolute_import, print_function
from setuptools import setup, find_packages


__version__ = '0.1.1'
__author__ = 'Dmitry Orlov <me@mosquito.su>'


setup(
    name='carbon-client',
    version=__version__,
    author=__author__,
    author_email='me@mosquito.su',
    license="LGPLv3",
    description="graphite/carbon udp client for sending metrics",
    platforms="all",
    url="http://github.com/mosquito/carbon-client",
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python',
    ],
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=('tests',)),
    install_requires=[],
)
