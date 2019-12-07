#!/usr/bin/python3

DEBUG = False
def log(*a, **kw):
    if DEBUG:
        print(*a, **kw)

class Terminated(Exception): pass
class IOCollision(Exception): pass
    
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
        if not plain:
            msg = f'{self.name} {msg}'
        log(msg, *a, **kw)

    def reset(self):
        self.mem = self.code.copy()
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

    def send(self, value):
        def bad(v):
            raise IOCollision("Tried to send when computer is trying to output")
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
        icode = self._incr()
        opcode = icode % 100
        pmode = list('{:03d}'.format(icode // 100))
        self._log(f"EXEC {''.join(pmode)} {opcode}: ", end='')
        def _param(count=None):
            if count is not None:
                return tuple(_param() for c in range(count))
            p = self._incr()
            if pmode.pop() == '0':
                return mem[p]
            return p
        def _write(v):
            mem[self._incr()] = v

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
                self._log(f"JUMP {pos}", plain=True)
        elif opcode == 6:
            cond, pos = _param(2)
            if not cond:
                self.i = pos
                self._log(f"JUMP {pos}", plain=True)
        elif opcode == 7:
            a, b = _param(2)
            _write(1 if a<b else 0)
        elif opcode == 8:
            a, b = _param(2)
            _write(1 if a==b else 0)




