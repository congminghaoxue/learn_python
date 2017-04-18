#!/usr/bin/env python
# encoding: utf-8

def answer(s):
    re = ''
    a = ord('a')
    z = ord('z')
    for c in s:
        ascii_code = ord(c)
        if ascii_code >= a and ascii_code <= z:
            tmp = chr(a + z -ascii_code)
            re = re + tmp
        else:
            re = re + c

    return re

if __name__ == '__main__':
    str = raw_input("Inputs:")
    print(answer(str))

