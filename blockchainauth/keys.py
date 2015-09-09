#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    ~~~~~
    :copyright: (c) 2015 by Halfmoon Labs, Inc.
    :license: MIT, see LICENSE for more details.
"""

import traceback

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.backends.openssl.backend import Backend
from cryptography.hazmat.backends.multibackend import MultiBackend
from cryptography.hazmat.primitives.serialization import (
    load_der_private_key, load_pem_private_key,
    load_der_public_key, load_pem_public_key
)
from cryptography.hazmat.primitives.asymmetric.ec import (
    EllipticCurvePrivateKey, EllipticCurvePublicKey
)


def load_signing_key(signing_key, crypto_backend=default_backend()):
    """ Optional: crypto backend object from the "cryptography" python library
    """
    if not isinstance(crypto_backend, (Backend, MultiBackend)):
        raise ValueError('backend must be a valid Backend object')

    if isinstance(signing_key, EllipticCurvePrivateKey):
        return signing_key
    elif isinstance(signing_key, (str, unicode)):
        invalid_strings = [b'-----BEGIN PUBLIC KEY-----']
        invalid_string_matches = [
            string_value in signing_key
            for string_value in invalid_strings
        ]
        if any(invalid_string_matches):
            raise ValueError(
                'Signing key must be a private key, not a public key.')

        try:
            return load_der_private_key(
                signing_key, password=None, backend=crypto_backend)
        except:
            try:
                return load_pem_private_key(
                    signing_key, password=None, backend=crypto_backend)
            except Exception as e:
                raise ValueError(
                    'Signing key must be a valid private key PEM or DER.')
    else:
        raise ValueError('Signing key must be in string or unicode format.')


def load_verifying_key(verifying_key, crypto_backend=default_backend()):
    """ Optional: crypto backend object from the "cryptography" python library
    """
    if not isinstance(crypto_backend, (Backend, MultiBackend)):
        raise ValueError('backend must be a valid Backend object')

    if isinstance(verifying_key, EllipticCurvePublicKey):
        return verifying_key
    elif isinstance(verifying_key, (str, unicode)):
        try:
            return load_der_public_key(
                verifying_key, backend=crypto_backend)
        except:
            try:
                return load_pem_public_key(
                    verifying_key, backend=crypto_backend)
            except Exception as e:
                raise ValueError('Invalid verifying key format')
    else:
        raise ValueError('Invalid verification key type')
