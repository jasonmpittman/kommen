""" """

__author__ = "H. Kyle Wiseman"
__copyright__ = "Copyright 2020"
__credits__ = ["H. Kyle Wiseman"]
__license__ = "GPLv3"
__version__ = "0.2.0"
__maintainer__ = "H. Kyle Wiseman"
__email__ = "kwiseman@highpoint.edu"
__status__ = "Development"

import sys
import socket
import getopt

class herein:
    def __init__(self):
        self.dest_addr = sys.argv[1]
        self.dest_port = []
        for i in range(2, len(sys.argv)):
            self.dest_port.append(int(sys.argv[i]))
        self.message = b'0x00'

#        self.protocol = "tcp"

    def make_tcp(self, d_port):
        try:
            packet = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            packet.connect((self.dest_addr, d_port))
            packet.send(self.message)
            print(packet.recv(1024))
            packet.close()
        except:
            print("Failure sending tcp packet.")

#    def make_udp(self):
#        try:
#            packet = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#            packet.connect((self.dest_addr, self.dest_port))
#            packet.send(self.message)
#            print(packet.recv(1024))
#            packet.close()
#        except:
#          print("Failure sending udp packet.")


    def send_packet(self):
#        if (self.protocol == 'tcp'):
        for port in self.dest_port:
            self.make_tcp(port)
   #    elif (self.protocol == 'udp'):
   #         self.make_udp()
    #    else:
    #        print("Error: Protocol undefined")



if __name__ == "__main__":
    try:
        herein().send_packet()
    except:
        print("Error running main.")

