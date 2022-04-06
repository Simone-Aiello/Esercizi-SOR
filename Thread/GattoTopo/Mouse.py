#!/usr/bin/python3
from threading import Thread
from random import randrange
from time import sleep
class Mouse(Thread):
    def __init__(self,field,game_lock):
        super().__init__()
        self.alive = True
        self.field = field
        self.game_lock = game_lock
    def __alive(self):
        try:
            self.field.index(".")
            return True
        except ValueError:
            return False
    def run(self):
        while self.alive:
            sleep(randrange(0,3)/3)
            with self.game_lock:
                if self.__alive():
                    possibleMoves = []
                    index = self.field.index(".")
                    possibleMoves.append(index)
                    if index - 1 >= 0:
                        possibleMoves.append(index - 1)
                    if index + 1 < len(self.field):
                        possibleMoves.append(index + 1)
                    #print(f"mosse possibili : {possibleMoves}")
                    rand = randrange(0,len(possibleMoves))
                    chosen = possibleMoves[rand]
                    #print("chosen %d" %(chosen))
                    self.field[index] = "_"
                    if self.field[chosen] == "#":
                        self.alive = False
                    else:
                        self.field[chosen] = "."
                else:
                    self.alive = False
                print("Sono il topo")
                #print(self.field)
