#_BSD_SOURCE
OPEN_PASSWORD = "open_up"          # /* This password will open the server's ports. Feel free to change it. */
CLOSE_PASSWORD = "close_em"         # /* This password will close the server's ports. */
IPTABLES_PATH = "/usr/sbin/iptables"        #/* The location of the iptables binary */
KEYBYTE = 256            # /* The size of a 1024-bit key */
FILTER_PART1 = "udp src port "         #/* Part one of pcap filter expression */
FILTER_PART2 =" and udp dst port " # /* Part two */
SUCCESS = 0              # /* success */
ERROR = 1              # /* error */
CIPHER = 200           # /* The size of the ciphertext char buffer */
PASS = 100           #  /* The size of character buffer to place our decrypted password into */

import sys
import OpenSSL
import arc4
import socket
import pcapy
#import iptc

#/* Global variables */
#pcap_t *session
#DH *dh = NULL          #/* Diffie-Hellman struct */
#BIGNUM *shared_secret = NULL  #/* DH shared secret */
#cli_src_port        # Client's source port 
#*cli_addr         #/* Client's IP address */
#*server_pub       #/* This will be the server's NULL-terminated public key in hex after a call to BN_bn2hex */
#ciphertext[CIPHER] = "";   #/* The encrypted password */

#Prints usage information
def usage():
    print("Cryptknockd-ng Options:")
    print("-i Interface to watch for clients")
    print("-s Expected source port of incoming UDP packets")
    print("-d Expected destination port of incoming UDP packets")
    print("Example: python3 cryptknockd -i eth0 -s 4500 -d 22796")
    return


# Compares decrypted password to open/close passwords
def compare_pass(supplied_pass):

    # 1 = Bad Password.
    # 2 = Open Ports
    # 3 - Close Ports

    equal = 0

    if (OPEN_PASSWORD == supplied_pass):
        return 2
    elif (CLOSE_PASSWORD == supplied_pass):
        return 3
    else:
        return 1

# Reading in arguments to fill in inputs
def read_options():
    # Prints usage information if program is not initialized properly
    if(len(sys.argv) != 7):
        print("ERROR: Not enough inputs.")
        usage()
    else:
        interface = sys.argv[2] # sys.argv[1] = -i
        source_port = sys.argv[4] # sys.argv[3] = -s
        dest_port = sys.argv[6] # sys.argv[5] = -d

def command_open(cli_addr):
    allow_list = []
    inList = False

    for i in range(0, len(allow_list)):
        if (i == cli_addr):
            inList = True

    if (inList == True):
        print("Client's IP Address is already allowed.")
    else:
        allow_list.append(cli_addr)


read_options()
