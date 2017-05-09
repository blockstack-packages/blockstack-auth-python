#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    ~~~~~
    :copyright: (c) 2015 by Halfmoon Labs, Inc.
    :copyright: (c) 2017 by Stanislav Pankratov
    :license: MIT, see LICENSE for more details.
"""

import json
import traceback
from jwt import DecodeError
from blockchainauth.tokenizer import Tokenizer


class AuthMessage:
    def __init__(self):
        raise NotImplementedError('')

    def _payload(self):
        raise NotImplementedError('')

    def token(self):
        if not hasattr(self, '_token'):
            self._token = self.tokenizer.encode(self._payload(), self.private_key)
        return self._token

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
