#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-28 11:18:56
# @Author  : Zhou Bo (congminghaoxue@gmail.com)
# @Link    : https://congminghaoxue.github.io/
# @Version : $Id$
from shutil import copyfile
from os import walk
import os
import imghdr
PIC_PATH = r'C:\Users\congm\Pictures\LOCKING'
for root, path, files in walk(r'C:\Users\congm\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets'):
    for file in files:
        file_type = (imghdr.what(os.path.join(root, file)))
        if os.path.getsize(os.path.join(root, file)) > 102400 \
                and file_type != 'png':
            copyfile(os.path.join(root, file),
                     os.path.join(PIC_PATH, file + '.' + file_type))
