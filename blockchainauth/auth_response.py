#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    ~~~~~
    :copyright: (c) 2015 by Halfmoon Labs, Inc.
    :license: MIT, see LICENSE for more details.
"""

import time
import json
from jwt.utils import merge_dict
from .auth_message import AuthMessage
from .identification import is_public_keychain_in_profile
from .keychain import do_master_and_child_keys_match


class AuthResponse(AuthMessage):
    """ Interface for creating signed auth response tokens, as well as decoding
        and verifying them.
    """

    def __init__(self, signing_key, verifying_key, challenge,
                 blockchainid=None, public_keychain=None, chain_path=None):
        """ signing_key should be provided in PEM format
            verifying_key should be provided in compressed hex format
            blockchainid should be a string
            master_public_key should be an extended public key
            chain_path should be a string
        """
        self.signing_key = signing_key
        self.verifying_key = verifying_key
        self.challenge = challenge
        self.blockchainid = blockchainid
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

        if self.chain_path and self.blockchainid and self.public_keychain:
            payload = merge_dict(payload, {
                'issuer': {
                    'publicKey': self.verifying_key,
                    'blockchainid': self.blockchainid,
                    'publicKeychain': self.public_keychain,
                    'chainPath': self.chain_path
                }
            })
        
        return payload

    @classmethod
    def has_valid_issuer(cls, token, resolver):
        decoded_token = cls.decode(token)
        try:
            blockchainid = decoded_token['issuer']['blockchainid']
            public_keychain = decoded_token['issuer']['publicKeychain']
            chain_path = decoded_token['issuer']['chainPath']
            child_public_key = decoded_token['issuer']['publicKey']
        except KeyError:
            return False

        master_and_child_keys_match = do_master_and_child_keys_match(
            public_keychain, child_public_key, chain_path)

        if not master_and_child_keys_match:
            return False

        public_keychain_in_profile = is_public_keychain_in_profile(
            blockchainid, public_keychain, resolver)

        return public_keychain_in_profile and master_and_child_keys_match
