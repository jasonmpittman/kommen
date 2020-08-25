#!/usr/bin/env python3

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
    """

    Asymmetric Cryptographic methods to handle keys and cryptograhic operations
    
    Attributes:

    Functions:
        do_keys_exist() -- check if a key pair exists 
        create_keys() -- create a new RSA key pair in local keystore
        remove_keys() -- remove keys from local keystore
        sign() -- use private key to sign an object (generate checksum)
        is_sign_valid() -- check if provided signature is cryprographically valid
        encrypt() -- encrypt object using a public key
        decrypt() -- decrypto object using a private key

    """

    def do_keys_exist(self, keypair=None): # Finished and tested 8/25
        """Checks for existence of key pair 
        
        Args:
            keypair (None): default value which causes a check for the server key pair
            keypair (tuple): passed value which causes a check for the indicated client key pair 

        Returns:
            exists (bool): True if exists, False otherwise
        
        """

        exists = False
        
        if keypair is not None: 
            secret_key = pathlib.Path(r'keys/' + keypair[0])
            public_key = pathlib.Path(r'keys/' + keypair[1])
        else:
            secret_key = pathlib.Path(r'keys/secret.pem')
            public_key = pathlib.Path(r'keys/public.pem')

        if secret_key.exists() and public_key.exists():
            exists = True

        return exists

    def create_keys(self, client=None): # Finished and tested 8/25
        """Creates a 2048 bit RSA key pair and outputs as private.pem and public.pem files
        
        Args:
            client (None): default value which is handled as the server
            client (str): passed value which is used as unique client identifier (maybe later we use index from keys.db)

        Returns:
            is_created (bool): True for success, False otherwise.
        
        """ 
        is_created = False
        key = RSA.generate(2048)
        secret_key = key.export_key()
        public_key = key.publickey().export_key()

        try:
            if client is not None:
                with open(pathlib.Path(r'keys/' + client + '_private.pem'), 'wb') as secret_file:
                    secret_file.write(secret_key)
            
                with open(pathlib.Path(r'keys/' + client +  '_public.pem'), 'wb') as public_file:
                    public_file.write(public_key)
            else:
                with open(pathlib.Path(r'keys/' 'private.pem'), 'wb') as secret_file:
                    secret_file.write(secret_key)
            
                with open(pathlib.Path(r'keys/' 'public.pem'), 'wb') as public_file:
                    public_file.write(public_key)
        except Exception as e:
            print('Error writing key to file: ' + str(e)) #add logging
        else:
            is_created = True

        return is_created
        

    def remove_keys(self, keypair): #keypair is a tuple
        """Deletes indicated key pair
        
        Args:
            keypair (tuple): 

        Returns:
            is_removed (bool): The return value. True for success, False otherwise.
        
        """ # use keys dir
        secret_key = pathlib.Path('private.pem')
        public_key = pathlib.Path('public.pem')

        pathlib.Path.unlink(secret_key)
        pathlib.Path.unlink(public_key)

    def sign(self, obj, privkey): # sign with private, verify with public
        """Creates cryptographic signature (checksum) of indicated object.
        
        Args:
            obj: Object to be signed.
            privkey: The private key to be used in generating the signature.

        Returns:
            is_signed (bool): The return value. True for success, False otherwise.
        
        """ 
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
        """Checks if provided signature is cryptographically valid and returns Boolean
        
        Args:
            obj: any object previously signed and to be validated
            signature (str): the signature string to be validated
            pubkey (str): a filepath to the public key .pem to be used in validating a signature

        Returns:
            is_valid (bool): True for valid, False otherwise.
        
        """
        with open('pubkey.pem', 'rb') as f:
            key = RSA.importKey(f.read())
        
        hasher = SHA512.new(obj)
        verifier = PKCS1_v1_5.new(key)
        
        if verifier.verify(hasher, signature):
            return True
        else:
            return False

    def encrypt(self, pubkey, plaintext):
        """Encrypts provided plaintext and returns ciphertext
        
        Args:
            pubkey (str): a filepath to a public key .pem file
            plaintext (str): the plaintext to be encrypted

        Returns:
            cipher.encrypt(): encrypted plaintext
        
        """
        
        with open(pubkey, "rb") as k:
            key = RSA.importKey(k.read())

        cipher = Cipher_PKCS1_v1_5.new(key)
        return cipher.encrypt(plaintext.encode())
    
    def decrypt(self, privkey, ciphertext):
        """Decrypts provided ciphertext and returns plaintext
        
        Args:
            privkey (str): a filepath to a secret key .pem file
            ciphertext (str): the ciphertext to be decrypted

        Returns:
            decipher.decrypt(): decrypted ciphertext
        
        """
        with open(privkey, "rb") as k: #privkey is a filepath to private key .pem file
            key = RSA.importKey(k.read())

        decipher = Cipher_PKCS1_v1_5.new(key)
        return decipher.decrypt(ciphertext, None).decode()