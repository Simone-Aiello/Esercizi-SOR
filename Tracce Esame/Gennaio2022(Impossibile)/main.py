#!/usr/bin/python3
from threading import Thread,Lock,Condition,RLock,get_ident
#from sortedcontainers import SortedSet

class IllegalMonitorStateException(Exception):
    pass

'''
#
# Note sull'implementazione
#
#
# Lo shared integer presenta come unica difficoltÃ  di implementazione il fatto che alcuni metodi (inc e setInTheFuture) modificano o leggono DUE sharedInteger
# CONTEMPORANEAMENTE.
#
# Per evitare deadlock e race condition insieme, si usano due classi molto utili:
#
# FriendlyLock: consente di fare acquire in contemporanea con un altro FriendlyLock 'amico', stando automaticamente attento a non creare deadlock
# usando il trucco dell'ordine lessicografico
#
# FriendlyCondition: una normale condition consente di andare in wait rilasciando solo il lock di appartenenza, ma non altri eventuali lock che si possiede;
# le FriendlyCondition consentono di fare wait() liberando tutti insieme un insieme di FriendlyLock. All'uscita della wait, tutti i friendlylock "amici" vengono riacquisiti.
#
# Grazie a FriendlyLock l'implementazione di inc diventa molto semplice, mentre invece FriendlyCondition ci aiuta a realizzare setInTheFuture in cui è necessario 
# attendere che cambi un certo intero per poi modificarne un secondo
#
'''

class FriendlyLock:
#(Lock): non è stato possibile ereditare da Lock poichè non si possono ereditare le classi builtin

    #
    # Contatore statico che vale per tutte le istanze di classe. Usato per disciplinare l'ordine di acquire contemporanee
    #
    internalSerialCounter = 0

    def __init__(self):
        super(FriendlyLock, self).__init__()
        self.taken = False
        self.internalLock = RLock()
        self.internalCondition = Condition(self.internalLock)
        FriendlyLock.internalSerialCounter += 1
        self.serial = FriendlyLock.internalSerialCounter
        self.currentHolder = None
        self.holds = 0

    def acquire(self, l  = None):
        # 
        # 	Se l != None, consente di prendere due FriendlyLock insieme nell'ordine anti-deadlock
        #
        if type(l) == FriendlyLock:
            if self.serial < l.serial:
                self.acquire()
                print("QUA")
                l.acquire()
            else:
                l.acquire()
                self.acquire()        #
        # Non c'è l oppure l è del tipo sbagliato, simula il comportamento di una normale acquire
        #
        else:
            self.internalLock.acquire()
            print(f"{get_ident()} vuole prendere {self}")
            while self.currentHolder != None and self.currentHolder != get_ident():
                    print(f"{get_ident()} vuole prendere {self} OCCUPATO E DORME")
                    self.internalCondition.wait()
            self.currentHolder = get_ident()
            # 
            #  Conta eventuali lock multipli per garantire la rientranza
            #
            self.holds += 1
            self.internalLock.release()
            print(f"{get_ident()} prende {self}")

    # 
    #  se il parametro l è presente, rilascia due lock insieme. Notare che qui l'ordine di rilascio non è importante
    #             
    def release(self, l  = None):
        if type(l) == FriendlyLock:
            self.release()
            l.release()
        else:
            self.internalLock.acquire()
            try:
                if self.currentHolder == get_ident():
                    self.holds -= 1
                    if self.holds == 0:
                        self.currentHolder = None
                        self.internalCondition.notify()
                        print(f"{get_ident()} lascia {self}")
                else:
                    # 
                    #  Non puoi rilasciare un lock che non appartiene al thread corrente (get_ident())
                    # 
                    raise IllegalMonitorStateException()
            finally:
                self.internalLock.release()
    def __lt__(self, other):
        return self.serial < other.serial

#
# Una friendlyCondition puÃ² avere piÃ¹ di un lock collegato, i quali vengono liberati tutti in caso di wait, e ripresi alla fine dell'attesa
#
class FriendlyCondition:
#(Condition): non è stato possibile ereditare da Condition poichè non si possono ereditare le classi builtin

    def __init__(self, l):
        super(FriendlyCondition, self).__init__()
        #
        # Insieme dei lock collegati
        #
        self.joinedLocks = set()
        #
        # Bisogna dichiarare almeno un lock collegati che viene subito messo tra i joinedLock
        #
        self.joinedLocks.add(l)
        #
        # Lock interno usato per disciplinare l'accesso alle variabili interne
        #
        self.internalLock = RLock()
        #
        # Useremo delle condition interne per simulare wait e notify. Ne terremo traccia qui dentro
        #
        self.internalConditions = set()

