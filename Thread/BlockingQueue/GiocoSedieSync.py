#!/usr/bin/python3
from threading import Thread
from random import randrange
from time import sleep
from threading import RLock
from queue import Queue

p_num = 10
bufferQueue = Queue(p_num)

class Chair:
    
    def __init__(self,index):
        self.index = index
        self.occupied = False
        self.lock = RLock()

    def sit(self,thread_name):
        with self.lock:
            if not self.occupied:
                self.occupied = True
                bufferQueue.put((self.index,thread_name))
                return True
            else:
                return False
            
    def is_taken(self):
        return self.occupied

class Player(Thread):
    def __init__(self,name,chairs):
        super().__init__()
        self.name = name
        self.chairs = chairs
        self.starting_index = randrange(2,len(chairs))
    def run(self):
        sleep(randrange(0,3)/3)
        for i in range(self.starting_index,len(self.chairs)):
            if self.chairs[i].sit(self.name):
                return
        for i in range(0,self.starting_index):
            if self.chairs[i].sit(self.name):
                return

class Display(Thread):
    def __init__(self,chairs):
        super().__init__()
        self.chairs = chairs
        self.updates = ["*"] * len(chairs)
    def run(self):
        while True:
            if "*" not in self.updates:
                return
            new_update = bufferQueue.get()
            self.updates[new_update[0]] = new_update[1]
            print(self.updates)

class Game:
    def __init__(self,playersNumber):
        self.chairs = [Chair(i) for i in range(playersNumber - 1)]
        self.player = [Player(f"Ciao{i}",self.chairs) for i in range(playersNumber)]
    
    def start(self):
        Display(self.chairs).start()
        for p in self.player:
            p.start()

game = Game(p_num)
game.start()
