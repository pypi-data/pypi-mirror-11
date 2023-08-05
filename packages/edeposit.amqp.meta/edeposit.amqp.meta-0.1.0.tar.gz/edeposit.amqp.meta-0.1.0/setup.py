#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from setuptools import setup


# Variables ===================================================================
CHANGELOG = open('CHANGELOG.rst').read()


# Function definitions ========================================================
def allSame(s):
    return not filter(lambda x: x != s[0], s)


def hasDigit(s):
    return any(map(lambda x: x.isdigit(), s))


def getVersion(data):
    data = data.splitlines()
    return filter(
        lambda (x, y):
            len(x) == len(y) and allSame(y) and hasDigit(x) and "." in x,
        zip(data, data[1:])
    )[0][0]


# Actual setup definition =====================================================
setup(
    name='edeposit.amqp.meta',
    version=getVersion(CHANGELOG),
    description="Meta package containing dependecies for Edeposit system.",
    url='https://github.com/edeposit/edeposit.amqp.meta',

    author='Edeposit team',
    author_email='edeposit@email.cz',

    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",

        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",

        "License :: OSI Approved :: MIT License",
    ],
    license='MIT',

    zip_safe=False,

    install_requires=[
        "edeposit.amqp",
        "edeposit.amqp.aleph>=1.4.1",
        "edeposit.amqp.serializers>=1.1.1",
        "edeposit.amqp.calibre>=1.0.1",
        "edeposit.amqp.ftp>=0.6.4",
        "edeposit.amqp.antivirus>=1.0.0",
        "edeposit.amqp.harvester",
        "edeposit.amqp.ltp",
        "edeposit.amqp.pdfgen",
        "edeposit.amqp.downloader",
        "edeposit.amqp.storage",
    ]
)
