#!/usr/bin/python3
from random import randrange
from threading import Thread
from time import sleep
class Cat(Thread):
    def __init__(self,field,game_lock):
        super().__init__()
        self.eaten = False
        self.field = field
        self.game_lock = game_lock
        self.direction = 1
    def __notEaten(self):
        try:
            self.field.index(".")
            return True
        except ValueError:
            return False
    def run(self):
        while not self.eaten:
            sleep(randrange(0,3)/3)
            with self.game_lock:
                if self.__notEaten():
                    currentPos = self.field.index("#")
                    nextPos = self.direction + currentPos
                    if nextPos >= 0 and nextPos < len(self.field):
                        self.field[currentPos] = "_"
                        self.field[nextPos] = "#"
                    else:
                        self.direction *= -1
                        nextPos = self.direction + currentPos
                        self.field[currentPos] = "_"
                        self.field[nextPos] = "#"
                    self.eaten = not self.__notEaten()
                else:
                    self.eaten = True
                print("Sono il gatto")
                #print(self.field)
