#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    ~~~~~
    :copyright: (c) 2015 by Halfmoon Labs, Inc.
    :license: MIT, see LICENSE for more details.
"""

PERMISSION_TYPES = {
    'blockchainid': {'message': 'blockchain ID and public profile'},
    'email': {'message': 'email address'},
    'friends': {'message': 'friends list'},
    'payments': {'message': 'payment details'},
    'birthday': {'message': 'birthday'},
    'address': {'message': 'address'}
}


def validate_permissions(permissions):
    # validate permissions
    if not isinstance(permissions, list):
        raise ValueError('"permissions" must be a list')
    invalid_permissions = [
        permission not in PERMISSION_TYPES
        for permission in permissions
    ]
    if any(invalid_permissions):
        raise ValueError('Invalid permission provided')
