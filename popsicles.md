Found this problem at [artofproblemsolving.com](http://artofproblemsolving.com/wiki/index.php?title=2017_AMC_12A_Problems/Problem_1).

	Pablo buys popsicles for his friends. The store sells single popsicles for $1 each, 3-popsicle boxes for $2,
	and 5-popsicle boxes for $3. What is the greatest number of popsicles that Pablo can buy with $8? 

This is optimization problem, and the solution using z3:

	from z3 import *

	box1pop, box3pop, box5pop = Ints('box1pop box3pop box5pop')
	pop_total = Int('pop_total')
	cost_total = Int('cost_total')

	s=Optimize()

	s.add(pop_total == box1pop*1 + box3pop*3 + box5pop*5)
	s.add(cost_total == box1pop*1 + box3pop*2 + box5pop*3)

	s.add(cost_total==8)

	s.add(box1pop>=0)
	s.add(box3pop>=0)
	s.add(box5pop>=0)

	s.maximize(pop_total)

	print s.check()
	print s.model()

And the solution:

	sat
	[box3pop = 1,
	 box5pop = 2,
	 cost_total = 8,
	 pop_total = 13,
	 box1pop = 0]

