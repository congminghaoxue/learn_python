#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-15 10:11:05
# @Author  : Zhou Bo (zhoub@suooter.com)
# @Link    : http://onlyus.online
# @Version : $Id$


try:
    from SimpleXMLRPCServer import SimpleXMLRPCServer
    from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
    from SocketServer import ThreadingMixIn
except ImportError:
    from socketserver import ThreadingMixIn
    from xmlrpc.server import SimpleXMLRPCServer
    from xmlrpc.server import SimpleXMLRPCRequestHandler





# from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler

#Threaded XML-RPC
class TXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer): pass


# Restrict to a particular path.
# class RequestHandler(SimpleXMLRPCRequestHandler):
#     rpc_paths = ('/RPC2',)

server = TXMLRPCServer(('', 8000), SimpleXMLRPCRequestHandler)
# Create server
# server = SimpleXMLRPCServer(("localhost", 8000),
#                             requestHandler=RequestHandler)
server.register_introspection_functions()

# Register pow() function; this will use the value of
# pow.__name__ as the name, which is just 'pow'.
server.register_function(pow)


# add two value
def adder_function(x, y):
    '''
    add two value
    '''
    return x + y


server.register_function(adder_function, 'add')


# Register an instance; all the methods of the instance are
# published as XML-RPC methods (in this case, just 'mul').
class MyFuncs:
    def mul(self, x, y):
        return x * y

server.register_instance(MyFuncs())

# Run the server's main loop
server.serve_forever()
