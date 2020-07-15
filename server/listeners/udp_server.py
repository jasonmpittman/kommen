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

class TcpServer:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        