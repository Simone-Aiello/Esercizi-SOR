#!/usr/bin/python3
from multiprocessing.dummy import RLock
from operator import index
from Chair import Chair
from Player import Player
from Display import Display
class Game:
    def __init__(self,playersNumber):
        self.chairs = [Chair(i) for i in range(playersNumber - 1)]
        self.player = [Player(f"Ciao{i}",self.chairs) for i in range(playersNumber)]
    
    def start(self):
        Display(self.chairs).start()
        for p in self.player:
            p.start()

game = Game(200)
game.start()
