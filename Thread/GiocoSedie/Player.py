#!/usr/bin/python3
from threading import Thread
from random import randrange
from time import sleep

class Player(Thread):
    def __init__(self,name,chairs):
        super().__init__()
        self.name = name
        self.chairs = chairs
        self.starting_index = randrange(2,len(chairs))
    def run(self):
        sleep(randrange(0,3)/3)
        for i in range(self.starting_index,len(self.chairs)):
            print(range(self.starting_index,len(self.chairs)))
            self.chairs[i].sit()
        for i in range(0,self.starting_index):
            self.chairs[i].sit()
        #for c in self.chairs:
            #if c.sit(self.name):
                #return
