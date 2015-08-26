import json
import uuid
import time
import traceback
from pybitcoin import BitcoinPublicKey

from .tokenizer import Tokenizer, load_signing_key
from .exceptions import DecodeError
from .utils import merge_dict
from .permissions import PERMISSION_TYPES


class AuthRequestTokenizer():
    """ Interface for creating signed auth request tokens, as well as decoding
        and verifying them.
    """

    def __init__(self, issuing_domain, permissions=[]):
        if not isinstance(permissions, list):
            raise ValueError('"permissions" must be a list')
        invalid_permissions = [
            permission not in PERMISSION_TYPES
            for permission in permissions
        ]
        if any(invalid_permissions):
            raise ValueError('Invalid permission provided')

        self.tokenizer = Tokenizer()
        self.issuing_domain = issuing_domain
        self.permissions = permissions

    def _create_payload(self, verifying_key):
        return {
            'issuer': {
                'domain': self.issuing_domain,
                'publicKey': verifying_key
            },
            'issuedAt': str(time.time()),
            'challenge': str(uuid.uuid4()),
            'permissions': self.permissions
        }

    def sign(self, signing_key, compressed_verifying_key, encoded=True):
        """ Verifying key must be provided as a PEM.
        """
        # signing_key = load_signing_key(signing_key)
        # verifying_key = signing_key.public_key()

        payload = self._create_payload(compressed_verifying_key)
        token = self.tokenizer.encode(payload, signing_key)
        if not encoded:
            token = self.decode(token)
        return token

    def decode(self, token, verify=False):
        # decode the token without any verification
        decoded_token = self.tokenizer.decode(token)

        if verify:
            public_key_str = json.loads(decoded_token)['issuer']['publicKey']
            public_key = BitcoinPublicKey(str(public_key_str))
            # decode the token again, this time by performing a verification
            # with the public key we extracted
            decoded_token = self.tokenizer.decode(token, public_key.to_pem())

        return decoded_token

    def verify(self, token):
        decoded_token = self.decode(token, verify=True)
        return True


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
            'issuer': {
                'publicKey': issuing_public_key
            },
            'issuedAt': str(time.time()),
            'challenge': challenge
        }

        if chain_path and self.blockchainid and self.master_public_key:
            payload = merge_dict(payload, {
                'issuer': {
                    'publicKey': issuing_public_key,
                    'blockchainid': self.blockchainid,
                    'masterPublicKey': self.master_public_key,
                    'chainPath': chain_path
                }
            })
        
        return payload

    def sign(self, signing_key, verifying_key, challenge, chain_path=None, encoded=True):
        payload = self._create_payload(verifying_key, challenge, chain_path)
        token = self.tokenizer.encode(payload, signing_key)
        if not encoded:
            token = self.decode(token)
        return token

    def verify(self, token):
        decoded_token = self.decode(token, verify=True)
        return True


