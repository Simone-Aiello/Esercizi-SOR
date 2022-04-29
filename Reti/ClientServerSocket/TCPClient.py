#!/usr/bin/python3
from socket import *

serverName = "192.168.56.1"
serverPort = 6789

#AF_INET = voglio ipv4 AF_INET6 se volessi ipv6
#SOCK_STREAM indica che voglio TCP, SOCK_USTREAM dice che voglio UDP
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
sentence = input("Frase in minuscolo: ")
clientSocket.makefile("w").writelines(sentence+"\n")
modifiedSentence = clientSocket.makefile().readline()
print(f"FROM SERVER: {modifiedSentence}")