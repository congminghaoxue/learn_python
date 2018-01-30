#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-19 20:52:04
# @Author  : Zhou Bo (zhoub@suooter.com)
# @Link    : http://onlyus.online
# @Version : $Id$

from os import listdir, remove
from os.path import isdir, isfile, join

my_path = "/Volumes/bak/ky/"

#


def dele_aria2(f):
    if isdir(f):
        for x in listdir(f):
            if isfile(join(f, x)) and join(f, x)[-5:] == "aria2":
                print(join(f, x))
            else:
                dele_aria2(join(f, x))
    elif f[-5:] == "aria2":
        print(f)


def main():
    for x in listdir(my_path):
        dele_aria2(join(my_path, x))


if __name__ == '__main__':
    main()
