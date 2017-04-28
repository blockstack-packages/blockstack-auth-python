#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    ~~~~~
    :copyright: (c) 2015 by Halfmoon Labs, Inc.
    :license: MIT, see LICENSE for more details.
"""

import time
from jwt.utils import merge_dict
from cryptography.hazmat.backends import default_backend
from pybitcoin import BitcoinPrivateKey, BitcoinPublicKey
from .auth_message import AuthMessage
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

    def __init__(self, signing_key, verifying_key, challenge,
                 blockchain_id=None, public_keychain=None, chain_path=None,
                 crypto_backend=default_backend()):
        """ signing_key should be provided in PEM format
            verifying_key should be provided in compressed hex format
            blockchainid should be a string
            master_public_key should be an extended public key
            chain_path should be a string
        """
        self.bitcoin_private_key = BitcoinPrivateKey(signing_key, compressed=True)
        self.bitcoin_public_key = BitcoinPublicKey(verifying_key)

        self.tokenizer = Tokenizer(crypto_backend=crypto_backend)
        self.signing_key = signing_key
        self.verifying_key = verifying_key
        self.challenge = challenge
        self.blockchain_id = blockchain_id
        self.public_keychain = public_keychain
        self.chain_path = chain_path

    def _payload(self):
        payload = {
            'issuer': {
                'publicKey': self.verifying_key
            },
            'issuedAt': str(time.time()),
            'challenge': self.challenge
        }

        if self.chain_path and self.blockchain_id and self.public_keychain:
            payload = merge_dict(payload, {
                'issuer': {
                    'publicKey': self.verifying_key,
                    'blockchainid': self.blockchain_id,
                    'publicKeychain': self.public_keychain,
                    'chainPath': self.chain_path
                }
            })
        
        return payload
