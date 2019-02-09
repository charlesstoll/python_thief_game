import socket
import sys
import re

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 12345)
sock.bind(server_address)

sock.listen()
current_dir = 0
while True:
    print('waiting for connection')
    connection, client_address = sock.accept()
    try :
        print('connection from', client_address)

        while True:
            data = connection.recv(20).decode('ascii')
            print('received {!r}'.format(data))
            if data:
                turn_amount = int(data.split()[0])
                current_dir = current_dir + turn_amount
                print("current direction: " + str(current_dir))
                data = b'ack'
                connection.sendall(data)
            else:
                print('no data from', client_address)
                break

    finally:
        connection.close()
