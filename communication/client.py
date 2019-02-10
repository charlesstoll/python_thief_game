import socket
import sys
import re


def send(ip_address, turn_amount):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (ip_address, 12345)
    print('connection to {} port {}'.format(*server_address))
    sock.connect(server_address)

    try:
        message = str(turn_amount).encode('ascii')
        print('sending {!r}'.format(message))
        sock.sendall(message)

        data = sock.recv(3)
        print('received: ' + str(data))
        sock.close()

    finally:
        print('closing socket')
        sock.close()

#send('127.0.0.1', 60)
#send('127.0.0.1', 40)
#send('127.0.0.1', 120)
