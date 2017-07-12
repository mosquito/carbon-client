# encoding: utf-8
from __future__ import absolute_import, print_function
from setuptools import setup, find_packages


__version__ = '0.3.0'
__author__ = 'Dmitry Orlov <me@mosquito.su>'


setup(
    name='carbon-client',
    version=__version__,
    author=__author__,
    author_email='me@mosquito.su',
    license="MIT",
    description="graphite/carbon udp client for sending metrics",
    platforms="all",
    url="http://github.com/mosquito/carbon-client",
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Topic :: Software Development :: Libraries',
        'Development Status :: 4 - Beta',

    ],
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=('tests',)),
    install_requires=[],
)
