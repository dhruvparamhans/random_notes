"""
Can find a closed knight's tour on 8*8 chess board for 150s on Intel Quad-Core Xeon E3-1220 3.10GHz:

 0 57 44 41  2 39 12 29
43 46  1 58 11 30 23 38
56 63 42 45 40  3 28 13
47  8 59 10 31 24 37 22
60 55 62 51  4 27 14 25
 7 48  9 32 17 34 21 36
54 61 50  5 52 19 26 15
49  6 53 18 33 16 35 20

However, this is WAY slower than C implementation on Rosetta Code: https://rosettacode.org/wiki/Knight%27s_tour#C
... which uses Warnsdorf's rule: https://en.wikipedia.org/wiki/Knight%27s_tour#Warnsdorff.27s_algorithm
Any idea how to implement it in SAT/SMT?

Another program for Z3 for finding Hamiltonian cycle: https://github.com/Z3Prover/z3/blob/master/examples/python/hamiltonian/hamiltonian.py
(Clever trick of using remainder.)

"""
from z3 import *
import pprint, math

SIZE=8
#closed=False
closed=True
# find King's tour instead of Knight's. just for demonstration
#king_tour=True
king_tour=False

def coord_to_idx(r, c):
    if r<0 or c<0:
        return None
    if r>=SIZE or c>=SIZE:
        return None
    return r*SIZE+c

"""
knight's movements:

. x . x . . . .
x . . . x . . .
. . o . . . . .
x . . . x . . .
. x . x . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .

"""
G={}

if king_tour:
# King's tour
    for r in range(SIZE):
        for c in range(SIZE):
            _from=coord_to_idx(r, c)
            _to=[]
            _to.append(coord_to_idx(r-1, c-1))
            _to.append(coord_to_idx(r-1, c+0))
            _to.append(coord_to_idx(r-1, c+1))
            _to.append(coord_to_idx(r-0, c-1))
            _to.append(coord_to_idx(r-0, c+1))
            _to.append(coord_to_idx(r+1, c-1))
            _to.append(coord_to_idx(r+1, c+0))
            _to.append(coord_to_idx(r+1, c+1))
            # remove "None" elements (moves beyond physical board):
            _to=filter(lambda x: x!=None, _to)
            G[_from]=_to
else:
# Knight's tour
    for r in range(SIZE):
        for c in range(SIZE):
            _from=coord_to_idx(r, c)
            _to=[]
            _to.append(coord_to_idx(r-2, c-1))
            _to.append(coord_to_idx(r-2, c+1))
            _to.append(coord_to_idx(r-1, c-2))
            _to.append(coord_to_idx(r-1, c+2))
            _to.append(coord_to_idx(r+1, c-2))
            _to.append(coord_to_idx(r+1, c+2))
            _to.append(coord_to_idx(r+2, c-1))
            _to.append(coord_to_idx(r+2, c+1))
            # remove "None" elements (moves beyond physical board):
            _to=filter(lambda x: x!=None, _to)
            G[_from]=_to

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(G)

s=Solver()

L=len(G)
# we use one-hot (or unitary) variables, thus we eliminate need to use adding + remainder
# as in https://github.com/Z3Prover/z3/blob/master/examples/python/hamiltonian/hamiltonian.py
V=[BitVec('V_%d' % i, L) for i in range(L)]

# on closed tour, we may omit this constraint, SAT/SMT solver got to know this is one-hot/unitary variable!
if closed==False:
    # without: faster on closed tours
    for v in range(L):
        or_list=[]
        for i in range(L):
            or_list.append(V[v]==2**i)
        s.add(Or(*or_list))

s.add(Distinct(V))

# first cell:
s.add(V[0]==BitVecVal(1, L))

def MUX(selector, selectors, vals):
    assert len(selectors)+1 == len(vals)
    l=len(vals)
    t=vals[0]
    for i in range(l-1):
        t=If(selector==selectors[i], vals[i+1], t)
    return t

for i in range(L):
    if closed==False and i==0:
        continue
    or_list=[]
    for j in G[i]:
        or_list.append(RotateLeft(V[j], 1))
    sel=Int('sel%d' % i)
    # no idea why, but using multiplexer is faster than chain of Or's in 
    # https://github.com/Z3Prover/z3/blob/master/examples/python/hamiltonian/hamiltonian.py
    e=MUX(sel, range(len(or_list)-1), or_list)
    """
    at this point e can look like:

    54 If(sel54 == 2,
       RotateLeft(V_60, 1),
       If(sel54 == 1,
          RotateLeft(V_44, 1),
          If(sel54 == 0,
             RotateLeft(V_39, 1),
             RotateLeft(V_37, 1))))
    
    selector is not used at all
    """
    #print i, e
    s.add(V[i]==e)

if s.check()==unsat:
    print "unsat"
    exit(0)
m=s.model()
#print m

print ""
for r in range(SIZE):
    for c in range(SIZE):
        t=coord_to_idx(r, c)
        print ("%2d" % int(math.log(m[V[t]].as_long(), 2))),
    print ""

