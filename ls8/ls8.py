#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

instructions = []

if len(sys.argv) != 2:
    print("Error: no filename given!")
    sys.exit(1)

with open(sys.argv[1]) as f:
    for i in f:
        i = i.split(' ')[0]
        i = i.split('#')[0]
        if len(i) >= 8:
            instructions.append(int(i, 2))

f.close()

cpu = CPU()

cpu.load(instructions)
cpu.run()