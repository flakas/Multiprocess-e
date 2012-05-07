import math
from decimal import *
from multiprocessing import Process, Queue
from sys import argv

# TODO: Plot function differences from each other and differences from real e

# Set precision
if len(argv) < 4:
    print "Usage: python main.py precision n processes"
    exit()

getcontext().prec = int(argv[1])
n = int(argv[2])
totalWorkers = int(argv[3])

globale = Decimal(0)

def worker(q2, q):
    mye = Decimal(0)
    one = Decimal(1)
    while not q.empty():
        try:
            mye += one / math.factorial(q.get())
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

e_str = str(globale)
seq = max([e_str[i:j] for i in xrange(len(e_str) + 1) for j in xrange(i + 2, len(e_str) + 1)], key=lambda s: e_str.count(s))

print "Ilgiausia seka yra '%s' ir ji pasikartoja %d kartu" % (seq, e_str.count(seq))
