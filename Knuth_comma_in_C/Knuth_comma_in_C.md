# Donald Knuth's usage of comma in C

Yet another hack (or trick).
How would you count memory accesses your code do?

Donald Knuth declares such macros:

	#define o mems++
	#define oo mems+= 2
	#define ooo mems+= 3

Then each line of C code which do memory access, prefixed with "o", "oo" or "ooo", like:

	if(j==0)
		ooo,cmem[c].start= k,cmem[c].wlink= cmem[p].wlink,cmem[p].wlink= c,j= 1;

	o,mem[k++].litno= p;

	...

	oo,move[level]= (cmem[level+level+1].wlink!=0||cmem[level+level].wlink==0);

	...

	oo,mem[i].litno= k,mem[p].litno= level+level+1-parity;

	ooo,cmem[c].wlink= cmem[k].wlink,cmem[k].wlink= c;

"mems" variable is dumped at the end.

Interesting to note, this can be used even in for() loop initializer:

	for(o,c= cmem[level+level+1-parity].wlink;c;c= q){
		oo,i= cmem[c].start,q= cmem[c].wlink,j= cmem[c-1].start;

		for(p= i+1;p<j;p++){
			o,k= mem[p].litno;

	...

I copypasted this from his sat0w.w SAT-solver, available [here](https://www-cs-faculty.stanford.edu/~knuth/programs/sat0w.w).
Processed (by CTANGLE) C source code is [here](https://github.com/DennisYurichev/random_notes/blob/master/Knuth_comma_in_C/sat0w.c).
PDF version of this program (processed by CWEAVE) is [here](https://github.com/DennisYurichev/random_notes/blob/master/Knuth_comma_in_C/sat0w.pdf).

