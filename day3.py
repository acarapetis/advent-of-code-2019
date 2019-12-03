#!/usr/bin/python3

import sys, re
import numpy as np

data = open('day3.txt').read()
lines = [l.strip() for l in data.splitlines()]
def parse_cmd(string):
    [direction, *strary] = string
    return direction, int(''.join(strary))

dirs = {
    'R': (1,0),
    'L': (-1,0),
    'U': (0,-1),
    'D': (0,1),
}
def add(x, y):
    return (x[0]+y[0], x[1]+y[1])

def parse_wire(line):
    commands = map(parse_cmd, line.split(','))
    out = []
    pos = (0,0)
    s = 0
    delays = {}
    for direction, mag in commands:
        for i in range(mag):
            s += 1
            pos = add(pos, dirs[direction])
            out.append(pos)
            delays[pos] = s
    return out, delays

wires = list(map(parse_wire, lines))
wire0 = set(wires[0][0])
wire1 = set(wires[1][0])
delay0 = wires[0][1]
delay1 = wires[1][1]
intersections = [x for x in wire0 if x in wire1]

def dist(x):
    return abs(x[0]) + abs(x[1])

print(min(map(dist, intersections)))

def delay(coord):
    return delay0[coord] + delay1[coord]

print(min(map(delay, intersections)))
