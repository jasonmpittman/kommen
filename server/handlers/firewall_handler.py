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
import subprocess
from subprocess import check_output
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

    def get_rules_in_chain(self, chain): #this looks done?
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

    def are_default_rules_present(self): #do we need this method?
        return 0

    def set_default_rules(self): # tested on 9/7 need error handling and maybe add a full table flush #check on 9/18 and the second rule isn't setting?
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

    def set_user_rules(self, services): #tested on 9/18 need error handling
        """Sets a list of user defined services to accomodate public servers

        Args:
            services (list):
        
        Returns:

        """
        config = configparser.ConfigParser()
        config.read(services)

        for section in config.sections():
            rule = iptc.Rule()
            if config.get(section, 'src') is not '':
                rule.src = config.get(section, 'src')
            if config.get(section, 'dst') is not '':
                rule.dst = config.get(section, 'dst')
            rule.in_interface = config.get(section, 'interface')
            rule.protocol = config.get(section, 'protocol')
            rule.target = rule.create_target(config.get(section, 'target'))
            match = rule.create_match("comment")
            match.comment = "user defined rule"
            match = rule.create_match(config.get(section, 'protocol'))
            match.dport = config.get(section, 'port') 
            chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), config.get(section, 'chain'))
            chain.insert_rule(rule)

    def is_knock_chain_present(self, chain): #tested on 9/22
        """
            Args:
                chain(str): 

            Returns:
                
        """
        output = check_output(["iptables", "-L"])
        
        if chain in str(output):
            return True
        else:
            return False

    def add_knock_chains(self, client, ports):
        """
            Args:
                chain(str): The unique id of the client
                ports(list): The list of knock ports
            
            Returns:

        """
        table = iptc.Table(iptc.Table.FILTER)
        
        #need to flush rules if chain exists and ensure __add runs

        if not self.is_knock_chain_present('STATE0_' + client):
            print('STATE0 chain not present...creating it now')
            STATE0 = table.create_chain('STATE0_' + client)
            self.__add_knock_rules('STATE0', client, ports) #should we flush before adding? we don't want to double rules
        
        if not self.is_knock_chain_present('STATE1_' + client):
            print('STATE1 chain not present...creating it now')
            #STATE1 = table.create_chain('STATE1_' + client)
            subprocess.run(["iptables -N STATE1_" + client], shell=True) #this works whereas iptc didn't
            self.__add_knock_rules('STATE1', client, ports)

        #STATE2 = table.create_chain('STATE2_' + client)
        #self.__add_knock_rules('STATE2', client, ports)

        #STATE3 = table.create_chain('STATE3_' + client)
        #self.__add_knock_rules('STATE3', client, ports)

        # add our knock state chains to the main INPUT chain
        #self.__add_knock_rules('INPUT', client, ports)

    def __build_command(self, client, knock, state, port): #tested 9/22 needs docstring
        """Utility method to build dynamic strings used in knock rules
            
            Args:

            Returns:
        """
        name = "KNOCK" + knock + "_" + client
        state = "STATE" + state + "_" + client
        command = "iptables -A " + state + " -p tcp --dport " + port + " -m recent --name " + name + " --set -j DROP"

        return command


    def __add_knock_rules(self, chain, client, ports):
        """
            Args:
                chain(str): name of chain to be added
                client(str):
                ports(list):

            Returns:
        
        """
        if chain == 'STATE0':
            command = self.__build_command(client, "1", "0", ports[0]) #this works
            subprocess.run([command], shell=True)           
            
            # -A STATE0_CLIENT -j DROP
            subprocess.run(["iptables -A STATE0_" + client + " -j DROP"], shell=True) #this works. do we need another util method?

        elif chain == 'STATE1':
            # -A STATE1_CLIENT -m recent --name KNOCK1_CLIENT --remove
            subprocess.run(["iptables -A STATE1_" + client + " -m recent --name KNOCK1_" + client + " --remove"], shell=True)
            # -A STATE1_CLIENT -p tcp --dport port[1] -m recent --name KNOCK2_CLIENT --set -j DROP
            command = self.__build_command(client, "2", "1", ports[1])
            subprocess.run([command], shell=True)
            # -A STATE1_CLIENT -j STATE0_CLIENT
            subprocess.run(["iptables -A STATE1_" + client + " -j DROP"], shell=True)

        elif chain == 'STATE2':
            print()
            # -A STATE2_CLIENT -m recent --name KNOCK2_CLIENT --remove
            # -A STATE2_CLIENT -p tcp --dport port[2] -m recent --name KNOCK3_CLIENT --set -j DROP
            # -A STATE2_CLIENT -j STATE0_CLIENT

        elif chain == 'STATE3':
            print()
            # -A STATE3_CLIENT -m recent --name KNOCK3_CLIENT --remove
            # -A STATE3_CLIENT -p tcp --dport 22 -j ACCEPT
            # -A STATE3_CLIENT -j STATE0_CLIENT
        elif chain == 'INPUT':
            print()
            # -A INPUT -m recent --name KNOCK3_CLIENT --rcheck -j STATE3_CLIENT
            # -A INPUT -m recent --name KNOCK2_CLIENT --rcheck -j STATE2_CLIENT
            # -A INPUT -m recent --name KNOCK1_CLIENT --rcheck -j STATE1_CLIENT
            # -A INPUT -j STATE0_CLIENT
        else:
            print() #failed to add rules to chain for some reason
        
 
        # match = rule.create_match("comment")
        # match.comment = "knock rule"
        # match = rule.create_match('tcp')
        # match.dport =  
        # knock_chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain)
        # knock_chain.insert_rule(rule)
        
        return 0
    
    def remove_knock_chains(self, client): # tested on 9/18 needs error handling
        """
            Args:
                client(str):

            Returns:

        """
        table = iptc.Table(iptc.Table.FILTER)

        try: #if there's a problem with one, the rest fail to execute... #assume this works for now; build intelligence in v2

            table.delete_chain('STATE0_' + client)
            table.delete_chain('STATE1_' + client)
            table.delete_chain('STATE2_' + client)
            table.delete_chain('STATE3_' + client)
        
        except Exception as e:
            #print(e(str)) # need to implement logging here
            print('error')