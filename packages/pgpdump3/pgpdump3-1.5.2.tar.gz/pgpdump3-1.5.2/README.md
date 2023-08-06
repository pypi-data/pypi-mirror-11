# python-pgpdump: a Python library for parsing PGP packets

[![Build Status](https://travis-ci.org/SkierPGP/python-pgpdump.svg?branch=master)](https://travis-ci.org/SkierPGP/python-pgpdump)
[![Downloads Weekly](https://img.shields.io/pypi/dw/Django.svg)](https://img.shields.io/pypi/dw/Django.svg)


This is based on the C version published at:
http://www.mew.org/~kazu/proj/pgpdump/

This version is a fork of the version by Dan McGee, dropping Python 2 compatibility.

The intent here is not on completeness, as we don't currently decode every
packet type, but on being able to do what people actually have to 95% of the
time. Currently supported things include:

* Signature packets
* Public key packets
* Secret key packets
* Trust, user ID, and user attribute packets
* ASCII-armor decoding and CRC check
* Compressed packet decompression automatically

This package is designed for Python 3 only. 
