#!/usr/bin/env python3

""" """

__author__ = "Jason M. Pittman"
__copyright__ = "Copyright 2020"
__credits__ = ["Jason M. Pittman"]
__license__ = "GPLv3"
__version__ = "0.2.0"
__maintainer__ = "Jason M. Pittman"
__email__ = "jpittman@highpoint.edu"
__status__ = "Development"

import sys
import socket
from select import select
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

    def run(self):
        # setup tcp server
        svr_tcp = tcp_server.TcpServer(self.ip_address, self.port, self.max_conn)
        tcp_socket = svr_tcp.bind()
        tcp_socket.listen()

        # setup udp server
        svr_udp = udp_server.UdpServer(self.ip_address, self.port)
        udp_socket = svr_udp.bind()

        sockets = [tcp_socket, udp_socket]

        # select which server to route incoming traffic to based
        while True:
            inputready, outputready, exceptready = select(sockets, [], [])

            for socket in sockets:
                if socket == tcp_socket:
                    svr_tcp.read_tcp(socket)
                elif socket == udp_socket:
                    svr_udp.read_udp(socket)
                else:
                    print("Unknown socket")


if __name__ == "__main__":
    kommen = Kommen(sys.argv[1])
    try:
        kommen.run()
    except:
        print("Error creating thread for socket")