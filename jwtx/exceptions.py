#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Classes of exceptions/errors taken from José Padilla's PyJWT
    ~~~~~
    :copyright: (c) 2015 by José Padilla
    :license: MIT, see LICENSE for more details.
"""

class InvalidTokenError(Exception):
    pass


class DecodeError(InvalidTokenError):
    pass