#
# Aggiunge un lock all'insieme dei collegati
#
    def join(self, l):
        self.internalLock.acquire()
        self.joinedLocks.add(l)
        self.internalLock.release()

#
# Scollega un certo lock che prima era collegato
#
    def unjoin(self, l : FriendlyLock):
        self.internalLock.acquire()
        self.joinedLocks.remove(l)
        self.internalLock.release()

    #
    # Per implementare wait e notify, creo ogni volta una condition usa e getta che verrÃ  usata per fare wait() e buttata alla prima notify().
    # 
    # Tutti i lock amici di questa Friendly condition vengo rilasciati temporaneamente e riacquisiti dopo la wait
    #
    def wait(self):
        self.internalLock.acquire()
        for i in self.joinedLocks:
            i.release()
        myCondition = Condition(self.internalLock)
        self.internalConditions.add(myCondition)
        # 
        #   Qui non uso un while di controllo. Come per le Condition native
        # 	Anchè la FriendlyCondition sarÃ  soggetta agli spurious wake-up.
        #   Gli spurious wake-up andranno gestiti dal programmatore
        #   che usa le FriendlyCondition
        # 
        myCondition.wait()
        #
        # Riprendo tutti i lock collegati che avevo lasciato
        #
        ordered = sorted(list(self.joinedLocks))
        print("Entro for")
        for i in ordered:
            print(f"inizio acquire di {i.serial}")
            i.acquire()
            print(f"finisco acquire di {i.serial}")
        print("Esco")
        self.internalLock.release()

    def notify(self):
        self.internalLock.acquire()
        toDelete = None
        for cond in self.internalConditions:
            # 
            #  Prendo solo la prima condition da notificare (questa non è notifyAll), faccio signal e poi faccio break;
            # 
            cond.notify()
            toDelete = cond
            break
        self.internalConditions.remove(toDelete)
        self.internalLock.release()

#
# In notifyAll devo considerare tutti i thread che potrebbero avere usato wait e sono in attesa. Per ciascuno ci sarÃ  una condition dentro internalCondition.
# Faccio notify su tutte e pulisco il set di internalConditions perchè non mi servono piÃ¹.
#
    def notifyAll(self):
        self.internalLock.acquire()
        print("Mo piango")
        for cond in self.internalConditions:
            cond.notify()
        self.internalConditions = set()
        self.internalLock.release()

    def notify(self):
        self.internalLock.acquire()
        toDelete = None
        for cond in self.internalConditions:
            # 
            #  Prendo solo la prima condition da notificare (questa non è notifyAll), faccio notify, cancello la condition e poi faccio break;
            # 
            cond.notify()
            toDelete = cond
            break
        self.internalConditions.remove(toDelete)
        self.internalLock.release()


#
# La classe Attesa mi serve per implementare gli SharedInteger e in particolare gestire tutti i thread che attendono il superamento di specifiche soglie.
# Ogni attesa corrisponde a una soglia fissata, e corrisponde a una Condition che è quella su cui fare notify per svegliare il thread corrispondente.
#
class Attesa:
    serialCounter = 0

    def __init__(self, i, c):
        #
        # Condition da notificare in futuro a superamento della soglia
        #
        self.c = c
        self.soglia = i
        Attesa.serialCounter += 1
        self.serial = Attesa.serialCounter

    # 
    #  Le attese sono ordinate dal valore piu' basso al piÃ¹ alto. 
    #  A parita' di valore vince l'elemento col seriale piÃ¹ basso.
    # 
    def __lt__(self, other):
        return self.soglia < other.soglia if self.soglia != other.soglia else self.serial < other.serial



