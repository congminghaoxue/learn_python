#!/usr/bin/env python
# encoding: utf-8

import socket


class UDPServer(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def __enter__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self._host, self._port))
        self._sock = sock
        return sock

    def __exit__(self, *exc_info):
        if exc_info[0]:
            import traceback
            traceback.print_exception(*exc_info)
        self._sock.close()


if __name__ == '__main__':
    host = '192.168.2.106'
    port = 5567
    with UDPServer(host, port) as s:
        while True:
            msg, addr = s.recvfrom(1024)
            print(addr)
            s.sendto(msg, addr)
