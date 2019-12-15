#!/usr/bin/python3

import sys
import re
from collections import defaultdict
from math import ceil

prodquant = re.compile(r'(\d+) (\w+)')

class Recipe:
    def __init__(self, product, quantity, ingredients):
        self.product = product
        self.quantity = int(quantity)
        self.ingredients = ingredients
        self.parents = []

    def __repr__(self):
        ings = (f"{q} {t}" for t,q in self.ingredients.items())
        return (f"({self.quantity} {self.product}) <= ["
                + ', '.join(ings) + "]")

def parse_recipe(l):
    ing, res = l.split('=>')
    ing = {p[1]: int(p[0])
           for p in prodquant.findall(ing)}
    q, r = prodquant.findall(res)[0]
    return r, Recipe(r, q, ing)

recipes = dict(parse_recipe(x) for x in sys.stdin.readlines())
for r in recipes.values():
    for i in r.ingredients.keys():
        try: recipes[i].parents.append(r)
        except KeyError: pass

FUEL = recipes['FUEL']

def ore_required(fuel_wanted=1):
    finished = defaultdict(lambda: False)
    def ready(rec: Recipe):
        return all(finished[x] for x in rec.parents)

    requirements = defaultdict(lambda: 0)
    requirements[FUEL] = fuel_wanted
    ore_used = 0
    while requirements:
        recipe = next(filter(ready, requirements.keys()))
        quantity = requirements.pop(recipe)
        count = ceil(quantity / recipe.quantity)
        for p, q in recipe.ingredients.items():
            if p == 'ORE':
                ore_used += q * count
            else:
                requirements[recipes[p]] += q * count
        finished[recipe] = True
    return ore_used

print(ore_required())
fuel = 1
ORE = 10**12
# exp bin search
while ore_required(fuel) < ORE:
    fuel *= 2
left = fuel//2
right = fuel

while right-left > 1:
    mid = left + (right-left)//2
    if ore_required(mid) < ORE:
        left = mid
    else:
        right = mid

print(left)
