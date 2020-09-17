#!/usr/bin/env python3


__author__ = "Jason M. Pittman"
__copyright__ = "Copyright 2020"
__credits__ = ["Jason M. Pittman"]
__license__ = "GPLv3"
__version__ = "0.1.0"
__maintainer__ = "Jason M. Pittman"
__email__ = "jpittman@highpoint.edu"
__status__ = "Development"
__dependecies__ = "pyotp"

import array, time
import base64, hmac, hashlib
import pyotp as otp

# get secret in base32 format
# decode to get bytes

class OtpHandler:
    _secret = 'DefaultSecretKey'
    _length = 15

    def __init__(self, secret=None, length=None):
        """
        Args:
            secret(str): the shared secret to seed one time password generation
            length(int): length of the one time password or number of integers

        Returns:

        """ 
        if secret != None:       
            self._secret = secret
        
        if length != None:
            self._length = length

    def convert_secret_base32(self):
        """Convert the secret to base32

        """
        return base64.b32decode(self._secret)

    def get_one_time_password(self, counter):
        """Generate a one time password
            Args:

            Returns:
        """
        hotp = otp.HOTP(self._secret, self._length, digest=hashlib.sha512) #move to class level and build in constructor?
        
        return hotp.at(counter)


    def verify_one_time_password(self, result, counter):
        """
            Args:

            Returns:
        """
        hotp = otp.HOTP(self._secret, self._length, digest=hashlib.sha512)
        isVerified = hotp.verify(result, counter)

        return isVerified