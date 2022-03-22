#!/usr/bin/python3
from random import randrange
from threading import RLock, Condition, Thread
from typing import final

class Transazione:
    def __init__(self,sorgente,destinazione,ammontare):
        self.sorgente = sorgente
        self.destinazione = destinazione
        self.ammontare = ammontare

class Conto:
    
    def __init__(self):
        self.lock = RLock()
        self.saldo = randrange(1000,10000)
        self.lista_movimenti = []
    
    def getSaldo(self):
        return self.saldo

class Banca:

    def __init__(self):
        self.conti = {key:Conto() for key in range(1000000)}


    def effettuaTransazione(self,transazione : Transazione):
        sor = self.conti[transazione.sorgente]
        des = self.conti[transazione.destinazione]
        try:
            if transazione.sorgente < transazione.destinazione:
                sor.lock.acquire()
                des.lock.acquire()
                if sor.getSaldo() < transazione.ammontare:
                    return False 
                sor.saldo -= transazione.ammontare
                des.saldo += transazione.ammontare
            else:
                des.lock.acquire() 
                sor.lock.acquire()
                if sor.getSaldo() < transazione.ammontare:
                    return False 
                sor.saldo -= transazione.ammontare
                des.saldo += transazione.ammontare
            sor.lista_movimenti.append(transazione)
            des.lista_movimenti.append(transazione)
            return True
        finally:
            des.lock.release()
            sor.lock.release()


#Manca il main con il thread cliente ma il resto è giusto

    


    