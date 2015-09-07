#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Various utils taken from José Padilla's PyJWT
    ~~~~~
    :copyright: (c) 2015 by José Padilla
    :license: MIT, see LICENSE for more details.
"""

import json


def json_encode(input):
    return json.dumps(input, separators=(',', ':')).encode('utf-8')
