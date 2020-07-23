#!/usr/bin/env python3

"""Establish UDP Listener"""

__author__ = "Jason M. Pittman"
__copyright__ = "Copyright 2020"
__credits__ = ["Jason M. Pittman"]
__license__ = "GPLv3"
__version__ = "0.2.0"
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
        s.setblocking(0)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock = (self.ip_address, int(self.port))
        s.bind(sock)
        
        return s

    def read_udp(self, udp_socket):
        try:
            payload, client_socket = udp_socket.recvfrom(1024)
            sent = udp_socket.sendto(payload, client_socket) 
        except socket.error as e:
            print('Exception occured in reading udp socket: ' + str(e))

    def close_socket(self, udp_socket):
        try:
            udp_socket.close()
        except socket.error as e:
            print('Error closing udp socket: ' + str(e))

        