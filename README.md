# Blockchain ID Auth

Library for Blockchain ID authentication, including interfaces for generating auth requests tokens and auth response tokens, as well as decoding and verifying them.

Also built-in is a JSON Web Token Library compatible with Bitcoin's SECP256K1.

## Installation

```
$ pip install idauth
```

## Auth Requests

### Request Format

```json
{
    "header": {
        "typ": "JWT",
        "alg": "ES256"
    },
    "payload": {
        "issuedAt":"1440624435.28",
        "challenge":"8befe9e5-db3a-408a-aaae-c41c1c8eee55",
        "permissions":["blockchainid"],
        "issuer": {
            "publicKey":"0231e4873b5569c5811b4849cf1797f2bff3dab358b07416aa7a9af638f7182ca3",
            "domain":"onename.com"
        }
    },
    "signature": "MEUCIQDzUaSrgTR_tTpNSVcitKYvYWd3bc3uylMe3xCfo-QclQIgDLN1hgXSyqiEk0AGQ21XB2wzuqrotTmE_yN3pn4f_38"
}
```

### Signing Requests

```python
>>> from pybitcoin import BitcoinPrivateKey
>>> from idauth import AuthRequest
>>> private_key = BitcoinPrivateKey(compressed=True)
>>> auth_request = AuthRequest(private_key.to_pem(), private_key.public_key().to_hex(), 'onename.com', permissions=['public-profile'])
>>> auth_request_token = auth_request.token()
>>> print auth_request_token
eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3N1ZWRBdCI6IjE0NDA3MTM0MTQuMTkiLCJjaGFsbGVuZ2UiOiIxZDc4NTBkNy01YmNmLTQ3ZDAtYTgxYy1jMDA4NTc5NzY1NDQiLCJwZXJtaXNzaW9ucyI6WyJibG9ja2NoYWluaWQiXSwiaXNzdWVyIjp7InB1YmxpY0tleSI6IjAzODI3YjZhMzRjZWJlZTZkYjEwZDEzNzg3ODQ2ZGVlYWMxMDIzYWNiODNhN2I4NjZlMTkyZmEzNmI5MTkwNjNlNCIsImRvbWFpbiI6Im9uZW5hbWUuY29tIn19.96Q_O_4DX8uPy1enosEwS2sIcyVelWhxvfj2F8rOvHldhqt9YRYilauepb95DVnmpqpCXxJb7jurT8auNCbptw
>>> AuthRequest.decode(auth_request_token)
{"issuedAt": "1440713414.19", "challenge": "1d7850d7-5bcf-47d0-a81c-c00857976544", "issuer": {"publicKey": "03827b6a34cebee6db10d13787846deeac1023acb83a7b866e192fa36b919063e4", "domain": "onename.com"}, "permissions": ["blockchainid"]}
```

### Verifying Requests

```python
>>> AuthRequest.verify(auth_request_token)
True
```

### Permission Types

+ read public data
    + blockchain ID and entire public profile
+ read private data
    + name
    + profile photo
    + bio
    + website
    + city of residence
    + social accounts
    + email
    + birthday
    + postal address
    + bitcoin address
    + credit card number
    + friends
    + photos
+ write public data
    + write access to a section set aside for the app
+ write private data
    + friends
    + photos

## Auth Responses

### Response Format

```json
{
    "header": {
        "typ": "JWT",
        "alg": "ES256"
    },
    "payload": {
        "issuedAt": "1440713414.85",
        "challenge": "7cd9ed5e-bb0e-49ea-a323-f28bde3a0549",
        "issuer": {
            "publicKey": "03fdd57adec3d438ea237fe46b33ee1e016eda6b585c3e27ea66686c2ea5358479",
            "blockchainid": "ryan",
            "publicKeychain": "xpub661MyMwAqRbcFQVrQr4Q4kPjaP4JjWaf39fBVKjPdK6oGBayE46GAmKzo5UDPQdLSM9DufZiP8eauy56XNuHicBySvZp7J5wsyQVpi2axzZ",
            "chainPath": "bd62885ec3f0e3838043115f4ce25eedd22cc86711803fb0c19601eeef185e39"
        }
    },
    "signature": "MEUCIQDzUaSrgTR_tTpNSVcitKYvYWd3bc3uylMe3xCfo-QclQIgDLN1hgXSyqiEk0AGQ21XB2wzuqrotTmE_yN3pn4f_38"
}
```

### Signing Responses

