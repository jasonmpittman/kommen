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

class OtpHandler:
    def __init__(self, secret):
        self.secret = secret
    
    def run_otp_generator():
        otp = []

        return otp