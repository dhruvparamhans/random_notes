Another problem from [http://artofproblemsolving.com](http://artofproblemsolving.com/wiki/index.php?title=2017_AMC_12A_Problems/Problem_2):

	The sum of two nonzero real numbers is 4 times their product. What is the sum of the reciprocals of the two numbers? 

We're going to solve this over real numbers:

	from z3 import *

	x, y = Reals('x y')

	s=Solver()

	s.add(x>0)
	s.add(y>0)

	s.add(x+y == 4*x*)

	print s.check()
	m=s.model()
	print "the model:"
	print m
	print "the answer:", m.evaluate (1/x + 1/y)

Instead of pulling values from the model and then compute the final result on Python's side, we can evaluate
an expression (1/x + 1/y) "inside" the model we've got:

	sat
	the model:
	[x = 1, y = 1/3]
	the answer: 4

