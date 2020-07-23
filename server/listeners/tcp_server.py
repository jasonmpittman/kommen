#!/usr/bin/env python3

"""Establish TCP Server Listener"""

__author__ = "Jason M. Pittman"
__copyright__ = "Copyright 2020"
__credits__ = ["Jason M. Pittman"]
__license__ = "GPLv3"
__version__ = "0.3.0"
__maintainer__ = "Jason M. Pittman"
__email__ = "jpittman@highpoint.edu"
__status__ = "Development"

import asyncio

class TcpServer:

    def __init__(self, ip_address, port, max_conn):
        """Constructor that takes IP Address, port, and maximum client connections as parameters"""
        self.ip_address = ip_address
        self.port = port
        self.max_conn = max_conn

    @asyncio.coroutine
    def handle_echo(self, reader, writer): #This is for testing only...we'll replace this with knock_handler module later
        while True:
            data = yield from reader.read(100)
            if len(data) > 0:
                message = data.decode()
                addr = writer.get_extra_info('peername')
                print("Received %r from %r" % (message, addr))

                print("Send: %r" % message)
                writer.write(data)
                yield from writer.drain()
            else:
                print("Close the client socket")
                writer.close()
                break

    def run_server(self): #add parameter for knock handler
        server_loop = asyncio.get_event_loop()
        routine = asyncio.start_server(self.handle_echo, self.ip_address, int(self.port), loop=server_loop)
        server = server_loop.run_until_complete(routine)

        try:
            server_loop.run_forever()
        except KeyboardInterrupt:
            pass
    
        server.close()
        server_loop.run_until_complete(server.wait_closed())
        server_loop.close()



    # def bind_socket(self):
    #     """Bind a new socket using the IP Address and Port passed to the constructor and returns the socket object"""
    #     try:
    #         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         #sock.setblocking(0)
    #         sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #         sock.bind((self.ip_address, int(self.port)))
    #     except socket.error as e:
    #         print('Exception occured in binding tcp socket: ' + str(e))

    #     return sock

    # def accept_socket(self, tcp_socket):
    #     """Accepts incoming client connection to our listening socket and returns it"""
    #     client_socket, client_socket_info = tcp_socket.accept()

    #     return client_socket

    # def read_socket(self, client_socket):
    #     """Reads from an accepted client connection and returns the received payload"""
    #     try:
    #         payload = client_socket.recv(1024)     
    #         client_socket.send(payload) # this is just for testing convenience
    #     except socket.error as e:
    #         print('Exception occured in reading tcp socket: ' + e)
            
    #     return payload

    # def write_socket(self, client_socket, payload):
    #     """Writes the passed payload to the passed client socket"""
    #     try:
    #         client_socket.send(payload)
    #     except socket.error as e:
    #         print('Error writing to socket: ' + str(e))

    # def close_socket(self, tcp_socket):
    #     """Closes the passed socket object"""
    #     try:
    #         tcp_socket.close()
    #     except socket.error as e:
    #         print('Error occured closing tcp socket: ' + e)