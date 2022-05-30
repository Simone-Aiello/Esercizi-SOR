#!/usr/bin/python3
import string
import sys
from socket import AF_INET, SOCK_STREAM, socket

def parse_code(string: str,expected : int):
    split = string.split(" ")
    return int(split[0]) == expected

if len(sys.argv) != 4:
    print("Numero di argv errati")
    exit()

server = sys.argv[1]
mittente = sys.argv[2]
dest = sys.argv[3]

server = server.split(":")
print(server)

client_socket = socket(AF_INET,SOCK_STREAM)

print("Cerco di connettermi al server...")
client_socket.connect((server[0],int(server[1])))

resp = client_socket.makefile().readline()
print("Il server mi saluta :D") if parse_code(resp,220) else print("Il server mi odia D:")
    

print("Cerco di ricambiare il saluto...")
client_socket.makefile("w").writelines("HELO crepes\n")

resp = client_socket.makefile().readline()
print("Il server accetta il mio saluto :D") if parse_code(resp,250) else print("Il server mi odia D:")



print(f"Mando una mail da {mittente}")
client_socket.makefile("w").writelines(f"MAIL FROM: <{mittente}>\n")

resp = client_socket.makefile().readline()
print("Il server accetta sender :D") if parse_code(resp,250) else print("Il server non mi accetta come sender D:")

print(f"Scrivo destinatario {dest}")
client_socket.makefile("w").writelines(f"RCPT TO: <{dest}>\n")

resp = client_socket.makefile().readline()
print("Il server accetta destinatario :D") if parse_code(resp,250) else print("Il server non mi accetta come destinatario D:")

data = input()

print("Richiedo di scrivere corpo mail")
client_socket.makefile("w").writelines("DATA\n")

resp = client_socket.makefile().readline()
print("Il server accetta richiesta corpo mail :D") if parse_code(resp,354) else print("Il server non accetta richiesta corpo mail D:")


print("Scrivo corpo email")
client_socket.makefile("w").writelines(f"{data}\n")

print("Invio fine mail")
client_socket.makefile("w").writelines(".\n")

print("Accetta mail")
resp = client_socket.makefile().readline()
print(resp)

print("Chiudo connessione")
client_socket.makefile("w").writelines("QUIT\n")

print("Il server mi saluta")
resp = client_socket.makefile().readline()
print(resp)