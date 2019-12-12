#!/usr/bin/python3

from intcode import IntProc
comp = IntProc()

for part in (1, 2):
    print(f"Part {part} output:")
    comp.reset()
    comp.write(part)
    while True:
        try:
            print(comp.read())
        except EOFError:
            break
