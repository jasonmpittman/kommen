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

    def get_chains(self): # tested on 8/31 need error handling
        """Queries local IPTables for list of active, non-default chains
        
        Args: 

        Returns:
            chains (list): The return value is the list collection of active, non-default chains
        
        """
        chains = [ ]

        for chain in self._table.chains:
            chains.append(chain.name)

        return chains

    def get_rules_in_chain(self, chain):
        """Queries local IPTables for list of rules in specified chain
        
        Args: 
            chain (str):

        Returns:
            rules (list): The return value is the list collection of rules in specified chain
        
        """
        rules = [ ]

        try:
            for active_chain in self._table.chains:
                if active_chain.name == chain:
                    for rule in active_chain.rules:
                        rules.append(rule.name)
        except Exception as ex:
            print(str(ex)) # add logging
        
        return rules

    def are_default_rules_present(self): #checks for the default rules necessary for port knocking; returns Boolean.
        return 0

    def set_default_rules(self): #sets default rules necessary for port knocking
        #pass knock traffic: iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
        #pass loopback traffic: iptables -A INPUT -s 127.0.0.0/8 -j ACCEPT
        """Sets a list of default rules common to all implementations
        
        Args: 

        Returns:
            is_set (bool): The return value is boolean; True for we set the rules and False for we failed to set the rules.
        
        """
        #get list of active rules in INPUT chain
        rules = self.get_rules_in_chain('INPUT')
        
        if rules[0]:
            is_set = False
        else:
            #set rules
            try:
                print('hi')
                is_set = True
            except Exception as ex:
                print(str(ex)) # need logging here 

        return is_set

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
