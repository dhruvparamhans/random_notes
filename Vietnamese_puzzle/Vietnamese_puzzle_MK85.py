from MK85 import *

s=MK85(verbose=0)

BIT_WIDTH=16

a=s.BitVec('a', BIT_WIDTH)
b=s.BitVec('b', BIT_WIDTH)
c=s.BitVec('c', BIT_WIDTH)
d=s.BitVec('d', BIT_WIDTH)
e=s.BitVec('e', BIT_WIDTH)
f=s.BitVec('f', BIT_WIDTH)
g=s.BitVec('g', BIT_WIDTH)
h=s.BitVec('h', BIT_WIDTH)
i=s.BitVec('i', BIT_WIDTH)

s.add(And(a>=1, a<=9))
s.add(And(b>=1, b<=9))
s.add(And(c>=1, c<=9))
s.add(And(d>=1, d<=9))
s.add(And(e>=1, e<=9))
s.add(And(f>=1, f<=9))
s.add(And(g>=1, g<=9))
s.add(And(h>=1, h<=9))
s.add(And(i>=1, i<=9))

s.add(s.Distinct([a,b,c,d,e,f,g,h,i]))

s.add(a+
	(s.BitVecConst(13, BIT_WIDTH)*b)/c+
	d+
	(s.BitVecConst(12, BIT_WIDTH)*e)-
	f-
	s.BitVecConst(11, BIT_WIDTH)+
	(g*h)/i-
	s.BitVecConst(10, BIT_WIDTH) == s.BitVecConst(66,BIT_WIDTH))

print s.count_models()
exit(0)

# .. slow ...

# enumerate all solutions:
results=0
while s.check():
    m = s.model()
    print "%d %d %d %d %d %d %d %d %d" % (m["a"], m["b"], m["c"], m["d"], m["e"], m["f"], m["g"], m["h"], m["i"])

    # block current solution and solve again:
    s.add(expr.Not(And(a==m["a"], b==m["b"], c==m["c"], d==m["d"], e==m["e"], f==m["f"], g==m["g"], h==m["h"], i==m["i"])))
    results=results+1

print "results total=", results

