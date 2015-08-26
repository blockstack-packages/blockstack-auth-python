import ast
import json
import uuid
import traceback
import unittest
from test import test_support
from pybitcoin import BitcoinPrivateKey
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ec import (
    EllipticCurvePrivateKey, EllipticCurvePublicKey
)

from idauth import Tokenizer, AuthRequest, AuthResponse


class AuthRequestTest(unittest.TestCase):
    def setUp(self):
        self.domain = 'onename.com'
        self.permissions = ['blockchainid']
        self.private_key = BitcoinPrivateKey(compressed=True)
        self.sample_encoded_token = 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3N1ZWRBdCI6IjE0NDA2MjQ0MzUuMjgiLCJjaGFsbGVuZ2UiOiI4YmVmZTllNS1kYjNhLTQwOGEtYWFhZS1jNDFjMWM4ZWVlNTUiLCJwZXJtaXNzaW9ucyI6WyJibG9ja2NoYWluaWQiXSwiaXNzdWVyIjp7InB1YmxpY0tleSI6IjAyMzFlNDg3M2I1NTY5YzU4MTFiNDg0OWNmMTc5N2YyYmZmM2RhYjM1OGIwNzQxNmFhN2E5YWY2MzhmNzE4MmNhMyIsImRvbWFpbiI6Im9uZW5hbWUuY29tIn19.iBNl-mluCLPJ2ttWi4QSx2uxSPpggOugmYVN0r9MTeFfWfrTxInVpjCpMxdaEBjnXDYOgDCcYuCQYOWELhbDJw'
        self.sample_decoded_token = {"issuedAt":"1440624435.28","challenge":"8befe9e5-db3a-408a-aaae-c41c1c8eee55","permissions":["blockchainid"],"issuer":{"publicKey":"0231e4873b5569c5811b4849cf1797f2bff3dab358b07416aa7a9af638f7182ca3","domain":"onename.com"}}

    def tearDown(self):
        pass

    def test_auth_request_token_encoding(self):
        auth_request = AuthRequest(
            self.private_key.to_pem(), self.private_key.public_key().to_hex(),
            self.domain, self.permissions)
        auth_request_token = auth_request.token()
        is_valid_token = AuthRequest.verify(auth_request_token)
        self.assertTrue(is_valid_token)
        
    def test_auth_request_token_decoding(self):
        decoded_token = AuthRequest.decode(self.sample_encoded_token)
        self.assertEqual(decoded_token, self.sample_decoded_token)


class AuthResponseTest(unittest.TestCase):
    def setUp(self):
        self.private_key = BitcoinPrivateKey(compressed=True)
        self.blockchainid = 'ryan'
        self.challenge = '7cd9ed5e-bb0e-49ea-a323-f28bde3a0549'
        self.master_public_key = 'xpub69W5QnTxuA3VSXzJUopfm3T5aX51HJGQo8mvvkRqwWNNbpnjQp3gb9ghpJk6NHxymLMqWPn3J2qr4vkG7Bcc9qqwg3Nom1XwR9yajP9nemf'
        self.chain_path = 'bd62885ec3f0e3838043115f4ce25eedd22cc86711803fb0c19601eeef185e39'
        self.sample_encoded_token = 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3N1ZWRBdCI6IjE0NDA2MjQ0MzUuNzYiLCJjaGFsbGVuZ2UiOiI3Y2Q5ZWQ1ZS1iYjBlLTQ5ZWEtYTMyMy1mMjhiZGUzYTA1NDkiLCJpc3N1ZXIiOnsicHVibGljS2V5IjoiMDM0ZTYyMjg1YmU1MTJmYWFlZmE0YzgzYmVjYjI3ZGMwNzQ2YjdjNjgyOGE3MGQ5NGQ3ZmIwMTczZDc5ZGE5YWY3IiwiY2hhaW5QYXRoIjoiYmQ2Mjg4NWVjM2YwZTM4MzgwNDMxMTVmNGNlMjVlZWRkMjJjYzg2NzExODAzZmIwYzE5NjAxZWVlZjE4NWUzOSIsIm1hc3RlclB1YmxpY0tleSI6InhwdWI2OVc1UW5UeHVBM1ZTWHpKVW9wZm0zVDVhWDUxSEpHUW84bXZ2a1Jxd1dOTmJwbmpRcDNnYjlnaHBKazZOSHh5bUxNcVdQbjNKMnFyNHZrRzdCY2M5cXF3ZzNOb20xWHdSOXlhalA5bmVtZiIsImJsb2NrY2hhaW5pZCI6InJ5YW4ifX0.xVhijOn8jcIWGf2TXn6SGUdX6fzAG0nN6QQDicpIJpPQmhZvHxhAiIkrlgx3g0cgMmhlnUtiUiLF5DLFzouPcA'
        self.sample_decoded_token = {"issuedAt":"1440624435.76","challenge":"7cd9ed5e-bb0e-49ea-a323-f28bde3a0549","issuer":{"publicKey":"034e62285be512faaefa4c83becb27dc0746b7c6828a70d94d7fb0173d79da9af7","chainPath":"bd62885ec3f0e3838043115f4ce25eedd22cc86711803fb0c19601eeef185e39","masterPublicKey":"xpub69W5QnTxuA3VSXzJUopfm3T5aX51HJGQo8mvvkRqwWNNbpnjQp3gb9ghpJk6NHxymLMqWPn3J2qr4vkG7Bcc9qqwg3Nom1XwR9yajP9nemf","blockchainid":"ryan"}}

    def tearDown(self):
        pass

    def test_auth_response_token_encoding(self):
        challenge = str(uuid.uuid4())
        auth_response = AuthResponse(
            self.private_key.to_pem(), self.private_key.public_key().to_hex(),
            self.challenge, self.blockchainid, self.master_public_key,
            self.chain_path)
        auth_response_token = auth_response.token()
        is_valid_token = AuthResponse.verify(auth_response_token)
        self.assertTrue(is_valid_token)

    def test_auth_response_token_decoding(self):
        decoded_token = AuthResponse.decode(self.sample_encoded_token)
        self.assertEqual(decoded_token, self.sample_decoded_token)


def test_main():
    test_support.run_unittest(
        AuthRequestTest,
        AuthResponseTest
    )

if __name__ == '__main__':
    test_main()