# 1959 AHSME Problems, Problem 8

8th problem at http://artofproblemsolving.com/wiki/index.php?title=1959_AHSME_Problems

```
The value of $x^2-6x+13$ can never be less than:
4, 4.5, 5, 7, 13
```

Let's see:

```python
from z3 import *

x, res=Ints('x res')

s=Optimize()

s.add(res==x*x - 6*x + 13)

s.minimize(res)

print s.check()
print s.model()
```

It's 13:

```
sat
[x = 0, res = 13]
```

