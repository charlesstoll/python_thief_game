"""
Script to send commands to the Raspberry Pi using a socket server

Author: Charles Stoll, Patrick Gmerek
ECE 579
"""

import socket
import sys
import re
from time import sleep


def send(ip_address, turn_amount):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (ip_address, 65432)
    print('Connection to {} port {}'.format(*server_address))
    sock.connect(server_address)

    message = str(turn_amount).encode('ascii')
    print('Sending \"{}\"'.format(message))
    sock.sendall(message)

    data = sock.recv(3)
    print('Received: \"{}\"'.format(data))
    sock.close()


send('127.0.0.1', 'up')
sleep(2)
send('127.0.0.1', 'down')
sleep(2)
send('127.0.0.1', 'left_down')
sleep(2)
send('127.0.0.1', 'left_up')
sleep(2)
send('127.0.0.1', 'right_down')
sleep(2)
send('127.0.0.1', 'right_up')
