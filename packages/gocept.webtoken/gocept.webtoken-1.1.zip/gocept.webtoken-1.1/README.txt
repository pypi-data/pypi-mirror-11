================================
The gocept.webtoken distribution
================================

This library helps you using JWT tokens with the Zope Component Architecture
(ZCA).

This package is compatible with Python version 2.7, 3.3 and 3.4.

This package requires ``cryptography``, which needs some install attention.
Please refer to its `install documentation`_ for further information.


.. _`install documentation`: https://cryptography.io/en/latest/installation/

.. contents::

Usage
=====

The ``CryptographicKey`` utility
--------------------------------

``gocept.webtoken`` uses a global utility of the class
``gocept.webtoken.CryptographicKeys``, which provides cryptographic keys for
different purposes. It loads a set of public and private keys from disk. It
takes the filesystem path to your key files and a list of key names::

    >>> keys = gocept.webtoken.CryptographicKeys(
    ...     '/path/to/keys', ['key1', 'key2'])

For each of the names, a private key file of the same name and a public key
file (with a .pub suffix) must reside inside the keys_dir.

The utility needs to be registered at the ZCA, either via a zcml file or via::

    >>> zope.component.provideUtility(keys)


Creating a token
----------------

Create a signed web token with the function ``create_web_token``. You will need
the private key name, which was registered at the CryptographycKey utility. It
is referenced by its name and the suffix ``-private``::

    >>> expires_in = 300  # The token is valid for 300 seconds
    >>> payload = {'your': 'data'}
    >>> result = gocept.webtoken.create_web_token(
    ...     'key1-private', 'issuer', 'subject', expires_in, payload)
    >>> result
    {'token': b'<TOKEN>',
     'data': {'nbf': 1443707771,
              'iss': 'issuer',
              'exp': 1443708071,
              'sub': 'subject',
              'data': {'your': 'data'},
              'iat': 1443707771}}

Decoding a token
----------------

Decode a signed web token with the function ``decode_web_token``. You will need
the public key name, which was registered at the CryptographycKey utility. It
is referenced by its name and the suffix ``-public``::

    >>> result = gocept.webtoken.decode_web_token(
    ...     result['token'], 'key1-public', 'subject')
    >>> result
    {'nbf': 1443707998,
     'iss': 'issuer',
     'exp': 1443708298,
     'sub': 'subject',
     'data': {'your': 'data'},
     'iat': 1443707998}

Note that the subject must match the subject given when the token was created.
