#!/usr/bin/python           # This is server.py file

import socket
import sys

if 1 : 
    for arg in sys.argv:
        print(arg)

# create an INET, STREAMing socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_address = (socket.gethostname(), 12345)

print ('[TCP Server] starting up on %s port %s' % server_address)
# Bind the socket to the port
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print ('[TCP Server] waiting for a connection')
    connection, client_address = sock.accept()
   
    try:
        print ('[TCP Server] connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1400)
            
            if data:
                print('[TCP Server] received "%s"' % data.decode())
                print ('[TCP Server] sending data back to the client')
                connection.sendall(data)
            else:
                print ('[TCP Server] no more data from', client_address)
                break
            
    finally:
        # Clean up the connection
        connection.close()
  
