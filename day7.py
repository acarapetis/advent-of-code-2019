#!/usr/bin/python3

import sys
from intcode import IntCode, Terminated, IntProc
from itertools import permutations

class Amplifier(IntProc):
    def __init__(self, *a, phase_setting, **kw):
        self.phase_setting = phase_setting
        super().__init__(*a, **kw)

    def reset(self, *a, **k):
        super().reset(*a, **k)
        self.write(self.phase_setting)

code = sys.stdin.read()
def signal(phases):
    A, B, C, D, E = (Amplifier(code, phase_setting=p) for p in phases)
    A.write(0)
    B.write(A.read())
    C.write(B.read())
    D.write(C.read())
    E.write(D.read())
    return E.read()

print(max(signal(p) for p in permutations(range(5))))

def loop_signal(phases):
    A, B, C, D, E = (Amplifier(code, phase_setting=p) for p in phases)
    v = 0
    try:
        while True:
            A.write(v)
            B.write(A.read())
            C.write(B.read())
            D.write(C.read())
            E.write(D.read())
            v = E.read()
    except (EOFError, BrokenPipeError):
        return v

print(max(loop_signal(p) for p in permutations(range(5, 10))))
