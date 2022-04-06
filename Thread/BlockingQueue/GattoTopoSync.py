#!/usr/bin/python3
from random import randrange
from threading import Thread
from time import sleep
from threading import Lock
from queue import Queue
class Cat(Thread):
    def __init__(self,field,game_lock,update_queue):
        super().__init__()
        self.eaten = False
        self.field = field
        self.game_lock = game_lock
        self.direction = 1
        self.update_queue = update_queue
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

class Display(Thread):
    def __init__(self,update_queue):
        super().__init__()
        self.update_queue = update_queue
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

class Mouse(Thread):
    def __init__(self,field,game_lock,update_queue):
        super().__init__()
        self.alive = True
        self.field = field
        self.game_lock = game_lock
        self.update_queue = update_queue
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

class Field:
    def __init__(self):
        self.field = ["#","_","_","_","_","_","_","_","_","_","."]
        self.game_lock = Lock()
        self.update_queue = Queue()
        self.mouse = Mouse(field=self.field,game_lock=self.game_lock,update_queue = self.update_queue)
        self.cat = Cat(field=self.field,game_lock=self.game_lock,update_queue = self.update_queue)
        self.display = Display(update_queue = self.update_queue)
    def start(self):
        self.mouse.start()
        self.cat.start()
        self.display.start()

field = Field()
field.start()