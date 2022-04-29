#!/usr/bin/python3
from threading import Thread

class Proc(Thread):
    def __init__(self):
        super().__init__()
        self.i = 0
    def run(self):
        while True:
            self.i += 1


p1 = Proc()
p2 = Proc()
p1.start()
p2.start()