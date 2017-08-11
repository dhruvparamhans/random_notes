# Discrete tomography and Z3 SMT-solver

How computed tomography (CT scan) actually works?
A body is bombarded by X-rays in various angles by X-ray tube in rotating torus.
X-ray detectors are also located in torus, and all the information is recorded.

Here is we can simulate simple tomograph.
An "i" character is going to be rotated by 4 angles.
Let's imagine, character is bombarded by X-ray tube at left.
All dots in each row is then summed and sum is "received" by X-ray detector at the right.

	WIDTH= 11 HEIGHT= 11
	angle=(π/4)*0
	    **      2
	    **      2
	            0
	   ***      3
	    **      2
	    **      2
	    **      2
	    **      2
	    **      2
	   ****     4
	            0
	[2, 2, 0, 3, 2, 2, 2, 2, 2, 4, 0] ,
	angle=(π/4)*1
	            0
	            0
	  *         1
	 **         2
	    *       1
	    **      2
	     **     2
	     ****   4
	       *    1
	      *     1
	            0
	[0, 0, 1, 2, 1, 2, 2, 4, 1, 1, 0] ,
	angle=(π/4)*2
	            0
	            0
	            0
	            0
	         *  1
	** *******  9
	** *******  9
	   *     *  2
	            0
	            0
	            0
	[0, 0, 0, 0, 1, 9, 9, 2, 0, 0, 0] ,
	angle=(π/4)*3
	            0
	            0
	       *    1
	       **   2
	      ** *  3
	     ***    3
	    **      2
	            0
	  **        2
	   *        1
	            0
	[0, 0, 1, 2, 3, 3, 2, 0, 2, 1, 0] ,

[The source code](https://github.com/dennis714/random_notes/blob/master/tomo/gen.py)

All we got from our toy-level tomograph is 4 vectors, these are sums of all dots in rows for 4 angles:

	[2, 2, 0, 3, 2, 2, 2, 2, 2, 4, 0] ,
	[0, 0, 1, 2, 1, 2, 2, 4, 1, 1, 0] ,
	[0, 0, 0, 0, 1, 9, 9, 2, 0, 0, 0] ,
	[0, 0, 1, 2, 3, 3, 2, 0, 2, 1, 0] ,

How do we recover initial image?
We are going to represent 11*11 matrix, where sum of each row must be equal to some value we already know.
Then we rotate matrix, and do this again.

The "rotate" function has been taken from the generation program, because, due to Python's dynamic typization nature, it's not important for the function to what operate on:
strings, characters, or Z3 variable instances, so it works very well for both.

	#-*- coding: utf-8 -*-

	import math, sys
	from z3 import *

	# https://en.wikipedia.org/wiki/Rotation_matrix
	def rotate(pic, angle):
	    WIDTH=len(pic[0])
	    HEIGHT=len(pic)
	    #print WIDTH, HEIGHT
	    assert WIDTH==HEIGHT
	    ofs=WIDTH/2

	    out = [[0 for x in range(WIDTH)] for y in range(HEIGHT)]

	    for x in range(-ofs,ofs):
	        for y in range(-ofs,ofs):
	            newX = int(round(math.cos(angle)*x - math.sin(angle)*y,3))+ofs
	            newY = int(round(math.sin(angle)*x + math.cos(angle)*y,3))+ofs
	            # clip at boundaries, hence min(..., HEIGHT-1)
	            out[min(newX,HEIGHT-1)][min(newY,WIDTH-1)]=pic[x+ofs][y+ofs]
	    return out

	vectors=[
	[2, 2, 0, 3, 2, 2, 2, 2, 2, 4, 0] ,
	[0, 0, 1, 2, 1, 2, 2, 4, 1, 1, 0] ,
	[0, 0, 0, 0, 1, 9, 9, 2, 0, 0, 0] ,
	[0, 0, 1, 2, 3, 3, 2, 0, 2, 1, 0]]

	WIDTH = HEIGHT = len(vectors[0])

	s=Solver()
	cells=[[Int('cell_r=%d_c=%d' % (r,c)) for c in range(WIDTH)] for r in range(HEIGHT)]

	# monochrome picture, only 0's or 1's:
	for c in range(WIDTH):
	    for r in range(HEIGHT):
	        s.add(Or(cells[r][c]==0, cells[r][c]==1))

	def all_zeroes_in_vector(vec):
	    for v in vec:
	        if v!=0:
	            return False
	    return True

	ANGLES=len(vectors)
	for a in range(ANGLES):
	    angle=a*(math.pi/ANGLES)
	    rows=rotate(cells, angle)
	    r=0
	    for row in rows:
	        # skip empty rows:
	        if all_zeroes_in_vector(row)==False:
	            # sum of row must be equal to the corresponding element of vector:
	            s.add(Sum(*row)==vectors[a][r])
	        r=r+1

	print s.check()
	m=s.model()
	for r in range(HEIGHT):
	    for c in range(WIDTH):
	        if str(m[cells[r][c]])=="1":
	            sys.stdout.write("*")
	        else:
	            sys.stdout.write(" ")
	    print ""

[The source code](https://github.com/dennis714/random_notes/blob/master/tomo/solve.py)

That works:

	% python solve.py
	sat
	    **
	    **

	   ***
	    **
	    **
	    **
	    **
	    **
	   ****

In other words, all SMT-solver does here is solving a system of equations.

So, 4 angles are enough.
What if we could use only 3 angles?

	WIDTH= 11 HEIGHT= 11
	angle=(π/3)*0
	    **      2
	    **      2
	            0
	   ***      3
	    **      2
	    **      2
	    **      2
	    **      2
	    **      2
	   ****     4
	            0
	[2, 2, 0, 3, 2, 2, 2, 2, 2, 4, 0] ,
	angle=(π/3)*1
	            0
	            0
	            0
	 **         2
	 **         2
	   ***      3
	     ****   4
	       **   2
	       *    1
	            0
	            0
	[0, 0, 0, 2, 2, 3, 4, 2, 1, 0, 0] ,
	angle=(π/3)*2
	            0
	            0
	            0
	       **   2
	       **   2
	     *****  5
	    **      2
	 **         2
	  *         1
	            0
	            0
	[0, 0, 0, 2, 2, 5, 2, 2, 1, 0, 0] ,

No, it's not enough:

	% time python solve3.py
	sat
	 *  *
	    **
	
	     * **
	   **
	   *  *
	    **
	     *   *
	*   *
	   ****

However, the result is correct, but only 3 vectors allows too many possible "images", and Z3 SMT-solver chooses first.

Further reading:
[1](https://en.wikipedia.org/wiki/Discrete_tomography)
[2](https://en.wikipedia.org/wiki/2-satisfiability#Discrete_tomography).

My other notes about SAT/SMT are [here](https://yurichev.com/writings/SAT_SMT_draft-EN.pdf) and in [my blog](https://yurichev.com/blog/).
