#!/usr/bin/python3
'''
Il blocco "with self.lock" è equivalente a circondare tutte le istruzioni in esso contenute con self.lock.acquire() e self.lock.release()
Notate che questo costrutto è molto comodo in presenza di return, poichè self.lock.release() verrà eseguita DOPO la return, cosa che normalmente
non sarebbe possibile (return normalmente è l'ultima istruzione di una funzione)
'''
from Cat import Cat
from Mouse import Mouse
from threading import Lock
from Display import Display
class Field:
    def __init__(self):
        self.field = ["#","_","_","_","_","_","_","_","_","_","."]
        self.game_lock = Lock()
        self.mouse = Mouse(field=self.field,game_lock=self.game_lock)
        self.cat = Cat(field=self.field,game_lock=self.game_lock)
        self.display = Display(field=self.field,game_lock=self.game_lock)
    def start(self):
        self.mouse.start()
        self.cat.start()
        self.display.start()

field = Field()
field.start()