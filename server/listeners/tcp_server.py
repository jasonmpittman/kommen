#!/usr/bin/env python3

"""Establish TCP Listener"""

__author__ = "Jason M. Pittman"
__copyright__ = "Copyright 2020"
__credits__ = ["Jason M. Pittman"]
__license__ = "GPLv3"
__version__ = "0.1.0"
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
        s.bind((self.ip_address, int(self.port)))

        return s

    def listen(self, socket):
        socket.listen(int(self.max_conn))

        while 1:
            client_socket, client_socket_info = socket.accept()

            request = client_socket.recv(1024)
             
            client_socket.send(request)

            client_socket.close()