#!/usr/bin/python3
from Cliente import Cliente
from queue import Queue
from Pizzaiolo import Pizzaiolo
class Pizzeria:
    def __init__(self,pizzaioli,clienti):
        self.clienti = [Cliente(self) for i in range(clienti)]
        self.pizzaioli = [Pizzaiolo(self) for i in range(pizzaioli)]
        self.buffer_ordini = Queue(10)

    def putOrdine(self,ordine):
        self.buffer_ordini.put(ordine)
    
    def getOrdine(self):
        return self.buffer_ordini.get()

    def start(self):
        for c in self.clienti:
            c.start()
        for p in self.pizzaioli:
            p.start()

pizzeria = Pizzeria(3,3)
pizzeria.start()
        