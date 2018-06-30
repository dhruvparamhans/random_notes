from z3 import *

"""

Choosing between short/long jumps in x86 assembler using Z3 SMT-solver

As you may know, there are two JMP instructions in x86: short one (EB xx) and long one (E9 xx xx xx xx).
The first can encode offsets [current_address-127 ... current_address+128], the second can encode 32-bit offset.
During assembling (converting assembly code into machine opcodes) you can put "long" JMPs, and it's OK.
But here is a problem: you may want to make your code as tight as possible and use "short" JMPs whenever possible.
What can you do?

This is an example of some assembly program:

label_1:
         +---------+
         |         |
         | block 1 |    block1_size
         |         |
         +---------+
         Jxx label_3    Jxx_1_size
label_2:
         +---------+
         |         |
         | block 2 |    block2_size
         |         |
         +---------+
         Jxx label_5    Jxx_2_size
label_3:
         +---------+
         |         |
         | block 3 |    block3_size
         |         |
         +---------+
         Jxx label_2    Jxx_3_size
label_4:
         +---------+
         |         |
         | block 4 |    block4_size
         |         |
         +---------+
         Jxx label_1    Jxx_4_size
label_5:
         +---------+
         |         |
         | block 5 |    block5_size
         |         |
         +---------+
         Jxx label_3    Jxx_5_size

"""

# this is simplification, "back" offsets are limited by 127 bytes, "forward" ones by 128 bytes, but OK, let's say,
# all of them are 128:
def Jxx_size (offset):
    return If(offset>128, 5, 2)

block1_size=64
block2_size=81
block3_size=12
block4_size=50
block5_size=60

s=Optimize()

Jxx_1_size=Int('Jxx_1_size')
Jxx_2_size=Int('Jxx_2_size')
Jxx_3_size=Int('Jxx_3_size')
Jxx_4_size=Int('Jxx_4_size')
Jxx_5_size=Int('Jxx_5_size')

Jxx_1_offset=Int('Jxx_1_offset')
Jxx_2_offset=Int('Jxx_2_offset')
Jxx_3_offset=Int('Jxx_3_offset')
Jxx_4_offset=Int('Jxx_4_offset')
Jxx_5_offset=Int('Jxx_5_offset')

# calculate all JMPs offsets, these are block sizes and also other's JMPs sizes between the current address
# and desination address:
s.add(Jxx_1_offset==block2_size+Jxx_2_size)
s.add(Jxx_2_offset==block3_size+Jxx_3_size + block4_size+Jxx_4_size)
s.add(Jxx_3_offset==block2_size+Jxx_2_size + block3_size)
s.add(Jxx_4_offset==block1_size+Jxx_1_size + block2_size+Jxx_2_size + block3_size+Jxx_3_size + block4_size)
s.add(Jxx_5_offset==block3_size+Jxx_3_size + block4_size+Jxx_4_size + block5_size)

# what are sizes of all JMPs, 2 or 5?
s.add(Jxx_1_size==Jxx_size(Jxx_1_offset))
s.add(Jxx_2_size==Jxx_size(Jxx_2_offset))
s.add(Jxx_3_size==Jxx_size(Jxx_3_offset))
s.add(Jxx_4_size==Jxx_size(Jxx_4_offset))
s.add(Jxx_5_size==Jxx_size(Jxx_5_offset))

# minimize sizes of all jumps (this is optimization problem):
s.minimize(Jxx_1_size + Jxx_2_size + Jxx_3_size + Jxx_4_size + Jxx_5_size)

print s.check()
print s.model()

"""
The result:

sat
[Jxx_2_size = 2,
 Jxx_1_offset = 83,
 Jxx_5_size = 5,
 Jxx_5_offset = 129,
 Jxx_2_offset = 69,
 Jxx_4_size = 5,
 Jxx_4_offset = 213,
 Jxx_1_size = 2,
 Jxx_3_size = 2,
 Jxx_3_offset = 95]

I.e., Jxx_4 and Jxx_5 JMPs must be "long" ones, others can be "short" ones.

Other simplification I made for the sake of example: "short" conditional JMPs can also be encoded using 2 bytes,
"long" ones using 6 bytes rather than 5 (5 is unconditional JMP).

"""
