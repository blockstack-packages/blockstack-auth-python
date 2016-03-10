"""
blockchainauth
==============

"""

from setuptools import setup, find_packages

setup(
    name='blockchainauth',
    version='0.2.1',
    url='https://github.com/blockstack/blockchain-auth-python',
    license='MIT',
    author='Blockstack Developers',
    author_email='hello@onename.com',
    description=("Blockchain Auth Library"),
    keywords='blockchain auth authentication id identity login bitcoin cryptocurrency',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'cryptography==1.2.3',
        'pybitcoin==0.9.8',
        'PyJWT==1.4.0',
        'onename==0.2.0',
        'bitmerchant==0.1.8',
        'requests==2.9.1',
        'utilitybelt==0.2.6'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
