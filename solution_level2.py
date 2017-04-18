#!/usr/bin/env python
# encoding: utf-8

import string
digs = string.digits + string.letters

def answer(n,b):
    def int2base(x, base):
        x = int(x)
        if x < 0:
            sign = -1
        elif x == 0:
            return digs[0]
        else:
            sign = 1
        x *= sign
        digits = []
        while x:
            digits.append(digs[x % base])
            x /= base
        if sign < 0:
            digits.append('-')
        digits.reverse()
        return ''.join(digits)
    k=len(n)
    x= "".join((lambda x:(x.sort(),x)[1])(list(n)))
    y = x[::-1]
    print(x)
    print(y)
    x = int(x,3)
    y= int(y,3)
    print(x)
    print(y)
    print(int2base(y-x,b))
answer('210022',3)
