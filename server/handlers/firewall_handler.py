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

        for chain in table.chains:
            print("Chain ", chain.name)

        #return table.chains

    def insert_chain(self, chain):
        table = iptc.Table(iptc.Table.FILTER)

    def add_rule(self, chain, rule):
        return 0
    
    #def remove_chain():


fw = FirewallHandler()
fw.get_chains()