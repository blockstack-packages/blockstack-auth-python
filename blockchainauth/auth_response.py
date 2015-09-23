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
from cryptography.hazmat.backends import default_backend
from pybitcoin import BitcoinPrivateKey, BitcoinPublicKey
from .auth_message import AuthMessage
from .identification import is_public_keychain_in_profile
from .keychain import do_master_and_child_keys_match
from .tokenizer import Tokenizer


class AuthResponse(AuthMessage):
    """ Interface for creating signed auth response tokens, as well as decoding
        and verifying them.
    """

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

    @classmethod
    def has_valid_issuer(cls, token, resolver):
        decoded_token = cls.decode(token)
        payload = decoded_token['payload']
        try:
            issuer = payload['issuer']
        except KeyError:
            return False

        anon_issuer_keys = set(['publicKey'])
        identified_issuer_keys = anon_issuer_keys.union(
            set(['blockchainid', 'publicKeychain', 'chainPath']))

        # if all three identifying values are here, proceed
        if set(issuer.keys()) == identified_issuer_keys:
            child_public_key = issuer['publicKey']
            blockchain_id = issuer['blockchainid']
            public_keychain = issuer['publicKeychain']
            chain_path = issuer['chainPath']
        # if all three identifying values are missing, the anon issuer is valid
        elif set(issuer.keys()) == anon_issuer_keys:
            return True
        # if 1-2 of the identifying values are present, the issuer is invalid
        else:
            return False

        master_and_child_keys_match = do_master_and_child_keys_match(
            public_keychain, child_public_key, chain_path)

        # if the master and child keys don't match, the issuer is invalid
        if not master_and_child_keys_match:
            return False

        public_keychain_in_profile = is_public_keychain_in_profile(
            blockchain_id, public_keychain, resolver)

        # consider the issuer valid only if the public keychain matches a
        # blockchain ID profile AND the included master and child keys match
        return public_keychain_in_profile and master_and_child_keys_match
