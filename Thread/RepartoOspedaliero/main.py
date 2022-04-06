#!/usr/bin/python3
from threading import Thread, Lock, Condition
from queue import Queue
from time import sleep


buffer_queue = Queue(10)
class Reparto:
    MEDICO = 0
    VISITATORE = 1
    def __init__(self,queue):
        self.queue = queue
        self.lock = Lock()
        self.condition = Condition(self.lock)
        self.stanza = [0,0]
        self.turni_senza_visite_mediche = 0
        self.medici_in_attesa = 0
    def medico_visita_paziente(self):
        with self.lock:
            self.medici_in_attesa += 1
            while self.stanza[Reparto.VISITATORE] > 0 or self.stanza[Reparto.MEDICO] > 0:
                self.condition.wait()
            self.medici_in_attesa -= 1
            self.stanza[Reparto.MEDICO] += 1
            self.queue.put((self.stanza[Reparto.MEDICO],self.stanza[Reparto.VISITATORE]))
            print("Sono un MEDICO ed entro nella stanza per visitare...")
            print(f"Nella stanza ci sono {self.stanza[Reparto.MEDICO]} medici e {self.stanza[Reparto.VISITATORE]} visitatori")

    def medico_finisce_visita(self):
        with self.lock:
            self.stanza[Reparto.MEDICO] -= 1
            self.condition.notify_all()
            print("Sono il MEDICO, finisco la mia visita...")
            self.queue.put((self.stanza[Reparto.MEDICO],self.stanza[Reparto.VISITATORE]))
            print(f"Nella stanza ci sono {self.stanza[Reparto.MEDICO]} medici e {self.stanza[Reparto.VISITATORE]} visitatori")
            self.turni_senza_visite_mediche = 0


    def visitatore_richiede_accesso(self):
        with self.lock:
            while self.stanza[Reparto.VISITATORE] > 4 or self.stanza[Reparto.MEDICO] > 0 or (self.turni_senza_visite_mediche >= 10 and self.medici_in_attesa > 0):
                self.condition.wait()
            self.stanza[Reparto.VISITATORE] += 1
            self.turni_senza_visite_mediche += 1
            self.queue.put((self.stanza[Reparto.MEDICO],self.stanza[Reparto.VISITATORE]))
            print("Sono un VISITATORE e sono andato a trovare fratm")
            print(f"Nella stanza ci sono {self.stanza[Reparto.MEDICO]} medici e {self.stanza[Reparto.VISITATORE]} visitatori")


    def visitatore_esce(self):
        with self.lock:
            self.stanza[Reparto.VISITATORE] -= 1
            self.queue.put((self.stanza[Reparto.MEDICO],self.stanza[Reparto.VISITATORE]))
            self.condition.notify_all()
            print("Sono un VISITATORE fratm sta buanu quindi esco")
            print(f"Nella stanza ci sono {self.stanza[Reparto.MEDICO]} medici e {self.stanza[Reparto.VISITATORE]} visitatori")



class Visitatore(Thread):
    def __init__(self,reparto):
        super().__init__()
        self.reparto = reparto
    
    def run(self):
        self.reparto.visitatore_richiede_accesso()
        sleep(2)
        self.reparto.visitatore_esce()
        
class Medico(Thread):
    def __init__(self,reparto):
        super().__init__()
        self.reparto = reparto
    
    def run(self):
        self.reparto.medico_visita_paziente()
        sleep(2)
        self.reparto.medico_finisce_visita()
        


class Display(Thread):
    def __init__(self,queue : Queue):
        super().__init__()
        self.queue = queue
    def run(self):
        while True:
            tp = self.queue.get()
            for i in range(tp[Reparto.MEDICO]):
                print("O", end= "")
            for i in range(tp[Reparto.VISITATORE]):
                print("*", end= "")
            print("")
if __name__ == "__main__":
    r = Reparto(buffer_queue)
    d =  Display(buffer_queue)
    d.start()
    n_visitatori = 50
    n_medici = 10
    for i in range(n_visitatori):
        t1 =  Visitatore(r)
        t1.start()
        if i < n_medici:
            m = Medico(r)
            m.start()
    

