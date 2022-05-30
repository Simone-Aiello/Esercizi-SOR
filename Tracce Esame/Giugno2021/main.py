#!/usr/bin/python3
from threading import Thread,RLock,Barrier,Condition
from queue import Queue
from time import sleep
from random import random,randint
class Vettura(object):
    def __init__(self):
        self.size = 0
        
    def printSize(self):
        print(self.size)

class Automobile(Vettura):
    def __init__(self):
        super(Automobile, self).__init__()
        self.size = 2

class Autobus(Vettura):
    def __init__(self):
        super(Autobus, self).__init__()
        self.size = 4

# class SorgenteVetture(Thread):
#     vetture = Queue(10)

#     def __init__(self,t):
#         super().__init__()
#         self.traghetto = t
#     #
#     # Questo metodo viene chiamato quando si vuol prendere una Vettura prodotta dalla SorgenteVettura
#     #
#     def getVettura(self):
#         return self.vetture.get()
    
#     def run(self):
#         while self.traghetto.qualcunoAncoraLavora():
#             #sleep(random()*2)
#             # Genera una vettura a intervalli casuali
#             v = Automobile() if randint(0,1) == 0 else Autobus()
#             try:
#                 self.vetture.put(v,timeout=1)
#             except:
#                 pass
#         self.traghetto.b.wait()

class SorgenteVetture(Thread):
    vetture = []
    MAX_SIZE = 10
    def __init__(self,t):
        super().__init__()
        self.traghetto = t
        self.lock = RLock()
        self.condition = Condition(self.lock)
        self.conditionAutomobile = Condition(self.lock)
        self.conditionAutobus = Condition(self.lock)
        self.postiLiberi = True    
        self.producoAutobus = True
    #
    # Questo metodo viene chiamato quando si vuol prendere una Vettura prodotta dalla SorgenteVettura
    #
    # def getVettura(self):
    #     return self.vetture.get()
    
    def ancoraPosto(self):
        with self.lock:
            return self.postiLiberi

    def __svuotaAutobus(self):
        ancoraAutobus = True
        while ancoraAutobus:
            ancoraAutobus = False
            removable = -1
            for idx,v in enumerate(self.vetture):
                if v.size == 4:
                    removable = idx
                    ancoraAutobus = True
                    break
            if removable != -1:
                self.vetture.pop(removable)


    def finePostiAutobus(self):
        with self.lock:
            self.producoAutobus = False
            self.__svuotaAutobus()
            self.conditionAutomobile.notify_all()
            self.condition.notify_all()


    def finePosti(self):
        with self.lock:
            self.postiLiberi = False
            self.producoAutobus = False
            self.condition.notify_all()
            self.conditionAutobus.notify_all()
            self.conditionAutomobile.notify_all()

    def producoAncoraAutobus(self):
        with self.lock:
            return self.producoAutobus

    def putInQueue(self,v):
        with self.lock:
            while len(self.vetture) == SorgenteVetture.MAX_SIZE and self.ancoraPosto():
                self.condition.wait()
            
            if not self.ancoraPosto():
                return False
            if not self.producoAncoraAutobus() and v.size == 4:
                return True
            print(f"Inserisco con size vettura {v.size}")
            self.vetture.append(v)
            self.conditionAutobus.notify_all() if v.size == 4 else self.conditionAutomobile.notify_all()
            return True

    def getAutobus(self):
        with self.lock:
            while (len(self.vetture) == 0 or self.vetture[0].size != 4) and self.producoAncoraAutobus():
                print("Aspetto autobus")
                self.conditionAutobus.wait()
            self.condition.notify_all()
            if not self.producoAncoraAutobus():
                print("AUTOBUS NONE")
                return None
            print("Prendo autobus")
            self.conditionAutomobile.notify_all()
            return self.vetture.pop(0)

    def getAutomobile(self):
        with self.lock:
            while (len(self.vetture) == 0 or self.vetture[0].size != 2) and self.ancoraPosto():
                print("Aspetto automobile")
                self.conditionAutomobile.wait()
            if not self.ancoraPosto():
                return None
            print("Prendo automobile")
            self.condition.notify_all()
            self.conditionAutobus.notify_all()
            return self.vetture.pop(0)

    def run(self):
        produci = True
        while produci:
            #sleep(random()*2)
            # Genera una vettura a intervalli casuali
            v = Automobile() if randint(0,1) == 0 else Autobus()
            produci = self.putInQueue(v)
        self.traghetto.b.wait()

