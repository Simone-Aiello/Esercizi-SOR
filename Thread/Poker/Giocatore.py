#!/usr/bin/python3
from threading import Thread
from time import sleep
from random import randrange
class Giocatore(Thread):
    def __init__(self,index,tavolo):
        super().__init__()
        self.index = index
        self.tavolo = tavolo
        self.posacenereCorrente = None

    def gioca(self):
        print(f"Il giocatore {self.index} gioca...")
        sleep(randrange(0,3) / 3)
        print(f"Il giocatore {self.index} smette di giocare...")

    def run(self):
        while True:
            self.gioca()
            print(f"Il giocatore {self.index} vuole fumare...")
            self.tavolo.fuma(self)
            sleep(randrange(0,3)/3)
            self.tavolo.smettiDiFumare(self)
            print(f"Il giocatore {self.index} smette di fumare...")

class Tavolo:
    
    def __init__(self):
        self.giocatori = [Giocatore(index = i,tavolo = self) for i in range(80)]
        self.posaceneri = [Posacenere(index=i) for i in range(3)]
        self.lock = Lock()
        self.cond = Condition(self.lock)

    def esistePosacenereVicino(self,playerIndex):
        vicinoDx = (playerIndex + 1) % len(self.giocatori)
        vicinoSx = (playerIndex - 1) % len(self.giocatori)
        for p in self.posaceneri:
            if p.pos == vicinoDx or p.pos == vicinoSx:
                return True
        return False

    def esistePosacenereLibero(self):
        for p in self.posaceneri:
            if p.pos == -1:
                return True
        return False
    
    def getPosacenereLibero(self):
        for p in self.posaceneri:
            if p.pos == -1:
                return p
        return None

    def getPosacenereVicino(self,playerIndex):
        vicinoDx = (playerIndex + 1) % len(self.giocatori)
        vicinoSx = (playerIndex - 1) % len(self.giocatori)
        for p in self.posaceneri:
            if p.pos == vicinoDx or p.pos == vicinoSx:
                return p
        return None

    def fuma(self,player):
        with self.lock:
            while not self.esistePosacenereLibero() and not self.esistePosacenereVicino(player.index):
                self.cond.wait()
            if self.esistePosacenereVicino(player.index):
                pv = self.getPosacenereVicino(player.index)
                if pv is None:
                    raise ValueError("pv non può essere None")
                else:
                    #Non prendo il posacenere, mi "accodo" solamente
                    pv.aggiungiFumatore(player.index)
                    player.posacenereCorrente = pv


            elif self.esistePosacenereLibero():
                ps = self.getPosacenereLibero()
                if ps is None:
                    raise ValueError("ps non può essere None")
                else:
                    #Mi prendo il posacenere e inizio a fumare lì
                    ps.pos = player.index
                    ps.aggiungiFumatore(player.index)
                    player.posacenereCorrente = ps
            else:
                pass
    
    def getPlayer(self,playerIndex):
        for g in self.giocatori:
            if g.index == playerIndex:
                return g
        return None

    def smettiDiFumare(self,player):
        with self.lock:
            pc = player.posacenereCorrente
            pc.rimuoviFumatore(player.index)
            player.posacenereCorrente = None
            if pc.numeroFumatori() == 0:
                pc.pos = -1
            elif pc.numeroFumatori() == 1:
                gIndex = pc.fumatoriAttuali[0]
                gRimasto = self.getPlayer(gIndex)
                if gRimasto is None:
                    raise ValueError("Il player rimanente non può essere None")
                pc.pos = gRimasto.index
                gRimasto.posacenereCorrente = pc # Non necessario
            self.cond.notifyAll()

    def start(self):
        for g in self.giocatori:
            g.start()


t = Tavolo()
t.start()