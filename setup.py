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
        'cryptography==1.0.0',
        'pybitcoin==0.9.3',
        'PyJWT==1.4.0',
        'onename==0.2.0',
        'bitmerchant==0.1.7'
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