class Striscia(object):
    def __init__(self):
        self.size = 5
        self.l = RLock()
    def put(self, v):
        self.size -= v.size
    def getPostiLiberi(self):
        return self.size
        #
        # Data una vettura v, prova a posizionarla in questa striscia.
        # Restituisce true se operazione avvenuta con successo.
        #
    def provaAInserire(self, v):
        with self.l:
            if self.getPostiLiberi() >= v.size:
                self.put(v)
                return True
            else:
                return False

class ParcheggiaAutobus(Thread):
    def __init__(self, t, id):
        super(ParcheggiaAutobus, self).__init__()
        self.traghetto = t
        self.id = id
        print(f"{self.id} Autobus")
    def run(self):
        possoParcheggiare = True
        while possoParcheggiare:
            v = self.traghetto.sorgente.getAutobus()
            trovato = False
            if v is not None:
                for i in range(6):
                    #
                    # Ogni parcheggiatore ha una sua striscia preferita che dipende da self.id
                    # La striscia preferita viene provata prima di tutte le altre
                    #
                    if self.traghetto.strisce[(i + self.id) % 6].provaAInserire(v):
                        trovato = True
                        print(f"S:{(i+self.id)%6}-{str(self.id)*v.size}")
                        break
            #
            # Un parcheggiatore che non trova posto non parcheggia la vettura corrente
            # e cessa tutte le attività
            #
            if not trovato:
                possoParcheggiare = False
                print("POSTI AUTOBUS FINITI")
                self.traghetto.sorgente.finePostiAutobus()
        print(f"Parcheggiatore {self.id} finisce")
        self.traghetto.b.wait()

class ParcheggiaAutomobili(Thread):
    def __init__(self, t, id):
        super(ParcheggiaAutomobili, self).__init__()
        self.traghetto = t
        self.id = id
        print(f"{self.id} Automobili")
    def run(self):
        possoParcheggiare = True
        while possoParcheggiare:
            print("Rientro in get automobile")
            v = self.traghetto.sorgente.getAutomobile()
            print(v)
            trovato = False
            if v is not None:
                for i in range(6):
                    #
                    # Ogni parcheggiatore ha una sua striscia preferita che dipende da self.id
                    # La striscia preferita viene provata prima di tutte le altre
                    #
                    if self.traghetto.strisce[(i + self.id) % 6].provaAInserire(v):
                        trovato = True
                        print(f"S:{(i+self.id)%6}-{str(self.id)*v.size}")
                        break
            #
            # Un parcheggiatore che non trova posto non parcheggia la vettura corrente
            # e cessa tutte le attività
            #
            if not trovato:
                #Se sono finiti i posti auto sono finiti anche quelli autobus
                possoParcheggiare = False
                self.traghetto.sorgente.finePosti()
                print("FINE POSTI AUTO")
        print(f"Parcheggiatore {self.id} finisce")
        self.traghetto.b.wait()

class Traghetto:
    def __init__(self):
        self.sorgente = SorgenteVetture(self)
        self.b = Barrier(6)
        self.strisce = [Striscia() for _ in range(6)]
        self.parcheggiatoriIniziali = 4
        self.parcheggiatoriAttivi = self.parcheggiatoriIniziali
        self.lock = RLock()
    def caricaTraghetto(self):
        self.sorgente.start()
        for i in range(4):
            if i % 2 == 0:    
                ParcheggiaAutomobili(self, i).start()
            else:
                ParcheggiaAutobus(self,i).start()
        self.b.wait()

    def qualcunoAncoraLavora(self):
        with self.lock:
            return self.parcheggiatoriAttivi > 0

    def parcheggiatoreFinisce(self):
        with self.lock:
            self.parcheggiatoriAttivi -= 1
            print(f"Parcheggiatori attivi {self.parcheggiatoriAttivi}")
            if(self.parcheggiatoriAttivi == 0):
                self.sorgente.tuttiIParcheggiatoriFiniscono()

if __name__ == '__main__':
    siremarOne = Traghetto()
    siremarOne.caricaTraghetto()

