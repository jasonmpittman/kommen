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
    _table = ''

    def __init__(self):
        self._table = iptc.Table(iptc.Table.FILTER)

    def get_chains(self): #just a test method to test interface to iptables

        for chain in self._table.chains:
            print("Chain ", chain.name)


    def are_default_rules_present(self): #checks for the default rules necessary for port knocking; returns Boolean.
        return 0

    def set_default_rules(self): #sets default rules necessary for port knocking
        #block everything
        return 0

    def are_knock_chains_present(self): #checks for our knock chains; only way to do this is to try and create them?
        knock0 = iptc.Chain(self._table, "KNOCK1") #iptc_is_chain
        
        print(knock0.name)
        
        if knock0:
            return True
        else:
            return False

    def insert_chain(self, chain):
        table = iptc.Table(iptc.Table.FILTER)

    def add_rule(self, chain, rule):
        return 0
    
    #def remove_chain():


fw = FirewallHandler()
#fw.get_chains()
boolean = fw.are_knock_chains_present()
print(boolean)