# My experience with Hex-Rays 2.2.0

## Bugs

There are couple of bugs.

First of all, Hex-Rays lost when FPU instructions are interleaved (by compiler codegenerator) with others.

For example, this:

	f               proc    near

                	lea     eax, [esp+4]
        	        fild    dword ptr [eax]
	                lea     eax, [esp+8]
                	fild    dword ptr [eax]
        	        fabs
	                fcompp
                	fnstsw  ax
        	        test    ah, 1
	                jz      l01

                	mov     eax, 1
        	        retn
	l01:
	                mov     eax, 2
        	        retn

	f               endp

... will be correcly decompiled to:

	signed int __cdecl f(signed int a1, signed int a2)
	{
	  signed int result; // eax@2

	  if ( fabs((double)a2) >= (double)a1 )
	    result = 2;
	  else
	    result = 1;
	  return result;
	}

But let's comment one of the instructions at the end:

	...
	l01:
        	        ;mov    eax, 2
                	retn
	...

... we getting an obvious bug:

	void __cdecl f(char a1, char a2)
	{
	  fabs((double)a2);
	}

This is another bug:

	extrn f1:dword
	extrn f2:dword

	f               proc    near

        	        fld     dword ptr [esp+4]
                	fadd    dword ptr [esp+8]
	                fst     dword ptr [esp+12]
        	        fcomp   ds:const_100
	                fld     dword ptr [esp+16]      ; comment this ins and it will be OK
        	        fnstsw  ax
                	test    ah, 1

	                jnz     short l01

        	        call    f1
                	retn
	l01:
        	        call    f2
                	retn

	f               endp

	...

	const_100       dd 42C80000h            ; 100.0

Result:

	int __cdecl f(float a1, float a2, float a3, float a4)
	{
	  double v5; // st7@1
	  char v6; // c0@1
	  int result; // eax@2

	  v5 = a4;
	  if ( v6 )
	    result = f2(v5);
	  else
	    result = f1(v5);
	  return result;
	}

v6 variable has "char" type and if you'll try to compile this code, compiler will warn you about variable
usage before assignment.

Another bug: FPATAN instruction is correctly decompiled into atan2(), but arguments are swapped.

## Odd peculiarities

Hex-Rays too often promotes 32-bit int to 64-bit one.
Here is example:

	f               proc    near

        	        mov     eax, [esp+4]
	                cdq
        	        xor     eax, edx
                	sub     eax, edx
	                ; EAX=abs(a1)

        	        sub     eax, [esp+8]
                	; EAX=EAX-a2

	                ; EAX at this point somehow gets promoted to 64-bit integer (RAX)

        	        cdq
                	xor     eax, edx
	                sub     eax, edx
        	        ; EAX=abs(abs(a1)-a2)

	                retn

	f               endp

Result:

	int __cdecl f(int a1, int a2)
	{
	  __int64 v2; // rax@1

	  v2 = abs(a1) - a2;
	  return (HIDWORD(v2) ^ v2) - HIDWORD(v2);
	}

Perhaps, this is result of CDQ instruction? I'm not sure.
Anyway, whenever you see \_\_int64 type in 32-bit code, pay attention.

This is also weird:

	f               proc    near

        	        mov     esi, [esp+4]

                	lea     ebx, [esi+10h]
	                cmp     esi, ebx
        	        jge     short l00

	                cmp     esi, 1000
        	        jg      short l00

	                mov     eax, 2
        	        retn

	l00:
        	        mov     eax, 1
                	retn

	f               endp

Result:

	signed int __cdecl f(signed int a1)
	{
	  signed int result; // eax@3

	  if ( __OFSUB__(a1, a1 + 16) ^ 1 && a1 <= 1000 )
	    result = 2;
	  else
	    result = 1;
	  return result;
	}

The code is correct, but needs manual intervention.

Sometimes, Hex-Rays doesn't fold division by multiplication code:

	f               proc    near

                	mov     eax, [esp+4]
        	        mov     edx, 2AAAAAABh
	                imul    edx
                	mov     eax, edx

        	        retn

	f               endp

Result:

	int __cdecl f(int a1)
	{
	  return (unsigned __int64)(715827883i64 * a1) >> 32;
	}

This can be folded manually.

