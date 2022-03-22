import imp
from threading import Lock, Condition, Thread
from queue import Queue
from time import sleep
from random import uniform,randrange
class Ponte:
    MARE = "MARE"
    MONTE = "MONTE"
    def __init__(self):
        self.direzione = Ponte.MARE
        self.lock = Lock()
        self.condition = Condition(self.lock)
        self.auto_che_attraversano = 0
        self.auto_in_attesa = {
            Ponte.MARE : 0,
            Ponte.MONTE : 0,
        }
        self.coda_mare = Queue(10)
        self.coda_monte = Queue(10)
        self.capienza_ponte = 10
        self.giri_senza_switch = 0
    def cambia_direzione(self,direzione):
        if direzione != self.direzione:
            self.giri_senza_switch = 0
        self.direzione = direzione

    def voglio_passare(self,direzione):
        with self.lock:
            direzione_opposta = Ponte.MARE if direzione == Ponte.MONTE else Ponte.MONTE
            self.auto_in_attesa[direzione] = self.auto_in_attesa[direzione] + 1
            while direzione != self.direzione and self.auto_che_attraversano != 0 or (direzione == self.direzione and self.auto_in_attesa[direzione_opposta] > 0 and self.giri_senza_switch > 5)\
            or self.auto_che_attraversano >= self.capienza_ponte:
                self.condition.wait()
            self.auto_in_attesa[direzione] = self.auto_in_attesa[direzione] - 1
            self.cambia_direzione(direzione) #la chiamo anche se la direzione è uguale, mi "risparmio" un if
            if self.auto_in_attesa[direzione_opposta] > 0:
                self.giri_senza_switch += 1
            self.auto_che_attraversano += 1

    def finisco_di_attraversare(self):
        with self.lock:
            self.auto_che_attraversano -= 1
            self.condition.notify_all()

class VigileUrbano(Thread):
    def __init__(self,ponte):
        super().__init__()
        self.ponte = ponte
        self.lock = self.ponte.lock
        self.condition = Condition(self.lock)

    def run(self):
        while True:
            with self.lock:
                if self.ponte.direzione == Ponte.MARE:
                    while self.ponte.coda_mare.empty():
                        self.condition.wait()
                else:
                    while self.ponte.coda_mare.empty():
                        self.condition.wait()

class Auto(Thread):
    def __init__(self,index,ponte):
        super().__init__()
        self.index = index
        self.ponte = ponte
        self.direzione = Ponte.MARE if randrange(0,2) == 0 else Ponte.MONTE

    def run(self):
        self.ponte.voglio_passare(self.direzione)
        print(f"Sto andando in gita al {self.direzione} e sono la macchina {self.index} il ponte è in direzione {self.ponte.direzione}")
        sleep(uniform(0.0,2))
        self.ponte.finisco_di_attraversare()
        print(f"Sono l'auto {self.index} e ho attraversato il ponte")

def main_classico():
    p = Ponte()
    for i in range(50):
        a = Auto(ponte=p,index=i)
        a.start()

def main_con_gestione_starvation():
    p = Ponte()
    index = 0
    while index < 100:
        a = Auto(ponte=p,index=index)
        if index >= 10 and index < 25:
            a.direzione = "MONTE"
        else:
            a.direzione = "MARE"
        a.start()
        index += 1

if __name__ == "__main__":
    #main_classico() # -> può esserci starvation
    main_con_gestione_starvation()# -> qui ci sarebbe la starvation 