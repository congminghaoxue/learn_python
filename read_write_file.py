#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-21 16:28:18
# @Author  : Zhou Bo (zhoub@suooter.com)
# @Link    : http://onlyus.online
# @Version : $Id$

from io import open

def filter(oldfile, newfile):
    '''\
    Read a list of names from a file line by line into an output file.
    If a line begins with a particular name, insert a string of text
    after the name before appending the line to the output file.
    '''

    with open(newfile, 'w') as outfile, open(oldfile, 'r', encoding='utf-8') as infile:
        for line in infile:
            outfile.write(line)

if __name__ == "__main__":
    filter('/etc/hosts', '/tmp/hosts')
