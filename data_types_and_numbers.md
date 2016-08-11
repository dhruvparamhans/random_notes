# Integral datatypes

Integral datatype is a type for a value which can be converted to number.
These are numbers, enumerations, booleans.

## Bit

Obvious usage for bits are boolean values: 0 for *false* and 1 for *true*.

Set of booleans can be packed into *word*: there will be 32 booleans in 32-bit word, etc.
This way is called *bitmap* or *bitfield*.

But it has obvious overhead: a bit jiggling, isolating, etc.
Using while *word* (or *int* type) for boolean variable is not economic, but very fast.

In C/C++ environment, 0 is for *false* and any non-zero value is for *true*.
For example:

	if (1234)
		printf ("this will always be executed\n");
	else
		printf ("this will never\n");

## Nibble AKA nybble

AKA half-byte, tetrade.
Equals to 4 bits.

All these terms are still in use today.

### Binary-coded decimal (BCD)

4-bit nibbles were used in 4-bit CPUs like legendary Intel 4004 (used in calculators).

It's interesting to know that there was *binary-coded decimal* (BCD) way of representing decimal digit using 4 bits.
Decimal 0 is represented as 0b0000, decimal 9 as 0b1001 and higher values are not used.
Decimal 1234 is represented as 0x1234.
Of course, this way is not economical.

Nevertheless, it has one advantage: decimal to BCD-packed number conversion and back is extremely easy.
BCD-numbers can be added, subtracted, etc, but an additional correction is needed.
x86 CPUs has rare instructions for that: *AAA/DAA* (adjust after addition), *AAS/DAS* (... after subtraction),
*AAM* (after multiplication), *AAD* (after division).

The need for CPUs to support BCD numbers is a reason why *half-carry flag* (on 8080/Z80) and *auxiliary flag* (on x86)
are exist: this is carry-flag generated after proceeding of lower 4 bits. The flag is then used for adjustment instructions.

*BCD* instructions in x86 were often used for other purposes, especially in undocumented ways, for example:

	cmp al,10
	sbb al,69h
	das

(This obscure code converts number in 0..15 range into ASCII character '0'..'9', 'A'..'F'.)

