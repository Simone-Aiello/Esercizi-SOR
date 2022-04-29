#!/usr/bin/python3
from threading import Thread,RLock,Condition
from time import sleep


class Item(Thread):
    def __init__(self,item,timeout,queue):
        super().__init__()
        self.item = item
        self.timeout = timeout
        self.timedQ = queue
        self.wait_for_me = Condition(self.timedQ.lock)
        self.extracted = False
        self.timedOut = False
    def run(self):
        sleep(self.timeout)
        index = -1
        with self.timedQ.lock:
            if not self.extracted:
                for i in range(len(self.timedQ.queue)):
                    if self.timedQ.queue[i].item == self.item:
                        index = i
                if index >= 0:
                    print(f"Il numero {self.timedQ.queue[index].item} scade!")
                    self.timedQ.queue.pop(index)
                    self.timedQ.wait_for_space.notify_all()
                    self.timedOut = True
                    self.wait_for_me.notify_all()

class TimedBlockingQueue:

    def __init__(self,N):
        self.N = N
        self.queue = []
        self.lock = RLock()
        self.wait_for_element = Condition(self.lock)
        self.wait_for_space = Condition(self.lock)
    
    def get(self):
        with self.lock:
            while len(self.queue) == 0:
                self.wait_for_element.wait()
            self.wait_for_space.notify_all()
            print(f"Estraggo {self.queue[0].item}")
            obj = self.queue.pop(0)
            obj.extracted = True
            return obj.item
    
    def put(self,item):
        with self.lock:
            while len(self.queue) == self.N:
                self.wait_for_space.wait()
            self.queue.append(Item(item,-1,self))
            self.wait_for_element.notify_all()

    def timedPut(self,e,timeout):
        with self.lock:
            while len(self.queue) == self.N:
                self.wait_for_space.wait()
            i = Item(e,timeout,self)
            self.queue.append(i)
            self.wait_for_element.notify_all()
            i.start()
    
    def waitFor(self,e):
        with self.lock:
            for i in range(len(self.queue)):
                if self.queue[i].item == e:
                    obj = self.queue[i]
                    while not obj.extracted and not obj.timedOut:
                        obj.wait_for_me.wait()
                    if obj.extracted:
                        return 1
                    elif obj.timedOut:
                        return 2
            return 3




class Producer(Thread):
    def __init__(self,queue : TimedBlockingQueue):
        super().__init__()
        self.queue = queue

    def run(self):
        for i in range(100):
            self.queue.timedPut(i,0.6)
            if i % 3 == 0:
                Aspettatore(i,self.queue).start()
        self.queue.put(123456)

class Consumer(Thread):
    def __init__(self,queue : TimedBlockingQueue):
        super().__init__()
        self.queue = queue

    def run(self):
        #sleep(3)
        while True:
            self.queue.get()
            sleep(2)
class Aspettatore(Thread):
    def __init__(self,num,queue : TimedBlockingQueue):
        super().__init__()
        self.num = num
        self.queue = queue
    def run(self):
        with self.queue.lock:
            res = self.queue.waitFor(self.num)
            if(res == 1):
                print(f"Aspettavo il numero {self.num} e lo hanno preso!!!!!!!!!!!")
            elif(res == 2):
                print(f"Aspettavo il numero {self.num} ed è morto D:")
            elif(res == 3):
                print("3")
queue = TimedBlockingQueue(5)
for i in range(10):
    c = Consumer(queue)
    c.start()
Producer(queue).start()