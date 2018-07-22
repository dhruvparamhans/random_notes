from z3 import *

a,b,c,d,e,f,g,h,i = BitVecs('a b c d e f g h i', 16)

s=Solver()

s.add(And(a>=1, a<=9))
s.add(And(b>=1, b<=9))
s.add(And(c>=1, c<=9))
s.add(And(d>=1, d<=9))
s.add(And(e>=1, e<=9))
s.add(And(f>=1, f<=9))
s.add(And(g>=1, g<=9))
s.add(And(h>=1, h<=9))
s.add(And(i>=1, i<=9))

s.add(Distinct(a,b,c,d,e,f,g,h,i))

s.add(a+13*b/c+d+12*e-f-11+g*h/i-10==66)

# enumerate all possible solutions:
results=[]
while True:
    if s.check() == sat:
        m = s.model()
        print m[a], m[b], m[c], m[d], m[e], m[f], m[g], m[h], m[i]

        results.append(m)
        block = []                                                                                        
        for _d in m:
            _c=_d()
            block.append(_c != m[_d])
        s.add(Or(block))
    else:
        print "results total=", len(results)
        break
