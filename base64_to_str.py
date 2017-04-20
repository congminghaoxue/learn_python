#!/usr/bin/env python
# encoding: utf-8


import base64
import sys

def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    if sys.version_info.major > 2:
        data = bytes(data, 'utf-8')
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data)

if __name__ == "__main__":
    try:
        print(decode_base64(sys.argv[1]))
    except:
        print('Please input the base64 string!')
