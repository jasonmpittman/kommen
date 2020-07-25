#!/usr/bin/env python3

"""
This module handles client registration and related functions.

Functions:

is_registered() -- check if passed client is already registered  
register_clietn() -- register a new client  
revoke_client_registration() -- remove passed client from client database  
get_registered_clients() -- create a collection of all clients in database  

"""

__author__ = "Jason M. Pittman"
__copyright__ = "Copyright 2020"
__credits__ = ["Jason M. Pittman"]
__license__ = "GPLv3"
__version__ = "0.2.0"
__maintainer__ = "Jason M. Pittman"
__email__ = "jpittman@highpoint.edu"
__status__ = "Development"

'''
Clients are registered *before* they are deployed. Registration involves
(a) generating a unique client id 
(b) generating a unique RSA keypair for the client id
(c) generating a unique knock sequence for the client id
(d) writing the above as a new entry in the clients.db
'''

class RegistrationHandler:

    def __init__(self, crypto, db):
        self.crypto = crypto
        self.db = db

    def is_registered(self, client):
        isRegistered = False

        #logic to validate if client is registered

        return isRegistered

    def register_client(self):
        """Registers a new client"""
        
    def revoke_client_registration(self):
        """Revokes existing clients registration"""
    
    def get_registered_clients(self):
        clients = []

        return clients