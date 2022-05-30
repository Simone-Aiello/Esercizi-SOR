#!/usr/bin/python3
from socket import socket

socket_server = socket()
serverPort = 6789
socket_server.bind(('172.25.170.59',serverPort))
socket_server.listen(3)

MIN = 0
MAX = 10

primi = [MIN,MAX]
all_socket = []


for i in range(3):
    connectionSocket, addr = socket_server.accept()
    all_socket.append(connectionSocket)
    connectionSocket.makefile("w").writelines(f"Ciao sei schiavo: {i}\n")

fetta = (MAX - MIN + 1) // len(all_socket)
for idx,skt in enumerate(all_socket):
    minI = MIN + idx * fetta
    maxI = MIN + (idx+1)*fetta - 1
    if idx == len(all_socket) - 1:
        maxI = primi[-1]
    print(minI,maxI)
    skt.makefile("w").writelines(f"{minI} {maxI}\n")

numeri_primi = 0
for skt in all_socket:
    numeri_primi += int(skt.makefile().readline())
    skt.close()
print(numeri_primi)
socket_server.close()