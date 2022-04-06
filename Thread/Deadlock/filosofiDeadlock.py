#!usr/bin/python3
from threading import Lock, Thread, Condition
from time import sleep
from random import randrange
from turtle import pos

class Bacchetta:

    def __init__(self):
        #self.lock = Lock()
        self.occupata = False

    def lasciaBacchetta(self):
        #self.lock.release()
        self.occupata = False
    
    def prendiBacchetta(self):
        #self.lock.acquire()
        self.occupata = True
    
    def checkOccupata(self):
        return self.occupata

class Tavolo:
    def __init__(self):
        self.bacchetta = [Bacchetta() for _ in range(5)]
        self.lock = Lock()
        self.cond = Condition(self.lock)
    
    def prendiLockSimultaneo(self,posizione):
        with self.lock:
            while(self.bacchetta[posizione].checkOccupata() or self.bacchetta[(posizione + 1) % 5].checkOccupata()):
                self.cond.wait()
            self.bacchetta[posizione].prendiBacchetta()
            self.bacchetta[(posizione + 1) % 5].prendiBacchetta()
    
    def prendiLockSimultaneo(self,posizione):
        with self.lock:
            self.bacchetta[posizione].prendiBacchetta()
            self.bacchetta[(posizione + 1) % 5].prendiBacchetta()
            self.cond.notifyAll()

class Filosofo(Thread):
    
    def __init__(self,tavolo,pos):
        super().__init__()
        self.posizione = pos
        self.t = tavolo
        self.name = f"Philip {pos}"

    def attesaCasuale(self,msec):
        sleep(randrange(msec)/1000.0)

    def mangia(self):
        #print(f"Il filosofo {self.getName()} vuole mangiare")
        
        #self.t.bacchetta[self.posizione].prendiBacchetta()
        
        #print(f"Il filosofo {self.getName()} prende prima bacchetta")

        #self.t.bacchetta[(self.posizione + 1) % 5].prendiBacchetta()
        #print(f"Il filosofo {self.getName()} prende seconda bacchetta e comincia a mangiare.")
        
        #
        # Attende per un tempo casuale che simula il tempo di elaborazione passato a mangiare
        #
        #self.attesaCasuale(1000)
        
        #print(f"Il filosofo {self.getName()}  termina di mangiare.")
        
        #self.t.bacchetta[self.posizione].lasciaBacchetta()
        #print(f"Il filosofo {self.getName()}  lascia prima bacchetta.")
        
        #self.t.bacchetta[(self.posizione + 1) % 5].lasciaBacchetta()
        #print(f"Il filosofo {self.getName()} lascia seconda bacchetta.")

        self.t.prendiLockSimultaneo(self.posizione)

    def pensa(self):
        print(f"Il filosofo {self.getName()} pensa.")
        
        #
        # Attende per un tempo casuale che simula il tempo di elaborazione passato a pensare
        #
        #self.attesaCasuale(1000)
        
        print(f"Il filosofo {self.getName()} smette di pensare.")

    def run(self):
        while True:
            self.pensa()
            self.mangia()

tavolo = Tavolo()
filosofi = [Filosofo(tavolo,i) for i in range(5)]
for f in filosofi:
    f.start()