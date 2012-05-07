import math
from decimal import *
from multiprocessing import Process, Queue

# Set precision
getcontext().prec = 10000
n = 4000
totalWorkers = 8

def factorialGenerator(n):
    num = 0
    while num <= n:
        yield num
        num += 1

globalGenerator = factorialGenerator(n)

globale = Decimal(0)
one = Decimal(1)


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

q = Queue()
q2 = Queue()
for i in xrange(n + 1):
    q.put(i)

q2.put(globale)
processes = [Process(target=worker, args=(q2, q)) for i in xrange(totalWorkers)]
# Start all processes
for i in processes:
    i.start()

# Wait for all processes to complete
for i in processes:
    i.join()

real_e = Decimal(1).exp()


globale = q2.get()
print "Suskaiciavau e: "
print globale
print "Tikras e: "
print (real_e)
print "Tikslumas: "
print (real_e - globale)
