# Sometimes a C structure can be used instead of array

## Arithmetic mean

	#include <stdio.h>

	int mean(int *a, int len)
	{
		int sum=0;
		for (int i=0; i<len; i++)
			sum=sum+a[i];
		return sum/len;
	};

	struct five_ints
	{
		int a0;
		int a1;
		int a2;
		int a3;
		int a4;
	};

	int main()
	{
		struct five_ints a;
		a.a0=123;
		a.a1=456;
		a.a2=789;
		a.a3=10;
		a.a4=100;
		printf ("%d\n", mean(&a, 5));
		// test: https://www.wolframalpha.com/input/?i=mean(123,456,789,10,100)
	};

This works: *mean()* function will never access behind the end of *five_ints* structure, because 5 is passed, meaining,
only 5 integers will be accessed.

## Putting string into structure

	#include <stdio.h>

	struct five_chars
	{
		char a0;
		char a1;
		char a2;
		char a3;
		char a4;
	} __attribute__ ((aligned (1),packed));

	int main()
	{
		struct five_chars a;
		a.a0='h';
		a.a1='i';
		a.a2='!';
		a.a3='\n';
		a.a4=0;
		printf (&a); // prints "hi!"
	};

*((aligned (1),packed))* attribute must be used, because otherwise, each structure field will be aligned on 4-byte or 8-byte
boundary.

## Summary

This is just another example of how structures and arrays are stored in memory.
Perhaps, no sane programmer will do something like in this example, except in case of some clever hack.
Or maybe in case of source code obfuscation?

