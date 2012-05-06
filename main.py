import math
from decimal import *
import threading
from multiprocessing import Process, Queue

# Set precision
getcontext().prec = 2000
n = 2000
totalWorkers = 8 

def factorialGenerator(n):
    num = 0
    while num <= n:
        yield num
        num += 1

globalGenerator = factorialGenerator(n)

globale = Decimal(0)
one = Decimal(1)

class WorkerThread(threading.Thread):
    def __init__(self, threadID):
        self.threadID = threadID
        threading.Thread.__init__(self)
    def run(self):
        worker()


def worker(q2, q):
    mye = Decimal(0)
    one = Decimal(1)
    while not q.empty():
        try:
            x = q.get()
            mye += one / math.factorial(x)
        except Exception as ex:
            print ex
            print 'Worker: ' + str(ex)
            break
    globale = q2.get()
    globale += mye
    q2.put(globale)

#workers = [WorkerThread(i) for i in xrange(5)]

#for i in workers:
    #i.run()

#def workerStatus(workers):
    #for i in workers:
        #if not i.isAlive():
            #return False
    #return True

## Wait for threads to finish
#while workerStatus(workers):
    #pass

q = Queue()
q2 = Queue()
for i in xrange(n + 1):
    q.put(i)

q2.put(globale)
processes = [Process(target=worker, args=(q2, q)) for i in xrange(totalWorkers)]
for i in processes:
    i.start()
for i in processes:
    i.join()
#p = Process(target=worker, args=(q2, q))
#p2 = Process(target=worker, args=(q2, q))
#p.start()
#p2.start()
#p.join()
#p2.join()

#pool = Pool(processes=4)
#result = pool.apply(worker)


globale = q2.get()
print "Suskaiciavau e: "
#print globale
#print "Tikras e: "
#print (Decimal(1).exp())
#print "Taiklumas: "
#print (Decimal(1).exp() - globale)