class SharedInteger(object):

    def __init__(self):
        self.value = 0
        #
        # Non avendo a disposizione un SortedSet di serie in Python, invocheremo self.attese.sort() alla bisogna.
        # CosÃ¬ facendo self.attese sarÃ  sempre ordinato.
        #
        self.attese = set()
        #
        # Qui sfrutteremo il FriendlyLock implementato sopra
        #
        self.lock = FriendlyLock()

    def sposta_int(self,I2,n):
        print("Entro")
        self.lock.acquire(I2.lock)
        self.value -= n
        I2.value += n
        self.signalWaiters()
        print("Primo signal fatto")
        I2.signalWaiters()
        print("Secondo signal fatto")
        print("MSIDHFJSAIJKHDJKASHDJKHASJKHJk")
        print(self.value)
        print(I2.value)
        print("VOGLIO FARE LA RELEASEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
        self.lock.release(I2.lock)
        print("Esco")
    #
    # Fa notify su tutti gli eventuali thread in attesa di superamento soglia
    #
    def signalWaiters(self):
        for a in self.attese:
            if self.value > a.soglia:
                print("Cerco di svegliare")
                a.c.notifyAll()
                print("Sveglio")
            else:
                # 
                #  Siccome le attese sono ordinate dalla soglia piÃ¹ bassa alla piÃ¹ alta, mi fermo alla prima non superata da value. 
                #  Le soglie successive non saranno sicuramente superate.
                # 
                break

#
# NOTATE CHE il FriendlyLock somiglia a un Lock nativo come interfaccia ma NON implementa il costrutto "with:"
# 
    def get(self):
        self.lock.acquire()
        try:
            return self.value
        finally:
            self.lock.release()
#
# set, inc, oppure inc_int potrebbero far superare delle soglie su cui qualcuno aspetta
#
    def set(self, i):
        self.lock.acquire()
        self.value = i
        self.signalWaiters()
        self.lock.release()

    def inc(self, I):
        self.lock.acquire(I.lock)
        self.value += I.value
        self.signalWaiters()
        self.lock.release(I.lock)

    def inc_int(self, i : int):
        self.lock.acquire()
        self.value += i
        self.signalWaiters()
        self.lock.release()

    def waitForAtLeast(self, soglia):
        self.lock.acquire()
        try:
            cond = FriendlyCondition(self.lock)
            att = Attesa(soglia, cond)
            self.attese.add(att)
            self.attese = set(sorted(list(self.attese)))
            while self.value < soglia:
                cond.wait()
            self.attese.remove(att)
            return self.value
        finally:
            self.lock.release()

    def setInTheFuture(self, I, soglia : int, valore : int):
        #Prendo il lock su di me e su l'altro intero
        self.lock.acquire(I.lock)
        #Creo una condition con il mio lock e anche l'altro
        cond = FriendlyCondition(self.lock)
        cond.join(I.lock)

        #Creo un attesa con la soglia passata e la condizione appena creata
        att = Attesa(soglia, cond)

        # 
        #  Non dimentichiamo che sto aspettando il cambiamendo del valore di I, non di self
        #  Tuttavia non POSSO usare I.waitForAtLeast(soglia) poichè non potrei in contemporanea bloccare il lock su self.
        #
        #  Lo spezzone di codice
        #       I.waitForAtLeast(soglia)
        #       self.set(valore)
        #
        # Contiene una RACE CONDITION che non mi da la garanzia che I sia maggiore di soglia all'atto della self.set(valore)
        # 
        # Il problema si risolve usando un FriendlyLock insieme a una FriendlyCondition
        # 
        I.attese.add(att)
        self.attese = set(sorted(list(self.attese)))
        while I.value < soglia:
            cond.wait()
        I.attese.remove(att)
        self.value = valore
        self.signalWaiters()
        self.lock.release(I.lock)

print("STARTING MAIN")
a = SharedInteger()
b = SharedInteger()
a.set(0)
b.set(9999)

class Thread1(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        print(f"A ora vale: {a.get()}")
        print(f"sono il thread {get_ident()} e imposterÃ² B a 5001 quando A supererÃ  999")
        b.setInTheFuture(a, 999, 5001)
        print(f"A è ora: {a.get()}")
        print(f"B è ora: {b.get()}")

class Thread2(Thread):

		
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        conta = 0
        for i in range(0,500):
            a.inc_int(1);
            print("+", end='')
            conta += 1
            if conta > 50:
                print
                conta = 0
                print(f"\nA vale ora: {a.get()}")

        print(f"Sono il Thread {get_ident()} e ora aspetterÃ² che B sia 5000. In questo momento B è: {b.get()}")
        b.waitForAtLeast(5000)
        print(f"Aspettato B, che adesso vale: {b.get()}")


class Thread3(Thread):

		
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        for i in range(50):
            b.sposta_int(a,30)
        print("FINISCO")

print("STARTING THREADS")
Thread1().start()
#Thread2().start()
#Thread2().start()
Thread3().start()
#Thread3().start()
print("MAIN STARTED")