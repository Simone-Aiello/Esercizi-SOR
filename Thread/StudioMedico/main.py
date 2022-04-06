from curses import def_prog_mode
from threading import Lock,Condition,Thread
from queue import Queue
from random import randrange
from time import sleep
class Sala:
    def __init__(self):
        self.attesa_visita = Queue(10)
        self.attesa_ricetta = Queue(10)
        self.attesa_ricetta_visita = Queue(10)
        self.lock = Lock()
        self.code_ricette_vuote = Condition(self.lock)

    def inserisci_in_visita(self,paziente):
        self.attesa_visita.put(paziente)
    
    def inserisci_in_solo_ricetta(self,paziente):
        print("Solo ricetta")
        self.attesa_ricetta.put(paziente)
        with self.lock:
            self.code_ricette_vuote.notify()
    
    def inserisci_in_ricetta_visita(self,paziente):
        self.attesa_ricetta_visita.put(paziente)
        with self.lock:
            self.code_ricette_vuote.notify()

    def visitaProssimo(self):
        return self.attesa_visita.get()

    def necessita_ricetta(self,paziente):
        self.attesa_ricetta_visita.put(paziente)

    def prossima_ricetta(self):
        with self.lock:
            while self.attesa_ricetta.empty() and self.attesa_ricetta_visita.empty():
                self.code_ricette_vuote.wait()
            if not self.attesa_ricetta_visita.empty():
                return self.attesa_ricetta_visita.get()
            else:
                return self.attesa_ricetta.get()
class Paziente(Thread):
    def __init__(self,sala,id):
        super().__init__()
        self.lock = Lock()
        self.id = id
        self.condition = Condition(self.lock)
        self.mi_serve_ricetta = None
        self.sala = sala
        self.ricetta = None
    
    def assegna_ricetta(self,ricetta):
        with self.lock:
            self.ricetta = ricetta
    
    def run(self):
        r = randrange(0,2)
        if r == 0: #mi serve la visita
            self.sala.inserisci_in_visita(self)
            with self.lock:
                while self.mi_serve_ricetta is None: #fino a quando non so se mi serve una ricetta o no vuol dire che non sono ancora stato visitato
                    self.condition.wait()
                if self.mi_serve_ricetta:
                    self.sala.inserisci_in_ricetta_visita(self)
                    while self.ricetta is None:
                        self.condition.wait()
                    print(f"Sono il paziente {self.id} esco con una ricetta dopo una visita")
                else:
                    print(f"Sono il paziente {self.id} ed esco senza una ricetta perché sto bene")        
        else: #mi serve solo la ricetta
            self.sala.inserisci_in_solo_ricetta(self)
            with self.lock:
                while self.ricetta is None:
                    self.condition.wait()
                print(f"Sono il paziente {self.id} esco con una ricetta")
            

class Medico(Thread):
    def __init__(self,sala):
        super().__init__()
        self.sala = sala

    def run(self):
        while True:
            paziente = self.sala.visitaProssimo()
            sleep(1)
            r = randrange(0,2)
            if r == 0:
                paziente.mi_serve_ricetta = False
            else:
                paziente.mi_serve_ricetta = True
            with paziente.lock:
                paziente.condition.notify()
                
class Segretaria(Thread):
    def __init__(self,sala):
        super().__init__()
        self.sala = sala

    def run(self):
        while True:
            paziente = sala.prossima_ricetta()
            sleep(1)
            paziente.ricetta = 3 #Non ho voglia di fare l'oggetto ricetta
            with paziente.lock:
                paziente.condition.notify()
if __name__ == "__main__":
    sala = Sala()
    medico = Medico(sala)
    seg = Segretaria(sala)
    seg.start()
    medico.start()
    for i in range(100):
        p = Paziente(sala,i)
        p.start()
