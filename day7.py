#!/usr/bin/python3

import sys
from intcode import IntCode, Terminated
from itertools import permutations

class Amplifier(IntCode):
    def __init__(self, *a, phase_setting, **kw):
        super().__init__(*a, **kw)
        self.phase_setting = phase_setting

    def reset(self, *a, **k):
        self._has_read_phase = False
        return super().reset(*a, **k)

    def _input(self):
        if self._has_read_phase:
            return super()._input()
        else:
            self._has_read_phase = True
            return self.phase_setting

code = sys.stdin.read()
def signal(phases):
    A, B, C, D, E = (Amplifier(code, phase_setting=p, name=n) for p, n in
                     zip(phases,'ABCDE'))
    b = A.run(0, True)
    c = B.run(b, True)
    d = C.run(c, True)
    e = D.run(d, True)
    v = E.run(e, True)
    return v

print(max(signal(p) for p in permutations(range(5))))

def loop_signal(phases):
    A, B, C, D, E = (Amplifier(code, phase_setting=p, name=n,
                               raise_on_terminate=True)
                     for p, n in zip(phases,'ABCDE'))
    v = 0
    try:
        while True:
            A.write(v)
            B.write(A.read())
            C.write(B.read())
            D.write(C.read())
            E.write(D.read())
            v = E.read()
    except Terminated:
        return v

print(max(loop_signal(p) for p in permutations(range(5, 10))))
