# Blockchain Auth Python

[![CircleCI](https://img.shields.io/circleci/project/blockstack/blockstack-auth-python.svg)](https://circleci.com/gh/blockstack/blockstack-auth-python/)
[![PyPI](https://img.shields.io/pypi/v/blockchainauth.svg)](https://pypi.python.org/pypi/blockchainauth/)
[![PyPI](https://img.shields.io/pypi/dm/blockchainauth.svg)](https://pypi.python.org/pypi/blockchainauth/)
[![PyPI](https://img.shields.io/pypi/l/blockchainauth.svg)](https://pypi.python.org/pypi/blockchainauth/)
[![Slack](http://slack.blockstack.org/badge.svg)](http://slack.blockstack.org/)

A Blockchain ID authentication library written in python that supports generating, decoding and verifying auth request and auth response tokens.

## Installation

```
$ pip install blockchainauth
```

## Auth Requests

### Request Format

```json
{
    'header': {'typ': 'JWT', 'alg': 'ES256K'},
    'payload': {
        'domain_name': 'http://localhost:5000',
        'exp': 1493412486,
        'iat': 1493408886,
        'iss': 'did:btc-addr:1NZNxhoxobqwsNvTb16pdeiqvFvce3Yg8U',
        'jti': '75719c8a-3679-45b7-9551-21b6dfc28444',
        'manifest_uri': 'http://localhost:5000/manifest.json',
        'public_keys': [027d28f9951ce46538951e3697c62588a87f1f1f295de4a14fdd4c780fc52cfe69],
        'redirect_uri': 'http://localhost:5000',
        'scopes': []
    },
    'signature': 'HBwhcgPj7hrKg_IOGyaMJ9L-U_kwE5EweK8H54E2fuNONeWElfJg-h10LJvbwrvf_3TcgzQRbqdxGSmro8Ey6A'
}
```

### Signing Requests

```python
>>> from blockchainauth import AuthRequest
>>> private_key = 'a5c61c6ca7b3e7e55edee68566aeab22e4da26baa285c7bd10e8d2218aa3b22901'
>>> auth_request = AuthRequest(private_key, 'localhost:5000')
>>> auth_request_token = auth_request.token()
>>> print auth_request_token
eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZXMiOltdLCJyZWRpcmVjdF91cmkiOiJsb2NhbGhvc3Q6NTAwMCIsImp0aSI6IjI3MWYxNGI5LTc3YmEtNDZiMy1iNmRjLTI2YzZjNjAyYWY5YiIsImV4cCI6IjE0OTM1NTI0MDQuMDYiLCJwdWJsaWNfa2V5cyI6WyIwMjdkMjhmOTk1MWNlNDY1Mzg5NTFlMzY5N2M2MjU4OGE4N2YxZjFmMjk1ZGU0YTE0ZmRkNGM3ODBmYzUyY2ZlNjkiXSwiaXNzIjoiZGlkOmJ0Yy1hZGRyOjFOWk54aG94b2Jxd3NOdlRiMTZwZGVpcXZGdmNlM1lnOFUiLCJpYXQiOiIxNDkzNTQ4ODA3Ljk2IiwibWFuaWZlc3RfdXJpIjoibG9jYWxob3N0OjUwMDAvbWFuaWZlc3QuanNvbiIsImRvbWFpbl9uYW1lIjoibG9jYWxob3N0OjUwMDAifQ.EotiYm1yGOJt3qqUWKzB0FQqkk8onxEB_rBgIllIUZ5l8gujREPPX1osWy8Wm6q8p0q81k41w1K8YyAAIgWucg
```

### Decoding Requests

```python
>>> AuthRequest.decode(auth_request_token)['payload']
{u'scopes': [], u'iss': u'did:btc-addr:1NZNxhoxobqwsNvTb16pdeiqvFvce3Yg8U', u'domain_name': u'localhost:5000', u'redirect_uri': u'localhost:5000', u'jti': u'271f14b9-77ba-46b3-b6dc-26c6c602af9b', u'exp': u'1493552404.06', u'iat': u'1493548807.96', u'public_keys': [u'027d28f9951ce46538951e3697c62588a87f1f1f295de4a14fdd4c780fc52cfe69'], u'manifest_uri': u'localhost:5000/manifest.json'}
```

### Verifying Requests

```python
>>> AuthRequest.verify(auth_request_token)
True
```

## Auth Responses

### Response Format

```json
{
    'header': {'typ': 'JWT', 'alg': 'ES256K'},
    'payload': {
        'exp': 1496141298.31,
        'iat': 1493549308.76,
        'iss': 'did:btc-addr:1NZNxhoxobqwsNvTb16pdeiqvFvce3Yg8U',
        'jti': 'b483adf1-1c3d-435c-be5e-bb88000bb2b4',
        'profile': {
            "@type": "Person",
            "account": [
                {
                    "service": "bitcoin",
                    "@type": "Account",
                    "identifier": "1LFS37yRSibwbf8CnXeCn5t1GKeTEZMmu9",
                    "role": "payment"
                },
                {
                    "service": "pgp",
                    "contentUrl": "https://s3.amazonaws.com/pk9/ryan",
                    "@type": "Account",
                    "identifier": "1E4329E6634C75730D4D88C0638F2769D55B9837"
                },
                {
                    "service": "openbazaar",
                    "proofType": "http",
                    "@type": "Account",
                    "proofUrl": "https://www.facebook.com/msrobot0/posts/10153644446452759",
                    "identifier": "f2250123a6af138c86b30f3233b338961dc8fbc3"
                },
                {
                    "service": "twitter",
                    "proofType": "http",
                    "@type": "Account",
                    "proofUrl": "https://twitter.com/ryaneshea/status/765575388735082496",
                    "identifier": "ryaneshea"
                },
                {
                    "service": "github",
                    "proofType": "http",
                    "@type": "Account",
                    "proofUrl": "https://gist.github.com/shea256/a6dc1f3182f28bb2285feaef07a14340",
                    "identifier": "shea256"
                },
                {
                    "service": "facebook",
                    "proofType": "http",
                    "@type": "Account",
                    "proofUrl": "https://www.facebook.com/ryaneshea/posts/10154182997407713",
                    "identifier": "ryaneshea"
                }
            ],
            "website": [
                {
                    "@type": "WebSite",
                    "url": "http://shea.io"
                }
            ],
            "description": "Co-founder of Blockstack Inc.",
            "name": "Ryan Shea",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "New York"
            },
            "image": [
                {
                    "@type": "ImageObject",
                    "contentUrl": "https://s3.amazonaws.com/kd4/ryan",
                    "name": "avatar"
                },
                {
                    "@type": "ImageObject",
                    "contentUrl": "https://s3.amazonaws.com/dx3/ryan",
                    "name": "cover"
                }
            ]
        },
        'public_keys': [027d28f9951ce46538951e3697c62588a87f1f1f295de4a14fdd4c780fc52cfe69],
        'username': 'ryan.id'
    },
    'signature': 'CoOAxoYEOAYd0ajaa31AWxFzvBhSxzdEUa-tm2LDlkICj_sNIgF-jHJY-6WPGfk4OmLLZ-8Uos5HdWes1PviRQ'
}
```

### Signing Responses

```python
>>> from blockchainauth import AuthResponse
>>> RYAN_PROFILE = {...}
>>> private_key = 'a5c61c6ca7b3e7e55edee68566aeab22e4da26baa285c7bd10e8d2218aa3b22901'
>>> username = 'ryan.id'
>>> from blockchainauth import AuthResponse
>>> auth_response = AuthResponse(private_key, RYAN_PROFILE, username)
>>> auth_response_token = auth_response.token()
>>> print auth_response_token
eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJwcm9maWxlIjp7IndlYnNpdGUiOlt7InVybCI6Imh0dHA6Ly9zaGVhLmlvIiwiQHR5cGUiOiJXZWJTaXRlIn1dLCJhY2NvdW50IjpbeyJpZGVudGlmaWVyIjoiMUxGUzM3eVJTaWJ3YmY4Q25YZUNuNXQxR0tlVEVaTW11OSIsInJvbGUiOiJwYXltZW50IiwiQHR5cGUiOiJBY2NvdW50Iiwic2VydmljZSI6ImJpdGNvaW4ifSx7ImNvbnRlbnRVcmwiOiJodHRwczovL3MzLmFtYXpvbmF3cy5jb20vcGs5L3J5YW4iLCJpZGVudGlmaWVyIjoiMUU0MzI5RTY2MzRDNzU3MzBENEQ4OEMwNjM4RjI3NjlENTVCOTgzNyIsIkB0eXBlIjoiQWNjb3VudCIsInNlcnZpY2UiOiJwZ3AifSx7ImlkZW50aWZpZXIiOiJmMjI1MDEyM2E2YWYxMzhjODZiMzBmMzIzM2IzMzg5NjFkYzhmYmMzIiwicHJvb2ZUeXBlIjoiaHR0cCIsIkB0eXBlIjoiQWNjb3VudCIsInNlcnZpY2UiOiJvcGVuYmF6YWFyIiwicHJvb2ZVcmwiOiJodHRwczovL3d3dy5mYWNlYm9vay5jb20vbXNyb2JvdDAvcG9zdHMvMTAxNTM2NDQ0NDY0NTI3NTkifSx7ImlkZW50aWZpZXIiOiJyeWFuZXNoZWEiLCJwcm9vZlR5cGUiOiJodHRwIiwiQHR5cGUiOiJBY2NvdW50Iiwic2VydmljZSI6InR3aXR0ZXIiLCJwcm9vZlVybCI6Imh0dHBzOi8vdHdpdHRlci5jb20vcnlhbmVzaGVhL3N0YXR1cy83NjU1NzUzODg3MzUwODI0OTYifSx7ImlkZW50aWZpZXIiOiJzaGVhMjU2IiwicHJvb2ZUeXBlIjoiaHR0cCIsIkB0eXBlIjoiQWNjb3VudCIsInNlcnZpY2UiOiJnaXRodWIiLCJwcm9vZlVybCI6Imh0dHBzOi8vZ2lzdC5naXRodWIuY29tL3NoZWEyNTYvYTZkYzFmMzE4MmYyOGJiMjI4NWZlYWVmMDdhMTQzNDAifSx7ImlkZW50aWZpZXIiOiJyeWFuZXNoZWEiLCJwcm9vZlR5cGUiOiJodHRwIiwiQHR5cGUiOiJBY2NvdW50Iiwic2VydmljZSI6ImZhY2Vib29rIiwicHJvb2ZVcmwiOiJodHRwczovL3d3dy5mYWNlYm9vay5jb20vcnlhbmVzaGVhL3Bvc3RzLzEwMTU0MTgyOTk3NDA3NzEzIn1dLCJuYW1lIjoiUnlhbiBTaGVhIiwiaW1hZ2UiOlt7ImNvbnRlbnRVcmwiOiJodHRwczovL3MzLmFtYXpvbmF3cy5jb20va2Q0L3J5YW4iLCJAdHlwZSI6IkltYWdlT2JqZWN0IiwibmFtZSI6ImF2YXRhciJ9LHsiY29udGVudFVybCI6Imh0dHBzOi8vczMuYW1hem9uYXdzLmNvbS9keDMvcnlhbiIsIkB0eXBlIjoiSW1hZ2VPYmplY3QiLCJuYW1lIjoiY292ZXIifV0sImFkZHJlc3MiOnsiYWRkcmVzc0xvY2FsaXR5IjoiTmV3IFlvcmsiLCJAdHlwZSI6IlBvc3RhbEFkZHJlc3MifSwiQHR5cGUiOiJQZXJzb24iLCJkZXNjcmlwdGlvbiI6IkNvLWZvdW5kZXIgb2YgQmxvY2tzdGFjayBJbmMuIn0sInVzZXJuYW1lIjoicnlhbi5pZCIsImlzcyI6ImRpZDpidGMtYWRkcjoxTlpOeGhveG9icXdzTnZUYjE2cGRlaXF2RnZjZTNZZzhVIiwianRpIjoiYjQ4M2FkZjEtMWMzZC00MzVjLWJlNWUtYmI4ODAwMGJiMmI0IiwiZXhwIjoiMTQ5NjE0MTI5OC4zMSIsInB1YmxpY19rZXlzIjpbIjAyN2QyOGY5OTUxY2U0NjUzODk1MWUzNjk3YzYyNTg4YTg3ZjFmMWYyOTVkZTRhMTRmZGQ0Yzc4MGZjNTJjZmU2OSJdLCJpYXQiOiIxNDkzNTQ5MzA4Ljc2In0.CoOAxoYEOAYd0ajaa31AWxFzvBhSxzdEUa-tm2LDlkICj_sNIgF-jHJY-6WPGfk4OmLLZ-8Uos5HdWes1PviRQ
```

### Decoding Responses

```python
>>> AuthResponse.decode(auth_response_token)['payload']
{u'profile': {u'website': [{u'url': u'http://shea.io', u'@type': u'WebSite'}], u'account': [{u'identifier': u'1LFS37yRSibwbf8CnXeCn5t1GKeTEZMmu9', u'role': u'payment', u'@type': u'Account', u'service': u'bitcoin'}, {u'contentUrl': u'https://s3.amazonaws.com/pk9/ryan', u'identifier': u'1E4329E6634C75730D4D88C0638F2769D55B9837', u'@type': u'Account', u'service': u'pgp'}, {u'identifier': u'f2250123a6af138c86b30f3233b338961dc8fbc3', u'proofUrl': u'https://www.facebook.com/msrobot0/posts/10153644446452759', u'proofType': u'http', u'service': u'openbazaar', u'@type': u'Account'}, {u'identifier': u'ryaneshea', u'proofUrl': u'https://twitter.com/ryaneshea/status/765575388735082496', u'proofType': u'http', u'service': u'twitter', u'@type': u'Account'}, {u'identifier': u'shea256', u'proofUrl': u'https://gist.github.com/shea256/a6dc1f3182f28bb2285feaef07a14340', u'proofType': u'http', u'service': u'github', u'@type': u'Account'}, {u'identifier': u'ryaneshea', u'proofUrl': u'https://www.facebook.com/ryaneshea/posts/10154182997407713', u'proofType': u'http', u'service': u'facebook', u'@type': u'Account'}], u'name': u'Ryan Shea', u'image': [{u'contentUrl': u'https://s3.amazonaws.com/kd4/ryan', u'@type': u'ImageObject', u'name': u'avatar'}, {u'contentUrl': u'https://s3.amazonaws.com/dx3/ryan', u'@type': u'ImageObject', u'name': u'cover'}], u'address': {u'addressLocality': u'New York', u'@type': u'PostalAddress'}, u'@type': u'Person', u'description': u'Co-founder of Blockstack Inc.'}, u'username': u'ryan.id', u'iss': u'did:btc-addr:1NZNxhoxobqwsNvTb16pdeiqvFvce3Yg8U', u'jti': u'b483adf1-1c3d-435c-be5e-bb88000bb2b4', u'exp': u'1496141298.31', u'iat': u'1493549308.76', u'public_keys': [u'027d28f9951ce46538951e3697c62588a87f1f1f295de4a14fdd4c780fc52cfe69']}
```

### Verifying Responses

```python
>>> AuthResponse.verify(auth_response_token)
True
```
