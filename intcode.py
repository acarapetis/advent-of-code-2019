#!/usr/bin/python3
from multiprocessing import Process, Pipe, Value
import sys

DEBUG = False
def log(*a, **kw):
    if DEBUG:
        print(*a, **kw)

class BadOpcode(ValueError): pass
class Terminated(EOFError): pass
class IOCollision(Exception): pass

class Memory(list):
    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([0]*(index + 1 - len(self)))
        return list.__setitem__(self, index, value)

    def __getitem__(self, index):
        if index >= len(self):
            self.extend([0]*(index + 1 - len(self)))
        return list.__getitem__(self, index)

class IntProc:
    def __init__(self, code=None):
        """Run an IntCode machine in a separate process."""
        if not code:
            code = sys.stdin.read()
        if isinstance(code, (str, bytes)):
            code = [int(s) for s in code.split(',')]
        self.code = code
        self.reset()

    def reset(self):
        if hasattr(self, 'worker'):
            self.worker.terminate()
        if hasattr(self, 'pipe'):
            self.pipe.close()
        self._blocked = Value('b')
        self._blocked.value = False
        self.pipe, pchild = Pipe()
        self.worker = Process(target=intcode_worker,
                              args=(self.code, pchild,
                                    self.pipe, self._blocked))
        self.worker.start()
        pchild.close()

    @property
    def blocked(self):
        return self._blocked.value
    
    def read(self, n=None):
        if n is not None:
            return tuple(self.read() for _ in range(n))
        try:
            return self.pipe.recv()
        except (EOFError, ConnectionResetError) as e:
            raise Terminated(e)

    def write(self, v):
        return self.pipe.send(v)

    def join(self):
        return self.worker.join()

    def is_alive(self):
        return self.worker.is_alive()

    def poll(self, v=None):
        return self.pipe.poll(v)

    def wait_for_output(self, v=0.00001):
        while not self.pipe.poll(v):
            pass

def intcode_worker(code, pipe, parent_pipe, blocked):
    def recv():
        if not pipe.poll():
            blocked.value = True
        v = pipe.recv()
        blocked.value = False
        return v
    parent_pipe.close()
    IntCode(code,
            input=recv,
            output=pipe.send).run()
    import os
    os.close(pipe.fileno())
    sys.exit(0)
    
class IntCode:
    def __init__(self, code, noun=None, verb=None,
                 input=None, output=None, name='',
                 raise_on_terminate=False):
        if isinstance(code, (str, bytes)):
            code = [int(s) for s in code.split(',')]
        self.code = list(code)
        if noun: self.code[1] = noun
        if verb: self.code[2] = verb
        self.input = input
        self.output = output
        self.name = name
        self.raise_on_terminate = raise_on_terminate
        self.reset()

    def _log(self, msg, *a, plain=False, **kw):
        n = str(self.name or '')
        if n: n += ' '
        if not plain:
            msg = f'{n}{msg}'
        log(msg, *a, **kw)

    def reset(self):
        self.rel_base = 0
        self.mem = Memory(self.code.copy())
        self.i = 0

    def _incr(self):
        v = self.mem[self.i]
        self.i += 1
        return v

    def run(self, input=None, return_last_output=False):
        self.reset()
        if input is not None:
            self.input = lambda: input
        if return_last_output:
            o = None
            def setout(v):
                nonlocal o
                o = v
            self.output = setout
        while True:
            v = self._tick()
            if v is not None:
                if return_last_output:
                    return o
                return v

    def read(self):
        def bad():
            raise IOCollision("Tried to read when computer expected input")
        self.input = bad

        out = None
        def good(v):
            nonlocal out
            out = v
        self.output = good

        while True:
            v = self._tick()
            if out is not None:
                return out
            elif v is not None:
                return None

    def write(self, value):
        def bad(v):
            raise IOCollision("Tried to write when output is waiting to be consumed")
        self.output = bad

        sent = False
        def good():
            nonlocal sent
            sent = True
            return value
        self.input = good

        while True:
            v = self._tick()
            if sent:
                return True
            elif v is not None:
                return None


    def _input(self):
        return self.input()

    def _output(self, v):
        return self.output(v)

    def _tick(self):
        mem = self.mem
        i = self.i
        icode = self._incr()
        opcode = icode % 100
        pmode = list('{:03d}'.format(icode // 100))
        self._log(f"EXEC@{i:03d} {''.join(pmode)} {opcode}: ", end='')
        def _param(count=None):
            if count is not None:
                return tuple(_param() for c in range(count))
            p = self._incr()
            mode = int(pmode.pop())
            if mode == 0:
                return mem[p]
            elif mode == 1:
                return p
            else:
                return mem[p+self.rel_base]
            return p

        def _write(v):
            p = self._incr()
            j = p + self.rel_base if int(pmode.pop()) == 2 else p
            mem[j] = v

        if opcode == 99:
            self._log(f"TERMINATE", plain=True)
            if self.raise_on_terminate:
                raise Terminated(mem)
            return mem[0]
        elif opcode == 1:
            a, b = _param(2)
            self._log(f"ADD {a} {b}", plain=True)
            _write(a+b)
        elif opcode == 2:
            a, b = _param(2)
            self._log(f"MUL {a} {b}", plain=True)
            _write(a*b)
        elif opcode == 3:
            v = self._input()
            self._log(f"INPUT {v}", plain=True)
            _write(v)
        elif opcode == 4:
            o = _param()
            self._log(f"OUTPUT {o}", plain=True)
            self._output(o)
        elif opcode == 5:
            cond, pos = _param(2)
            if cond:
                self.i = pos
                self._log(f"JNZ {cond} => JUMP {pos}", plain=True)
            else:
                self._log(f"JNZ {cond} => NO JUMP", plain=True)
        elif opcode == 6:
            cond, pos = _param(2)
            if not cond:
                self.i = pos
                self._log(f"JZ {cond} => JUMP {pos}", plain=True)
            else:
                self._log(f"JZ {cond} => NO JUMP", plain=True)
        elif opcode == 7:
            a, b = _param(2)
            _write(1 if a<b else 0)
            self._log(f"CMP {a}<{b}", plain=True)
        elif opcode == 8:
            a, b = _param(2)
            _write(1 if a==b else 0)
            self._log(f"CMP {a}=={b}", plain=True)
        elif opcode == 9:
            p = _param()
            self.rel_base += p
            self._log(f"REL += {p}", plain=True)
        else:
            raise BadOpcode(opcode)
