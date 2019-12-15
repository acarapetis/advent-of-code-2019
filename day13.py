#!/usr/bin/python3

import intcode
from collections import defaultdict
from screen import display
canvas = defaultdict(lambda: 0)

code = [int(c) for c in open('day13.txt').read().split(',')]
machine = intcode.IntProc(code)
try:
    while True:
        x, y, t = machine.read(3)
        canvas[(x,y)] = t
except intcode.Terminated:
    print(sum(1 for _, t in canvas.items()
              if t == 2))

cmp = lambda a, b: (a > b) - (a < b)

BLANK = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

# part 2
SYMBOLS = {
    BLANK:  ' ',
    WALL:   '#',
    BLOCK:  '*',
    PADDLE: '_',
    BALL:   'O',
}
code[0] = 2
machine = intcode.IntProc(code)
score = 0
ball = 0
paddle = 0
try:
    while True:
        while machine.poll(0.00001):
            x, y, t = machine.read(3)
            if x == -1 and y == 0:
                score = t
            else:
                canvas[(x,y)] = t
                if t == BALL:
                    ball = x
                elif t == PADDLE:
                    paddle = x

        if machine.blocked:
            machine.write(cmp(ball, paddle))
except (intcode.Terminated, BrokenPipeError):
    pass
finally:
    print(score)
