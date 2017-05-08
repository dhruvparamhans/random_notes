(The note below has been copypasted to the [my article about SAT/SMT](https://yurichev.com/tmp/SAT_SMT_DRAFT.pdf))

# Simple program synthesis using Z3 SMT-solver

Sometimes, multiplication operation can be replaced with couple of shifting/addition/subtraction operations.
Compilers do so, because pack of instructions can be faster than multiplication unit in CPU.

For example, multiplication by 19 is replaced by GCC 5.4 with pair of instructions: `lea edx, [eax+eax*8]` and
`lea eax, [eax+edx*2]`.
This is sometimes also called "superoptimization".

Let's see if we can find a shortest possible instructions pack for some specified multiplier.

As I've already wrote once, SMT-solver can be seen as a solver of huge systems of equations.
The task is to construct such system of equations, which could produce a short program on output.
I will use electronics analogy here, it can make things a little simpler.

First of all, what our program could be? There will be 3 operations allowed: ADD/SUB/SHL.
Only registers allowed as operands, except for the second operand of SHL (which could be in 1..31 range).
Each register will be assigned only once (as in SSA (Static single assignment form)).

And there will be some magic block, which takes all previous register states, it also takes operation type,
operands and produces a value of next register's state.


	        op ------------+
	        op1_reg -----+ |
	        op2_reg ---+ | |
	                   | | |
	                   v v v
	             +---------------+
	             |               |
	registers -> |               | -> new register's state
	             |               |
	             +---------------+


Now let's take a look on our schematics on top level:

	0 -> blk -> blk -> blk .. -> blk -> 0

	1 -> blk -> blk -> blk .. -> blk -> multiplier

Each block takes previous state of registers and produces new set.
There are two chains.
First chain takes 0 as state of R0 at the very beginning, and the chain is supposed to produce 0 at the end
(since zero multiplied by any value is still zero).
The second chain takes 1 and must produce multiplier as the state of very last register
(since 1 multiplied by multiplier must equal to multiplier).

Each block is "controlled" by operation type, operand types, etc.
For each column, there is each own set.

Now you can view these two chains as two equations.
Ultimate goal is to find such state of all operand types, etc, so the first chain will equal to 0,
and the second to multiplier.

Let's also take a look into "magic block" inside:


	                op1_reg         op
	                   |            v
	                   v         +-----+
	registers ---> selector1 --> | ADD |
	           +                 | SUB | ---> result
	           |                 | SHL |
	           +-> selector2 --> +-----+
	                  ^             ^
	                  |             |
	               op2_reg       op2_imm

Each selector can be viewed as simple multipositional switch.
If operation is SHL, a value in range of 1..31 is used as second operand.

So you can imagine this electric circuit and your goal is to turn all switches in such a state, so two chains
will have 0 and multiplier on output.
This sounds like logic puzzle in some way.
Now we will try to use Z3 to solve this puzzle.

First, we define all varibles:

	R=[[BitVec('S_s%d_c%d' % (s, c), 32) for s in range(MAX_STEPS)] for c in range (CHAINS)]
	op=[Int('op_s%d' % s) for s in range(MAX_STEPS)]
	op1_reg=[Int('op1_reg_s%d' % s) for s in range(MAX_STEPS)]
	op2_reg=[Int('op2_reg_s%d' % s) for s in range(MAX_STEPS)]
	op2_imm=[BitVec('op2_imm_s%d' % s, 32) for s in range(MAX_STEPS)]

R[][] is registers state for each chain and each step.
On contrary, op/op1\_reg/op2\_reg/op2\_imm variables are defined for each step, but for all chains,
since both chains at each column has the same operation/etc.

Now we must limit count of operations, and also, register's number for each step must not be bigger than step number,
in other words, instruction at each step is allowed to access only registers which were already set before:

	for s in range(1, STEPS):
	    # for each step
	    sl.add(And(op[s]>=0, op[s]<=2))
	    sl.add(And(op1_reg[s]>=0, op1_reg[s]<s))
	    sl.add(And(op2_reg[s]>=0, op2_reg[s]<s))
	    sl.add(And(op2_imm[s]>=1, op2_imm[s]<=31))

Fix register of first step for each chain:

	for c in range(CHAINS):
	    # for each chain:
	    sl.add(R[c][0]==chain_inputs[c])
	    sl.add(R[c][STEPS-1]==chain_inputs[c]*multiplier)

Now this is "magic block":

	for s in range(1, STEPS):
	    sl.add(R[c][s]==simulate_op(R,c, op[s], op1_reg[s], op2_reg[s], op2_imm[s]))

Now how "magic block" is defined?

	def selector(R, c, s):
	    # for all MAX_STEPS:
	    return If(s==0, R[c][0],
        	    If(s==1, R[c][1],
	            If(s==2, R[c][2],
        	    If(s==3, R[c][3],
	            If(s==4, R[c][4],
	            If(s==5, R[c][5],
        	    If(s==6, R[c][6],
	            If(s==7, R[c][7],
        	    If(s==8, R[c][8],
	            If(s==9, R[c][9],
        	        0)))))))))) # default

	def simulate_op(R, c, op, op1_reg, op2_reg, op2_imm):
	    op1_val=selector(R,c,op1_reg)
	    return If(op==0, op1_val + selector(R, c, op2_reg),
        	   If(op==1, op1_val - selector(R, c, op2_reg),
	           If(op==2, op1_val << op2_imm,
        	       0))) # default

This is very important to understand: if the operation is ADD/SUB, op2\_imm's value is just ignored.
Otherwise, if operation is SHL, value of op2\_reg is ignored.
Just like in case of digital circuit.

The code: https://github.com/dennis714/random_notes/blob/master/mult.py

Now let's see how it works:

	 % ./mult.py 12
	multiplier= 12
	attempt, STEPS= 2
	unsat
	attempt, STEPS= 3
	unsat
	attempt, STEPS= 4
	sat!
	r1=SHL r0, 2
	r2=SHL r1, 1
	r3=ADD r1, r2
	tests are OK

The first step is always a step containing 0/1, or, r0.
So when our solver reporting about 4 steps, this means 3 instructions.

Something harder:

	 % ./mult.py 123
	multiplier= 123
	attempt, STEPS= 2
	unsat
	attempt, STEPS= 3
	unsat
	attempt, STEPS= 4
	unsat
	attempt, STEPS= 5
	sat!
	r1=SHL r0, 2
	r2=SHL r1, 5
	r3=SUB r2, r1
	r4=SUB r3, r0
	tests are OK

Now the code multiplying by 1234:

	r1=SHL r0, 6
	r2=ADD r0, r1
	r3=ADD r2, r1
	r4=SHL r2, 4
	r5=ADD r2, r3
	r6=ADD r5, r4

Looks great, but it took ~23 seconds to find it on my Intel Xeon CPU E31220 @ 3.10GHz.
I agree, this is far from practical usage.
Also, I'm not quite sure that this piece of code will work faster than a single multiplication instruction.
But anyway, it's a good demonstration of SMT solvers capabilities.

The code multiplying by 12345 (~150 seconds):

	r1=SHL r0, 5
	r2=SHL r0, 3
	r3=SUB r2, r1
	r4=SUB r1, r3
	r5=SHL r3, 9
	r6=SUB r4, r5
	r7=ADD r0, r6

Multiplication by 123456 (~8 minutes!):

	r1=SHL r0, 9
	r2=SHL r0, 13
	r3=SHL r0, 2
	r4=SUB r1, r2
	r5=SUB r3, r4
	r6=SHL r5, 4
	r7=ADD r1, r6

## Few notes

I've removed SHR instruction support, simply because the code multiplying by a constant makes no use of it.
Even more: it's not a problem to add support of immediates as second operand for all instructions,
but again, you wouldn't find a piece of code which does this job and uses some additional constants.
Or maybe I wrong?

Of course, for another job you'll need to add support of immediates and other operations.
But at the same time, it will work slower and slower.
So I had to keep ISA (instruction set architecture) of this toy CPU as compact as possible.

## The code

https://github.com/dennis714/random_notes/blob/master/mult.py

## Further reading

A somewhat more advanced article I wrote once: [Finding unknown algorithm using only input/output pairs and Z3 SMT
solver](https://yurichev.com/writings/z3_rockey.pdf)

Other SMT solver examples: https://yurichev.com/tmp/SAT_SMT_DRAFT.pdf


