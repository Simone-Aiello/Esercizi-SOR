#!/usr/bin/python3
import random, time, os
from threading import Thread,Condition,RLock, get_ident
from queue import Queue

#
# Una sede sarÃ  formata da tanti Uffici
#
class Ufficio:
    def __init__(self,l):
        Thread.__init__(self)
        self.lock = RLock()
        self.condition = Condition(self.lock)
        self.lettera = l
        self.ticketRilasciati = 0
        self.ticketServiti = 0

    #
    # Fornisce un ticket formattato abbinando correttamente lettera e numero
    #
    def formatTicket(self,lettera,numero):
        return "%s%03d" % (lettera, numero)
    
    #
    # Restituisce quanti ticket in attesa ci sono in questo ufficio
    #
    def getTicketInAttesa(self):
        with self.lock:
            return self.ticketRilasciati - self.ticketServiti

    #
    # Invocato da un utente  quando deve prendere un numerino
    #
    def prendiProssimoTicket(self):
        with self.lock:
            #
            # self.ticketDaRilasciare e self.ticketDaServire stanno per diventare diversi e cioÃ¨ ci sono utenti da smaltire
            #
            if (self.ticketRilasciati <= self.ticketServiti):
                print(self.ticketRilasciati,self.ticketServiti)
                self.condition.notify_all()
            self.ticketRilasciati+=1
            return self.formatTicket(self.lettera, self.ticketRilasciati)

    #
    # Invocato da un impiegato quando deve chiamare la prossima persona
    #
    def chiamaProssimoTicket(self):
        with self.lock:
            #
            # Non ci sono ticket in attesa da elaborare. Attendo
            #
            while(self.ticketRilasciati <= self.ticketServiti):
                self.condition.wait()

            self.ticketServiti+=1
            
            return self.formatTicket(self.lettera, self.ticketServiti)
                
 
class Sede:

    def __init__(self,n):
        self.n = n
        #
        # Gestiremo gli n uffici con un dizionario. Esempio: per selezionare l'ufficio "C" si usa self.uffici["C"]
        #
        self.uffici = {} 
        for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[0:n]:
            self.uffici[l] = Ufficio(l) 
        self.lock = RLock()
        self.condition = Condition(self.lock)
        self.ultimiTicket = []
        self.update = False
        self.setPrintAttese = False
        self.vecchiTicket = []
        self.dimensioneSchermo = 5

    #
    # Preleva ticket da rispettivo ufficio. N.B. si usa il lock del rispettivo ufficio
    #
    def prendiTicket(self,uff):
        return self.uffici[uff].prendiProssimoTicket()

    #
    # Chiama ticket del rispettivo ufficio. N.B. si usa il lock del rispettivo ufficio e poi si aggiorna l'elenco degli ultimi ticket con il lock di SEDE
    #
    def chiamaTicket(self,uff):
        ticket = self.uffici[uff].chiamaProssimoTicket()
        with self.lock:
            self.condition.notifyAll()
            #
            # Questo aggiornamento serve a far capire al display che ci sono novitÃ  da stampare a video
            #
            self.update = True
            if(len(self.ultimiTicket) >= self.dimensioneSchermo):
                rimosso = self.ultimiTicket.pop()
                self.vecchiTicket.append(rimosso)
            self.ultimiTicket.insert(0,ticket)
            

    def waitForTicket(self,ticket):
        with self.lock:
            while(ticket not in self.ultimiTicket):
                self.condition.wait()

    def waitForTicketSafe(self,ticket):
        with self.lock:
            while((ticket not in self.ultimiTicket) and (ticket not in self.vecchiTicket)):
                self.condition.wait()
            return not ticket in self.vecchiTicket
    #
    # Serve a segnalare al display di stampare il riepilogo
    #
    def printAttese(self):
        with self.lock:
            self.setPrintAttese = True
        
    #
    #  Stampa gli ultimi numeri chiamati
    #
    def printUltimi(self):
        with self.lock:
            while not self.update:
                self.condition.wait()
            self.update = False
            #os.system('clear')
            #
            # Se qualcuno lo ha chiesto, stampo l'elenco degli utenti in coda per ogni ufficio
            #
            if (self.setPrintAttese):
                for u in self.uffici:
                    print("%s : %d" % (self.uffici[u].lettera, self.uffici[u].getTicketInAttesa()))
                self.setPrintAttese = False
            for t in self.ultimiTicket:
                print(t)
            print ("="*10)

    def almenoUnoChiamato(self,tickets):
        for t in tickets:
            if t in self.ultimiTicket:
                return True
        return False

    def tuttiScaduti(self,tickets):
        for t in tickets:
            if t not in self.vecchiTicket:
                return False
        return True

    def waitForTickets(self, tickets: list):
        with self.lock:
            while((not self.almenoUnoChiamato(tickets)) and (not self.tuttiScaduti(tickets))):
                self.condition.wait()
            return self.almenoUnoChiamato(tickets)

    def incDecSizeUltimi(self,n: int):
        with self.lock:
            if(n < 0 or -n >= len(self.ultimiTicket)):
                return
            else:
                self.dimensioneSchermo += n
            