Many of these peculiarities can be solved by manual reordering of instructions, recompiling assembly code,
and then feeding it to Hex-Rays again.

## Silence

	extrn some_func:dword

	f               proc    near

                	mov     ecx, [esp+4]
        	        mov     eax, [esp+8]
	                push    eax
                	call    some_func
        	        add     esp, 4

	                ; use ECX
                	mov     eax, ecx

        	        retn

	f               endp

Result:

	int __cdecl f(int a1, int a2)
	{
	  int v2; // ecx@1

	  some_func(a2);
	  return v2;
	}

v2 variable (from ECX) is lost...
Yes, this code is incorrect, but it would be good for Hex-Rays to give a warning.

Another one:

	extrn some_func:dword

	f               proc    near

        	        call    some_func
                	jnz     l01

	                mov     eax, 1
        	        retn
	l01:
        	        mov     eax, 2
                	retn

	f               endp

Result:

	signed int f()
	{
	  char v0; // zf@1
	  signed int result; // eax@2

	  some_func();
	  if ( v0 )
	    result = 1;
	  else
	    result = 2;
	  return result;
	}

Again, warning would be great.

Anyway, whenever you see variable of char type, or variable which is used without assignment, this is clear sign
that something went wrong and needs manual intervention.

## Comma

Comma in C/C++ has a bad fame, because it can lead to a confusing code.

Quick quiz, what does this C/C++ function returns?

	int f()
	{
		return 1, 2;
	};

It's 2: when compiler encounters comma-expression, it generates code which executes all sub-expressions, and
"returns" value of the last sub-expression.

I've seen something like that in production code:

	if (cond)
		return global_var=123, 456; // 456 is returned
	else
		return global_var=789, 321; // 321 is returned

Apparently, programmer wanted to make code slightly shorter without additional curly brackets.
In other words, comma allows to pack couple of expressions into one, without forming
statement/code block inside of curly brackets.

Comma in C/C++ is close to "begin" in Scheme/Racket: https://docs.racket-lang.org/guide/begin.html

Perhaps, the only legitimate usage of comma is in for() statements:

	char *s="hello, world";
	for(int i=0; *s; s++, i++);
	; i = string lenght

Both s++ and i++ are executed at each loop iteration.

Read more: http://stackoverflow.com/questions/52550/what-does-the-comma-operator-do-in-c

I'm writing all this because Hex-Rays produces (at least in my case) code which is rich with both commas and short-circuit
expressions.
For example, this is real output from Hex-Rays:

	 if ( a >= b || (c = a, (d[a] - e) >> 2 > f) )
	    {
	    	...

This is correct, it compiles and works, and let god help you to understand it.
Here is it rewritten:

	if (cond1 || (comma_expr, cond2))
	{
		...

Short-circuit is effective here: first cond1 is checked, if it's true, if() body is executed, the the rest
of if() expression is ignored completely.
If cond1 is false, comma\_expr is executed (in the previous example, "a" is copied to "c"), then cond2 is checked.
If cond2 is true, again, if() body is executed, if it's not, body isn't executed.
In other words, if() body gets executed if cond1 is true or cond2 is true, but if the latter is true,
comma\_expr is also executed.

A common beginner's misconception is that sub-conditions are checked in some unspecified order, which is not true.

Now you can see why comma is so notorious.

## Data types

Data types is a problem for decompilers.

Hex-Rays can be blind to arrays in local stack, if they weren't set correctly before decompilation.
Same story about global arrays.

Another problem is too big functions, where a single slot in local array can be used by several variables
across function's execution.
It's not a rare case when a slot is used for int-variable, then for pointer, then for float-variable.
Hex-Rays correctly decompiles it: it creates a variable with some type, then cast it to another type in various
parts of functions.
This problem has been solved by me by manual splitting big function into several.
Just make local variables as global ones, etc, etc.
And don't forget about tests.

## My plan

* Split big functions (and don't forget about tests).
Sometimes it's very helpful to form new functions out of big loop bodies.

* Check/set data type of variables, arrays, etc.

* If you see odd output, dangling variable (which used before assignment), try to swap instructions manually,
recompile it and feed to Hex-Rays again.

## Summary

Nevertheless, quality of Hex-Rays 2.2.0 is very, very good.
It makes life way easier.

