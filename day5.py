#!/usr/bin/python3

import sys
from intcode import IntCode

code = sys.stdin.read()
print(IntCode(code).run(1, True))
print(IntCode(code).run(5, True))
