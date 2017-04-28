#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    ~~~~~
    :copyright: (c) 2015 by Halfmoon Labs, Inc.
    :license: MIT, see LICENSE for more details.
"""

import time
import uuid
from cryptography.hazmat.backends import default_backend
from pybitcoin import BitcoinPrivateKey
from .auth_message import AuthMessage
from .dids import make_did_from_address
from .tokenizer import Tokenizer
from .verification import is_expiration_date_valid, is_issuance_date_valid, \
    do_signatures_match_public_keys, do_public_keys_match_issuer, do_public_keys_match_username


class AuthResponse(AuthMessage):
    """ Interface for creating signed auth response tokens, as well as decoding
        and verifying them.
    """

    verify_methods = [
        is_expiration_date_valid,
        is_issuance_date_valid,
        do_signatures_match_public_keys,
        do_public_keys_match_issuer,
        do_public_keys_match_username
    ]

    def __init__(self, private_key, profile=None, username=None,
                 expires_at=None, crypto_backend=default_backend()):
        """ private_key should be provided in HEX, WIF or binary format 
            profile should be a dictionary
            username should be a string
            expires_at should be a float number of seconds since the epoch
        """
        if not private_key:
            raise ValueError('Private key is missing')

        if not profile:
            profile = {}

        if not expires_at:
            expires_at = time.time() + 30 * 24 * 3600  # next month

        self.private_key = private_key
        self.public_key = BitcoinPrivateKey(self.private_key).public_key()
        self.address = self.public_key.address()
        self.profile = profile
        self.username = username
        self.expires_at = expires_at
        self.tokenizer = Tokenizer(crypto_backend=crypto_backend)

    def _payload(self):
        return {
            'jti': str(uuid.uuid4()),
            'iat': str(time.time()),
            'exp': str(self.expires_at),
            'iss': make_did_from_address(self.address),
            'public_keys': [self.public_key.to_hex()],
            'profile': self.profile,
            'username': self.username
        }
