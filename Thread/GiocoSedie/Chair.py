#!/usr/bin/python3
from threading import RLock
from time import sleep
class Chair:
    
    def __init__(self,index):
        self.index = index
        self.occupied = False
        self.lock = RLock()

    def sit(self):
        with self.lock:
            if not self.occupied:
                self.occupied = True
                return True
            else:
                return False
            
    def is_taken(self):
        return self.occupied