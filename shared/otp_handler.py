#!/usr/bin/env python3

"""
This module implements One Time Password algorithms per RFC 4226 and 6238

Functions:
"""

__author__ = "Jason M. Pittman"
__copyright__ = "Copyright 2020"
__credits__ = ["Jason M. Pittman"]
__license__ = "GPLv3"
__version__ = "0.1.0"
__maintainer__ = "Jason M. Pittman"
__email__ = "jpittman@highpoint.edu"
__status__ = "Development"
__dependecies__ = ""

import array, time
import base64, hmac, hashlib

# get secret in base32 format
# decode to get bytes

class OtpHandler:
    secret = 'DefaultSecretKey'
    length = 6

    def __init__(self, secret=None, length=None):
        """
        Args:
            secret(str): the shared secret to seed one time password generation
            length(int): length of the one time password or number of integers

        Returns:

        """ 
        if secret != None:       
            self.secret = secret
        
        if length != None:
            self.length = length

    
    def convert_secret_to_bytes(self):
        """Decode the base32 secret to byte array

            Args:

            Returns:
                bytes():

        """
        missing_padding = len(self.secret) % 8 #we are picking the secret so do we need to check for padding?
        
        if missing_padding != 0:
            self.secret += '=' * (8 - missing_padding)
        
        return base64.b32decode(self.secret, casefold=True)

    def convert_int_to_bytes(self, i, padding):
        """
            Args:

            Returns:
        """
        converted = bytearray()

        while i != 0:
            converted.append(i & 0xFF)
            i >>= 8

        return bytes(bytearray(reversed(converted)).rjust(padding, b'\0'))

    def get_one_time_password(self):
        """Generate a one time password
            Args:

            Returns:
        """

        h = hmac.new(self.convert_secret_to_bytes(), self.convert_int_to_bytes(), hashlib.sha1)
        hmac_hash = bytearray(h.digest())
        offset = hmac_hash[-1] & 0xf

        otp = ((hmac_hash[offset] & 0x7f) << 24 | (hmac_hash[offset + 1] & 0xff) << 16 | (hmac_hash[offset + 2] & 0xff) << 8 | (hmac_hash[offset + 3] & 0xff))
        str_otp = str(otp % 10 ** self.length)
        
        while len(str_otp) < self.length:
            str_otp = '0' + str_otp

        return str_otp

    def verify_one_time_password(self, otp):
        """
            Args:

            Returns:
        """