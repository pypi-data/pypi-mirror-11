# fernet-inspector

A tool for inspecting the contents of a Fernet token, local to the server it
was generated from.

## Example Usage

```
> fernet-inspector -h
usage: fernet-inspector [-h] [-k KEY_REPOSITORY] token

Inspect the contents of a Keystone Fernet token from the host it was issued
from.

positional arguments:
  token                 token to decrypt

optional arguments:
  -h, --help            show this help message and exit
  -k KEY_REPOSITORY, --key-repository KEY_REPOSITORY
                        location of Fernet key repository.
```

You should be able to decrypt a Keystone Fernet token and get the resulting
payload:

```
> python inspector.py -t <token-to-decrypt>
[2, 'b03ed914036b46b394c940419e12da0f', 1, '5aced855355a48f6aed86e403b9a9860', 1442335932.57696, ['\x80w\x02D\x1a\xa4M\xec\xb2\xea\nB\x87\x86\x14\x18']]
```

This tool is only meant to supply information about a token. It's not intended
to make assumptions about a particular token format in Keystone, or assertions
about the order in which the data was packed.

Now you can map to the appropriate payload based on the first element of the
payload, which is the token `version`. The first element is `2` in this case,
which means we are dealing with a `ProjectScopedPayload` of the
`keystone.token.providers.fernet.token_formatter.py:TokenFormatter` class. Note
that the last element of this particular token is a list. Keystone token
formats uses lists for both audit IDs and group IDs. The audit ID, as keystone
knows generates it, is done like:

```
base64.urlsafe_b64encode(uuid.uuid4().bytes)[:-2]
```

Where the group IDs within a list are converted to bytes. When the
`fernet_inspector` tool encounters a list of values in the payload, it leaves
the values as is. This tool doesn't know enough context about the order in
which Keystone packs tokens to make accurate assumptions about how to organize
the data. This would require `fernet_inspector` to track upstream Keystone
token formats in order to operated effectively. Instead, `fernet_inspector`
will leave values packed in lists in their UUID byte format. The values can
still be calculated based on the `UUID.byte` representation. For example,
converting `UUID.byte` representation to a Keystone audit ID:

```
>>> import base64
>>> base64.urlsafe_b64encode('\x80w\x02D\x1a\xa4M\xec\xb2\xea\nB\x87\x86\x14\x18')
'gHcCRBqkTeyy6gpCh4YUGA=='
```

Converting `UUID.byte` representation to `UUID.hex` format:

```
>>> import uuid
>>> uuid.UUID(bytes='\x80w\x02D\x1a\xa4M\xec\xb2\xea\nB\x87\x86\x14\x18').hex
'807702441aa44decb2ea0a4287861418'
```
