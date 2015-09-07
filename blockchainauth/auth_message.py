#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    ~~~~~
    :copyright: (c) 2015 by Halfmoon Labs, Inc.
    :license: MIT, see LICENSE for more details.
"""

import json
from pybitcoin import BitcoinPublicKey
from .tokenizer import Tokenizer
from .resolver import Resolver


class AuthMessage():
    tokenizer = Tokenizer()

    def __init__(self):
        raise NotImplementedError('')

    def _payload(self):
        raise NotImplementedError('')

    @classmethod
    def has_valid_issuer(cls):
        raise NotImplementedError('')

    def token(self):
        return self.tokenizer.encode(self._payload(), self.signing_key)

    def json(self):
        return json.loads(self.decode(self.token()))

    @classmethod
    def decode(cls, token, verify=False):
        if not isinstance(token, (str, unicode)):
            raise ValueError('Token must be a string')
        # decode the token without any verification
        decoded_token = cls.tokenizer.decode(token)

        if verify:
            public_key_str = json.loads(decoded_token)['issuer']['publicKey']
            public_key = BitcoinPublicKey(str(public_key_str))
            # decode the token again, this time by performing a verification
            # with the public key we extracted
            decoded_token = cls.tokenizer.decode(token, public_key.to_pem())

        return json.loads(decoded_token)

    @classmethod
    def is_valid_jwt(cls, token):
        decoded_token = cls.decode(token, verify=True)
        if decoded_token:
            return True
        return False

    @classmethod
    def verify(cls, token, resolver=None):
        is_valid_jwt = cls.is_valid_jwt(token)
        if not resolver:
            return is_valid_jwt
        if not isinstance(resolver, Resolver):
            raise ValueError('"resolver" must be a valid Resolver object')
        has_valid_issuer = cls.has_valid_issuer(token, resolver)
        is_valid_auth_token = is_valid_jwt and has_valid_issuer
        return is_valid_auth_token