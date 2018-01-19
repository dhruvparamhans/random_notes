# 2015 AIME II Problems/Problem 12

At http://artofproblemsolving.com/wiki/index.php?title=2015_AIME_II_Problems/Problem_12

```
There are $2^{10} = 1024$ possible 10-letter strings in which each letter is either an A or a B.
Find the number of such strings that do not have more than 3 adjacent letters that are identical. 
```

We just find all 10-bit numbers, which don't have 4-bit runs of zeros or ones:

```python
from z3 import *

a = BitVec('a', 10)

s=Solver()

for i in range(10-4+1):
    s.add(((a>>i)&15)!=0)
    s.add(((a>>i)&15)!=15)

results=[]
while True:
    if s.check() == sat:
        m = s.model()
        print "0x%x" % m[a].as_long()

        results.append(m)
        block = []
        for d in m:
            c=d()
            block.append(c != m[d])
        s.add(Or(block))
    else:
        print "total results", len(results)
        break
```

It's 548.

