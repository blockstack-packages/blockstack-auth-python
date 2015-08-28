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
from bitmerchant.wallet import Wallet
from .auth_request import AuthRequest
from .resolver import Resolver

class AuthResponse(AuthRequest):
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

    def token(self):
        return self.tokenizer.encode(self._payload(), self.signing_key)

    def json(self):
        return json.loads(self.decode(self.token()))

    @classmethod
    def master_and_child_keys_match(cls, public_keychain, child_public_key,
                                    chain_path):
        public_child = Wallet.deserialize(public_keychain)
        chain_step_bytes = 4
        max_bits_per_step = 2**31
        chain_steps = [
            int(chain_path[i:i+chain_step_bytes*2], 16) % max_bits_per_step
            for i in range(0, len(chain_path), chain_step_bytes*2)
        ]
        for step in chain_steps:
            public_child = public_child.get_child(step)
        public_child_hex = public_child.get_public_key_hex(compressed=True)
        if public_child_hex == child_public_key:
            return True
        return False

    @classmethod
    def public_keychain_in_profile(cls, blockchainid, public_keychain,
                                     resolver):
        profile = resolver.get_profile(blockchainid)
        if 'auth' in profile:
            for auth_item in profile['auth']:
                if ('publicKeychain' in auth_item and
                    auth_item['publicKeychain'] == public_keychain):
                    return True
        return False

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

        public_keychain_in_profile = cls.public_keychain_in_profile(
            blockchainid, public_keychain, resolver)
        master_and_child_keys_match = cls.master_and_child_keys_match(
            public_keychain, child_public_key, chain_path)

        return public_keychain_in_profile and master_and_child_keys_match
