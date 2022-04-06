#!/usr/bin/python3

from threading import Thread,RLock

class Stampa:
    def __init__(self):
        #Il lock permette di far eseguire pezzi di codice in mutua esclusione (1 thread per volta)
        self.lock = RLock()

    def stampa(self, c, l):
        #print(l*c)
        for i in range(0, l+1):
            # flush = True -> visualizza subito a video senza bufferizzare.
            print(c, end = '', flush = True)
        print('')

    def stampaStriscia(self, c):
        self.lock.acquire() # se acquire è libero lo reclamo, altrimenti vado in wait fino a quando non vengo svegliato
        #for i in range(10):
        self.stampa(c, 20)
        self.lock.release() #quando un thread invoca release rilascia il lock e se ci sono thread in wait dell'acquire ne viene selezionato uno A CASO NON IN ORDINE DI ATTESA e il suo stato passo da wait a ready, iniziando a stampare


class StampatoreAsterischi(Thread):
    def __init__(self, s):
        super().__init__()
        self.st = s

    # Metodo run -> main del thread
    def run(self):
        while True:
            self.st.stampaStriscia('*')

class StampatoreTrattini(Thread):
    def __init__(self, s):
        super().__init__()
        self.st = s

    # Metodo run -> main del thread
    def run(self):
        while True:
            self.st.stampaStriscia('-')

st = Stampa()
john = StampatoreAsterischi(st)
al = StampatoreTrattini(st)

# Metodo 'run()' è un metodo single-thread, mentre 'start()' no. 
# Con 'start()' si crea un nuovo flusso di esecuzione parallelo al main.
john.start()
al.start()

# Risultato: entrambi i thread non finiscono di stampare i 50 caratteri consecutivamente a causa del context switch, e al quanto temporale scaduto per ogni thread (john e al).
# Non disciplinando le stampe si va in una race condition.
print('Main terminato')