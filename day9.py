#!/usr/bin/python3

from intcode import IntCode, Terminated, Memory
import sys
code = sys.stdin.read()
comp = IntCode(code, raise_on_terminate=True)
comp.write(2)
while True:
    try:
        print(comp.read())
    except Terminated:
        print('TERM')
        break
