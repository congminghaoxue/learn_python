#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-15 10:13:21
# @Author  : Zhou Bo (zhoub@suooter.com)
# @Link    : http://onlyus.online
# @Version : $Id$

import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8000')
print(s.pow(2,3))  # Returns 2**3 = 8
print(s.add(2,3))  # Returns 5
print(s.mul(5,2))  # Returns 5*2 = 10

# Print list of available methods
print(s.system.listMethods())
