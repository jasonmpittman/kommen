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

    def run(self):
        svr = tcp_server.TcpServer(self.ip_address, self.port, self.max_conn)
        socket = svr.bind()
        svr.listen(socket)

if __name__ == "__main__":
    kommen = Kommen(sys.argv[1])
    kommen.run()