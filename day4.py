#!/usr/bin/python3

import sys, re

start = int(sys.stdin.read(6))
sys.stdin.read(1)
end = int(sys.stdin.read(6))

# Brute force ahoy

def match(n, day=1):
    digits = [int(d) for d in str(n)]
    i=0
    for d in digits:
        if d < i:
            return False
        i = d
    repeats = [xx for xx, x in re.findall(r'((\d)\2+)', str(n))]
    if day == 1:
        return len(repeats) > 0
    return any(len(xx) == 2 for xx in repeats)

def solncount(day):
    return sum(1 for x in range(start, end+1)
               if match(x, day=day))

print(solncount(1))
print(solncount(2))
