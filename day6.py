#!/usr/bin/env python3

import sys, re
from collections import defaultdict

class Obj:
    def __init__(self):
        self.orbiting = None
        self.satellites = set()

    def orbits(self, parent):
        self.orbiting = parent
        parent.satellites.add(self)

    def norbits(self):
        if not self.orbiting:
            return 0
        return 1 + self.orbiting.norbits()

    def lineage(self):
        if self.orbiting:
            return [self] + self.orbiting.lineage()
        return [self]

objs = defaultdict(lambda: Obj())

for l in sys.stdin.readlines():
    a, b = re.match(r'(\w+)\)(\w+)', l).groups()
    objs[b].orbits(objs[a])

#p1
print(sum(map(Obj.norbits, objs.values())))

#p2
l1 = objs['YOU'].lineage()
l2 = objs['SAN'].lineage()
def dist():
    for i, o1 in enumerate(l1):
        for j, o2 in enumerate(l2):
            if o1 == o2:
                return i + j - 2
print(dist())
