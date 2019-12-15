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
score = 0
ball = 0
paddle = 0
outbuf = []

import asyncio

async def handle_output(v):
    global outbuf, score, ball, paddle
    outbuf.append(v)
    if len(outbuf) == 3:
        x, y, t = outbuf
        outbuf = []
        if x == -1 and y == 0:
            score = t
        else:
            canvas[(x,y)] = t
            if t == BALL:
                ball = x
            elif t == PADDLE:
                paddle = x

async def provide_input():
    return cmp(ball, paddle)

cpu = intcode.AsyncIntCode(code, input=provide_input, output=handle_output)
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(cpu.run())
    print(score)
finally:
    loop.close()
