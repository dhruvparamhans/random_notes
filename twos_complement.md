# Couple of additions about two's complement form

## Getting maximum number of some *word*

Maximum number in unsigned form is just a number where all bits are set: *0xFF..FF* (this is -1 if the *word* is
treated as signed integer).
So you take a *word*, set all bits and get the value:

	#include <stdio.h>

	int main()
	{
		int val=~0; // change to char to get maximal value for the unsigned 8-bit byte
		printf ("%u\n", val); // %u for unsigned
	};

This is 4294967295 for 32-bit integer.

## Getting minimum number for some signed *word*

Minimum signed number has form of *0x80..00*, i.e., most significant bit is set, while others are cleared.
Maximum signed number has the same form, but all bits are inverted: *0x7F..FF*.

Let's shift a lone bit left until it disappears:

	#include <stdio.h>

	int main()
	{
		int val=1; // change to "char" to find values for signed byte
		while (val!=0)
		{
			printf ("%d %d\n", val, ~val);
			val=val<<1;
		};
	};

Output is:

	...

	536870912 -536870913
	1073741824 -1073741825
	-2147483648 2147483647

Two last numbers are minimum and maximum signed 32-bit *int* respectively.

