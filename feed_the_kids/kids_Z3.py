from z3 import *

# apples = 0
# bananas = 1
# cherries = 2
# dates = 3

E, F, G, H = Ints('E F G H')

s=Solver()

# children's preferences:
s.add(Or(E==2, E==3))
s.add(Or(F==0, F==2))
s.add(Or(G==1, G==2))
s.add(Or(H==0, H==1, H==3))

# each child must get a food of one type:
s.add(Distinct(E,F,G,H))

# enumerate all possible solutions:
results=[]
while True:
    if s.check() == sat:
        m = s.model()
        print m

        results.append(m)
        block = []                                                                                                                
        for d in m:
            c=d()
            block.append(c != m[d])
        s.add(Or(block))
    else:
        print "results total=", len(results)
        break
"""
There are only 3 ways to allocate food to kids:

[G = 1, F = 2, E = 3, H = 0]
[G = 2, F = 0, E = 3, H = 1]
[G = 1, F = 0, E = 2, H = 3]
results total= 3
"""

