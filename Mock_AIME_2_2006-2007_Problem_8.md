Again, [artofproblemsolving.com](http://artofproblemsolving.com/wiki/index.php?title=Mock_AIME_2_2006-2007_Problems/Problem_8):

	The positive integers $x_1, x_2, ... , x_7$ satisfy $x_6 = 144$ and $x_{n+3} = x_{n+2}(x_{n+1}+x_n)$ 
	for $n = 1, 2, 3, 4$. Find the last three digits of $x_7$.

This is it:

	from z3 import *

	s=Solver()

	x1, x2, x3, x4, x5, x6, x7=Ints('x1 x2 x3 x4 x5 x6 x7')

	s.add(x1>=0)
	s.add(x2>=0)
	s.add(x3>=0)
	s.add(x4>=0)
	s.add(x5>=0)
	s.add(x6>=0)
	s.add(x7>=0)

	s.add(x6==144)

	s.add(x4==x3*(x2+x1))
	s.add(x5==x4*(x3+x2))
	s.add(x6==x5*(x4+x3))
	s.add(x7==x6*(x5+x4))

	# get all results:

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

Two solutions possible, but in both x7 is ending by 456:

	[x2 = 1,
	 x3 = 1,
	 x1 = 7,
	 x4 = 8,
	 x5 = 16,
	 x7 = 3456,
	 x6 = 144]
	[x3 = 2,
	 x2 = 1,
	 x1 = 2,
	 x6 = 144,
	 x4 = 6,
	 x5 = 18,
	 x7 = 3456]
	total results 2