The fact of easy conversion had led to popularity of [Peter Abel *IBM PC assembly language and programming* (1987)] book.
But aside of this book, the author of these notes never seen BCD numbers in practice, except for
[magic numbers](https://github.com/dennis714/RE-for-beginners/blob/5fe2c076ace7ac22bba6facdcf06600a0426fba6/digging_into_code/constants.tex) like when someone's birthday is encoded like 0x19861115 -- this is indeed packed BCD number.

### Z80

Z80 was clone of 8-bit Intel 8080 CPU, and because of space constraints, it has 4-bit *ALU*, i.e., each operation
over two 8-bit numbers had to be proceeded in two steps.
One side-effect of this was easy and natural generation of *half-carry flag*.

# Byte

Byte is primarly used for character storage.
8-bit bytes were not common as today.
Teletypes and punched tapes had 5 and 6 possible holes, this is 5 or 6 bits for byte.

To emphasize the fact the byte has 8 bits, byte is sometimes called *octet*: it least *fetchmail* uses this terminology.

9-bit bytes were exist in 36-bit architectures: 4 9-bit bytes were fit in single word.
Probably because of this fact, C/C++ standard tells that *char* has to have *at least* 8 bits.

## Standard ASCII table

7-bit ASCII table is standard, which has only 128 possible characters.
Early E-Mail transport software were operating only on 7-bit ASCII codes, so a MIME standard needed to encode messages
in non-Latin writing systems.
7-bit ASCII code was augmented by parity bit, resulting in 8 bits.

*Data Encryption Standard* (DES) has a 56 bits key, this is 8 7-bit bytes, leaving a space to parity bit for each character.

There is no need to memorize whole ASCII table, but ranges.
[0..0x1F] are not control characters (non-printable).
[0x20..0x7E] are printable ones.
Codes after 0x80 are usually used for non-Latin writing systems and/or pseudographics.

Significant codes which will be easily memorized are:
0 (end of C/C++ string, '\0' in C/C++);
0xA or 10 (line feed, '\n' in C/C++);
0xD or 13 (carriage return, '\r' in C/C++).

0x20 (space) is also often memorized.

## 8-bit CPUs

x86 has capability to work with byte(s) on register level (because they are descendents of 8-bit 8080 CPU),
RISC CPUs like ARM and MIPS -- not.

# Wide char

This is attempt to support multi-lingual environment by extending byte to 16-bit.
Most well-known example is Windows NT kernel and win32 functions with *W* suffix.
This is why each Latin character in text string is interleaved with zero byte.
This encoding is called UCS-2 or UTF-16

Usually, *wchar_t* is synonym to 16-bit *short*.

# Signed integer vs unsigned

Some may argue, why unsigned data types exist at first place, since any unsigned number can be represented as signed.
Yes, but absence of sign bit in a value extends its range twice.
Hence, signed byte has range of -128..127, and unsigned one: 0..255.
Another benefit of using unsigned data types is self-documenting: you define value which must not be negative.

Unsigned data types absent in Java, for which it's criticized.
It's hard to implement cryptographical algorithms using boolean operations over signed data types.

Values like 0xFFFFFFFF (-1) are used often, mostly as error codes.

# Word

*Word* word is somewhat ambiguous term and usually denotes a data type fitting in *General Purpose Register (GPR)*.
Bytes are practical for characters, but impractical for other arithmetical calculations.

Hence, many computers has GPRs with width of 16, 32 or 64 bits.
Even 8-bit CPUs like 8080 and Z80 offers to work with 8-bit register pairs, each pair forms 16-bit *pseudoregister*
(*BC*, *DE*, *HL*, etc).
Z80 has some capability to work with register pairs, making it as some kind of 16-bit CPU emulation.

In general, if a CPU marketed as "n-bit CPU", this usually means it has n-bit *GPRs*.

Hard to believe, but there was a time when hard disks and RAM modules were marketed as having *n* kilo-words instead of
*b* kilobytes/megabytes.
For example, [Apollo Guidance Computer](https://en.wikipedia.org/wiki/Apollo_Guidance_Computer) has 2048 words of RAM.
This was a 16-bit computer, so there was 4096 bytes of RAM.
[DECSYSTEM-2060](https://en.wikipedia.org/wiki/DECSYSTEM-20) could have up to 4096 kilowords of "solid state memory"
(i.e., hard disks, tapes, etc).
This was 36-bit computer, so this is 18432 kilobytes or ~18 megabytes.

---

By old standards, *int* in C/C++ is almost always mapped to *word*.
(Except of AMD64 architecture where *int* is still 32-bit one, perhaps, for the reason of better portability).

*int* is 16-bit on PDP-11 and old MS-DOS compilers.
*int* is 32-bit on VAX, on x86 starting at 80386, etc.

Even more than that, if type declaration is omitted in C/C++, *int* is used silently.
Perhaps, this is inheritance of [B programming language](http://yurichev.com/blog/typeless/).

---

*GPR* is usually fastest container for variable, faster than packed bit,
and sometimes even faster than byte (no need to isolate byte from *GPR*).
Even if you use it as a container for loop counter in *0..99* range.

---

*Word* is still 16-bit for x86, because it was so for 16-bit 8086.
*Double word* is 32-bit, *quad word* is 64-bit.
That's why 16-bit words are declared using *DW* in x86 assembly, 32-bit ones using *DD* and 64-bit ones using *DQ*.

*Word* is 32-bit for ARM, MIPS, etc., 16-bit data types are called *half-word* there. Hence, *double word* on 32-bit RISC
is 64-bit data type.

*GDB* has the following terminology: *halfword* for 16-bit, *word* for 32-bit and *giant word* for 64-bit.

16-bit C/C++ environment on PDP-11 MS-DOS has *long* data type with width of 32 bits, perhaps, they meant *long word* or
*long int*?

32-bit C/C++ environment has *long long* data type with width of 64 bits.

Now you see why the *word* word is ambiguous.

## Should I use *int*?

Some people argue that *int* shouldn't be used at all, because it ambiguity can lead to bugs.
For example, well-known *lzhuf* library uses *int* at one point and everything works fine on 16-bit architecture.
But if ported to architecture with 32-bit *int*, it [can be crashed](http://yurichev.com/blog/lzhuf/).

Less ambiguous types are [defined](https://en.wikipedia.org/wiki/C_data_types) in *stdint.h* file:
*uint8_t*, *uint16_t*, *uint32_t*, *uint64_t*, etc.

Some people like Donald E. Knuth [proposed](http://www-cs-faculty.stanford.edu/~uno/news98.html) more sonorous words
for these types: *byte/wyde/tetrabyte/octabyte*.
But these names are less popular than clear terms with inclusion of *u* (*unsigned*) character 
and number right into the type name.

## Word-oriented computers

Despite the ambiguity of the *word* term, modern computers are still word-oriented: *RAM* and all levels of cache
are still organized by words (they are marketed using *byte* term, though).
<!-- TODO word length on intel, etc... -->

Word-aligned RAM/cache access is always cheap, not-aligned may be not.

Effective data structures should always take into consideration lenght of the *word* on the CPU to be executed on.
Sometimes compiler do this for programmer, sometimes not.

# Address register

For those who fostered on 32-bit and/or 64-bit x86, and/or RISC of 90s like ARM, MIPS, PowerPC, it's natural that
address bus has the same width as *GPR* or *word*.
Nevertheless, width of address bus can be different on other architectures.

8-bit Z80 CPU can address 2^16 bytes, using 8-bit registers pairs or dedicated registers (*IX*, *IY*).
*SP* and *PC* registers are also 16-bit ones.

Cray-1 supercomputer has 64-bit GPRs, but 24-bit address registers, so it can address 2^24 (16 megawords or 128 megabytes).
Even for supercomputers RAM was expensive, and it cannot be expected in 1970s it could have more.
So why to allocate 64-bit register for address or pointer?

8086/8088 CPUs has really weird addressing scheme:
two 16-bit registers were summed in weird manner resulting 20-bit address.
Probably this was some kind of toy-level [virtualization](https://github.com/dennis714/RE-for-beginners/blob/5fe2c076ace7ac22bba6facdcf06600a0426fba6/other/8086mm.tex)?
8086 could run several programs (not simultaneously, though).

Early ARM1 has interesting artefact:

> Another interesting thing about the register file is the PC register is missing a few bits. Since the ARM1 uses 26-bit addresses, the top 6 bits are not used. Because all instructions are aligned on a 32-bit boundary, the bottom two address bits in the PC are always zero. These 8 bits are not only unused, they are omitted from the chip entirely.

( [Source](http://www.righto.com/2015/12/reverse-engineering-arm1-ancestor-of.html) )

Hence, it's physically not possible to push a value with one of two last bits set into PC register.
Nor it's possible to set any bits in high 6 bits of PC.

x86-64 architecture has virtual 64-bit pointers/addresses, but internally, width of address bus is 48 bits
(seems enough to address 256TB of RAM).

# Numbers

What numbers are used for?

When you see some number(s) altering in CPU register, you may be interesting, what this number means.
It's good skill for reverse engineering to determine possible data type from a set of changing numbers.

## Boolean

If the number is switching from 0 to 1 and back, most chances that this value has boolean data type.

## Loop counter, array index

Number increasing from 0, like: 0, 1, 2, 3 ... -- a good chance this is loop counter and/or array index.

## 32-bit number

There are numbers [so large](https://en.wikipedia.org/wiki/Large_numbers),
that there is even special notation for it exist ([Knuth's up-arrow notation](https://en.wikipedia.org/wiki/Knuth%27s_up-arrow_notation)).
These numbers are so large so these are not practical for engineering, science and mathematics.

Almost all engineers and scientists are happy with IEEE 754 double precision floating point, which has maximal
value around 1.8 * 10^308.

In fact, upper bound in practical computing is much, much lower.
If you get [source code of UNIX v6 for PDP-11](http://minnie.tuhs.org/Archive/PDP-11/Distributions/research/Dennis_v6/),
16-bit *int* is used everywhere while 32-bit *long* type is not used at all.

Same story was in MS-DOS era: 16-bit *int* was used almost for everything (array indices, loop counters),
while 32-bit *long* was used rarely.

During advent of x86-64, it was decided for *int* to stay as 32 bit size integer, because, probably,
usage of 64-bit *int* is even rarer.

I would say, 16-bit numbers in range (0..65535) are probably most used numbers in computing.

Given that, if you see unusually large 32-bit value like 0x87654321, this is a good chance this can be:
1) address (can be checked using memory map feature of debugger);
2) packed bytes (can be checked visually);
3) bit flags;
4) something related to (amateur) cryptography;
5) magic number;
6) IEEE 754 floating point number (can also be checked).

Almost same story for 64-bit values.

### ... so 16-bit *int* is enough for almost everything?

It's interesting to note: Michael Abrash in
[*Graphics Programming Black Book*](https://github.com/jagregory/abrash-black-book) (chapter 13)
writes there are plenty cases in which 16-bit values are just enough.
In a meantime, he has a pity that 80386 and 80486 CPUs has so little available registers, so he offers to put
two 16-bit values into one 32-bit register and then to rotate it using
*ROR reg, 16* (on 80386 and later) (*ROL reg, 16* will also work) or 
*BSWAP* (on 80486 and later) instruction.

That reminds us Z80 with alternate pack of registers (suffixed with apostrophe), to which CPU can switch
(and then switch back) using *EXX* instruction.

## Size of buffer

When a programmer need to declare a size of some buffer, values like 2^x are usually used (512 bytes, 1024, etc).
Values in 2^x form are [easily recognizable](https://github.com/dennis714/RE-for-beginners/blob/4d7a5a76a6af147417737455e4036f22e427f466/patterns/14_bitfields/4_popcnt/main_EN.tex) in both decimal, hexadecimal and binary forms.

But needless to say, programmers are still humans with their decimal culture.
And somehow, in DBMS area, size of textual database fields is often declared as 10^x number, like 100, 200.
They just think "Okay, 100 is enough, wait, 200 will be better".
And they are right, of course.

Maximum width of VARCHAR2 data type in Oracle RDBMS is 4000 characters, not 4096.

There is nothing wrong with this, this is just a place where numbers like 10^x can be encountered.

## Address

It's always good idea to keep in mind approximate memory map of the process you currently debug.
For example, many win32 executables started at 0x00401000, so address like 0x00451230 is probably located inside
executable section. You'll see addresses like these in EIP register.

Stack is usually located somewhere below (TODO).

Many debuggers is able to show the memory map of the debuggee, for example,
[OllyDbg](https://github.com/dennis714/RE-for-beginners/blob/efa9770edc1f23f020ac1bc25bc52b3595480010/patterns/04_scanf/2_global/ex2_olly_2.png).

If a value is increasing by step 4 on 32-bit architecture or by step 8 on 64-bit one,
this probably sliding address of some element of array.

It's important to know that win32 doesn't use addresses below 0x1000 (TODO), so if you see some number below this value,
this cannot be an address.

Anyway, many debuggers can show you if the value in a register can be an address to something.
OllyDbg can also show an ASCII string if the value is an address of it.

## Bit field

If you see a value where one (or more) bit(s) are flipping from time to time like 0xABCD1234 -> 0xABCD1434 and back,
this is probably bit field (or bitmap).

## Packed bytes

When strcmp() or memcmp() copies a buffer, it loads/stores 4 (or 8) bytes simultaneously,
so if a string containing "4321" would be copied to another place,
at one point you'll see 0x31323334 value in register.
This is 4 packed bytes into 32-bit value.

