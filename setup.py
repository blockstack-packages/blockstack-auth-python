"""
idauth
==============

"""

from setuptools import setup, find_packages

setup(
    name='idauth',
    version='0.0.0',
    url='https://github.com/blockstack/blockchain-id-auth',
    license='MIT',
    author='Blockstack Developers',
    author_email='hello@onename.com',
    description=("Blockchain ID Auth Library"),
    keywords='bitcoin btc litecoin namecoin dogecoin cryptocurrency',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'cryptography>=1.0.0',
        'pybitcoin>=0.9.1'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
