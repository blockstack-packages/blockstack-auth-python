#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    ~~~~~
    :copyright: (c) 2015 by Halfmoon Labs, Inc.
    :license: MIT, see LICENSE for more details.
"""


def domain_and_public_key_match(domain, public_key, resolver):
    dkim_info = resolver.get_dkim(domain)
    if 'public_key' in dkim_info:
        if public_key == dkim_info['public_key']:
            return True
    return False


def is_public_keychain_in_profile(blockchainid, public_keychain, resolver):
    profile = resolver.get_profile(blockchainid)
    if 'auth' in profile:
        for auth_item in profile['auth']:
            if ('publicKeychain' in auth_item and
                auth_item['publicKeychain'] == public_keychain):
                return True
    return False