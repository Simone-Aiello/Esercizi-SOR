#!/usr/bin/python3
import subprocess
import os
import re
from socket import socket
server_port = 1111
server_socket = socket()
server_socket.bind(('127.0.0.1',server_port))
server_socket.listen(5)
while True:
    print("ASPETTO...")
    connectionSocket, addr = server_socket.accept()
    line = connectionSocket.makefile().readline().strip()
    while line != "END" and line != "":
        if re.search("^ls$",line,re.IGNORECASE):
            output = subprocess.run(["ls"],stdout=subprocess.PIPE,text=True)
            st = f"{output.stdout}<EOF>"
            connectionSocket.send(st.encode())
        elif re.search("^cat .*",line,re.IGNORECASE):
            file = line.split(" ")[1]
            file_output = subprocess.run(["file", file],stdout=subprocess.PIPE)
            if re.search(".*directory.*",file_output.stdout.decode()):
                connectionSocket.send("ERROR<EOF>".encode())
            else:
                with open(file,"r") as f:
                    lines = f.readlines()
                    to_str = "".join(lines)
                    connectionSocket.send(f"{to_str}<EOF>".encode())
        elif re.search("^cd .*",line,re.IGNORECASE):
            folder = line.split(" ")[1]
            try:
                os.chdir(folder)
                connectionSocket.send("PATH CHANGED<EOF>".encode())
            except FileNotFoundError as e:
                connectionSocket.send("PATH NON ESISTENTE<EOF>".encode())
        print("ASPETTO NUOVO COMANDO...")
        line = connectionSocket.makefile().readline().strip()
    connectionSocket.close()

#try:
#    os.chdir("..")
#    output = subprocess.run(["ls"],stdout=subprocess.PIPE)
#    str_out = output.stdout.decode("UTF-8").split("\n")
#    print(str_out)
#    find_output = subprocess.run(["file","RemoteShell"],stdout=subprocess.PIPE)
#    print(find_output)
#except FileNotFoundError as e:
#    print(e.strerror)