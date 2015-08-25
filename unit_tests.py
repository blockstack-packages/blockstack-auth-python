import jwt
from jwtx import Tokenizer
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ec import (
    EllipticCurvePrivateKey, EllipticCurvePublicKey
)

payload = {'name':'ryan'}
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
