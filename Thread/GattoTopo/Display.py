#!/usr/bin/python3
from operator import imod
from threading import Thread
from time import sleep
from random import randrange
class Display(Thread):
    def __init__(self,field,game_lock):
        super().__init__()
        self.field = field
        self.game_lock = game_lock
        self.keep_printing = True
    def __mouseAlive(self):
        try:
            self.field.index(".")
            return True
        except ValueError:
            return False
    def run(self):
        while self.keep_printing:
            sleep(randrange(0,3)/3)
            with self.game_lock:
                print(self.field)
                if not self.__mouseAlive():
                    self.keep_printing = False