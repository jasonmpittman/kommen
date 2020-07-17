#!/usr/bin/env python3

""" """

__author__ = "Jason M. Pittman"
__copyright__ = "Copyright 2020"
__credits__ = ["Jason M. Pittman"]
__license__ = "GPLv3"
__version__ = "0.1.0"
__maintainer__ = "Jason M. Pittman"
__email__ = "jpittman@highpoint.edu"
__status__ = "Development"

import sys
import configparser

from listeners import tcp_server
from listeners import udp_server

class Kommen:
    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        self.ip_address = config['socket']['ip']
        self.port = config['socket']['port']
        self.max_conn = config['socket']['max_conn']

    def run_tcp(self):
        try:
            svr_tcp = tcp_server.TcpServer(self.ip_address, self.port, self.max_conn)
            tcp_socket = svr_tcp.bind()
            print("TCP Server started...")
            svr_tcp.listen(tcp_socket)
        except:
            print("Error establishing socket in run_tcp method")

    def run_udp(self):
        try:
            svr_udp = udp_server.UdpServer(self.ip_address, self.port)
            svr_udp.bind()
        except:
            print("Error establishing socket in run_udp method")

if __name__ == "__main__":
    kommen = Kommen(sys.argv[1])
    try:
        kommen.run_tcp()
        kommen.run_udp()
    except:
        print("Error creating thread for socket")