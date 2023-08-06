"""
pybitcoin
==============

"""

from setuptools import setup, find_packages

setup(
    name='pybitcoin',
    version='0.9.2',
    url='https://github.com/blockstack/pybitcoin',
    license='MIT',
    author='Blockstack Developers',
    author_email='hello@onename.com',
    description=("Tools for Bitcoin & other cryptocurrencies (private & ",
                 "public keys, addresses, transactions, RPC, etc.)."),
    keywords='bitcoin btc litecoin namecoin dogecoin cryptocurrency',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'commontools==0.1.0',
        'ecdsa==0.11',
        'utilitybelt>=0.2.1',
        'requests>=2.4.3',
        'pybitcointools==1.1.15',
        'python-bitcoinrpc==0.1'
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
