#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    ~~~~~
    :copyright: (c) 2015 by Halfmoon Labs, Inc.
    :license: MIT, see LICENSE for more details.
"""

from onename import OnenameClient

class Resolver():
    def __init__(self):
        raise NotImplementedError('')

    def get_domain_dkim(domain):
        raise NotImplementedError('')

    def get_blockchainid_profile(blockchainid):
        raise NotImplementedError('')


class OnenameAPIResolver(Resolver):
    def __init__(self, onename_app_id, onename_app_secret):
        self.onename_client = OnenameClient(onename_app_id, onename_app_secret)

    def get_dkim(self, domain):
        return self.onename_client.get_dkim_info(domain)

    def get_profile(self, blockchainid):
        users = self.onename_client.get_users([blockchainid])
        if blockchainid in users and 'profile' in users[blockchainid]:
            profile = users[blockchainid]['profile']
            return profile
        return None
