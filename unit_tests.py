import jwt
import json
from idauth import Tokenizer, AuthRequestTokenizer, AuthResponseTokenizer
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ec import (
    EllipticCurvePrivateKey, EllipticCurvePublicKey
)
from pybitcoin import BitcoinPrivateKey

"""payload = {'name':'ryan'}
private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
public_key = private_key.public_key()

tokenizer = Tokenizer()
encoded_token = tokenizer.encode(payload, private_key)
print encoded_token

encoded_token_2 = jwt.encode(payload, private_key, algorithm='ES256')
print encoded_token_2

decoded_token = tokenizer.decode(encoded_token_2, verifying_key=public_key)
print decoded_token

decoded_token_2 = jwt.decode(encoded_token, key=public_key, algorithms=['ES256'])
print decoded_token_2
"""

tokenizer = Tokenizer()
payload = {'name':'ryan'}
private_key = BitcoinPrivateKey(compressed=True)
private_key_pem = private_key.to_pem()
public_key = private_key.public_key()
public_key_hex = public_key.to_hex()
public_key_pem = public_key.to_pem()
#private_key_pem = '-----BEGIN EC PRIVATE KEY-----\nMHQCAQEEINmVY72qsqic5sX0HPqQRfutEyBDx9+x1mzGb61kcx/RoAcGBSuBBAAK\noUQDQgAE7qwEJZRsyGS7H8laHY2IES2vfwRki33ALxEoAxdpJqfnn01IDX6NZoMJ\n1ACPt66su1KCoNgGM7r7lblUj2Aqng==\n-----END EC PRIVATE KEY-----\n'
#public_key_pem = '-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEFEaBL9tIkLPEgn8AAwqBSVoXoMNUx1nS\nte7f443dw3M/y0WYI9X0YLSPhTUtYpyXQm5UnpGPI9zcVjvUuSE7rA==\n-----END PUBLIC KEY-----\n'
#token = tokenizer.encode(payload, private_key_pem)
#load_pem_private_key(signing_key, password=None, backend=default_backend())

auth_tokenizer = AuthRequestTokenizer('onename.com', permissions=['public-profile'])

encoded_token = auth_tokenizer.sign(private_key_pem)
is_valid_token = auth_tokenizer.verify(encoded_token, public_key_pem)
decoded_token = auth_tokenizer.decode(encoded_token)
print encoded_token
print is_valid_token
print decoded_token

challenge = json.loads(decoded_token)['challenge']
print challenge

blockchainid = 'ryan'
master_public_key = 'xpub69W5QnTxuA3VSXzJUopfm3T5aX51HJGQo8mvvkRqwWNNbpnjQp3gb9ghpJk6NHxymLMqWPn3J2qr4vkG7Bcc9qqwg3Nom1XwR9yajP9nemf'
response_tokenizer = AuthResponseTokenizer(blockchainid, master_public_key)

chain_path = 'bd62885ec3f0e3838043115f4ce25eedd22cc86711803fb0c19601eeef185e39'

encoded_response_token = response_tokenizer.sign(
    private_key_pem, public_key_hex, challenge, chain_path=chain_path)
decoded_response_token = auth_tokenizer.decode(encoded_response_token)
print encoded_response_token
print decoded_response_token