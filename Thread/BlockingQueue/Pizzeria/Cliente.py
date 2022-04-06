#!/usr/bin/python3
from threading import Thread
from time import sleep
from Ordine import Ordine
from random import randrange
class Cliente(Thread):
    def __init__(self,pizzeria):
        super().__init__()
        self.ordineCorrente = None
        self.pizzeria = pizzeria
    def run(self):
        while True:
            sleep(1)
            #Genero un ordine
            q = randrange(1,5)
            self.ordine = Ordine(randrange(1,5),q)
            #Sottometto ordine
            self.pizzeria.putOrdine(self.ordine)
            #Aspetto più o meno il tempo che la mia pizza sia pronta
            sleep(q)
            
            #Prelevo pizza...
        
