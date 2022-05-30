#!/usr/bin/python3
from socket import socket, AF_INET, SOCK_DGRAM

address = ("172.25.166.172",6789)

print("Listening...")
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(address)

while True:
    data,addr = serverSocket.recvfrom(2048)
    print(f"L'utente {addr} dice: {data.decode()}")