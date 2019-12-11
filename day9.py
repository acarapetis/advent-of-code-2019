#!/usr/bin/python3

import sys
from intcode import IntCode, Terminated
code = sys.stdin.read()
comp = IntCode(code, raise_on_terminate=True)

for part in (1, 2):
    print(f"Part {part} output:")
    comp.reset()
    comp.write(part)
    while True:
        try:
            print(comp.read())
        except Terminated:
            break
