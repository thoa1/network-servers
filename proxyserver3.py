# import socket module
from socket import *
import threading

import time

from datetime import datetime

# In order to terminate the program
import sys


ADDR = ('149.125.84.120',8000)

# Prepare a sever socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', 8081))
serverSocket.listen()

cache = {}

def handle(connectionSocket):
    message = connectionSocket.recv(4096)
    response = b""
    _, location, _ = message.decode().splitlines()[0].split()
    now = datetime.now()
    if location in cache and (now-cache[location][0]).total_seconds() <= 120:
        response = cache[location][1]
        print(f"proxy-cache,client,{threading.get_ident()},{now}")
    else:
        # Send one HTTP header line into socket
        serverConnection = socket(AF_INET, SOCK_STREAM)
        serverConnection.settimeout(30)
        serverConnection.connect(ADDR)
        print(f"proxy-forward,server,{threading.get_ident()},{now}")
        serverConnection.settimeout(30)
        serverConnection.send(message)
        response = b""
        
        while more  := serverConnection.recv(28000):
            response += more
        cache[location] = (now, response)
        for location in cache:
            if (now-cache[location][0]).total_seconds() > 120:
                del cache[location]
        # Send the content of the requested file into socket
        print(f"proxy-forward,client,{threading.get_ident()},{now}")
    connectionSocket.send(response)

    # Close client socket
    connectionSocket.close()


def ping():
    server_info = ('149.125.84.120', 8000)

    clientSocket = socket(AF_INET, SOCK_DGRAM)
    

    ping_seq_num = 0
    success = 0

    rtts = []

    start = time.time()
    while time.time() - start < 180:
        clientSocket.settimeout(30)

        message = f'ping {ping_seq_num}, {time.time()}'
        clientSocket.sendto(message.encode(), server_info)
        print(f'Message sent: {message}')
        ping_seq_num += 1

        sent = time.time()

        try:

            response, server = clientSocket.recvfrom(1024)
            success += 1

            received = time.time()

            rtt = received - sent
            rtts.append(rtt)

            print(f'Response: {response.decode()}')
            print(f'RTT (Rount Trip Time): {rtt}')
            


        except timeout:
            print('Client ping timed out')
        time.sleep(3)

    print('-'*30)
    print('Stats:')
    print()

    print(f'minimum RTT: {min(rtts)}s')
    print(f'maximum RTT: {max(rtts)}s')
    print(f'successful RTTs: {success}')
    sum = 0 
    for rtt in rtts:
        sum += rtt
    print(f'average RTT: {sum / len(rtts)}s')

    

def main():
    ping_thread = threading.Thread(target=ping)
    ping_thread.start()

    while True:
        # Establish the connection
        
        connectionSocket, addr = serverSocket.accept()

        t = threading.Thread(target=handle,args=(connectionSocket,),daemon=True)
        t.start()

        # Close server socket
    serverSocket.close()

       

main()