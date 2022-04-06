#!/usr/bin/python3
from enum import Flag
from threading import Thread
from time import sleep
from Chair import Chair
class Display(Thread):
    def __init__(self,chairs):
        super().__init__()
        self.chairs = chairs
    
    def run(self):
        flag = True
        while flag:
            flag = False
            for c in self.chairs:
                if c.is_taken():
                    print("*", end = " ",flush=True)
                else:
                    flag = True
                    print("0",end = " ",flush=True)
            print("")
