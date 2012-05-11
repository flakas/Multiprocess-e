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
values = {}
getcontext().prec = 50

def f1(n):
    one = Decimal(1)
    try:
        return (one + one/n) ** n
    except: # Catch division by zero
        return 0

def f2(n):
    myE = Decimal(0)
    one = Decimal(1)
    for i in xrange(0, n + 1):
        myE += one / math.factorial(i)
        yield myE

f2generator = f2(n)
reale = Decimal(1).exp()

print '|Tikras e - f1|', '|Tikras e - f2|', '|f2 - f1|'
for i in xrange(0, n + 1):
    obj = {}
    val1 = f1(i)
    val2 = f2generator.next()
    obj['f1_error'] = reale - val1
    obj['f2_error'] = reale - val2
    obj['f1_f2_difference'] = val2 - val1
    values[i] = obj
    print obj['f1_error'], obj['f2_error'], obj['f1_f2_difference']

exit()

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

# Find longest most frequent sequence
e_str = str(globale)
seq = max((e_str[i:j] for i in xrange(len(e_str) + 1) for j in xrange(i + 2, len(e_str) + 1)), key=lambda s: e_str.count(s))

print "Ilgiausia seka yra '%s' ir ji pasikartoja %d kartu" % (seq, e_str.count(seq))
