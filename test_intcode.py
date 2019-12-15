import pytest
import asyncio
import intcode
from intcode import IntProc, AsyncIntCode, buffered, grouped

intcode.DEBUG = True
cat_code = [
    3,20, # INPUT @20
    1006,20,10, # JUMP $10 IF @20 == 0
    4,20, # OUTPUT @20
    1005,0,0, # JUMP $0 IF @20 != 0
    # @10
    99 # TERM
]
int_seq = [1,2,3,4,-4,12431249283]

def test_cat():
    machine = IntProc(cat_code)
    for v in int_seq:
        machine.write(v)
        assert machine.read() == v
    machine.write(0)
    machine.join()
    assert not machine.is_alive()

def test_blocked():
    machine = IntProc(cat_code)
    from time import sleep
    sleep(0.1)
    assert machine.blocked
    machine.write(1)
    machine.write(0)
    machine.join()

@pytest.mark.asyncio
async def test_asyncio():
    seq = [1,2,3,4,-4,12431249283]
    ibuf = iter([*seq, 0])
    outs = []
    async def mread():
        return next(ibuf)
    async def mwrite(v):
        outs.append(v)
    machine = AsyncIntCode(cat_code, input=mread, output=mwrite)
    await machine.run()
    assert outs == seq

@pytest.mark.asyncio
async def test_asyncio_buffered():
    ibuf = iter([*int_seq, 0])
    outs = []
    async def mread():
        return next(ibuf)
    @buffered
    async def mwrite(buf):
        nonlocal outs
        outs = buf
    machine = AsyncIntCode(cat_code, input=mread, output=mwrite)
    await machine.run()
    assert outs == int_seq

@pytest.mark.asyncio
async def test_asyncio_grouped():
    seq = [1,2,3,4,8,2]
    ibuf = iter([*seq, 0])
    outs = []
    async def mread():
        return next(ibuf)
    @grouped(2)
    async def mwrite(a,b):
        nonlocal outs
        outs.append((a,b))
    machine = AsyncIntCode(cat_code, input=mread, output=mwrite)
    await machine.run()
    assert outs == [(1,2),(3,4),(8,2)]
