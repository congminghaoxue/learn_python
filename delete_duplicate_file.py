#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import argparse
import hashlib
from os.path import isdir
from os import remove
import collections 

def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk


def get_hash(filename, first_chunk_only=False, hash=hashlib.sha1):
    hashobj = hash()
    file_object = open(filename, 'rb')

    if first_chunk_only:
        hashobj.update(file_object.read(1024))
    else:
        for chunk in chunk_reader(file_object):
            hashobj.update(chunk)
    hashed = hashobj.digest()

    file_object.close()
    return hashed


def check_for_duplicates(path, hash=hashlib.sha1):
    hashes_by_size = collections.defaultdict(list)
    hashes_on_1k = collections.defaultdict(list)
    hashes_full = {}
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            try:
                file_size = os.path.getsize(full_path)
            except (OSError,):
                # not accessible (permissions, etc) - pass on
                pass
            hashes_by_size[file_size].append(full_path)

    # For all files with the same file size, get their hash on the 1st 1024 bytes
    for __, files in hashes_by_size.items():
        if len(files) < 2:
            continue    # this file size is unique, no need to spend cpy cycles on it

        for filename in files:
            small_hash = get_hash(filename, first_chunk_only=True)

            hashes_on_1k[small_hash].append(filename)

    # For all files with the hash on the 1st 1024 bytes, get their hash on the full file - collisions will be duplicates
    for __, files in hashes_on_1k.items():
        if len(files) < 2:
            continue    # this hash of fist 1k file bytes is unique, no need to spend cpy cycles on it

        for filename in files:
            full_hash = get_hash(filename, first_chunk_only=False)

            duplicate = hashes_full.get(full_hash)
            if duplicate:
                if(len(filename) > len(duplicate)):
                    filename, duplicate = duplicate, filename                   
                remove(duplicate)
                print(duplicate)

            hashes_full[full_hash] = filename

def main():
    parser = argparse.ArgumentParser(description="Tool for delete the duplicate files")
    parser.add_argument('-P', '--path', help='the path that should be deal with')
    args = parser.parse_args()
    PATH = args.path
    if PATH:
        if not isdir(PATH):
            print('Pls input the real path')
        else:
            PATH=os.path.abspath(PATH)
    else:
        PATH = os.path.abspath('.')
    check_for_duplicates(PATH)

if __name__ == '__main__':
    main()