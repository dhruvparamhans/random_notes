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
        #print m
        print "left: ",
        print ("w1" if m[w1].as_long()==1 else "  "),
        print ("w3" if m[w3].as_long()==1 else "  "),
        print ("w9" if m[w9].as_long()==1 else "  "),
        print (("obj_w=%2d" % m[obj_w].as_long()) if m[obj].as_long()==1 else "        "),

        print "    | right: ",
        print ("w1" if m[w1].as_long()==2 else "  "),
        print ("w3" if m[w3].as_long()==2 else "  "),
        print ("w9" if m[w9].as_long()==2 else "  "),
        print (("obj_w=%2d" % m[obj_w].as_long()) if m[obj].as_long()==2 else "        "),
        print ""

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
left:     w3                 | right:  w1       obj_w= 2
left:     w3    obj_w= 7     | right:  w1    w9
left:     w3 w9              | right:  w1       obj_w=11
left:     w3    obj_w= 6     | right:        w9
left:  w1 w3    obj_w= 5     | right:        w9
left:     w3 w9              | right:           obj_w=12
left:  w1 w3 w9              | right:           obj_w=13
left:  w1 w3                 | right:           obj_w= 4
left:     w3                 | right:           obj_w= 3
left:           obj_w= 4     | right:  w1 w3
left:           obj_w=13     | right:  w1 w3 w9
left:           obj_w= 3     | right:     w3
left:  w1       obj_w= 2     | right:     w3
left:  w1       obj_w=11     | right:     w3 w9
left:           obj_w=12     | right:     w3 w9
left:  w1                    | right:           obj_w= 1
left:        w9              | right:  w1       obj_w= 8
left:        w9              | right:           obj_w= 9
left:  w1    w9              | right:           obj_w=10
left:  w1    w9              | right:     w3    obj_w= 7
left:        w9              | right:  w1 w3    obj_w= 5
left:        w9              | right:     w3    obj_w= 6
left:           obj_w= 9     | right:        w9
left:           obj_w=10     | right:  w1    w9
left:           obj_w= 1     | right:  w1
left:  w1       obj_w= 8     | right:        w9
total results 26
```

There are 13 distinct obj_w values. So this is an answer.
