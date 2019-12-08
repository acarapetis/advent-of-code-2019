#!/usr/bin/python3

import sys
from intcode import IntCode

code = sys.stdin.read()

def result(noun, verb):
    computer = IntCode(code, noun=noun, verb=verb)
    return computer.run()

def invert(target):
    for noun in range(99):
        for verb in range(99):
            if result(noun, verb) == target:
                return 100 * noun + verb

print(result(12, 2))
print(invert(19690720))
