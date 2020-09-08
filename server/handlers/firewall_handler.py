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
import configparser

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

    def set_default_rules(self): # tested on 9/7 need error handling and maybe add a full table flush
        """Sets a list of default rules to allow traffic on our loopback as well as knock traffic
        
        Args: 

        Returns:
            
        
        """
        #get list of active rules in INPUT chain
        #rules = self.get_rules_in_chain('INPUT')
        
        rule_loopback = iptc.Rule()
        rule_loopback.src = "127.0.0.1"
        rule_loopback.target = rule_loopback.create_target("ACCEPT")
        match = rule_loopback.create_match("comment")
        match.comment = "default pk rule to accept loopback traffic"
        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
        chain.insert_rule(rule_loopback)

        rule_knock = iptc.Rule()
        rule_knock.target = rule_knock.create_target("ACCEPT")
        match = rule_knock.create_match("comment")
        match.comment = "default pk rule to accept knock traffic" 
        match = iptc.Match(rule_knock, "state")
        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
        match.state = "RELATED, ESTABLISHED"
        rule_knock.add_match(match)
        chain.insert_rule(rule_knock)

    def set_user_rules(self, services):
        """Sets a list of user defined services to accomodate public servers

        Args:
            services (list):
        
        Returns:

        """
        #print(services)

        config = configparser.ConfigParser()
        config.read(services)

        #print(config.sections())
        for section in config.sections():
            print(section[0])
        #    rule = iptc.Rule()

        #    rule.target = rule.create_target("ACCEPT")
        #    match = rule_knock.create_match("comment")
        #    match.comment = "user defined rule" 
        #    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
        #    chain.insert_rule(rule)


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
