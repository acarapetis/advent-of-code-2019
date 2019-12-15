#!/usr/bin/python3
import sys
from intcode import IntProc, Terminated
from collections import defaultdict

code = sys.stdin.read()
def run_robot(starting_color=0):
    pos = (0,0)
    facing = (0,1)
    canvas = defaultdict(lambda: 0)
    canvas[pos] = starting_color
    cpu = IntProc(code)

    def rotate(v):
        nonlocal facing
        if v:
            facing = (facing[1], -facing[0])
        else:
            facing = (-facing[1], facing[0])
    def move():
        nonlocal pos
        pos = (pos[0] + facing[0], pos[1] + facing[1])

    while True:
        try:
            cpu.write(canvas[pos])
            canvas[pos] = cpu.read()
            rotate(cpu.read())
            move()
        except Terminated:
            return canvas

print(len(run_robot(0)))
registration = run_robot(1)

xmin = min(x[0] for x in registration.keys())
ymin = min(x[1] for x in registration.keys())
xmax = max(x[0] for x in registration.keys())
ymax = max(x[1] for x in registration.keys())

for y in range(ymax, ymin-1, -1):
    for x in range(xmin, xmax+1):
        print(registration[(x,y)] and '#' or '.', end='')
    print()
