#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    ~~~~~
    :copyright: (c) 2017 by Blockstack.org
    :license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

PRIVATE_KEY = 'a5c61c6ca7b3e7e55edee68566aeab22e4da26baa285c7bd10e8d2218aa3b22901'
PUBLIC_KEY = '027d28f9951ce46538951e3697c62588a87f1f1f295de4a14fdd4c780fc52cfe69'

REQUEST_SAMPLE_ENCODED_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NksifQ.eyJqdGkiOiI3NTcxOWM4YS0zNjc5LTQ1YjctOTU1MS0yMWI2ZGZjMjg0NDQiLCJpYXQiOjE0OTM0MDg4ODYsImV4cCI6MTQ5MzQxMjQ4NiwiaXNzIjoiZGlkOmJ0Yy1hZGRyOjFOWk54aG94b2Jxd3NOdlRiMTZwZGVpcXZGdmNlM1lnOFUiLCJwdWJsaWNfa2V5cyI6WyIwMjdkMjhmOTk1MWNlNDY1Mzg5NTFlMzY5N2M2MjU4OGE4N2YxZjFmMjk1ZGU0YTE0ZmRkNGM3ODBmYzUyY2ZlNjkiXSwiZG9tYWluX25hbWUiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJtYW5pZmVzdF91cmkiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAvbWFuaWZlc3QuanNvbiIsInJlZGlyZWN0X3VyaSI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTAwMCIsInNjb3BlcyI6W119.HBwhcgPj7hrKg_IOGyaMJ9L-U_kwE5EweK8H54E2fuNONeWElfJg-h10LJvbwrvf_3TcgzQRbqdxGSmro8Ey6A'
REQUEST_SAMPLE_DECODED_TOKEN = {
    'header': {'typ': 'JWT', 'alg': 'ES256K'},
    'payload': {
        'domain_name': 'http://localhost:5000',
        'exp': 1493412486,
        'iat': 1493408886,
        'iss': 'did:btc-addr:1NZNxhoxobqwsNvTb16pdeiqvFvce3Yg8U',
        'jti': '75719c8a-3679-45b7-9551-21b6dfc28444',
        'manifest_uri': 'http://localhost:5000/manifest.json',
        'public_keys': [PUBLIC_KEY],
        'redirect_uri': 'http://localhost:5000',
        'scopes': []
    },
    'signature': 'HBwhcgPj7hrKg_IOGyaMJ9L-U_kwE5EweK8H54E2fuNONeWElfJg-h10LJvbwrvf_3TcgzQRbqdxGSmro8Ey6A'
}

