"""
Script to receive commands to the Raspberry Pi using a socket server

Author: Charles Stoll, Patrick Gmerek
ECE 579
"""

import socket
import sys
import re

# Check if python3
if sys.version_info < (3, 0):
    print ("This script requires Python 3. Try executing the following:")
    print ("sudo python3 server.py")
    sys.exit(1)

host = '127.0.0.1'
port = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()

    # In degrees, with the 0 degress pointing straight up
    current_direction = 0 
    print('Waiting for connection...')
    connection, client_address = s.accept()

    with connection:
        print('Connection from ', client_address)
        while True:
            data = connection.recv(20).decode('ascii')
            print('received {!r}'.format(data))
            if data:
                turn_amount = int(data.split()[0])
                #robot moving logic will go

                current_direction = current_direction + turn_amount
                print("current direction: " + str(current_direction))
                # Send acknowledge signal back to client
                data = b'ack'
                connection.sendall(data)
            else:
                print('no data from', client_address)
                break

