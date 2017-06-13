#!/usr/bin/env python
# encoding: utf-8

import argparse
import base64
import json
import re
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
if __name__== "__main__":
    argc = len(sys.argv)
    cmdargs = str(sys.argv)
    parser = argparse.ArgumentParser(description="Tool to get user_id from token in the logs")
    parser.add_argument('-f', '--file', required=True, help='the file path of the input file')
    args = parser.parse_args()
    file = args.file
    user = dict()
    with open(file) as f:
        for index, item in enumerate(f):
            if item.find('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.') != -1:
                token = re.search('(?<=bearer\ eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.)(.*)(?=\.)', item)
                if token:
                    token=token.group(0)
                    user_id = json.loads(decode_base64(token))['sub']
                    if user_id in user:
                        pass
                    else:
                        user[user_id] = token
                        print(str(user_id) + '##' + token)