class UtenteFurbetto(Thread):
    def __init__(self, sede):
        Thread.__init__(self)
        self.sede = sede
        self.n = len(sede.uffici)

    def run(self):
        while True:
            tickets = []
            for i in range(3):
                ticket = self.sede.prendiTicket(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[0:self.n]))
                tickets.append(ticket)
            print(f"Sono l'utente FURBETTO {get_ident()} e mi faccio un giro prima di mettermi ad aspettare i miei ticket {tickets}")
            time.sleep(random.randint(1,3))
            print(f"Sono l'utente {get_ident()}, ho preso i miei ticket e adesso aspetto: {tickets}") 
            if not self.sede.waitForTickets(tickets):
                print("SONO UN FURBETTO RITARDATARIO E HO PERSO IL MIO TURNO")
            else:
                print(f"Sono l'utente FURBETTO con ticket {ticket} vengo servito")



class Utente(Thread):
    def __init__(self, sede):
        Thread.__init__(self)
        self.sede = sede
        self.n = len(sede.uffici)

    def run(self):
        for i in range(10):
            ticket = self.sede.prendiTicket(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[0:self.n]))
            #print(f"Sono l'utente {get_ident()} e mi faccio un giro prima di mettermi ad aspettare il mio ticket {ticket}")
            time.sleep(random.randint(1,3))
            #print(f"Sono l'utente {get_ident()}, ho preso un caffÃ¨ e adesso aspetto il mio ticket: {ticket}") 
            self.sede.waitForTicket(str(ticket))
            #print(f"Sono l'utente con ticket {ticket} vengo servito")

class UtenteRitardatario(Thread):
    def __init__(self, sede):
        Thread.__init__(self)
        self.sede = sede
        self.n = len(sede.uffici)

    def run(self):
        while True:
            ticket = self.sede.prendiTicket(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[0:self.n]))
            #print(f"Sono l'utente RITARDATARIO {get_ident()} e mi faccio un giro prima di mettermi ad aspettare il mio ticket {ticket}")
            time.sleep(random.randint(10,10))
            #print(f"Sono l'utente {get_ident()}, ho fatto una maratona e adesso aspetto il mio ticket: {ticket}") 
            if not self.sede.waitForTicketSafe(str(ticket)):
                print("SONO UN RITARDATARIO E HO PERSO IL MIO TURNO")
            else:
                print(f"Sono l'utente RITARDATARIOOOOO con ticket {ticket} vengo servito")

class Impiegato(Thread):
    def __init__(self, sede, lettera):
        Thread.__init__(self)
        self.sede = sede
        self.ufficio = lettera
 
    def run(self):
        while True:
            self.sede.chiamaTicket(self.ufficio)
            #
            # Simula un certo tempo in cui l'impiegato serve l'utente appena chiamato
            #
            time.sleep(random.randint(1,4))
            #
            # Notifica di voler stampare il riepilogo attese 
            #
            if random.randint(0,5) >= 4:
                self.sede.printAttese()


class CambiaSize(Thread):
    def __init__(self, sede):
        Thread.__init__(self)
        self.sede = sede
        

    def run(self):
        while True:
            time.sleep(3)
            n = random.randint(-self.sede.dimensioneSchermo,self.sede.dimensioneSchermo)
            self.sede.incDecSizeUltimi(n)


class Display(Thread):
    def __init__(self, sede):
        Thread.__init__(self)
        self.sede = sede
        

    def run(self):
        while True:
            self.sede.printUltimi()
            





sede = Sede(6)

display = Display(sede)
display.start()


utenti = [Utente(sede) for p in range(0)]
impiegato = [Impiegato(sede, i) for i in "ABCDEF"]

ritardatari = [UtenteRitardatario(sede) for p in range(0)]
furbetti = [UtenteFurbetto(sede) for p in range(1)]

CambiaSize(sede).start()

for p in utenti:
    p.start()

for i in impiegato:
    i.start()

for r in ritardatari:
    r.start()

for f in furbetti:
    f.start()