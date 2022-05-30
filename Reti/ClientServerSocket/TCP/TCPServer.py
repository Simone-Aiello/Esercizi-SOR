#!/usr/bin/python3
from socket import socket

serverPort = 6789
welcomeSocket = socket()
 
# La stringa vuota '' vuol dire TUTTE le interfacce di rete, altrimenti si mette l'ip che vogliamo 
welcomeSocket.bind(('172.25.167.218',serverPort))

#Creo buffere delle connessioni
welcomeSocket.listen(5) #Il 5 sono le connessioni che posso bufferizzare (client in parallelo che si possono gestire), la sesta non viene accettata

while True:
    #connection socket è la chiamata con ricevente e dest, addr invece pè ip+porta del client
    connectionSocket, addr = welcomeSocket.accept() #aspetta che qualcuno "chiami", è una get bloccante sul buffer delle chiamate
    print(addr)

    #Generalmente il lavoro viene affidato ad un thread, come facevamo in IGPE

    clientSentence = connectionSocket.makefile().readline()
    capitalizedSentence = clientSentence.upper()
    #time.sleep(1000)
    connectionSocket.makefile("w").writelines(capitalizedSentence+"\n")
    connectionSocket.close()