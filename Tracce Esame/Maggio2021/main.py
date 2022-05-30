#!/usr/bin/python3
from threading import RLock, Condition, Thread
from time import sleep
from random import random
class Sala:
    def __init__(self, num_piste, num_palle):
        self.lock = RLock()
        self.condition = Condition(self.lock)
        self.num_piste = num_piste
        self.pista = [False] * num_piste
        self.palleDisponibili = num_palle
        self.prossimo_da_servire = 1
        self.bollino = 1
        self.squadre_in_attesa = []
        self.squadre_in_sala = {}

    def registrati(self,squadra):
        with self.lock:
            self.squadre_in_sala[squadra.id] = squadra
    
    # senza starvation
    def richiediPista(self, id_squadra, numGiocatori):
        with self.lock:
            mioBollino = self.bollino
            self.bollino += 1
            while (self.__cercaPistaLibera() == -1 or
                self.palleDisponibili < numGiocatori or
                mioBollino != self.prossimo_da_servire):
                print(f"La squadra {id_squadra} con {numGiocatori} giocatori deve attendere il suo turno con bollino {mioBollino}")
                self.condition.wait()
            # fa scorrere il turno
            self.prossimo_da_servire += 1
            # si da la possibilita' immediata di provare a giocare al prossimo numero da servire
            self.condition.notifyAll()
            self.palleDisponibili -= numGiocatori
            p = self.__cercaPistaLibera()
            self.pista[p] = True
            print(f"La squadra {id_squadra} ottiene la pista {p} con {numGiocatori} giocatori e bollino {mioBollino}")
            return p

    def retrocedi(self,squadra):
        with self.lock:
            index = -1
            for idx,s in enumerate(self.squadre_in_attesa):
                if s == squadra:
                    index = idx
                    break
            # #print("PRIMA DELLA RETROCESSIONEEEEEE")
            # for s in self.squadre_in_attesa:
            #     print(f"Squadra: {s.id} bollino: {s.bollino}")
            nuovoIndice = index + 4
            self.squadre_in_attesa.remove(squadra)
            #SOLO PER DEBUG
            preBollino =  squadra.bollino
            ############
            squadra.bollino = squadra.bollino + 4 + 1 if len(self.squadre_in_attesa) > 4 else squadra.bollino + len(self.squadre_in_attesa) + 1
            #print(f"La squadra con indice {index} retrocede ad indice {nuovoIndice}, pre bollino: {preBollino} post bollino: {squadra.bollino}")
            #print(f"LEEEEEEEEN = {len(self.squadre_in_attesa)}")
            self.squadre_in_attesa.insert(nuovoIndice,squadra) if nuovoIndice < len(self.squadre_in_attesa) else self.squadre_in_attesa.append(squadra)
            #print(f"LEEEEEEEEN2 = {len(self.squadre_in_attesa)}")
            indiceDiPartenza = nuovoIndice + 1
            max_bollino = squadra.bollino
            for i in range(indiceDiPartenza,len(self.squadre_in_attesa)):
                self.squadre_in_attesa[i].bollino += 1
                if(max_bollino < self.squadre_in_attesa[i].bollino):
                    max_bollino = self.squadre_in_attesa[i].bollino
            self.bollino = max_bollino + 1
            self.condition.notify_all()
            self.prossimo_da_servire += 1
            #print("DOPO LA RETROCESSIONEEEEE")
            # for s in self.squadre_in_attesa:
            #     print(f"Squadra: {s.id} bollino: {s.bollino}")

    def richiediPistaGentilmente(self, id_squadra, numGiocatori):
        with self.lock:
            squadra = self.squadre_in_sala[id_squadra]
            squadra.bollino = self.bollino
            #print(f"Bollino assegnato: {squadra.bollino} Da servire: {self.prossimo_da_servire}")
            self.bollino += 1
            self.squadre_in_attesa.append(squadra)
            while (self.__cercaPistaLibera() == -1 or
                self.palleDisponibili < numGiocatori or
                squadra.bollino != self.prossimo_da_servire):
                if((self.__cercaPistaLibera() == -1 or self.palleDisponibili < numGiocatori) and squadra.bollino == self.prossimo_da_servire):
                    self.retrocedi(squadra)
                #print(f"La squadra {id_squadra} con {numGiocatori} giocatori deve attendere il suo turno con bollino {squadra.bollino}")
                self.condition.wait()
            self.squadre_in_attesa.remove(squadra)
            # fa scorrere il turno
            self.prossimo_da_servire += 1
            # si da la possibilita' immediata di provare a giocare al prossimo numero da servire
            self.condition.notifyAll()
            self.palleDisponibili -= numGiocatori
            p = self.__cercaPistaLibera()
            self.pista[p] = True
            #print(f"La squadra {id_squadra} ottiene la pista {p} con {numGiocatori} giocatori e bollino {squadra.bollino}")
            return p

    def liberaPista(self, numPista, numGiocatori):
        with self.lock:
            self.palleDisponibili += numGiocatori
            self.pista[numPista] = False
            self.condition.notifyAll()

    def __cercaPistaLibera(self):
        for i in range(0,len(self.pista)):
            if not self.pista[i]:
                return i
        return -1

class Squadra(Thread):

    def __init__(self, id, sala):
        super(Squadra, self).__init__()
        self.sala = sala
        self.id = id
        self.bollino = -1

    def run(self):
        self.sala.registrati(self)
        while True:
            # il giocatore fa altro prima di chiedere una pista
            sleep(int((random() * 6)))
            # prova a chiedere una pista
            numGiocatori = int((random() * 20))+1
            print(f"La squadra {self.id} chiede una pista per {numGiocatori} giocatori.")
            pista = self.sala.richiediPistaGentilmente(self.id, numGiocatori)
            print(f"La squadra {self.id} gioca sulla pista {pista} .")
            # tempo di gioco
            #sleep(int((random() * 4)))
            self.sala.liberaPista(pista, numGiocatori)
            print(f"La squadra {self.id} lascia la pista {pista}.")
    def __str__(self) -> str:
        return str(self.id)
if __name__ == '__main__':
    s = Sala(3, 20)
    for i in range(0,5):
        Squadra(i, s).start()
