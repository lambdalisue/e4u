#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author:        alisue
# date:            2011/03/22
#
from setuptools import setup, find_packages

version = "0.1rc5"


def read(filename):
    import os.path
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name="e4u",
    version=version,
    description=(
        "Python's emoji conversion (unicode emoji <=> carrier's emoji) "
        "library (emoji4unicode project wrapper library)"
    ),
    long_description=read('README.rst'),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords="emoji emoji4unicode mobile",
    author="Alisue",
    author_email="lambdalisue@hashnote.net",
    url=r"https://github.com/lambdalisue/e4u",
    download_url=r"https://github.com/lambdalisue/e4u/tarball/master",
    license='BSD',
    packages=find_packages(exclude=["test", "utils"]),
    include_package_data=True,
    zip_safe=True,
    install_requires=['setuptools', 'BeautifulSoup'],
)
