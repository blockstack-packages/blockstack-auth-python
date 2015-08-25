# Blockchain ID Auth

Library for Blockchain ID authentication, including interfaces for generating auth requests tokens and auth response tokens.

Also built-in is a JSON Web Token Library compatible with Bitcoin's SECP256K1.

### Signing Auth Requests

```python
>>> from pybitcoin import BitcoinPrivateKey
>>> from idauth import AuthRequestTokenizer
>>> private_key = BitcoinPrivateKey(compressed=True)
>>> request_tokenizer = AuthRequestTokenizer('onename.com', permissions=['public-profile'])
>>> auth_request_token = request_tokenizer.sign(private_key.to_pem())
>>> print auth_request_token
eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3N1ZWRBdCI6IjE0NDA1NDYxNTUuMTQiLCJjaGFsbGVuZ2UiOiJjZWM5YWVmMy05MDU1LTQyZDEtODFkNy1iNmIyMWFhYTQ0YjAiLCJpc3N1aW5nRG9tYWluIjoib25lbmFtZS5jb20iLCJwZXJtaXNzaW9ucyI6WyJwdWJsaWMtcHJvZmlsZSJdfQ.xq04F4iu0HrR8dfVM3vJQ4usYrDmdf6Z94V0X4yO2pUUi2Zft8n-sqhlG0KpJ1Hn-F-U34iKJOYksPOmtun7mw
>>> request_tokenizer.decode(auth_request_token)
{"issuedAt":"1440542996.19","challenge":"97f4a043-a915-4f46-9a57-59d2a8714813","issuingDomain":"onename.com","permissions":["public-profile"]}
```

### Verifying Auth Requests

```python
>>> public_key = private_key.public_key()
>>> request_tokenizer.verify(auth_request_token, public_key.to_pem())
True
```

### Signing Auth Responses

```python
>>> from idauth import AuthResponseTokenizer
>>> private_key = BitcoinPrivateKey(compressed=True)
>>> blockchainid = 'ryan'
>>> master_public_key = 'xpub69W5QnTxuA3VSXzJUopfm3T5aX51HJGQo8mvvkRqwWNNbpnjQp3gb9ghpJk6NHxymLMqWPn3J2qr4vkG7Bcc9qqwg3Nom1XwR9yajP9nemf'
>>> response_tokenizer = AuthResponseTokenizer(blockchainid, master_public_key)
>>> challenge = 'ad21e749-b8dc-4167-9486-72c92a85227a'
>>> chain_path = 'bd62885ec3f0e3838043115f4ce25eedd22cc86711803fb0c19601eeef185e39'
>>> auth_response_token = response_tokenizer.sign(
    private_key.to_pem(), private_key.public_key().to_hex(), challenge, chain_path=chain_path)
>>> print auth_response_token
eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3N1ZWRBdCI6IjE0NDA1NDYxNTUuNjIiLCJibG9ja2NoYWluaWQiOiJyeWFuIiwiY2hhbGxlbmdlIjoiZTdiMWEyMTQtZDYxZi00ZmFjLTljYTUtYTIwYmI3YWQ2ZWY4IiwiaXNzdWluZ1B1YmxpY0tleSI6IjAyZjNhNmE1YTE4ZTc0N2U1YjJlMDM4NzAzNTdlZDE1NDcyYzExZGMyMTdmZTU4M2Y1NGFjOTU0NmFhOTRkN2VkOSIsIm1hc3RlclB1YmxpY0tleSI6InhwdWI2OVc1UW5UeHVBM1ZTWHpKVW9wZm0zVDVhWDUxSEpHUW84bXZ2a1Jxd1dOTmJwbmpRcDNnYjlnaHBKazZOSHh5bUxNcVdQbjNKMnFyNHZrRzdCY2M5cXF3ZzNOb20xWHdSOXlhalA5bmVtZiIsImNoYWluUGF0aCI6ImJkNjI4ODVlYzNmMGUzODM4MDQzMTE1ZjRjZTI1ZWVkZDIyY2M4NjcxMTgwM2ZiMGMxOTYwMWVlZWYxODVlMzkifQ.9NQGe4IEEGzTSQlD3giUmDkgETcDc8qbt1BMD17n3cQMJZyb3TEdXsLINyO5LmIpE5m0LqOAbtHOCKbxsRMS4w
>>> response_tokenizer.decode(auth_response_token)
{"issuedAt":"1440542996.35","blockchainid":"ryan","challenge":"97f4a043-a915-4f46-9a57-59d2a8714813","issuingPublicKey":"03b012a24985788afa54a158d3b43ca03a85765ff3b785fe66a6cbc050b8198689","masterPublicKey":"xpub69W5QnTxuA3VSXzJUopfm3T5aX51HJGQo8mvvkRqwWNNbpnjQp3gb9ghpJk6NHxymLMqWPn3J2qr4vkG7Bcc9qqwg3Nom1XwR9yajP9nemf","chainPath":"bd62885ec3f0e3838043115f4ce25eedd22cc86711803fb0c19601eeef185e39"}
```

### Verifying Auth Responses

```python
>>> public_key = private_key.public_key()
>>> response_tokenizer.verify(auth_response_token, public_key.to_pem())
True
```
