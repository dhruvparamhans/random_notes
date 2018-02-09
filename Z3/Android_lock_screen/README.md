# Anroid lock screen (9 dots) has 10296 possible ways to (un)lock it

How would you count?

```python
from z3 import *

"""
1 2 3
4 5 6
7 8 9
"""

# where the next dot can be if the current dot is at $a$
# next dot can only be a neighbour
# here we define starlike connections between dots (as in Android lock screen)
# this is like switch() or multiplexer
def next_dot(a, b):
    return If(a==1, Or(b==2, b==4, b==5),
        If(a==2, Or(b==1, b==3, b==4, b==5, b==6),
        If(a==3, Or(b==2, b==5, b==6),
        If(a==4, Or(b==1, b==2, b==5, b==7, b==8),
        If(a==5, Or(b==1, b==2, b==3, b==4, b==6, b==7, b==8, b==9),
        If(a==6, Or(b==2, b==3, b==5, b==8, b==9),
        If(a==7, Or(b==4, b==5, b==8),
        If(a==8, Or(b==4, b==5, b==6, b==7, b==9),
        If(a==9, Or(b==5, b==6, b==8),
            False))))))))) # default

# if only non-diagonal lines between dots are allowed:
"""
def next_dot(a, b):
    return If(a==1, Or(b==2, b==4),
        If(a==2, Or(b==1, b==3, b==5),
        If(a==3, Or(b==2, b==6),
        If(a==4, Or(b==1, b==5, b==7),
        If(a==5, Or(b==2, b==4, b==6, b==8),
        If(a==6, Or(b==3, b==5, b==9),
        If(a==7, Or(b==4, b==8),
        If(a==8, Or(b==5, b==7, b==9),
        If(a==9, Or(b==6, b==8),
            False))))))))) # default
"""

def paths_for_length (LENGTH):
    s=Solver()

    path=[Int('path_%d' % i) for i in range(LENGTH)]

    # all elements of path must be distinct
    s.add(Distinct(path))

    # all elements in [1..9] range:
    for i in range(LENGTH):
        s.add(And(path[i]>=1, path[i]<=9))

    # next element of path is defined by next_dot() function, unless it's the last one:
    for i in range(LENGTH-1):
        s.add(next_dot(path[i], path[i+1]))

    results=[]

    # enumerate all possible solutions:
    while True:
        if s.check() == sat:
            m = s.model()
            tmp=[]
            for i in range(LENGTH):
                tmp.append(m[path[i]].as_long())
            #print m
            print "path", tmp
            # print visual representation:
            for k in [[1,2,3],[4,5,6],[7,8,9]]:
                for j in k:
                    if j in tmp:
                        print tmp.index(j)+1,
                    else:
                        print ".",
                print ""
            print ""
            results.append(m)
            block = []
            for d in m:
                c=d()
                block.append(c != m[d])
            s.add(Or(block))
        else:
            print "length=", LENGTH, "results total=", len(results)
            return len(results)

total=0
for l in range(2,10):
    total=total+paths_for_length(l)

print "total=", total
```

Sample paths of 7 elements:

```
...

path [7, 5, 1, 4, 8, 6, 3]
3 . 7
4 2 6
1 5 .

path [9, 5, 7, 4, 8, 6, 3]
. . 7
4 2 6
3 5 1

path [9, 5, 1, 4, 8, 6, 3]
3 . 7
4 2 6
. 5 1

...
```

Each element of "path" is number of dot, like on phone's keypad:
```
1 2 3
4 5 6
7 8 9
```

Numbers on 3 * 3 box represent a sequence: which dot is the 1st, 2nd, etc...

Of 9:

```
...

path [7, 8, 9, 5, 4, 1, 2, 6, 3]
6 7 9
5 4 8
1 2 3

path [1, 4, 7, 5, 2, 3, 6, 9, 8]
1 5 6
2 4 7
3 9 8

path [9, 6, 8, 7, 4, 1, 5, 2, 3]
6 8 9
5 7 2
4 3 1

...
```

All possible paths: https://github.com/DennisYurichev/random_notes/blob/master/Z3/Android_lock_screen/starlike (~500k file).

Statistics:

```
length= 2 results total= 40
length= 3 results total= 160
length= 4 results total= 496
length= 5 results total= 1208
length= 6 results total= 2240
length= 7 results total= 2984
length= 8 results total= 2384
length= 9 results total= 784
total= 10296
```

What if only non-diagonal lines would be allowed (which isn't a case of a real Android lock screen)?

```
length= 2 results total= 24
length= 3 results total= 44
length= 4 results total= 80
length= 5 results total= 104
length= 6 results total= 128
length= 7 results total= 112
length= 8 results total= 112
length= 9 results total= 40
total= 644
```

All possible non-diagonal paths: https://github.com/DennisYurichev/random_notes/blob/master/Z3/Android_lock_screen/nondiagonal

Obviously, it's hard to bruteforce all them on a real smartphone/tablet, but nevertheless, it was fun to learn about it, at first, I though these numbers should be much bigger.

