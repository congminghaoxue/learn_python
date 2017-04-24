#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-15 13:53:50
# @Author  : Zhou Bo (zhoub@suooter.com)
# @Link    : http://onlyus.online
# @Version : $Id$

# from gevent.wsgi import WSGIServer
# from SimpleXMLRPCServer import server

# http_server = WSGIServer(('', 8800), server)
# http_server.serve_forever()
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from gevent import monkey

#Threaded XML-RPC && Monkey Patch
monkey.patch_socket() #Just 2 line!
monkey.patch_thread() #Just 3 line!
monkey.patch_select() #Just 3 line!
class TXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer): pass

#Logic function
def add(a, b):
    return a + b

#Logic function 2
def gen(n):
    return "0" * n

#create server
server = TXMLRPCServer(('', 8000), SimpleXMLRPCRequestHandler)
server.register_function(add, "add")
server.register_function(gen, "gen")
server.serve_forever()
