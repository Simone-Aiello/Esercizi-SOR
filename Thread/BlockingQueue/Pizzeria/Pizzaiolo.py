#!/usr/bin/python3
from time import sleep
from random import randrange
from threading import Thread
class Pizzaiolo(Thread):
    def __init__(self,pizzeria):
        super().__init__()
        self.pizzeria = pizzeria
    def run(self):
        while True:
            ordine = self.pizzeria.getOrdine()
            print("Hanno ordinato %d pizze con id %d" %(ordine.q, ordine.idPizza),flush=True)