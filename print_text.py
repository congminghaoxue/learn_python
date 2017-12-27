#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-28 14:26:04
# @Author  : Zhou Bo (zhoub@suooter.com)
# @Link    : http://onlyus.online
# @Version : $Id$

import os


def show_content(file, paginate):
    """
    show the content of a file,display paginate lines
    and ask user to press any key to continue
    """
    with open(file) as f:
        for idx, line in enumerate(f, start=1):
            print(line, end='')
            if not idx % paginate:
                print('Press any key to continue')
                _ = input()


if __name__ == '__main__':
    show_content(os.environ['HOME'] + '/.vimrc', 25)
