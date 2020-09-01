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
from handlers import asym_cryptography_handler as asym_crypto
from handlers import registration_handler as registration
from handlers import firewall_handler as firewall

class Kommen:
    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        self.ip_address = config['socket']['ip']
        self.port = config['socket']['port']
        self.max_conn = config['socket']['max_conn']

    def run(self):

        # crypto testing
        #c = asym_crypto.AsymmetricCryptographyHandler()
        #print(c.do_keys_exist()) # test 1
        
        #if not c.do_keys_exist('ClientA'): # test 2
            #result = c.create_keys('clientA')
        #print(result)

        #keys = ("clientA_public.pem", "clientA_private.pem") # test 3
        #result = c.remove_keys()

        #cipher = c.encrypt("testing", 'ClientA_public.pem') # test 4
        #print(cipher)
        #plain = c.decrypt(cipher, 'ClientA_private.pem') # test 5
        #print(plain)

        #obj = 'test'.encode("utf8")
        #signature = c.sign(obj) # test 6

        #obj2 = 'testing'.encode("utf8")
        #result = c.is_sign_valid(obj2, signature) # test 7
        #print(result)

        # firewall testing

        fw = firewall.FirewallHandler()
        chains = fw.get_chains()
        for chain in chains:
            print(chain)

        #server = tcp_server.TcpServer(self.ip_address, self.port, self.max_conn)
        #server.run_server()

if __name__ == "__main__":
    kommen = Kommen(sys.argv[1])
    try:
        kommen.run()
    except Exception as e:
        print("Error running server: " + str(e))