RESPONSE_SAMPLE_ENCODED_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NksifQ.eyJqdGkiOiIyNjhjMTllMC1hZmZkLTQ5MmUtYmI5Mi0yNGVmZDZiNTM0MmQiLCJpYXQiOjE0OTM0MjQwMDUsImV4cCI6MTQ5NjAxNjAwNSwiaXNzIjoiZGlkOmJ0Yy1hZGRyOjFMSG5vZFlSZTZRSDE3YlRGYTluV2tuSjJuNHhyNEJGYSIsInB1YmxpY19rZXlzIjpbIjAzYjQ1MWE5NjliZGU1YTY4ZWQwZTMxNWEyNWE3YjQ3MjI1MzE0MDdhNTU2ZThmNGU2YzY2Mzk1MmQwNWY0NDljNyJdLCJwcm9maWxlIjp7ImFjY291bnQiOlt7InByb29mVXJsIjoiaHR0cHM6Ly93d3cuZmFjZWJvb2suY29tL3Blcm1hbGluay5waHA_c3RvcnlfZmJpZD0xOTE5ODk5OTc5ODE3ODgmaWQ9MTAwMDE1MTIzNjc3MzUzIiwicHJvb2ZUeXBlIjoiaHR0cCIsIkB0eXBlIjoiQWNjb3VudCIsInNlcnZpY2UiOiJmYWNlYm9vayIsImlkZW50aWZpZXIiOiJwcm9maWxlLnBocD9pZD0xMDAwMTUxMjM2NzczNTMifSx7InByb29mVXJsIjoiaHR0cHM6Ly9naXN0LmdpdGh1Yi5jb20vc3BhbmtyYXRvdi80ZTE3MzBkZmQ0MDVjMTEzY2Q3MDhiMzQxZGQ0MmM1OCIsInByb29mVHlwZSI6Imh0dHAiLCJAdHlwZSI6IkFjY291bnQiLCJzZXJ2aWNlIjoiZ2l0aHViIiwiaWRlbnRpZmllciI6InNwYW5rcmF0b3YifSx7IkB0eXBlIjoiQWNjb3VudCIsInByb29mVHlwZSI6Imh0dHAiLCJwcm9vZlVybCI6Imh0dHBzOi8vdHdpdHRlci5jb20va2F0aHJpbjE1OTgvc3RhdHVzLzg1NTEzNDgwMjEzNTE5OTc0NCIsInNlcnZpY2UiOiJ0d2l0dGVyIiwiaWRlbnRpZmllciI6ImthdGhyaW4xNTk4In1dLCJpbWFnZSI6W3siY29udGVudFVybCI6Imh0dHBzOi8vczMuYW1hem9uYXdzLmNvbS9keDMvc3RhbmlzbGF2X3BhbmtyYXRvdiIsIm5hbWUiOiJjb3ZlciIsIkB0eXBlIjoiSW1hZ2VPYmplY3QifSx7ImNvbnRlbnRVcmwiOiJodHRwczovL3MzLmFtYXpvbmF3cy5jb20va2Q0L3N0YW5pc2xhdl9wYW5rcmF0b3YiLCJAdHlwZSI6IkltYWdlT2JqZWN0IiwibmFtZSI6ImF2YXRhciJ9XSwiQHR5cGUiOiJQZXJzb24iLCJuYW1lIjoiU3RhbmlzbGF2IFBhbmtyYXRvdiJ9LCJ1c2VybmFtZSI6InN0YW5pc2xhdl9wYW5rcmF0b3YuaWQifQ.9omzzPH269KQqwgd-fpfy4AqhhTx9u3jkGiIHh2uSgVvApGINk2EUKkWTa1hibhkei8Czko82xXoDZ5s3LM7fw'
RESPONSE_SAMPLE_DECODED_TOKEN = {
    'header': {'typ': 'JWT', 'alg': 'ES256K'},
    'payload': {
        'exp': 1496016005,
        'iat': 1493424005,
        'iss': 'did:btc-addr:1LHnodYRe6QH17bTFa9nWknJ2n4xr4BFa',
        'jti': '268c19e0-affd-492e-bb92-24efd6b5342d',
        'profile': {
            '@type': "Person",
            'account': [
                {
                    '@type': 'Account',
                    'identifier': "profile.php?id=100015123677353",
                    'proofType': 'http',
                    'proofUrl': 'https://www.facebook.com/permalink.php?story_fbid=191989997981788&id=100015123677353',
                    'service': 'facebook'
                },
                {
                    '@type': 'Account',
                    'identifier': "spankratov",
                    'proofType': 'http',
                    'proofUrl': 'https://gist.github.com/spankratov/4e1730dfd405c113cd708b341dd42c58',
                    'service': 'github'
                },
                {
                    '@type': 'Account',
                    'identifier': "kathrin1598",
                    'proofType': 'http',
                    'proofUrl': 'https://twitter.com/kathrin1598/status/855134802135199744',
                    'service': 'twitter'
                },
            ],
            'image': [
                {
                    '@type': 'ImageObject',
                    'contentUrl': 'https://s3.amazonaws.com/dx3/stanislav_pankratov',
                    'name': 'cover'
                },
                {
                    '@type': 'ImageObject',
                    'contentUrl': 'https://s3.amazonaws.com/kd4/stanislav_pankratov',
                    'name': 'avatar'
                }
            ],
            'name': 'Stanislav Pankratov',
        },
        'public_keys': ['03b451a969bde5a68ed0e315a25a7b4722531407a556e8f4e6c663952d05f449c7'],
        'username': 'stanislav_pankratov.id'
    },
    'signature': '9omzzPH269KQqwgd-fpfy4AqhhTx9u3jkGiIHh2uSgVvApGINk2EUKkWTa1hibhkei8Czko82xXoDZ5s3LM7fw'
}

RYAN_PROFILE = {
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
}
