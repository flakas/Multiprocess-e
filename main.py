#!/usr/bin/env python
import math
from decimal import *
from multiprocessing import Process, Queue
from sys import argv
import string
import time
from itertools import groupby

# Set precision
if len(argv) < 6:
    print "Usage: python main.py cmp_n cmp_precision longest_precision longest_n longest_processes"
    exit()

(cmp_n, cmp_precision, longest_precision, longest_n, longest_processes) = map(int, argv[1:])

getcontext().prec = int(argv[1])
n = int(argv[2])
totalWorkers = int(argv[3])

globale = Decimal(0)
values = {}
getcontext().prec = cmp_precision

def f1(n):
    one = Decimal(1)
    try:
        return (one + one/n) ** n
    except: # Catch division by zero
        return 0

def f2(n):
    myE = Decimal(0)
    one = Decimal(1)
    fact = 1
    for i in xrange(0, n + 1):
        if i != 0:
            fact *= i
        myE += one / fact
        yield myE

def factorialGenerator(n):
    fact = 1
    yield fact
    for i in xrange(1, n + 1):
        fact *= i
        yield fact


f2generator = f2(cmp_n)
reale = Decimal(1).exp()

print string.ljust('|Tikras e - f1|', getcontext().prec+1), string.ljust('|Tikras e - f2|', getcontext().prec+1), string.ljust('|f2 - f1|', getcontext().prec+1)

for i in xrange(0, cmp_n + 1):
    obj = {}
    val1 = f1(i)
    val2 = f2generator.next()
    obj['f1_error'] = reale - val1
    obj['f2_error'] = reale - val2
    obj['f1_f2_difference'] = val2 - val1
    values[i] = obj
    print obj['f1_error'], obj['f2_error'], obj['f1_f2_difference']

print 'f1 ir f2 palyginimas baigtas'
print u'Skaiciuoju e kuo tiksliau...'

getcontext().prec = longest_precision

def worker(q2, q, step):
    mye = Decimal(0)
    one = Decimal(1)

    start = q.get()
    first = one / math.factorial(start + 1)
    mye += first
    for i in xrange(start + 2, start + step + 1):
        first *= one / i
        mye += first
    q2.put(mye)
    return

q = Queue()
q2 = Queue()
for i in xrange(0, longest_n, longest_n / longest_processes):
    q.put(i)

processes = [Process(target=worker, args=(q2, q, longest_n / longest_processes)) for i in xrange(longest_processes)]
# Start all processes
for i in processes:
    i.start()

globale = Decimal(1)
# Wait for all processes to complete
for i in processes:
    globale += q2.get()

#print 'Skaiciuoju exp(1)'
#real_e = Decimal(1).exp()

print "Suskaiciavau e: "
print globale
#print "Tikras e: "
#print (real_e)
#print "Tikslumas: "
#print (real_e - globale)

#print 'Ieskau dazniausiai pasikartojancios sekos'
## Find longest most frequent sequence
e_str = str(globale)
#seq = max((e_str[i:j] for i in xrange(len(e_str) + 1) for j in xrange(i + 2, len(e_str) + 1)), key=lambda s: e_str.count(s))

#print "Dazniausiai pasikartojanti seka yra '%s' ir ji pasikartoja %d kartu" % (seq, e_str.count(seq))

print ''
print 'Ieskau ilgiausiu kuo dazniau pasikartojanciu seku (rodo max 5 ilgiui):'

print 'Ieskau bent 2 kartus pasikartojanciu seku'
# Skip '2.'
e_str = e_str[2:]

lengthsQueue = Queue()
for i in xrange(2, int(len(e_str) / 10)):
    lengthsQueue.put(i)

print 'Sudedu ilgius i eile'

statsQueue = Queue()
#statsQueue.put({})
def substringFinder(lengthsQueue, statsQueue, e_str):
    substrings = {}
    substringCounts = {}
    while not lengthsQueue.empty():
        try:
            length = lengthsQueue.get()
            foundSubstrings = 0
            for i in xrange(0, int(len(e_str) - length)):
                s = e_str[i:i+length]
                if not s in substrings.values() and e_str.count(s) >= 2:
                    substrings.update({s: e_str.count(s)})
                    foundSubstrings += 1
            if foundSubstrings == 0:
                break
        except Exception as ex:
            print 'Exception', str(ex)
            break
    #globalSubstrings = statsQueue.get()
    #globalSubstrings.update(substrings)
    statsQueue.put(substrings)
    return

print 'Uzbaigineju praeitus procesus, galbut likusius'
for i in processes:
    if i.is_alive():
        i.terminate()

print 'Paleidineju procesus'
processes = [Process(target=substringFinder, args=(lengthsQueue, statsQueue, e_str)) for i in xrange(longest_processes)]
# Start all processes
for i in processes:
    i.start()

print 'Paleidau procesus, laukiu, kol jie baigs'
sequences = {}
# Wait for all processes to complete
seq = []
#for i in processes:
while len(seq) < longest_processes:
    #sequences.update(statsQueue.get())
    seq.append(statsQueue.get())
    time.sleep(5)
print 'Turi tiek, kiek reikia itemu'
for i in seq:
    sequences.update(i)
    #i.join()

#sequences = {}
#while not statsQueue.empty():
    #sequences.update(statsQueue.get())

#sequences = statsQueue.get()


#curr_len = int(len(e_str) / 10)
#sequences = {}
#while curr_len >= 2:
    #seq_counter = 0
    #for i in xrange(0, int(len(e_str) - curr_len)):
        #s = e_str[i:i+curr_len]
        #if not s in sequences.values() and e_str.count(s) >= 2:
            ##seq_counter += 1
            ##print 'Ilgiausia seka yra \'%s\' ir ji pasikartoja %d kartu' % (s, e_str.count(s))
            #sequences.update({s: e_str.count(s)})
            ##if seq_counter >= 5:
                ##break
    #curr_len -= 1
    #if curr_len <= 1:
        #break

print 'Konvertuoju ir sortinu sekas'
sequences = [(k, sequences[k]) for k in sequences.keys()]

sequences = sorted(sequences, cmp=lambda x, y: cmp(len(x[0]), len(y[0])), reverse=True)

print 'Ruosiu spausdinimui'
groups = []
uniquekeys = []
for k, g in groupby(sequences, key=lambda x: len(x[0])):
    groups.append(list(g))
    uniquekeys.append(k)

for i in groups:
    i = sorted(i, key=lambda x: x[1], reverse=True)
    for j in i[:5]:
        print 'Seka: \'%s\' ir ji pasikartoja %d kartus' % (j[0], j[1])

print 'Radau bent 2 kartus pasikartojanciu seku: %d' % len(sequences)
