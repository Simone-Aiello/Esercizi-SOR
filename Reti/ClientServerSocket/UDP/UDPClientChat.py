#!/usr/bin/python3
from socket import socket, AF_INET, SOCK_DGRAM

server_address = ("172.25.166.172",6789)
clientSocket = socket(AF_INET, SOCK_DGRAM)

sentence = ""
while sentence != "EXIT":
    sentence = input("Inserire il messaggio che vuoi inviare: ")
    clientSocket.sendto(sentence.encode('utf-8'), server_address)

