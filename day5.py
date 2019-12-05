#!/usr/bin/python3

import sys

data = sys.stdin.read()
code = [int(s) for s in data.split(',')]

def result(inval=1, noun=None, verb=None):
    mem = code.copy()
    if noun:
        mem[1] = noun
    if verb:
        mem[2] = verb
    i = 0

    def nx():
        nonlocal i
        i += 1
        return mem[i-1]

    while True:
        c = nx()
        x = c % 100
        param_modes = list('000' + str(c//100))

        def getparam():
            v = nx()
            if param_modes.pop() == '1':
                return v
            return mem[v]

        if x == 99:
            return mem[0]
        elif x == 1:
            out = getparam() + getparam()
            mem[nx()] = out
        elif x == 2:
            out = getparam() * getparam()
            mem[nx()] = out
        elif x == 3:
            mem[nx()] = inval
        elif x == 4:
            print(getparam())
        elif x == 5:
            cond, addr = getparam(), getparam()
            if cond != 0:
                i = addr
        elif x == 6:
            cond, addr = getparam(), getparam()
            if cond == 0:
                i = addr
        elif x == 7:
            a, b = getparam(), getparam()
            mem[nx()] = 1 if a < b else 0
        elif x == 8:
            a, b = getparam(), getparam()
            mem[nx()] = 1 if a == b else 0

result(inval=1)
result(inval=5)
