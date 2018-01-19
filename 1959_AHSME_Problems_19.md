# 1959 AHSME Problems, Problem_6

From http://artofproblemsolving.com/wiki/index.php?title=1959_AHSME_Problems

```
With the use of three different weights, namely $1$ lb., $3$ lb., and $9$ lb., 
how many objects of different weights can be weighed, if the objects is to be weighed 
and the given weights may be placed in either pan of the scale? 
15, 13, 11, 9, 7
```

This is fun!

```python
from z3 import *

# 0 - weight absent, 1 - on left pan, 2 - on right pan:
w1, w3, w9, obj = Ints('w1 w3 w9 obj')

obj_w = Int('obj_w')

s=Solver()

s.add(And(w1>=0, w1<=2))
s.add(And(w3>=0, w3<=2))
s.add(And(w9>=0, w9<=2))

# object is always on left or right pan:
s.add(And(obj>=1, obj<=2))

# object must weight something:
s.add(obj_w>0)

left, right = Ints('left right')

# left pan is a sum of weights/object, if they are present on pan:
s.add(left  == If(w1==1, 1, 0) + If(w3==1, 3, 0) + If(w9==1, 9, 0) + If(obj==1, obj_w, 0))
# same for right pan:
s.add(right == If(w1==2, 1, 0) + If(w3==2, 3, 0) + If(w9==2, 9, 0) + If(obj==2, obj_w, 0))

# both pans must weight something:
s.add(left>0)
s.add(right>0)

# pans must have equal weights:
s.add(left==right)

# get all results:
results=[]
while True:
    if s.check() == sat:
        m = s.model()
        print m

        results.append(m)
        block = []
        for d in m:
            # skip internal variables, do not add them to blocking constraint:
            if str(d).startswith ("z3name"):
                continue
            c=d()
            block.append(c != m[d])
        s.add(Or(block))
    else:
        print "total results", len(results)
        break
```

Output:

```
...
[w1 = 0,
 w3 = 0,
 w9 = 2,
 obj = 1,
 obj_w = 9,
 right = 9,
 left = 9]
[w1 = 2,
 w3 = 0,
 w9 = 2,
 obj = 1,
 obj_w = 10,
 right = 10,
 left = 10]
[w1 = 2,
 w3 = 0,
 w9 = 0,
 obj = 1,
 obj_w = 1,
 right = 1,
 left = 1]
[w1 = 1,
 w3 = 0,
 w9 = 2,
 obj = 1,
 obj_w = 8,
 right = 9,
 left = 9]
total results 26
```

Let's grep for object's weights:
```
 obj_w = 1,
 obj_w = 10,
 obj_w = 11,
 obj_w = 12,
 obj_w = 13,
 obj_w = 2,
 obj_w = 3,
 obj_w = 4,
 obj_w = 5,
 obj_w = 6,
 obj_w = 7,
 obj_w = 8,
 obj_w = 9,
```

And how many of them are there?

```
% python 6.py | grep obj_w | sort | uniq | wc -l
13
```

