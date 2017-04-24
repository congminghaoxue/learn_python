#!/usr/bin/env python
# encoding: utf-8

import sys

if sys.version_info.major > 2:
    import http.server as http_server
    import socketserver
else:
    import SimpleHTTPServer as http_server
    import SocketServer as socketserver

PORT = 8080

Handler = http_server.SimpleHTTPRequestHandler

Handler.extensions_map={
    '.manifest': 'text/cache-manifest',
    '.html': 'text/html',
    '.png': 'image/png',
    '.jpg': 'image/jpg',
    '.svg':    'image/svg+xml',
    '.css':    'text/css',
    '.js':    'application/x-javascript',
    '.md':    'text/x-markdown',
    '': 'application/octet-stream', # Default
    }

httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()
