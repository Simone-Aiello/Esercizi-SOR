#!/usr/bin/python3
from threading import Thread,RLock
from time import sleep
from random import randrange
class Serpente(Thread):
    def __init__(self, lunghezza: int, carattere : str,verticale: bool, delay: float,testa: tuple, coda: tuple,matrice):
        super().__init__()
        self.lunghezza = lunghezza
        self.carattere = carattere
        self.delay = delay
        self.verticale = verticale
        self.testa = testa
        self.coda = coda
        self.matrice = matrice
    def run(self):
        while True:
            self.matrice.muoviSerpente(self)
            sleep(self.delay)

class MatriceColorata:
    def __init__(self,N : int):
        self.matrix = [[" " for i in range(N)] for i in range(N)]
        self.lock = RLock()
        self.N = N
    def print(self):
        with self.lock:
            print("---------------------------------------------------")
            with self.lock:
                for row in self.matrix:
                    print(row)
    def strisciaLibera(self, verticale: bool, riga: int, colonna: int, lunghezza: int):
        with self.lock:
            if verticale:
                for i in range(lunghezza):
                    if self.matrix[(riga + i) % self.N][colonna] != " ":
                        return False
            else:
                for i in range(lunghezza):
                    if self.matrix[riga][(colonna + i) % self.N] != " ":
                        return False
            return True
    def addSerpente(self, lunghezza: int, carattere : str,verticale: bool, delay: float ) -> int:
        with self.lock:
            if lunghezza > self.N:
                print ("Il serpente non ci entra :(")
                return -1
            index = randrange(0,self.N)
            testa = None
            coda = None
            if verticale:
                for i in range(0,lunghezza):
                    if not self.strisciaLibera(verticale=verticale,riga=0,colonna=index,lunghezza=lunghezza):
                        print("Incrocio di serpenti :(")
                        return -1
                coda = (0,index)
                for i in range(0,lunghezza):
                    if i == lunghezza - 1:
                        carattere = carattere.upper()
                        testa = (i,index)
                    self.matrix[i][index] = carattere
            else:
                if not self.strisciaLibera(verticale=verticale,riga=index,colonna=0,lunghezza=lunghezza):
                    print("Incrocio di serpenti :(")
                    return -1
                coda = (index,0)
                for i in range(0,lunghezza):
                    if i == lunghezza - 1:
                        testa = (index,i)
                        carattere = carattere.upper()
                    self.matrix[index][i] = carattere
            s = Serpente(carattere=carattere.lower(),coda=coda,testa=testa,delay=delay,lunghezza=lunghezza,verticale=verticale,matrice=self)
            s.start()
            #print(f"Index:{index}")
            #print(f"Testa: {testa}")
            #print(f"Coda: {coda}")
    def muoviSerpente(self, serpente : Serpente):
        with self.lock:
            row_testa = serpente.testa[0]
            col_testa = serpente.testa[1]
            row_coda = serpente.coda[0]
            col_coda = serpente.coda[1]
            new_coda = None
            new_testa = None
            if serpente.verticale:
                if self.matrix[(row_testa + 1) % self.N][col_testa] != " ":
                    #print(f"Il serpente orizzontale con testa: {serpente.testa} e coda {serpente.coda} non si muove")
                    #print("Il serpente non si può muovere :(")
                    return
                self.matrix[row_coda][col_coda] = ' '
                #Cancella il serpente precedente
                for i in range(serpente.lunghezza):
                    if i == serpente.lunghezza - 1:
                        self.matrix[(row_coda + i + 1) % self.N][col_coda] = serpente.carattere.upper()
                    else:
                        self.matrix[(row_coda + i + 1) % self.N][col_coda] = serpente.carattere
                new_coda = ((row_coda + 1) % self.N,col_coda)
                new_testa = ((row_testa + 1) % self.N,col_testa)
            else:
                if self.matrix[row_testa][(col_testa + 1) % self.N] != " ":
                    #print(f"Il serpente verticale con testa: {serpente.testa} e coda {serpente.coda} non si muove")
                    #print("Il serpente non si può muovere :(")
                    return
                self.matrix[row_coda][col_coda] = ' '
                #Cancella il serpente precedente
                for i in range(serpente.lunghezza):
                    if i == serpente.lunghezza - 1:
                        self.matrix[row_coda][(col_coda + i + 1) % self.N] = serpente.carattere.upper()
                    else:
                        self.matrix[row_coda][(col_coda + i + 1) % self.N] = serpente.carattere
                new_coda = (row_coda,(col_coda + 1) % self.N)
                new_testa = (row_testa,(col_testa + 1) % self.N)
            
            serpente.coda = new_coda
            serpente.testa = new_testa
            self.print()
            print(serpente.testa,serpente.coda)

class AmmaestratoreDiSerpenti(Thread):
    def __init__(self,N,matrice):
        super().__init__()
        self.N = N
        self.matrice = matrice
        self.caratteri = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    def run(self):
        for i in range(self.N):
            idx = randrange(0,len(self.caratteri))
            self.matrice.addSerpente(randrange(0,self.matrice.N),self.caratteri[idx],True if randrange(0,2) == 1 else False,randrange(3,5)/3)



m = MatriceColorata(20)
AmmaestratoreDiSerpenti(10,m).start()