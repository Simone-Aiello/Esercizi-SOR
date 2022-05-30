#!/usr/bin/python3
from socket import socket,AF_INET,SOCK_STREAM,MSG_WAITALL
import re
server_ip = "192.168.0.43"
server_port = 1112

client_socket = socket(AF_INET,SOCK_STREAM)
client_socket.connect((server_ip,server_port))
inp = ""
while inp != "END":
    inp = input("Inserire il comando da eseguire: ")
    client_socket.makefile("w").write(f"{inp}\n")
    res = ""
    while not re.search(".*<EOF>",res):
        res += client_socket.recv(1024).decode()
    print(res)
client_socket.close()