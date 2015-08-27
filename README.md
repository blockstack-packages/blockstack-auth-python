# Blockchain ID Auth

Library for Blockchain ID authentication, including interfaces for generating auth requests tokens and auth response tokens.

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
        "issuedAt":"1440542996.19",
        "challenge":"97f4a043-a915-4f46-9a57-59d2a8714813",
        "issuingDomain":"onename.com",
        "permissions":["public-profile"]
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
eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3N1ZWRBdCI6IjE0NDA2MjQ0MzUuMjgiLCJjaGFsbGVuZ2UiOiI4YmVmZTllNS1kYjNhLTQwOGEtYWFhZS1jNDFjMWM4ZWVlNTUiLCJwZXJtaXNzaW9ucyI6WyJibG9ja2NoYWluaWQiXSwiaXNzdWVyIjp7InB1YmxpY0tleSI6IjAyMzFlNDg3M2I1NTY5YzU4MTFiNDg0OWNmMTc5N2YyYmZmM2RhYjM1OGIwNzQxNmFhN2E5YWY2MzhmNzE4MmNhMyIsImRvbWFpbiI6Im9uZW5hbWUuY29tIn19.iBNl-mluCLPJ2ttWi4QSx2uxSPpggOugmYVN0r9MTeFfWfrTxInVpjCpMxdaEBjnXDYOgDCcYuCQYOWELhbDJw
>>> AuthRequest.decode(auth_request_token)
{"issuedAt":"1440624435.28","challenge":"8befe9e5-db3a-408a-aaae-c41c1c8eee55","permissions":["blockchainid"],"issuer":{"publicKey":"0231e4873b5569c5811b4849cf1797f2bff3dab358b07416aa7a9af638f7182ca3","domain":"onename.com"}}
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
        "issuedAt":"1440542996.35",
        "blockchainid":"ryan",
        "challenge":"97f4a043-a915-4f46-9a57-59d2a8714813",
        "issuingPublicKey":"03b012a24985788afa54a158d3b43ca03a85765ff3b785fe66a6cbc050b8198689",
        "masterPublicKey":"xpub69W5QnTxuA3VSXzJUopfm3T5aX51HJGQo8mvvkRqwWNNbpnjQp3gb9ghpJk6NHxymLMqWPn3J2qr4vkG7Bcc9qqwg3Nom1XwR9yajP9nemf",
        "chainPath":"bd62885ec3f0e3838043115f4ce25eedd22cc86711803fb0c19601eeef185e39"
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
eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3N1ZWRBdCI6IjE0NDA2MjQ0MzUuNzYiLCJjaGFsbGVuZ2UiOiI3Y2Q5ZWQ1ZS1iYjBlLTQ5ZWEtYTMyMy1mMjhiZGUzYTA1NDkiLCJpc3N1ZXIiOnsicHVibGljS2V5IjoiMDM0ZTYyMjg1YmU1MTJmYWFlZmE0YzgzYmVjYjI3ZGMwNzQ2YjdjNjgyOGE3MGQ5NGQ3ZmIwMTczZDc5ZGE5YWY3IiwiY2hhaW5QYXRoIjoiYmQ2Mjg4NWVjM2YwZTM4MzgwNDMxMTVmNGNlMjVlZWRkMjJjYzg2NzExODAzZmIwYzE5NjAxZWVlZjE4NWUzOSIsIm1hc3RlclB1YmxpY0tleSI6InhwdWI2OVc1UW5UeHVBM1ZTWHpKVW9wZm0zVDVhWDUxSEpHUW84bXZ2a1Jxd1dOTmJwbmpRcDNnYjlnaHBKazZOSHh5bUxNcVdQbjNKMnFyNHZrRzdCY2M5cXF3ZzNOb20xWHdSOXlhalA5bmVtZiIsImJsb2NrY2hhaW5pZCI6InJ5YW4ifX0.xVhijOn8jcIWGf2TXn6SGUdX6fzAG0nN6QQDicpIJpPQmhZvHxhAiIkrlgx3g0cgMmhlnUtiUiLF5DLFzouPcA
>>> AuthResponse.decode(auth_response_token)
{"issuedAt":"1440624435.76","challenge":"7cd9ed5e-bb0e-49ea-a323-f28bde3a0549","issuer":{"publicKey":"034e62285be512faaefa4c83becb27dc0746b7c6828a70d94d7fb0173d79da9af7","chainPath":"bd62885ec3f0e3838043115f4ce25eedd22cc86711803fb0c19601eeef185e39","masterPublicKey":"xpub69W5QnTxuA3VSXzJUopfm3T5aX51HJGQo8mvvkRqwWNNbpnjQp3gb9ghpJk6NHxymLMqWPn3J2qr4vkG7Bcc9qqwg3Nom1XwR9yajP9nemf","blockchainid":"ryan"}}
```

### Verifying Responses

```python
>>> AuthResponse.verify(auth_response_token)
True
```
