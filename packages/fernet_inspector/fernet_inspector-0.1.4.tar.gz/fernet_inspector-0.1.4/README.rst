================
fernet-inspector
================

A tool for inspecting the contents of a Keystone Fernet token, with respect to
the server it was generated from. The contents of a token can then be unpacked
and mapped using the appropriate token format. This tool is designed to be an
inspection tool and does not guarantee consistent format of the token payload.

Installation
------------

.. code:: bash

    $ pip install fernet-inspector

Usage
-----

.. code:: bash

    >>> fernet-inspector -h
    usage: fernet-inspector [-h] [-k KEY_REPOSITORY] token

    Inspect the contents of a Keystone Fernet token from the host it was issued
    from.

    positional arguments:
      token                 token to decrypt

    optional arguments:
      -h, --help            show this help message and exit
      -k KEY_REPOSITORY, --key-repository KEY_REPOSITORY
                            location of Fernet key repository.

You should be able to decrypt a Fernet token and get the resulting payload:

.. code:: bash

    >>> fernet-inspector <token-to-decrypt>
    [2, '\xb0>\xd9\x14\x03kF\xb3\x94\xc9@A\x9e\x12\xda\x0f', 1, 'Z\xce\xd8U5ZH\xf6\xae\xd8n@;\x9a\x98`', 1442338543.238753, ['\xf0\xa8\x03T\x07\xbaJk\x8c;G\x9cG\xab\xdfX']]

This tool is only meant to supply information about a token. It's not intended
to make assumptions about a particular token format, or assertions about the
order in which the data was packed.

.. WARNING::

    The order and contents of any particular token format are subject to change
    at any time.

Now you can map to the appropriate payload based on the first element of the
payload, which is the token ``version``. In this case, the first element is
``2``, which means we are dealing with a ``ProjectScopedPayload`` of the
``keystone.token.providers.fernet.token_formatter.py:TokenFormatter`` class.

Handing Audit IDs
~~~~~~~~~~~~~~~~~

Audit IDs can be converted to their ``base64`` representation with the
following:

.. code:: bash

    >>> import base64
    >>> base64.urlsafe_b64encode('\xf0\xa8\x03T\x07\xbaJk\x8c;G\x9cG\xab\xdfX')
    '8KgDVAe6SmuMOecR6vfWA=='

Handling UUIDs
~~~~~~~~~~~~~~

Most unique identifiers packed into the token are converted from ``UUID.hex``
to their respective ``UUID.bytes`` representation. This results in a shorter
overall token. The ``UUID.bytes`` representation of the token can be converted
back to ``UUID.hex`` with the following:

.. code:: bash

    >>> import uuid
    >>> uuid.UUID(bytes='\xb0>\xd9\x14\x03kF\xb3\x94\xc9@A\x9e\x12\xda\x0f').hex
    'b03ed914036b46b394c940419e12da0f'

Handling Timestamps
~~~~~~~~~~~~~~~~~~~

The expiration of a token is converted to an integer because it saves space in
the token. The integer can be converted back to the original ``datetime``
object with the following:

.. code:: bash

    >>> import datetime
    >>> datetime.datetime.utcfromtimestamp(1442338543.238753)
    datetime.datetime(2015, 9, 15, 17, 35, 43, 238753)
