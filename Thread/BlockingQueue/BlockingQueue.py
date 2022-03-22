from threading import Lock, Condition, Thread
import time
import random
class BlockingQueue:

        def __init__(self,dim):
            self.ins = 0
            self.out = 0
            self.slotPieni = 0
            self.dim = dim
            self.thebuffer = [None] * dim
            self.lock = Lock()
            self.condTuttoPieno = Condition(self.lock)
            self.condTuttoVuoto = Condition(self.lock)

        def show(self):
            
            self.lock.acquire()
            val = [None] * self.dim
            
            for i in range(0,self.slotPieni):
                val[(self.out + i) % len(self.thebuffer)] = '*'
            
            for i in range(0,len(self.thebuffer) - self.slotPieni):
                val[(self.ins + i) % len(self.thebuffer)] = '-'
            
            print("In: %d Out: %d C: %d" % (self.ins,self.out,self.slotPieni))
            print("".join(val))
            self.lock.release()

           

        def put(self,c):
            with self.lock:
                while self.slotPieni == self.dim:
                    self.condTuttoPieno.wait()

                self.thebuffer[self.ins] = c
                self.ins = (self.ins + 1) % self.dim
                self.slotPieni += 1
                self.condTuttoVuoto.notifyAll() #notify all non è sbagliato, semplicemente so che inserisco 1 solo elemento, idem nella get

        
        def get(self):
            with self.lock:
                while self.slotPieni == 0:
                    self.condTuttoVuoto.wait()

                returnValue = self.thebuffer[self.out]
                self.out = (self.out+1) % self.dim
                self.slotPieni -= 1
                self.condTuttoPieno.notify()
                return returnValue


class Consumer(Thread): 
    
    def __init__(self,buffer):
        self.queue = buffer
        Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(random.random()*2)
            self.queue.get()
            self.queue.show()


class Producer(Thread):

    def __init__(self,buffer):
        self.queue = buffer
        Thread.__init__(self)

    def run(self): 
        while True:
            time.sleep(random.random() * 2)
            self.queue.put(self.name)
            self.queue.show()
#
#  Main
#
buffer = BlockingQueue(10)

producers = [Producer(buffer) for x in range(5)]
consumers = [Consumer(buffer) for x in range(3)]

for p in producers:
    p.start()

for c in consumers:
    c.start()

