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
__dependecies__ = "Python-IPtables"

import iptc

class FirewallHandler():

    def get_chains(self):
        table = iptc.Table(iptc.Table.FILTER)
    
        return table

    #def insert_chain():

    
    #def remove_chain():