#!/usr/bin/env python3

"""Asymmetric Cryptographic methods to support secure """

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
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512

class AsymmetricCryptographyHandler:

    def do_keys_exist(self):
        """Checks for existence of server key pair and returns Boolean""" # use keys dir
        exists = False
        secret_key = pathlib.Path('private.pem')
        public_key = pathlib.Path('public.pem')

        if secret_key.exists() and public_key.exists():
            exists = True

        return exists

    def create_keys(self):
        """Creates a 2048 bit RSA key pair and outputs as private.pem and public.pem files""" # drop files in keys dir
        key = RSA.generate(2048)
        secret_key = key.export_key()
        public_key = key.publickey().export_key()

        try:
            with open('private.pem', 'wb') as secret_file:
                secret_file.write(secret_key)
            
            with open('public.pem', 'wb') as public_file:
                public_file.write(public_key)

        except Exception as e:
            print('Error writing key to file: ' + str(e))
        

    def remove_keys(self, keypair): #keypair is a tuple
        """Deletes indicated key pair""" # use keys dir
        secret_key = pathlib.Path('private.pem')
        public_key = pathlib.Path('public.pem')

        pathlib.Path.unlink(secret_key)
        pathlib.Path.unlink(public_key)

    def sign(self, obj, privkey): # sign with private, verify with public
        """ """
        try:
            with open(privkey, 'r') as k:
                key = RSA.importKey(k.read())
        except IOError as e:
            print('Error loading private key: ' + str(e))

        hash = SHA512.new(obj)

        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(hash)

        return signature

    def is_sign_valid(self, obj, signature, pubkey): #this needs reviewed
        """Checks if provided signature is cryptographically valid and returns Boolean"""
        with open('pubkey.pem', 'rb') as f:
            key = RSA.importKey(f.read())
        
        hasher = SHA512.new(obj)
        verifier = PKCS1_v1_5.new(key)
        
        if verifier.verify(hasher, signature):
            return True
        else:
            return False

    def encrypt(self, pubkey, plaintext): #pubkey is a filepath to public key .pem file
        with open(pubkey, "rb") as k:
            key = RSA.importKey(k.read())

        cipher = Cipher_PKCS1_v1_5.new(key)
        return cipher.encrypt(plaintext.encode())


    
    def decrypt(self, privkey, ciphertext):
        with open(privkey, "rb") as k: #privkey is a filepath to private key .pem file
            key = RSA.importKey(k.read())

        decipher = Cipher_PKCS1_v1_5.new(key)
        return decipher.decrypt(ciphertext, None).decode()