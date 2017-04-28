#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    ~~~~~
    :copyright: (c) 2015 by Halfmoon Labs, Inc.
    :license: MIT, see LICENSE for more details.
"""

import json
import traceback
from jwt import DecodeError
from .tokenizer import Tokenizer


class AuthMessage:
    def __init__(self):
        raise NotImplementedError('')

    def _payload(self):
        raise NotImplementedError('')

    def token(self):
        return self.tokenizer.encode(self._payload(), self.private_key)

    def json(self):
        return json.loads(self.decode(self.token(), self.tokenizer))

    @classmethod
    def decode(cls, token):
        if not isinstance(token, (str, unicode)):
            raise ValueError('Token must be a string')
        # decode the token without any verification
        return Tokenizer.decode(token)

    @classmethod
    def verify(cls, token, tokenizer=Tokenizer()):
        # decode the token
        try:
            decoded_token = cls.decode(token)
        except DecodeError:
            traceback.print_exc()
            return False

        return all([method(token, tokenizer, decoded_token) for method in
                   cls.verify_methods])
