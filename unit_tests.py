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

from idauth import Tokenizer, AuthRequestTokenizer, AuthResponseTokenizer


class AuthRequestTest(unittest.TestCase):
    def setUp(self):
        self.request_tokenizer = AuthRequestTokenizer(
            'onename.com', permissions=['public-profile'])
        self.private_key = BitcoinPrivateKey(compressed=True)
        self.sample_encoded_token = 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3N1ZWRBdCI6IjE0NDA1NDI5OTYuMTkiLCJjaGFsbGVuZ2UiOiI5N2Y0YTA0My1hOTE1LTRmNDYtOWE1Ny01OWQyYTg3MTQ4MTMiLCJpc3N1aW5nRG9tYWluIjoib25lbmFtZS5jb20iLCJwZXJtaXNzaW9ucyI6WyJwdWJsaWMtcHJvZmlsZSJdfQ.XcAtWE2hW4z0vHkjUqA4NsyH38Fz7MygI-cKoEE2JKpKp8HWVe38LLLs2hKdFjRYKiCFuXDspkZqvNLPP0Ad1Q'
        self.sample_decoded_token = {
            "issuedAt":"1440542996.19",
            "challenge":"97f4a043-a915-4f46-9a57-59d2a8714813",
            "issuingDomain":"onename.com",
            "permissions":["public-profile"]
        }

    def tearDown(self):
        pass

    def test_auth_request_token_encoding(self):
        request_token = self.request_tokenizer.sign(self.private_key.to_pem())
        is_valid_token = self.request_tokenizer.verify(
            request_token, self.private_key.public_key().to_pem())
        self.assertTrue(is_valid_token)
        
    def test_auth_request_token_decoding(self):
        decoded_token = self.request_tokenizer.decode(self.sample_encoded_token)
        self.assertEqual(json.loads(decoded_token), self.sample_decoded_token)


class AuthResponseTest(unittest.TestCase):
    def setUp(self):
        self.private_key = BitcoinPrivateKey(compressed=True)
        self.blockchainid = 'ryan'
        self.master_public_key = 'xpub69W5QnTxuA3VSXzJUopfm3T5aX51HJGQo8mvvkRqwWNNbpnjQp3gb9ghpJk6NHxymLMqWPn3J2qr4vkG7Bcc9qqwg3Nom1XwR9yajP9nemf'
        self.response_tokenizer = AuthResponseTokenizer(self.blockchainid, self.master_public_key)
        self.sample_encoded_token = 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3N1ZWRBdCI6IjE0NDA1NDI5OTYuMzUiLCJibG9ja2NoYWluaWQiOiJyeWFuIiwiY2hhbGxlbmdlIjoiOTdmNGEwNDMtYTkxNS00ZjQ2LTlhNTctNTlkMmE4NzE0ODEzIiwiaXNzdWluZ1B1YmxpY0tleSI6IjAzYjAxMmEyNDk4NTc4OGFmYTU0YTE1OGQzYjQzY2EwM2E4NTc2NWZmM2I3ODVmZTY2YTZjYmMwNTBiODE5ODY4OSIsIm1hc3RlclB1YmxpY0tleSI6InhwdWI2OVc1UW5UeHVBM1ZTWHpKVW9wZm0zVDVhWDUxSEpHUW84bXZ2a1Jxd1dOTmJwbmpRcDNnYjlnaHBKazZOSHh5bUxNcVdQbjNKMnFyNHZrRzdCY2M5cXF3ZzNOb20xWHdSOXlhalA5bmVtZiIsImNoYWluUGF0aCI6ImJkNjI4ODVlYzNmMGUzODM4MDQzMTE1ZjRjZTI1ZWVkZDIyY2M4NjcxMTgwM2ZiMGMxOTYwMWVlZWYxODVlMzkifQ.VgtRmUG2ynHf2Ss8f8suyO24yOnBZgiCrHPlkw9dhMRR8zcn3gWJPJMPAXFTPxgaZAZScddRgzPgtazbitgX_w'
        self.sample_decoded_token = {
            "issuedAt":"1440542996.35",
            "blockchainid":"ryan",
            "challenge":"97f4a043-a915-4f46-9a57-59d2a8714813",
            "issuingPublicKey":"03b012a24985788afa54a158d3b43ca03a85765ff3b785fe66a6cbc050b8198689",
            "masterPublicKey":"xpub69W5QnTxuA3VSXzJUopfm3T5aX51HJGQo8mvvkRqwWNNbpnjQp3gb9ghpJk6NHxymLMqWPn3J2qr4vkG7Bcc9qqwg3Nom1XwR9yajP9nemf","chainPath":"bd62885ec3f0e3838043115f4ce25eedd22cc86711803fb0c19601eeef185e39"
        }

    def tearDown(self):
        pass

    def test_auth_response_token_encoding(self):
        chain_path = 'bd62885ec3f0e3838043115f4ce25eedd22cc86711803fb0c19601eeef185e39'
        challenge = str(uuid.uuid4())
        response_token = self.response_tokenizer.sign(
            self.private_key.to_pem(), self.private_key.public_key().to_hex(),
            challenge, chain_path=chain_path)
        is_valid_token = self.response_tokenizer.verify(
            response_token, self.private_key.public_key().to_pem())
        self.assertTrue(is_valid_token)

    def test_auth_response_token_decoding(self):
        decoded_token = self.response_tokenizer.decode(self.sample_encoded_token)
        self.assertEqual(json.loads(decoded_token), self.sample_decoded_token)


def test_main():
    test_support.run_unittest(
        AuthRequestTest,
        AuthResponseTest
    )

if __name__ == '__main__':
    test_main()