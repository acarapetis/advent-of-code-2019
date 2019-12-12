#!/usr/bin/python3

from intcode import IntProc

machine = IntProc()
machine.write(1)
while True:
    try:
        print(machine.read())
    except EOFError:
        break