```python
>>> from idauth import AuthResponse
>>> private_key = BitcoinPrivateKey(compressed=True)
>>> blockchainid = 'ryan'
>>> master_public_key = 'xpub69W5QnTxuA3VSXzJUopfm3T5aX51HJGQo8mvvkRqwWNNbpnjQp3gb9ghpJk6NHxymLMqWPn3J2qr4vkG7Bcc9qqwg3Nom1XwR9yajP9nemf'
>>> challenge = 'ad21e749-b8dc-4167-9486-72c92a85227a'
>>> chain_path = 'bd62885ec3f0e3838043115f4ce25eedd22cc86711803fb0c19601eeef185e39'
>>> auth_response = AuthResponse(private_key.to_pem(), private_key.public_key().to_hex(), challenge, blockchainid, master_public_key, chain_path)
>>> auth_response_token = auth_response.token()
>>> print auth_response_token
eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3N1ZWRBdCI6IjE0NDA3MTM0MTQuODUiLCJjaGFsbGVuZ2UiOiI3Y2Q5ZWQ1ZS1iYjBlLTQ5ZWEtYTMyMy1mMjhiZGUzYTA1NDkiLCJpc3N1ZXIiOnsicHVibGljS2V5IjoiMDNmZGQ1N2FkZWMzZDQzOGVhMjM3ZmU0NmIzM2VlMWUwMTZlZGE2YjU4NWMzZTI3ZWE2NjY4NmMyZWE1MzU4NDc5IiwiY2hhaW5QYXRoIjoiYmQ2Mjg4NWVjM2YwZTM4MzgwNDMxMTVmNGNlMjVlZWRkMjJjYzg2NzExODAzZmIwYzE5NjAxZWVlZjE4NWUzOSIsInB1YmxpY0tleWNoYWluIjoieHB1YjY2MU15TXdBcVJiY0ZRVnJRcjRRNGtQamFQNEpqV2FmMzlmQlZLalBkSzZvR0JheUU0NkdBbUt6bzVVRFBRZExTTTlEdWZaaVA4ZWF1eTU2WE51SGljQnlTdlpwN0o1d3N5UVZwaTJheHpaIiwiYmxvY2tjaGFpbmlkIjoicnlhbiJ9fQ.oO7ROPKq3T3X0azAXzHsf6ub6CYy5nUUFDoy8MS22B3TlYisqsBrRtzWIQcSYiFXLytrXwAdt6vjehj3OFioDQ
>>> AuthResponse.decode(auth_response_token)
{"issuedAt": "1440713414.85", "challenge": "7cd9ed5e-bb0e-49ea-a323-f28bde3a0549", "issuer": {"publicKey": "03fdd57adec3d438ea237fe46b33ee1e016eda6b585c3e27ea66686c2ea5358479", "blockchainid": "ryan", "publicKeychain": "xpub661MyMwAqRbcFQVrQr4Q4kPjaP4JjWaf39fBVKjPdK6oGBayE46GAmKzo5UDPQdLSM9DufZiP8eauy56XNuHicBySvZp7J5wsyQVpi2axzZ", "chainPath": "bd62885ec3f0e3838043115f4ce25eedd22cc86711803fb0c19601eeef185e39"}}
```

### Verifying Responses

```python
>>> AuthResponse.verify(auth_response_token)
True
```

### Response Types

There are two types of auth responses - pseudo-anonymous auth responses and identified auth responses.

With pseudo-anonymous auth responses, only a persistent public key is specified, as well as optional private information. No blockchain ID, and by extension public profile, is provided by the user.

With identified auth responses, the user additionally provides a blockchain ID, as well as evidence that they are the owner of said blockchain ID.

### How Response Verification Works

Pseudo-anonymous auth response verification only requires a single step - verification that the token is a valid JWT that was signed by the specified public key.

Identified auth responses, meanwhile, require two additional verification steps:

1. verification that the provided public keychain and chain path combo together can be used to derive the public key of the signer
2. verification that the provided public keychain is explicitly specified by the user in his/her blockchain ID profile as a keychain that has authorization to perform authentication

The public keychain is verified against the chain path and public key in the following way:

1. the chain path is split up into 8 32-bit pieces, which are each modded with 2^31, yielding 8 31-bit "chain steps"
2. each chain step is used in succession to produce a child key from the previous parent key until a final child key (aka "ancestor" key) is produced
3. the ancestor key is checked for equality with the public key of the signer
