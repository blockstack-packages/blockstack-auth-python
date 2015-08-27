import json
import uuid
import time
import traceback
from pybitcoin import BitcoinPublicKey
from .tokenizer import Tokenizer, load_signing_key
from .exceptions import DecodeError
from .permissions import PERMISSION_TYPES, validate_permissions
from .identifier import Identifier


class AuthRequest():
    """ Interface for creating signed auth request tokens, as well as decoding
        and verifying them.
    """
    tokenizer = Tokenizer()

    def __init__(self, signing_key, verifying_key, issuing_domain,
                 permissions=[]):
        """ signing_key should be provided in PEM format
            verifying_key should be provided in compressed hex format
            issuing_domain should be a valid domain
            permissions should be a list
        """
        validate_permissions(permissions)
        self.issuing_domain = issuing_domain
        self.permissions = permissions
        self.signing_key = signing_key
        self.verifying_key = verifying_key

    def _payload(self):
        return {
            'issuer': {
                'domain': self.issuing_domain,
                'publicKey': self.verifying_key
            },
            'issuedAt': str(time.time()),
            'challenge': str(uuid.uuid4()),
            'permissions': self.permissions
        }

    def token(self):
        return self.tokenizer.encode(self._payload(), self.signing_key)

    def json(self):
        return json.loads(self.decode(self.token()))

    @classmethod
    def decode(cls, token, verify=False):
        if not isinstance(token, (str, unicode)):
            raise ValueError('Token must be a string')
        # decode the token without any verification
        decoded_token = cls.tokenizer.decode(token)

        if verify:
            public_key_str = json.loads(decoded_token)['issuer']['publicKey']
            public_key = BitcoinPublicKey(str(public_key_str))
            # decode the token again, this time by performing a verification
            # with the public key we extracted
            decoded_token = cls.tokenizer.decode(token, public_key.to_pem())

        return json.loads(decoded_token)

    @classmethod
    def is_valid_jwt(cls, token):
        decoded_token = cls.decode(token, verify=True)
        if decoded_token:
            return True
        return False

    @classmethod
    def has_valid_issuer(cls, token, identifier):
        decoded_token = cls.decode(token)
        try:
            domain = decoded_token['issuer']['domain']
            public_key = decoded_token['issuer']['publicKey']
            if identifier.domain_matches_key(domain, public_key):
                return True
        except KeyError:
            pass
        return False

    @classmethod
    def verify(cls, token, identifier=None):
        is_valid_jwt = cls.is_valid_jwt(token)
        if not identifier:
            return is_valid_jwt
        if not isinstance(identifier, Identifier):
            raise ValueError('"identifier" must be a valid Identifier object')
        has_valid_issuer = cls.has_valid_issuer(token, identifier)
        is_valid_auth_token = is_valid_jwt and has_valid_issuer
        return is_valid_auth_token
