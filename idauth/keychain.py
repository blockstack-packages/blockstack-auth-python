#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    ~~~~~
    :copyright: (c) 2015 by Halfmoon Labs, Inc.
    :license: MIT, see LICENSE for more details.
"""

from bitmerchant.wallet import Wallet


def do_master_and_child_keys_match(public_keychain, child_public_key, chain_path):
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