#!/usr/bin/python3

import sys, re

def fuel(x):
    return x//3 - 2

def megafuel(x):
    f = x
    t = 0
    while f > 0:
        f = fuel(f)
        if f>0: t += f
    return t

lines = sys.stdin.readlines()
nums = [int(line) for line in lines]

print(sum(map(fuel, nums)))
print(sum(map(megafuel, nums)))
