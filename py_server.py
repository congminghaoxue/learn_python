#!/usr/bin/env python
# encoding: utf-8

import sys

if sys.version_info.major > 2:
    import http.server as http_server
    import socketserver
else:
    import SimpleHTTPServer as http_server
    import SocketServer as socketserver

Handler = http_server.SimpleHTTPRequestHandler
# python -c "import SimpleHTTPServer; m = SimpleHTTPServer.SimpleHTTPRequestHandler.extensions_map; m[''] = 'text/plain'; m.update(dict([(k, v + ';charset=UTF-8') for k, v in m.items()])); SimpleHTTPServer.test();"

Handler.extensions_map={
    '.manifest': 'text/cache-manifest',
    '.html': 'text/html',
    '.txt': 'text/html',
    '.png': 'image/png',
    '.jpg': 'image/jpg',
    '.svg':'image/svg+xml',
    '.css':'text/css',
    '.js':'application/x-javascript',
    '.md':'text/x-markdown',
    '.markdown':'text/x-markdown',
    '': 'application/octet-stream', # Default
}
m=Handler.extensions_map
m.update(dict([(k, v + ';charset=UTF-8') for k, v in m.items()]));
PORT = 8081
httpd = socketserver.TCPServer(("0.0.0.0", PORT), Handler)
print('serving at port: {}'.format(PORT))
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print('\nserver shutdown!')

httpd.server_close()
