#!/usr/bin/python3
import math
from socket import *
def eprimo(n):
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    for i in range(3,int(math.sqrt(n)+1),2):
        if n % i == 0:
            return False
    return True

serverName = "192.168.0.43"
serverPort = 6789

clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
resp = clientSocket.makefile().readline()
print(resp)

resp = clientSocket.makefile().readline()
split = resp.split(" ")
mn = int(split[0])
mx = int(split[1])
conta_locale = 0
for i in range(mn,mx + 1):
    if eprimo(i):
        print(i)
        conta_locale += 1
print(f"Trovati: {conta_locale}")
clientSocket.makefile("w").writelines(f"{conta_locale}\n")
