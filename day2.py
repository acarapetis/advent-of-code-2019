#!/usr/bin/python3

import sys

data = sys.stdin.read()
code = [int(s) for s in data.split(',')]

i = 0

def result(noun, verb):
    mem = code.copy()
    mem[1] = noun
    mem[2] = verb
    op = iter(mem)
    while True:
        x = next(op)
        if x == 99:
            return mem[0]
        elif x == 1:
            out = mem[next(op)] + mem[next(op)]
            mem[next(op)] = out
        elif x == 2:
            out = mem[next(op)] * mem[next(op)]
            mem[next(op)] = out

def invert(target):
    for noun in range(99):
        for verb in range(99):
            if result(noun, verb) == target:
                return 100 * noun + verb

print(result(12, 2))
print(invert(19690720))
