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
    def foo(n,b):
        k=len(n)
        x= "".join((lambda x:(x.sort(),x)[1])(list(n)))
        y = x[::-1]
        x = int(x,b)
        y= int(y,b)
        z=int2base(y-x,b)
        if k != len(z):
            z = int(z) * 10**(k-len(z))
        return z
    lst = [n]
    for v in lst:
        tmp = foo(str(v),b)
        if tmp in lst:
            return len(lst) - lst.index(tmp)
        else:
            lst.append(tmp)

if __name__ == '__main__':
    foo = input('input string:')
    bar = input('input base:')
    print(answer(foo,bar))
