#!/usr/bin/python3

class Posacenere:

    def __init__(self,index,pos = -1):
        self.pos = pos
        self.fumatoriAttuali = []
        self.name = index

    def aggiungiFumatore(self,index):
        self.fumatoriAttuali.append(index)
        if len(self.fumatoriAttuali) > 3:
            raise ValueError(f"Troppi fumatori per il posacenere {self.name}")

    def rimuoviFumatore(self,index):
        if index in self.fumatoriAttuali:
            self.fumatoriAttuali.remove(index)
        else:
            raise IndexError(f"Il fumatore {index} non aveva l'accesso al posacenere {self.name}")
    
    def numeroFumatori(self):
        return len(self.fumatoriAttuali)