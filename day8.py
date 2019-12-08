#!/usr/bin/python3
import sys, re
layers = []

while True:
    v = sys.stdin.read(6*25)
    if not v:
        break
    try:
        layers += [[int(x) for x in v]]
    except:
        pass

def dcount(n):
    return lambda l: sum(1 for x in l if x==n)

layer = min(layers, key=dcount(0))
print(dcount(1)(layer) * dcount(2)(layer))

import numpy as np
layers = [np.asarray(x) for x in layers]
canvas = np.ones_like(layers[0])*2
for l in layers:
    canvas[canvas == 2] = l[canvas == 2]

x = np.zeros_like(canvas, dtype=str)
x[canvas == 0] = ' '
x[canvas == 1] = '*'

for line in np.reshape(x, (6,25)):
    print(''.join(line))
