# Dependency hell and Z3 SMT-solver

(The note below has been copypasted to the [my article about SAT/SMT](https://yurichev.com/tmp/SAT_SMT_DRAFT.pdf))

Here is simplified example:

	#!/usr/bin/env python

	from z3 import *

	s=Optimize()

	libA=Int('libA')
	# libA's version is 1..5 or 999 (which means library will not be installed):
	s.add(Or(And(libA>=1, libA<=5),libA==999))

	libB=Int('libB')
	# libB's version is 1, 4, 5 or 999:
	s.add(Or(libB==1, libB==4, libB==5, libB==999))

	libC=Int('libC')
	# libC's version is 10, 11, 14 or 999:
	s.add(Or(libC==10, libC==11, libC==14, libC==999))

	# libC is dependent on libA
	# libC v10 is dependent on libA v1..3, but not newer
	# libC v11 requires at least libA v3
	# libC v14 requires at least libA v5
	s.add(If(libC==10, And(libA>=1, libA<=3), True))
	s.add(If(libC==11, libA>=3, True))
	s.add(If(libC==14, libA>=5, True))

	libD=Int('libD')
	# libD's version is 1..10
	s.add(Or(And(libD>=1, libD<=10),libD==999))

	programA=Int('programA')
	# programA came as v1 or v2:
	s.add(Or(programA==1, programA==2))

	# programA is dependent on libA, libB and libC
	# programA v1 requires libA v2 (only this version), libB v4 or v5, libC v10:
	s.add(If(programA==1, And(libA==2, Or(libB==4, libB==5), libC==10), True))
	# programA v2 requires these libraries: libA v3, libB v5, libC v11
	s.add(If(programA==2, And(libA==3, libB==5, libC==11), True))

	programB=Int('programB')
	# programB came as v7 or v8:
	s.add(Or(programB==7, programB==8))

	# programB v7 requires libA at least v2 and libC at least v10:
	s.add(If(programB==7, And(libA>=2, libC>=10), True))
	# programB v8 requires libA at least v6 and libC at least v11:
	s.add(If(programB==8, And(libA>=6, libC>=11), True))

	s.add(programA==1)
	s.add(programB==7) # change this to 8 to make it unsat

	# we want latest libraries' versions.
	# if the library is not required, its version is "pulled up" to 999,
	# and 999 means the library is not needed to be installed
	s.maximize(Sum(libA,libB,libC,libD))

	print s.check()
	print s.model()

( [The source code](https://github.com/dennis714/random_notes/blob/master/dependency/dependency.py) )

The output:

	sat
	[libB = 5,
	 libD = 999,
	 libC = 10,
	 programB = 7,
	 programA = 1,
	 libA = 2]

999 means that there is no need to install libD, it's not required by other packages.

Change ProgramB to v8 and it will says "unsat", meaning, there is a conflict:
ProgramA requires libA v2, but ProgramB v8 eventually requires newer libA.

Still, there is a work to do: "unsat" is somewhat useless to end user, some information about conflicting items should be
printed.

Here is my another optimization problem example: [Making smallest possible test suite using Z3](https://yurichev.com/blog/set_cover/)

More about using SAT/SMT solvers in package managers: [1](https://research.swtch.com/version-sat),
[2](https://cseweb.ucsd.edu/~lerner/papers/opium.pdf).

Now in the opposite direction: [forcing aptitude package manager to solve Sudoku](http://web.archive.org/web/20160326062818/http://algebraicthunk.net/~dburrows/blog/entry/package-management-sudoku/).

Some readers may ask, how to order libraries/programs/packages to be installed?
This is simpler problem, which is often solved by [topological sorting](https://en.wikipedia.org/wiki/Topological_sorting).
The algorithm reorders graph in such a way so that vertices not depended on anything will be on the top of queue.
Next, there will be vertices dependend on vertices from the previous layer. And so on.

"make" UNIX utility does this while constructing order of items to be processed.
Even more: older "make" utilities offloaded the job to the external utility ("tsort").
Some older UNIX has it, [at least some versions of NetBSD](http://netbsd.gw.com/cgi-bin/man-cgi/man?tsort+1+NetBSD-current).

My other notes about SAT/SMT are [here](https://yurichev.com/writings/SAT_SMT_draft-EN.pdf) and in [my blog](https://yurichev.com/blog/).

