#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-15 13:55:57
# @Author  : Zhou Bo (zhoub@suooter.com)
# @Link    : http://onlyus.online
# @Version : $Id$


from xmlrpc.server import CGIXMLRPCRequestHandler


class MyFuncs:
    def div(self, x, y):
        return x // y


handler = CGIXMLRPCRequestHandler()
handler.register_function(pow)
handler.register_function(lambda x, y: x + y, 'add')
handler.register_introspection_functions()
handler.register_instance(MyFuncs())
handler.handle_request()
