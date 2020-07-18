#!/usr/bin/env python3

"""Establish TCP Listener"""

__author__ = "Jason M. Pittman"
__copyright__ = "Copyright 2020"
__credits__ = ["Jason M. Pittman"]
__license__ = "GPLv3"
__version__ = "0.2.0"
__maintainer__ = "Jason M. Pittman"
__email__ = "jpittman@highpoint.edu"
__status__ = "Development"

import socket

class TcpServer:

    def __init__(self, ip_address, port, max_conn):
        self.ip_address = ip_address
        self.port = port
        self.max_conn = max_conn

    def bind(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.ip_address, int(self.port)))

        return s

    def read_tcp(self, tcp_socket):
        client_socket, client_socket_info = tcp_socket.accept()

        payload = client_socket.recv(1024)     
        client_socket.send(payload)

        client_socket.close()