# 2012 AIME I Problems/Problem 1

From http://artofproblemsolving.com/wiki/index.php?title=2012_AIME_I_Problems/Problem_1

```
Find the number of positive integers with three not necessarily distinct digits, $abc$, with $a \neq 0$ and $c \neq 0$ such that both $abc$ and $cba$ are multiples of $4$.
```

```python
from z3 import *

a, b, c = Ints('a b c')

s=Solver()

s.add(a>0)
s.add(b>=0)
s.add(c>0)

s.add(a<=9)
s.add(b<=9)
s.add(c<=9)

s.add((a*100 + b*10 + c) % 4 == 0)
s.add((c*100 + b*10 + a) % 4 == 0)

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
        print "total results", len(results)
        break
```

Let's see:

```
[c = 4, b = 0, a = 4]
[b = 1, c = 2, a = 2]
[b = 6, c = 4, a = 4]
[b = 4, c = 4, a = 4]
[b = 2, c = 4, a = 4]
[b = 4, c = 4, a = 8]
[b = 8, c = 4, a = 4]
[b = 6, c = 4, a = 8]
[b = 8, c = 4, a = 8]
[b = 0, c = 4, a = 8]
[b = 2, c = 4, a = 8]
[b = 8, c = 8, a = 8]
[b = 9, c = 6, a = 6]
[b = 2, c = 8, a = 8]
[b = 2, c = 8, a = 4]
[b = 4, c = 8, a = 4]
[b = 4, c = 8, a = 8]
[b = 8, c = 8, a = 4]
[b = 6, c = 8, a = 4]
[b = 6, c = 8, a = 8]
[b = 0, c = 8, a = 4]
[b = 0, c = 8, a = 8]
[b = 7, c = 6, a = 6]
[b = 7, c = 2, a = 6]
[b = 7, c = 6, a = 2]
[b = 7, c = 2, a = 2]
[b = 9, c = 2, a = 6]
[b = 9, c = 2, a = 2]
[b = 9, c = 6, a = 2]
[b = 5, c = 6, a = 2]
[b = 1, c = 6, a = 2]
[b = 3, c = 6, a = 2]
[b = 5, c = 2, a = 2]
[b = 3, c = 2, a = 2]
[b = 5, c = 6, a = 6]
[b = 5, c = 2, a = 6]
[b = 3, c = 2, a = 6]
[b = 1, c = 2, a = 6]
[b = 1, c = 6, a = 6]
[b = 3, c = 6, a = 6]
total results 40
```

My [toy-level SMT-solver](https://github.com/DennisYurichev/MK85) can enumerate all solutions as well:

```
(set-logic QF_BV)
(set-info :smt-lib-version 2.0)

(declare-fun a () (_ BitVec 8))
(declare-fun b () (_ BitVec 8))
(declare-fun c () (_ BitVec 8))

(assert (bvugt a #x00))
(assert (bvuge b #x00))
(assert (bvugt c #x00))

(assert (bvule a #x09))
(assert (bvule b #x09))
(assert (bvule c #x09))

; slower:
;(assert (= (bvurem (bvadd (bvmul a (_ bv100 8)) (bvmul b (_ bv00 8)) c) #x04) #x00))
;(assert (= (bvurem (bvadd (bvmul c (_ bv100 8)) (bvmul b (_ bv00 8)) a) #x04) #x00))

; faster:
(assert (= (bvand (bvadd (bvmul a (_ bv100 8)) (bvmul b (_ bv00 8)) c) #x03) #x00))
(assert (= (bvand (bvadd (bvmul c (_ bv100 8)) (bvmul b (_ bv00 8)) a) #x03) #x00))

;(check-sat)
;(get-model)
(get-all-models)
;(count-models)
```

Faster version doesn't find remainder, it just isolates two last bits.

