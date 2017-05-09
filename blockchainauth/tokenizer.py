#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    An interface for encoding and decoding JSON Web Tokens (JWTs)
    ~~~~~
    :copyright: (c) 2015 by Halfmoon Labs, Inc.
    :copyright: (c) 2017 by Stanislav Pankratov
    :license: MIT, see LICENSE for more details.
"""

import json
import binascii
from collections import Mapping

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature

from jwt.utils import (
    base64url_encode, base64url_decode, der_to_raw_signature,
    raw_to_der_signature
)
from jwt import DecodeError
from pybitcoin import BitcoinPrivateKey
from blockchainauth.utils import json_encode
from blockchainauth.keys import load_signing_key, load_verifying_key


class Tokenizer:
    def __init__(self, crypto_backend=default_backend()):
        self.crypto_backend = crypto_backend
        self.token_type = 'JWT'
        self.signing_algorithm = 'ES256'
        self.signing_function = ec.ECDSA(hashes.SHA256())

    def _get_signer(self, signing_key):
        return signing_key.signer(self.signing_function)

    @staticmethod
    def _create_signing_input(payload, header):
        return b'.'.join(
            [base64url_encode(json_encode(header)), base64url_encode(json_encode(payload))])

    def encode(self, payload, signing_key=None):
        if not isinstance(payload, Mapping):
            raise TypeError('Expecting a mapping object, as only '
                            'JSON objects can be used as payloads.')

        if not signing_key:
            # create unsecured token
            header = {'typ': self.token_type, 'alg': 'none'}
            return self._create_signing_input(payload, header) + b'.'

        signing_key = load_signing_key(BitcoinPrivateKey(signing_key).to_pem(), self.crypto_backend)

        # prepare header
        header = {'typ': self.token_type, 'alg': self.signing_algorithm}

        # get token signing_input
        signing_input = self._create_signing_input(payload, header)

        # prepare signature
        signer = self._get_signer(signing_key)
        signer.update(signing_input)
        signature = signer.finalize()
        raw_signature = der_to_raw_signature(signature, signing_key.curve)

        # combine the header, payload, and signature into a token and return it
        return signing_input + b'.' + base64url_encode(raw_signature)

    def _get_verifier(self, verifying_key, signature):
        return verifying_key.verifier(signature, self.signing_function)

    @classmethod
    def _unpack(cls, token):
        if isinstance(token, (str, unicode)):
            token = token.encode('utf-8')

        try:
            signing_input, crypto_segment = token.rsplit(b'.', 1)
            header_segment, payload_segment = signing_input.split(b'.', 1)
        except ValueError:
            raise DecodeError('Not enough segments')

        try:
            header_data = base64url_decode(header_segment)
        except (TypeError, binascii.Error):
            raise DecodeError('Invalid header padding')

        try:
            header = json.loads(header_data.decode('utf-8'))
        except ValueError as e:
            raise DecodeError('Invalid header string: %s' % e)

        if not isinstance(header, Mapping):
            raise DecodeError('Invalid header string: must be a json object')

        try:
            payload_data = base64url_decode(payload_segment)
        except (TypeError, binascii.Error):
            raise DecodeError('Invalid payload padding')

        try:
            payload = json.loads(payload_data.decode('utf-8'))
        except ValueError as e:
            raise DecodeError('Invalid payload string: %s' % e)

        try:
            signature = base64url_decode(crypto_segment)
        except (TypeError, binascii.Error):
            raise DecodeError('Invalid crypto padding')

        return header, payload, signature, signing_input

    def verify(self, token, verifying_key):
        # grab the token parts
        token_parts = self._unpack(token)
        header, payload, raw_signature, signing_input = token_parts
        # load the verifying key
        verifying_key = load_verifying_key(verifying_key, self.crypto_backend)
        # convert the raw_signature to DER format
        der_signature = raw_to_der_signature(
            raw_signature, verifying_key.curve)
        # initialize the verifier
        verifier = self._get_verifier(verifying_key, der_signature)
        verifier.update(signing_input)
        # check to see whether the signature is valid
        try:
            verifier.verify()
        except InvalidSignature:
            # raise DecodeError('Signature verification failed')
            return False
        return True

    @classmethod
    def decode(cls, token):
        header, payload, raw_signature, signing_input = cls._unpack(token)
        token = { 
            u"header": header,
            u"payload": payload,
            u"signature": unicode(base64url_encode(raw_signature))
        }
        return token

