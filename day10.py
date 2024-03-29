#!/usr/bin/python3
import sys, re, numpy as np

data = [l.strip() for l in sys.stdin.readlines()]
asteroids = np.asarray([[x == '#' for x in list(line)] for line in data],
                       dtype=bool)

def blocked(station, blockers, coord):
    if np.all(coord == station):
        return True
    others = np.any(blockers != station, axis=1)
    b = blockers[others,:]
    ratio = (np.asarray(coord - station, dtype=float) /
        np.asarray(b - station, dtype=float))
    diag = np.all(b != station, axis=1) \
        & (ratio[:,0]==ratio[:,1]) \
        & (ratio[:,0] > 1)
    ax0 = (coord[0] == station[0]) & (b[:,0] == station[0]) & (ratio[:,1] > 1)
    ax1 = (coord[1] == station[1]) & (b[:,1] == station[1]) & (ratio[:,0] > 1)
    return np.any(diag | ax0 | ax1)

astcoords = np.argwhere(asteroids)
def nvisible(station):
    return sum(0 if blocked(station, astcoords, c) else 1
               for c in astcoords if not np.all(c == station))

best_station = max(astcoords, key=nvisible)
print(nvisible(best_station))

def angle(x):
    from math import atan2
    return -atan2(x[1]-best_station[1], 
                  x[0]-best_station[0])

targets = astcoords.copy()
destroyed = 0
while len(targets) > 0:
    remainder = [x for x in targets
                 if blocked(best_station, targets, x)]
    next_destroyed = len(astcoords) - len(remainder)
    if next_destroyed >= 200:
        visible = [x for x in targets
                   if not blocked(best_station, targets, x)]
        [y,x] = list(sorted(visible, key=angle))[199-destroyed]
        print(x*100+y)
        break
    destroyed = next_destroyed
    targets = np.array(remainder, copy=True)
