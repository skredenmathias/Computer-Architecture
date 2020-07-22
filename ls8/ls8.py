#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) < 2:
    print('please provide a file name')
    exit()
else:
    filename = sys.argv[1]


cpu = CPU()

cpu.load(filename)
cpu.run()