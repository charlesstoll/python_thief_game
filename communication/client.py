"""
Script to send commands to the Raspberry Pi using a socket server

Author: Charles Stoll, Patrick Gmerek
ECE 579
"""

import socket
import sys
import re
from time import sleep

testing = 1

def send(ip_address, move_direction, move_distance):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (ip_address, 65432)
    print('Connection to {} port {}'.format(*server_address))
    sock.connect(server_address)

    #message = move_direction.encode('ascii') + "," + move_distance.encode('ascii')
    message = "{0},{1}".format(move_direction, move_distance)
    print('Sending \"{}\"'.format(message))
    sock.sendall(message.encode('ascii'))

    data = sock.recv(3)
    print('Received: \"{}\"'.format(data))
    sock.close()

if(testing == 1):
    send('127.0.0.1', '90', '2')
    sleep(2)
    send('127.0.0.1', '80', '1.5')
    sleep(2)
    send('127.0.0.1', '70', '3')
    sleep(2)
    send('127.0.0.1', '60', '2')
