# import socket module
from socket import *

#import threading module
from _thread import *

# In order to terminate the program
import sys

# Prepare a sever socket
serverSocket = socket(AF_INET, SOCK_STREAM)
hostname = gethostname()
ip_address = gethostbyname(hostname)
port_number = 59670
serverSocket.bind((ip_address, port_number))
serverSocket.listen(5)
ThreadCount = 0
print(ip_address + ':' + str(port_number))

def multithreading(connection):
    try:
        message = connectionSocket.recv(1024)
        if message:
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = f.read()

            # Send one HTTP header line into socket
            returnmes = 'HTTP/1.1 200 OK\r\n\r\n'.encode()
            connectionSocket.send(returnmes)

            # Send the content of the requested file into socket
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())
        else:
            #Avoid index error
            print("file not found")
        # Close client socket
        connectionSocket.close()
    except IOError:
        # Send response message for file not found
        returnmes = 'HTTP/1.1 404 Not found \r\n\r\n'.encode()
        connectionSocket.send(returnmes)
        # Close client socket
        connectionSocket.close()

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    start_new_thread(multithreading, (connectionSocket, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

    

# Close server socket
serverSocket.close()

# Terminate the program after sending the corresponding data
sys.exit()
