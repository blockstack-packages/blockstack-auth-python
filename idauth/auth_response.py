import time
import json

from .utils import merge_dict
from .auth_request import AuthRequest


class AuthResponse(AuthRequest):
    """ Interface for creating signed auth response tokens, as well as decoding
        and verifying them.
    """

    def __init__(self, signing_key, verifying_key, challenge,
                 blockchainid=None, master_public_key=None, chain_path=None):
        self.signing_key = signing_key
        self.verifying_key = verifying_key
        self.challenge = challenge
        self.blockchainid = blockchainid
        self.master_public_key = master_public_key
        self.chain_path = chain_path

    def _payload(self):
        payload = {
            'issuer': {
                'publicKey': self.verifying_key
            },
            'issuedAt': str(time.time()),
            'challenge': self.challenge
        }

        if self.chain_path and self.blockchainid and self.master_public_key:
            payload = merge_dict(payload, {
                'issuer': {
                    'publicKey': self.verifying_key,
                    'blockchainid': self.blockchainid,
                    'masterPublicKey': self.master_public_key,
                    'chainPath': self.chain_path
                }
            })
        
        return payload

    def token(self):
        return self.tokenizer.encode(self._payload(), self.signing_key)

    def json(self):
        return json.loads(self.decode(self.token()))

    @classmethod
    def has_valid_issuer(cls, token):
        return True

    @classmethod
    def verify(cls, token, verify_issuer=True):
        is_valid_jwt = AuthRequest.is_valid_jwt(token)
        if not verify_issuer:
            return is_valid_jwt
        has_valid_issuer = cls.has_valid_issuer(token)
        is_valid_auth_response_token = is_valid_jwt and has_valid_issuer
        return is_valid_auth_response_token
