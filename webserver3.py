# import socket module
from socket import *
import threading
from datetime import datetime
import os
import random
import time

# In order to terminate the program
import sys

def UDP_server():
     # We will need the following module to generate randomized lost packets
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.settimeout(30)

    # Assign IP address and port number to socket
    serverSocket.bind(('149.125.84.120', 8000))


    sequence_number = 0
    packets_lost = 0
    total = 0


    while True:
        # Generate random number in the range of 0 to 10
        rand = random.randint(0, 10)

        try:
            # Receive the client packet along with the address it is coming from
            message, address = serverSocket.recvfrom(1024)
            total += 1

            # If rand is less is than 4, we consider the packet lost and do not respond
            if rand < 4:
                # print('packet lost')
                packets_lost += 1
                continue
            else:
                response = f'echo, {sequence_number}, {time.time()}'
                sequence_number += 1
                serverSocket.sendto(response.encode(), address)
        except timeout:
            if total != 0:
                print(f'packet loss rate: {(packets_lost / total) * 100}%')
            print('Server echo timed out.')
            break

def handle(connectionSocket):
    try:
        message = connectionSocket.recv(28000)
        filename = message.split()[1].decode()
        print(f"server-response,{threading.get_ident()},{datetime.now()}")
        # Check file extension and set content type accordingly
        if filename.endswith(".pdf"):
            content_type = "application/pdf"
        elif filename.endswith(".html"):
            content_type = "text/html"
        else:
            # Unsupported file type
            connectionSocket.send("HTTP/1.1 415 Unsupported Media Type\r\n\r\n".encode())
            connectionSocket.close()
            return

        # Open the requested file
        with open(filename[1:], "rb") as f:
            outputdata = f.read()

        # Send the response header
        response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode()

        # Send the content of the requested file
        connectionSocket.send(response + outputdata)
        
        # Close client socket
        connectionSocket.close()
    except IOError:
        # Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())

        # Close client socket
        connectionSocket.close()
        
def main():
    serverSocket = socket(AF_INET, SOCK_STREAM) 
    host = '149.125.84.120'
    print(host) 
    port = 8080
    serverSocket.bind((host, port))
    serverSocket.listen()

    UDP_thread = threading.Thread(target=UDP_server)
    UDP_thread.start()
    UDP_thread.join()

    while True:
        print("Ready to serve...")

        connectionSocket, addr = serverSocket.accept() 

        thr = threading.Thread(target=handle, args=(connectionSocket,))
        thr.start()

main()