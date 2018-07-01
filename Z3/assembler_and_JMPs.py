from z3 import *

"""

Choosing between short/long jumps in x86 assembler using Z3 SMT-solver

As you may know, there are two JMP instructions in x86: short one (EB xx) and long one (E9 xx xx xx xx).
The first can encode "short offsets": [current_address-127 ... current_address+128], the second can encode 32-bit offset.
During assembling (converting assembly code into machine opcodes) you can put "long" JMPs, and it's OK.
But here is a problem: you may want to make your code as tight as possible and use "short" JMPs whenever possible.
Given the fact that JMPs are inside code itself and affecting code size.
What can you do?

This is an example of some assembly program:

label_1:
         +---------+
         |         |
         | block 1 |    block1_size
         |         |
         +---------+
         JMP label_3    JMP_1_size
label_2:
         +---------+
         |         |
         | block 2 |    block2_size
         |         |
         +---------+
         JMP label_5    JMP_2_size
label_3:
         +---------+
         |         |
         | block 3 |    block3_size
         |         |
         +---------+
         JMP label_2    JMP_3_size
label_4:
         +---------+
         |         |
         | block 4 |    block4_size
         |         |
         +---------+
         JMP label_1    JMP_4_size
label_5:
         +---------+
         |         |
         | block 5 |    block5_size
         |         |
         +---------+
         JMP label_3    JMP_5_size

"""

# this is simplification, "back" offsets are limited by 127 bytes, "forward" ones by 128 bytes, but OK, let's say,
# all of them are 128:
def JMP_size (offset):
    return If(offset>128, 5, 2)

block1_size=64
block2_size=81
block3_size=12
block4_size=50
block5_size=60

s=Optimize()

JMP_1_size=Int('JMP_1_size')
JMP_2_size=Int('JMP_2_size')
JMP_3_size=Int('JMP_3_size')
JMP_4_size=Int('JMP_4_size')
JMP_5_size=Int('JMP_5_size')

JMP_1_offset=Int('JMP_1_offset')
JMP_2_offset=Int('JMP_2_offset')
JMP_3_offset=Int('JMP_3_offset')
JMP_4_offset=Int('JMP_4_offset')
JMP_5_offset=Int('JMP_5_offset')

# calculate all JMPs offsets, these are block sizes and also other's JMPs sizes between the current address
# and desination address:
s.add(JMP_1_offset==block2_size+JMP_2_size)
s.add(JMP_2_offset==block3_size+JMP_3_size + block4_size+JMP_4_size)
s.add(JMP_3_offset==block2_size+JMP_2_size + block3_size)
s.add(JMP_4_offset==block1_size+JMP_1_size + block2_size+JMP_2_size + block3_size+JMP_3_size + block4_size)
s.add(JMP_5_offset==block3_size+JMP_3_size + block4_size+JMP_4_size + block5_size)

# what are sizes of all JMPs, 2 or 5?
s.add(JMP_1_size==JMP_size(JMP_1_offset))
s.add(JMP_2_size==JMP_size(JMP_2_offset))
s.add(JMP_3_size==JMP_size(JMP_3_offset))
s.add(JMP_4_size==JMP_size(JMP_4_offset))
s.add(JMP_5_size==JMP_size(JMP_5_offset))

# minimize size of all jumps (this is optimization problem):
s.minimize(JMP_1_size + JMP_2_size + JMP_3_size + JMP_4_size + JMP_5_size)

print s.check()
print s.model()

"""
The result:

sat
[JMP_2_size = 2,
 JMP_1_offset = 83,
 JMP_5_size = 5,
 JMP_5_offset = 129,
 JMP_2_offset = 69,
 JMP_4_size = 5,
 JMP_4_offset = 213,
 JMP_1_size = 2,
 JMP_3_size = 2,
 JMP_3_offset = 95]

I.e., JMP_4 and JMP_5 JMPs must be "long" ones, others can be "short" ones.

Other simplification I made for the sake of example: "short" conditional Jcc's can also be encoded using 2 bytes,
"long" ones using 6 bytes rather than 5 (5 is unconditional JMP).

"""
