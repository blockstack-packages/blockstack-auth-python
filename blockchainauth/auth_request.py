#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    ~~~~~
    :copyright: (c) 2015 by Halfmoon Labs, Inc.
    :license: MIT, see LICENSE for more details.
"""

import json
import uuid
import time
from cryptography.hazmat.backends import default_backend
from pybitcoin import BitcoinPrivateKey, BitcoinPublicKey
from .permissions import PERMISSION_TYPES, validate_permissions
from .auth_message import AuthMessage
from .identification import domain_and_public_key_match
from .tokenizer import Tokenizer


class AuthRequest(AuthMessage):
    """ Interface for creating signed auth request tokens, as well as decoding
        and verifying them.
    """

    def __init__(self, signing_key, verifying_key, issuing_domain,
                 permissions=[], crypto_backend=default_backend()):
        """ signing_key should be provided in PEM format
            verifying_key should be provided in compressed hex format
            issuing_domain should be a valid domain
            permissions should be a list
        """
        validate_permissions(permissions)

        self.bitcoin_private_key = BitcoinPrivateKey(signing_key, compressed=True)
        self.bitcoin_public_key = BitcoinPublicKey(verifying_key)

        self.tokenizer = Tokenizer(crypto_backend=crypto_backend)
        self.issuing_domain = issuing_domain
        self.permissions = permissions
        self.signing_key = signing_key
        self.verifying_key = verifying_key

    def _payload(self):
        return {
            'issuer': {
                'domain': self.issuing_domain,
                'publicKey': self.verifying_key
            },
            'issuedAt': str(time.time()),
            'challenge': str(uuid.uuid4()),
            'permissions': self.permissions
        }

    @classmethod
    def has_valid_issuer(cls, token, resolver):
        decoded_token = cls.decode(token)
        payload = decoded_token['payload']
        try:
            domain = payload['issuer']['domain']
            public_key = payload['issuer']['publicKey']
        except KeyError:
            return False
        return domain_and_public_key_match(domain, public_key, resolver)

