#!/usr/bin/env python3

"""Establish UDP Listener"""

__author__ = "Jason M. Pittman"
__copyright__ = "Copyright 2020"
__credits__ = ["Jason M. Pittman"]
__license__ = "GPLv3"
__version__ = "0.1.0"
__maintainer__ = "Jason M. Pittman"
__email__ = "jpittman@highpoint.edu"
__status__ = "Development"

import socket

class UdpServer:
    
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

    def bind(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock = (self.ip_address, int(self.port))
        s.bind(sock)
        
        while True:
            payload, client_socket = s.recvfrom(1024)
            s.sendto(payload, client_socket) 


        