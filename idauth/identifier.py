from onename import OnenameClient

class Identifier():
    def __init__(self):
        raise NotImplementedError('')

    def check_domain(domain, public_key):
        raise NotImplementedError('')

    def check_blockchainid(blockchainid, master_public_key):
        raise NotImplementedError('')


class OnenameAPIIdentifier(Identifier):
    def __init__(self, onename_app_id, onename_app_secret):
        self.onename_client = OnenameClient(onename_app_id, onename_app_secret)

    def check_domain(self, domain, public_key):
        dkim_info = self.onename_client.get_dkim_info(domain)
        if 'public_key' in dkim_info:
            public_key = dkim_info['public_key']
            if public_key == public_key:
                return True
        return False

    def check_blockchainid(self, blockchainid, master_public_key):
        users = self.onename_client.get_users([blockchainid])
        if blockchainid in users and 'profile' in users[blockchainid]:
            profile = users[blockchainid]['profile']
            if 'auth' in profile and 'publickey' in profile['auth']:
                public_key = profile['auth']['publickey']
                if public_key == master_public_key:
                    return True
        return False
