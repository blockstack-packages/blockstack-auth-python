#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    ~~~~~
    :license: MIT, see LICENSE for more details.
"""


def make_did_from_address(address):
    return 'did:btc-addr:' + address


def make_did_from_public_key(public_key):
    return 'did:ecdsa-pub' + public_key


def get_did_type(decentralized_id):
    did_parts = decentralized_id.split(':')

    if len(did_parts) != 3:
        raise ValueError('Decentralized IDs must have 3 parts')

    if did_parts[0].lower() != 'did':
        raise ValueError('Decentralized IDs must start with "did"')

    return did_parts[1].lower()


def get_address_from_did(decentralized_id):
    did_type = get_did_type(decentralized_id)
    if did_type == 'btc-addr':
        return decentralized_id.split(':')[2]
    else:
        return ''


def get_public_key_from_did(decentralized_id):
    did_type = get_did_type(decentralized_id)
    if did_type == 'ecdsa-pub':
        return decentralized_id.split(':')[2]
