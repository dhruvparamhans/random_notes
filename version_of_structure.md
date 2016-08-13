# Version of C structure

Many Windows programmers have seen this is MSDN:

> SizeOfStruct
>     The size of the structure, in bytes. This member must be set to sizeof(SYMBOL_INFO).

( [MSDN entry](https://msdn.microsoft.com/en-us/library/windows/desktop/ms680686(v=vs.85).aspx) )

Some structures like SYMBOL_INFO has started with this field indeed. Why?
This is some kind of structure version.

Imagine you have a function which draws circle.
It takes a single argument - a pointer to a structure with only two fields: X and Y.
And then color displays flooded a market, sometimes in 1980s. And you need to add *color* argument to the function.
But, let's say, you cannot add another argument to it (a lot of software use your API and cannot be recompiled).
And if the old piece of software uses your API, let your function draw a circle in (default) black and white colors.

Another day you add another feature: circle now can be filled, and brush type can be set.

Here is one solution to the problem:

	#include <stdio.h>

	struct ver1
	{
		size_t SizeOfStruct;
		int coord_X;
		int coord_Y;
	};

	struct ver2
	{
		size_t SizeOfStruct;
		int coord_X;
		int coord_Y;
		int color;
	};

	struct ver3
	{
		size_t SizeOfStruct;
		int coord_X;
		int coord_Y;
		int color;
		int fill_brush_type; // 0 - do not fill circle
	};

	void draw_circle(struct ver3 *s) // latest struct version is used here
	{
		// we presume SizeOfStruct, coord_X and coord_Y fields are always present
		printf ("We are going to draw a circle at %d:%d\n", s->coord_X, s->coord_Y);

		if (s->SizeOfStruct>=sizeof(int)*4)
		{
			// this is at least ver2, color field is present
			printf ("We are going to set color %d\n", s->color);
		}

		if (s->SizeOfStruct>=sizeof(int)*5)
		{
			// this is at least ver3, fill_brush_type field is present
			printf ("We are going to fill it using brush type %d\n", s->fill_brush_type);
		}
	};

	// early software version
	void call_as_ver1()
	{
		struct ver1 s;
		s.SizeOfStruct=sizeof(s);
		s.coord_X=123;
		s.coord_Y=456;
		printf ("** %s()\n", __FUNCTION__);
		draw_circle(&s);
	};

	// next software version
	void call_as_ver2()
	{
		struct ver2 s;
		s.SizeOfStruct=sizeof(s);
		s.coord_X=123;
		s.coord_Y=456;
		s.color=1;
		printf ("** %s()\n", __FUNCTION__);
		draw_circle(&s);
	};

	// latest, most advanced version
	void call_as_ver3()
	{
		struct ver3 s;
		s.SizeOfStruct=sizeof(s);
		s.coord_X=123;
		s.coord_Y=456;
		s.color=1;
		s.fill_brush_type=3;
		printf ("** %s()\n", __FUNCTION__);
		draw_circle(&s);
	};

	int main()
	{
		call_as_ver1();
		call_as_ver2();
		call_as_ver3();
	};

In other words, *SizeOfStruct* field takes a role of *version of structure* field.
It could be enumerate type (1, 2, 3, etc), but to set *SizeOfStruct* field to *sizeof(struct...)*
is less prone to mistakes/bugs.

In C++, this problem is solved using [inheritance](https://github.com/dennis714/RE-for-beginners/tree/master/advanced/350_cpp/classes).
You just extend your base class (let's call it *Circle*),
and then you will have *ColoredCircle* and then *FilledColoredCircle*, and so on.
A current *version* of an object (or, more precisely, current *type*) will be determined using C++ *RTTI*.

So when you see *SizeOfStruct* somewhere in MSDN -- perhaps this structure was extended at least once in past.

