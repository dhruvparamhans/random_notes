(The note below has been copypasted to the [Reverse Engineering for Beginners book](http://beginners.re/))

# memmove() and memcpy()

The difference between these standard functions is that *memcpy()* blindly copies a block to another place,
while *memmove()* correctly handles overlapping blocks.
For example, you need to tug a string two bytes forward:

`|.|.|h|e|l|l|o|...` -> `|h|e|l|l|o|...`

memcpy() which copies 32-bit or 64-bit words at once, or even SIMD, will obviously fail here, a byte-wise copy routine
should be used instead.

Now even more complex example, insert two bytes in front of string:

`|h|e|l|l|o|...` -> `|.|.|h|e|l|l|o|...`

Now even byte-wise memory copy routine will fail, you need to copy bytes starting at the end.

That's a rare case where *DF* x86 flag is to be set before *REP MOVSB* instruction: *DF* defines direction, and now
we need to move backwardly.

The typical memmove() routine works like this:
1) if source is below destination, copy forward;
2) if source is above destination, copy backward.

This is memmove() from uClibc:

	void *memmove(void *dest, const void *src, size_t n)
	{
		int eax, ecx, esi, edi;
		__asm__ __volatile__(
			"	movl	%%eax, %%edi\n"
			"	cmpl	%%esi, %%eax\n"
			"	je	2f\n" /* (optional) src == dest -> NOP */
			"	jb	1f\n" /* src > dest -> simple copy */
			"	leal	-1(%%esi,%%ecx), %%esi\n"
			"	leal	-1(%%eax,%%ecx), %%edi\n"
			"	std\n"
			"1:	rep; movsb\n"
			"	cld\n"
			"2:\n"
			: "=&c" (ecx), "=&S" (esi), "=&a" (eax), "=&D" (edi)
			: "0" (n), "1" (src), "2" (dest)
			: "memory"
		);
		return (void*)eax;
	}

In the first case, *REP MOVSB* is called with *DF* flag cleared.
In the second, *DF* is set, then cleared.

More complex algorithm has the following piece in it:
"if difference between *source* and *destination* is larger than width of *word*, copy using words rather then bytes,
and use byte-wise copy to copy unaligned parts".
This how it happens in Glibc 2.24 in non-optimized C part.

Given all that, *memmove()* may be slower than *memcpy()*.
But some people, including Linus Torvalds, [argue](https://bugzilla.redhat.com/show_bug.cgi?id=638477#c132)
that *memmove()* should be an alias of *memcpy()*, and the single
function should just check at start, if the buffers are overlapping or not, and then behave as *memcpy()* or *memmove()*.
Nowadays, check for overlapping buffers is very cheap, after all.

## Anti-debugging trick

I've heard about anti-debugging trick where all you need is just set *DF* to crash the process: the very next *memcpy()*
routine crashes because it copies backwardly.
But I can't check this: it seems all memory copy routines clears/sets *DF* as they need to.
On the other hand, *memmove()* from uClibc I cited in this article,
has no explicit clear of *DF* (it assumes *DF* is always clear?),
so it can really crash.

