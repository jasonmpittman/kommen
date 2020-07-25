#!/usr/bin/env python3

""" """

__author__ = "Jason M. Pittman"
__copyright__ = "Copyright 2020"
__credits__ = ["Jason M. Pittman"]
__license__ = "GPLv3"
__version__ = "0.3.0"
__maintainer__ = "Jason M. Pittman"
__email__ = "jpittman@highpoint.edu"
__status__ = "Development"

import sys
import socket
#from threading import Thread
#from select import select
import configparser

from listeners import tcp_server
#from listeners import udp_server
from handlers import cryptography_handler as crypto
from handlers import registration_handler as registration

class Kommen:
    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        self.ip_address = config['socket']['ip']
        self.port = config['socket']['port']
        self.max_conn = config['socket']['max_conn']

    def run(self):

        c = crypto.CryptographyHandler()
        if not c.do_keys_exist():
            c.create_keys()

                server = tcp_server.TcpServer(self.ip_address, self.port, self.max_conn)
        server.run_server()

if __name__ == "__main__":
    kommen = Kommen(sys.argv[1])
    try:
        kommen.run()
    except Exception as e:
        print("Error running server: " + str(e))