import uuid
import time
import traceback

from .tokenizer import Tokenizer
from .exceptions import DecodeError
from .utils import merge_dict

PERMISSION_TYPES = {
    'public-profile': {'message': 'public profile'},
    'email': {'message': 'email address'},
    'friends': {'message': 'friends list'},
    'payments': {'message': 'payment details'},
    'birthday': {'message': 'birthday'},
    'address': {'message': 'address'}
}


class AuthRequestTokenizer():
    """ Interface for creating signed auth request tokens, as well as decoding
        and verifying them.
    """

    def __init__(self, issuing_domain, permissions=[]):
        invalid_permissions = [
            permission not in PERMISSION_TYPES
            for permission in permissions
        ]
        if any(invalid_permissions):
            raise ValueError('Invalid permission provided')

        self.tokenizer = Tokenizer()
        self.issuing_domain = issuing_domain
        self.permissions = permissions

    def _create_payload(self):
        return {
            'issuingDomain': self.issuing_domain,
            'issuedAt': str(time.time()),
            'challenge': str(uuid.uuid4()),
            'permissions': self.permissions
        }

    def sign(self, signing_key, encoded=True):
        payload = self._create_payload()
        token = self.tokenizer.encode(payload, signing_key)
        if not encoded:
            token = self.decode(token)
        return token

    def decode(self, token, verifying_key=None):
        decoded_token = self.tokenizer.decode(token, verifying_key)
        return decoded_token

    def verify(self, token, verifying_key):
        try:
            decoded_token = self.decode(token, verifying_key)
            return True
        except DecodeError:
            return False


class AuthResponseTokenizer(AuthRequestTokenizer):
    """ Interface for creating signed auth response tokens, as well as decoding
        and verifying them.
    """

    def __init__(self, blockchainid=None, master_public_key=None):
        self.tokenizer = Tokenizer()
        self.blockchainid = blockchainid
        self.master_public_key = master_public_key

    def _create_payload(self, issuing_public_key, challenge, chain_path=None):
        payload = {
            'issuingPublicKey': issuing_public_key,
            'issuedAt': str(time.time()),
            'challenge': challenge
        }

        if chain_path and self.blockchainid and self.master_public_key:
            payload = merge_dict(payload, {
                'blockchainid': self.blockchainid,
                'masterPublicKey': self.master_public_key,
                'chainPath': chain_path
            })
        
        return payload

    def sign(self, signing_key, verifying_key, challenge, chain_path=None, encoded=True):
        payload = self._create_payload(verifying_key, challenge, chain_path)
        token = self.tokenizer.encode(payload, signing_key)
        if not encoded:
            token = self.decode(token)
        return token


