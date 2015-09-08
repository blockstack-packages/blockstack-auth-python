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
    def decode(cls, token):
        if not isinstance(token, (str, unicode)):
            raise ValueError('Token must be a string')
        # decode the token without any verification
        return cls.tokenizer.decode(token)

    @classmethod
    def is_valid_jwt(cls, token):
        # decode the token
        try:
            decoded_token = cls.decode(token)
        except DecodeError:
            traceback.print_exc()
            return False

        # extract the public key from the token
        try:
            payload = decoded_token['payload']
            public_key_str = payload['issuer']['publicKey']
            public_key = BitcoinPublicKey(str(public_key_str))
        except KeyError:
            traceback.print_exc()
            return False

        # return whether the token is verified/valid
        return cls.tokenizer.verify(token, public_key.to_pem())

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