#!/usr/bin/env python3

"""Cryptographic methods to support secure """

__author__ = "Jason M. Pittman"
__copyright__ = "Copyright 2020"
__credits__ = ["Jason M. Pittman"]
__license__ = "GPLv3"
__version__ = "0.2.0"
__maintainer__ = "Jason M. Pittman"
__email__ = "jpittman@highpoint.edu"
__status__ = "Development"
__dependecies__ = "PyCryptodome"

import pathlib
from Crypto.PublicKey import RSA

class CryptographyHandler:

    def do_keys_exist(self):
        exists = False
        secret_key = pathlib.Path('secret.pem')
        public_key = pathlib.Path('public.pem')

        if secret_key.exists() and public_key.exists():
            exists = True

        return exists

    def create_keys(self):
        key = RSA.generate(2048)
        secret_key = key.export_key()
        public_key = key.publickey().export_key()

        try:
            with open('secret.pem', 'wb') as secret_file:
                secret_file.write(secret_key)
            
            with open('public.pem', 'wb') as public_file:
                public_file.write(public_key)

        except Exception as e:
            print('Error writing key to file: ' + str(e))
        

    def remove_keys(self):
        secret_key = pathlib.Path('secret.pem')
        public_key = pathlib.Path('public.pem')

        pathlib.Path.unlink(secret_key)
        pathlib.Path.unlink(public_key)

    def sign_key(self, key):
        keys = []

        return keys

    def is_valid_key(self, key):
        is_valid = False

        return is_valid