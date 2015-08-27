from onename import OnenameClient

class Identifier():
    def __init__(self):
        raise NotImplementedError('')

    def domain_matches_key(domain, public_key):
        raise NotImplementedError('')

    def blockchainid_matches_key(blockchainid, master_public_key):
        raise NotImplementedError('')


class OnenameAPIIdentifier(Identifier):
    def __init__(self, onename_app_id, onename_app_secret):
        self.onename_client = OnenameClient(onename_app_id, onename_app_secret)

    def domain_matches_key(self, domain, public_key):
        dkim_info = self.onename_client.get_dkim_info(domain)
        if 'public_key' in dkim_info:
            public_key = dkim_info['public_key']
            if public_key == public_key:
                return True
        return False

    def blockchainid_matches_key(self, blockchainid, master_public_key):
        users = self.onename_client.get_users([blockchainid])
        if blockchainid in users and 'profile' in users[blockchainid]:
            profile = users[blockchainid]['profile']
            if 'auth' in profile:
                for auth_item in profile['auth']:
                    if ('masterPublicKey' in auth_item and
                        auth_item['masterPublickey'] == master_public_key):
                        return True
        return False
