from z3 import *

"""
The problem from the "Discrete Structures, Logic and Computability" book by James L. Hein, 4th ed.

"Suppose a survey revealed that 70% of the population visited
an amusement park and 80% visited a national park.
At least what percentage of the population visited both?"

The problem is supposed to be solved using finite sets counting...
"""

# each element is 0/1, reflecting 10% of park1/park2 levels of attendance...
p1=[Int('park1_%d' % i) for i in range(10)]
p2=[Int('park2_%d' % i) for i in range(10)]
# 1 if visited both, 0 otherwise:
b=[Int('both_%d' % i) for i in range(10)]

s=Optimize()
# sum of p1[] must be 7 (or 70%)
s.add(Sum(p1)==7)
# sum of p2[] must be 8 (or 80%)
s.add(Sum(p2)==8)

for i in range(10):
    # all in limits:
    s.add(And(p1[i]>=0, p1[i]<=1))
    s.add(And(p2[i]>=0, p2[i]<=1))
    # if both p1[] and p2[] has 1, b[] would have 1 as well:
    s.add(b[i]==If(And(p1[i]==1, p2[i]==1), 1, 0))

both=Int('both')
s.add(Sum(b)==both)

s.minimize(both)
#s.maximize(both)
assert s.check()==sat
m=s.model()

print "park1 : "+"".join([("*" if m[p1[i]].as_long()==1 else ".") for i in range(10)])
print "park2 : "+"".join([("*" if m[p2[i]].as_long()==1 else ".") for i in range(10)])
print "both  : "+"".join([("*" if m[b[i]].as_long()==1 else ".") for i in range(10)])+" (%d)" % m[both].as_long()

"""
This is fun!

If minimize:

park1 : ***...****
park2 : *..*******
both  : *.....**** (5)

If maximize:

park1 : ..*******.
park2 : ..********
both  : ..*******. (7)

In other words, "stars" are allocated in such a way, so that the sum of "stars" in b[] would be minimal/maximal

Observing this, we can deduce general formula:

Maximal both = min(park1, park2)

What about minimal both?
We can see that "stars" from one park1 must "shift out" or "hide in" to what corresponding empty space of park2.
So, minimal both = park2 - (100% - park1)

SMT solver is overkill for the job, but perfect for illustration and helping in better understanding.

----

Variations of the problem from the same book:

"Suppose that 100 senators voted on three separate senate bills as follows:
70 percent of the senators voted for the first bill, 65 percent voted for the second bill,
and 60 percent voted for the third bill. At least what percentage of the senators voted for all three bills?"

"Suppose that 25 people attended a conference with three sessions, where 15 people attended the first session, 
18 the second session, and 12 the third session. At least how many people attended all three sessions?"

"""

