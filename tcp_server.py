#!/usr/bin/env python
# encoding: utf-8

import socket


class Server(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def __enter__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self._host, self._port))
        sock.listen(10)
        self._sock = sock
        return self._sock

    def __exit__(self, *exc_info):
        if exc_info[0]:
            import traceback
            traceback.print_exception(*exc_info)
        self._sock.close()


if __name__ == '__main__':
    host = '192.168.2.106'
    port = 5566
    with Server(host, 5566) as s:
        while True:
            print('aa')
            conn, addr = s.accept()
            msg = conn.recv(1024)
            print(msg)
            conn.send(msg)
            conn.close()
