#!/usr/bin/python3

import intcode
from collections import defaultdict
from screen import display

machine = intcode.IntProc()
canvas = defaultdict(lambda: -1)
droid = (0,0)
canvas[droid] = 3

directions = {(0,1): 1, (0,-1): 2, (-1,0): 3, (1,0): 4}

def nbhd(p):
    return (add(p,q) for q in directions)

def floodcreep(paint):
    r = set(paint)
    for p in paint:
        for q in nbhd(p):
            if canvas[q] != 0:
                r.add(q)
    return r

def astar_field(pt, ref=None):
    s = {pt}
    field = defaultdict(lambda: 9999)
    field[pt] = 0
    i = 0
    same = False
    while not (same or ref in s):
        i += 1
        new = floodcreep(s)
        for p in new:
            if p not in s:
                field[p] = i
        same = new == s
        s = new
    return field

def add(p,q):
    return (p[0]+q[0],p[1]+q[1])

def move_towards(pt):
    f = astar_field(pt, droid)
    return min(directions, key=lambda d: f[add(droid,d)])

def closest_unknown():
    xs = {droid}
    while True:
        new = floodcreep(xs)
        if new == xs:
            return None
        xs = new
        for x in xs:
            if canvas[x] == -1:
                return x

while True:
    # pathfind to closest foggy tile
    u = closest_unknown()
    if not u:
        # we've explored everywhere
        break
    d = move_towards(u)
    target = add(droid, d)
    machine.write(directions[d])
    result = machine.read()
    canvas[target] = result
    #display(canvas, { -1: ' ', 0: '#', 1: '.', 2: '>', 3: '<' })
    if result != 0:
        droid = target
    if result == 2:
        oxy = target

machine.worker.terminate()

f = astar_field(oxy)
print(f[(0,0)])
print(max(x for x in f.values()
          if x is not 9999))
