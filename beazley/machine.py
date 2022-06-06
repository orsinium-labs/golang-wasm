# machine.py

import math
from numpy import (
    frombuffer, int16, int32, int64, float32, float64, int8, uint16, uint32, uint64, uint8,
)

import struct


_const = {
    'i32.const': int32,
    'i64.const': int64,
    'f32.const': float32,
    'f64.const': float64,
}

_binary = {
    # 32-bit integer
    'i32.add': lambda x, y: int32(x + y),
    'i32.sub': lambda x, y: int32(x - y),
    'i32.mul': lambda x, y: int32(x * y),
    'i32.div_s': lambda x, y: int32(x // y),
    'i32.div_u': lambda x, y: int32(uint32(x) / uint32(y)),
    'i32.and': lambda x, y: int32(x & y),
    'i32.or': lambda x, y: int32(x | y),
    'i32.xor': lambda x, y: int32(x ^ y),
    'i32.rem_s': lambda x, y: int32(x % y),
    'i32.rem_u': lambda x, y: int32(uint32(x) // uint32(y)),
    'i32.eq': lambda x, y: int32(x == y),
    'i32.ne': lambda x, y: int32(x != y),
    'i32.lt_s': lambda x, y: int32(x < y),
    'i32.le_s': lambda x, y: int32(x <= y),
    'i32.gt_s': lambda x, y: int32(x > y),
    'i32.ge_s': lambda x, y: int32(x >= y),
    'i32.lt_u': lambda x, y: int32(uint32(x) < uint32(y)),
    'i32.gt_u': lambda x, y: int32(uint32(x) > uint32(y)),
    'i32.le_u': lambda x, y: int32(uint32(x) <= uint32(y)),
    'i32.ge_u': lambda x, y: int32(uint32(x) >= uint32(y)),
    'i32.rotr': lambda x, y: int32((x >> y) | ((x & ((2**y)-1)) << (32-y))),
    'i32.rotl': lambda x, y: int32((x << y) | ((x & ((2**y)-1)) >> (32-y))),
    'i32.shr_u': lambda x, y: int32(int(uint32(x)) >> int(y)),
    'i32.shl': lambda x, y: int32(x << y),

    # 64-bit integer
    'i64.add': lambda x, y: int64(x + y),
    'i64.sub': lambda x, y: int64(x - y),
    'i64.mul': lambda x, y: int64(x * y),
    'i64.div_s': lambda x, y: int64(x // y),
    'i64.div_u': lambda x, y: int64(uint64(x) / uint64(y)),
    'i64.and': lambda x, y: int64(x & y),
    'i64.or': lambda x, y: int64(x | y),
    'i64.xor': lambda x, y: int64(x ^ y),
    'i64.rem_s': lambda x, y: int64(x % y),
    'i64.rem_u': lambda x, y: int64(uint64(x) // uint64(y)),
    'i64.eq': lambda x, y: int32(x == y),
    'i64.ne': lambda x, y: int32(x != y),
    'i64.lt_s': lambda x, y: int32(x < y),
    'i64.le_s': lambda x, y: int32(x <= y),
    'i64.gt_s': lambda x, y: int32(x > y),
    'i64.ge_s': lambda x, y: int32(x >= y),
    'i64.lt_u': lambda x, y: int32(uint64(x) < uint64(y)),
    'i64.gt_u': lambda x, y: int32(uint64(x) > uint64(y)),
    'i64.le_u': lambda x, y: int32(uint64(x) <= uint64(y)),
    'i64.ge_u': lambda x, y: int32(uint64(x) >= uint64(y)),
    'i64.rotr': lambda x, y: int64((x >> y) | ((x & ((2**y)-1)) << (64-y))),
    'i64.rotl': lambda x, y: int64((x << y) | ((x & ((2**y)-1)) >> (64-y))),
    'i64.shr_u': lambda x, y: int64(int(uint64(x)) >> int(y)),
    'i64.shl': lambda x, y: int64(x << y),

    # -- 64 bit float
    'f64.add': lambda x, y: float64(x + y),
    'f64.sub': lambda x, y: float64(x - y),
    'f64.mul': lambda x, y: float64(x * y),
    'f64.div': lambda x, y: float64(x / y),
    'f64.eq': lambda x, y: int32(x == y),
    'f64.ne': lambda x, y: int32(x != y),
    'f64.lt': lambda x, y: int32(x < y),
    'f64.gt': lambda x, y: int32(x > y),
    'f64.le': lambda x, y: int32(x <= y),
    'f64.ge': lambda x, y: int32(x >= y),
}

_unary = {
    'i32.eqz': lambda x: int32(x == 0),
    'i32.clz': lambda x: int32(32 - len(bin(uint32(x))[2:])),
    'i32.ctz': lambda x: int32(len(bin(uint32(x)).rsplit('1', 1)[-1])),
    'i32.wrap_i64': lambda x: int32(uint64(x)),
    'i64.extend_i32_u': lambda x: int64(uint32(x)),
    'f64.reinterpret_i64': lambda x: frombuffer(x.tobytes(), float64)[0],
    'f64.sqrt': lambda x: float64(math.sqrt(x)),
    'f64.convert_i32_u': lambda x: float64(uint32(x)),
}


_load = {
    'i32.load': lambda raw: frombuffer(raw, int32)[0],
    'i64.load': lambda raw: frombuffer(raw, int64)[0],
    'f64.load': lambda raw: frombuffer(raw, float64)[0],
    'i32.load8_s': lambda raw: int32(frombuffer(raw, int8)[0]),
    'i32.load8_u': lambda raw: int32(frombuffer(raw, uint8)[0]),
    'i32.load16_s': lambda raw: int32(frombuffer(raw, int16)[0]),
    'i32.load16_u': lambda raw: int32(frombuffer(raw, uint16)[0]),
    'i64.load8_s': lambda raw: int64(frombuffer(raw, int8)[0]),
    'i64.load8_u': lambda raw: int64(frombuffer(raw, uint8)[0]),
    'i64.load16_s': lambda raw: int64(frombuffer(raw, int16)[0]),
    'i64.load16_u': lambda raw: int64(frombuffer(raw, uint16)[0]),
    'i64.load32_s': lambda raw: int64(frombuffer(raw, int32)[0]),
    'i64.load32_u': lambda raw: int64(frombuffer(raw, uint32)[0]),
}

_store = {
    'i32.store': lambda val: val.tobytes(),
    'i64.store': lambda val: val.tobytes(),
    'f64.store': lambda val: val.tobytes(),
    'i32.store8': lambda val: val.tobytes()[:1],
    'i32.store16': lambda val: val.tobytes()[:2],
    'i64.store8': lambda val: val.tobytes()[:1],
    'i64.store16': lambda val: val.tobytes()[:2],
    'i64.store32': lambda val: val.tobytes()[:4],
}


class Function:
    def __init__(self, nparams, returns, code):
        self.nparams = nparams
        self.returns = returns
        self.code = code


class ImportFunction:
    def __init__(self, nparams, returns, call):
        self.nparams = nparams
        self.returns = returns
        self.call = call


class Machine:
    def __init__(self, functions, memsize=65536):
        self.functions = functions  # function table
        self.items = []
        self.memory = bytearray(memsize)

    def load(self, addr):
        return struct.unpack('<d', self.memory[addr:addr+8])[0]

    def store(self, addr, val):
        self.memory[addr:addr+8] = struct.pack('<d', val)

    def push(self, item):
        assert type(item) in {int32, int64, float32, float64}
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def call(self, func, *args):
        locals = dict(enumerate(args))    # { 0: args[0], 1: args[1], 2: args[2] }
        if isinstance(func, Function):
            try:
                self.execute(func.code, locals)
            except Return:
                pass
            if func.returns:
                return self.pop()
        else:
            return func.call(*args)   # External (import function)

    def execute(self, instructions, locals):
        for op, *args in instructions:
            #            print(op, args, self.items)
            if op in _const:
                self.push(_const[op](args[0]))
            elif op in _binary:
                right = self.pop()
                left = self.pop()
                self.push(_binary[op](left, right))
            elif op in _unary:
                self.push(_unary[op](self.pop()))

            elif op in _load:
                addr = self.pop() + args[1]   # Offset
                self.push(_load[op](self.memory[addr:addr+8]))

            elif op in _store:
                val = self.pop()
                addr = self.pop() + args[1]
                raw = _store[op](val)
                self.memory[addr:addr+len(raw)] = raw

            elif op == 'memory.size':
                self.push(int32(len(self.memory)//65536))

            elif op == 'memory.grow':
                npages = self.pop()
                self.memory.extend(bytes(npages*65536))
                self.push(int32(len(self.memory)//65536))

            elif op == 'local.get':
                self.push(locals[args[0]])
            elif op == 'local.set':
                locals[args[0]] = self.pop()
            elif op == 'local.tee':
                locals[args[0]] = self.items[-1]

            elif op == 'drop':
                self.pop()

            elif op == 'select':
                c = self.pop()
                v2 = self.pop()
                v1 = self.pop()
                self.push(v1 if c else v2)

            elif op == 'call':
                func = self.functions[args[0]]
                fargs = reversed([self.pop() for _ in range(func.nparams)])
                result = self.call(func, *fargs)
                if func.returns:
                    self.push(result)

            elif op == 'br':
                raise Break(args[0])

            elif op == 'br_if':
                if self.pop():
                    raise Break(args[0])
            elif op == 'br_table':       # (br_tabel, [], default)
                n = self.pop()
                if n < len(args[0]):
                    raise Break(args[0][n])
                else:
                    raise Break(args[1])
            elif op == 'block':   # ('block', type, [ instructions ])
                try:
                    self.execute(args[1], locals)
                except Break as b:
                    if b.level > 0:
                        b.level -= 1
                        raise
            # if (test) { consequence } else {alternative }
            #
            # ('block', [
            #             ('block', [
            #                         test
            #                         ('br_if, 0),  # Goto 0
            #                         alternative,
            #                         ('br', 1),    # Goto 1
            #                       ]
            #             ),  # Label : 0
            #             consequence,
            #           ]
            # ) # Label 1:

            elif op == 'loop':
                while True:
                    try:
                        self.execute(args[1], locals)
                        break
                    except Break as b:
                        if b.level > 0:
                            b.level -= 1
                            raise

            # while (test) { body }
            # ('block', [
            #            ('loop', [     # Label 0
            #                      not test
            #                      ('br_if', 1), # Goto 1:  (break)
            #                      body
            #                      ('br', 0),    # Goto 0:  (continue)
            #                      ]
            #            )
            #           ]
            # ) # label 1

            elif op == 'return':
                raise Return()

            else:
                raise RuntimeError(f'Bad op {op}')


class Break(Exception):
    def __init__(self, level):
        self.level = level


class Return(Exception):
    pass


def example():
    def py_display_player(x):
        import time
        print(' '*int(x) + '<O:>')
        time.sleep(0.02)

    display_player = ImportFunction(nparams=1, returns=None, call=py_display_player)

    # def update_position(x, v, dt):
    #     return x + v*dt
    #
    update_position = Function(nparams=3, returns=True, code=[
        ('local.get', 0),  # x
        ('local.get', 1),  # v
        ('local.get', 2),  # dt
        ('mul',),
        ('add',),
    ])

    functions = [update_position, display_player]

    # x = 2
    # v = 3
    # x = x + v*0.1
    x_addr = 22
    v_addr = 42

    m = Machine(functions)
    m.store(x_addr, 2.0)
    m.store(v_addr, 3.0)

    # while x > 0 {
    #    x = update_position(x, v, 0.1)
    #    if x >= 70 {
    #        v = -v;
    #    }
    # }
    m.execute([
        ('block', [
            ('loop', [
                ('const', x_addr),
                ('load',),
                ('call', 1),
                ('const', x_addr),
                ('load',),
                ('const', 0.0),
                ('le',),
                ('br_if', 1),
                ('const', x_addr),
                ('const', x_addr),
                ('load',),
                ('const', v_addr),
                ('load',),
                ('const', 0.1),
                ('call', 0),
                ('store',),
                ('block', [
                    ('const', x_addr),
                    ('load',),
                    ('const', 70.0),
                    ('ge',),
                    ('block', [
                        ('br_if', 0),
                        ('br', 1),
                    ]
                    ),
                    ('const', v_addr),
                    ('const', 0.0),
                    ('const', v_addr),
                    ('load',),
                    ('sub',),
                    ('store',),
                ],
                ),
                ('br', 0),
            ],
            ),
        ],
        ),

    ], None)

    print('Result:', m.load(x_addr))


if __name__ == '__main__':
    example()
