import socket
import sys

# the message
message = 'This is the message.  It will be repeated'
    
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (socket.gethostname(), 12345)
print ('[TCP Client] connecting to %s port %s' % server_address)
sock.connect(server_address)

try:
    
    # Send data       
    print ('[TCP Client] tx : "%s"' % message)
    sock.sendall(message.encode())

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(1400).decode()
        amount_received += len(data)
        print ('[TCP Client] rx : "%s"' % data)

finally:
    
    print('[TCP Client] closing socket')
    sock.close()
    
    if data == message : 
        print("[TCP Client] Echo succeded") 
    else:
        print("[TCP Client] Echo failed!!!")
            
    
