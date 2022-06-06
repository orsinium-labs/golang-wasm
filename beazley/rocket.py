# rocket.py

import pygame
import time
from machine import float64, int32
import machine
import math
import wadze    # Web Assembly Decoder
module = wadze.parse_module(open('program.wasm', 'rb').read())

# Build imported functions

# These functions are imported by Wasm.  Must be implemented in the host
# environment (Python).   These are listed in the required order.


def imp_Math_atan(x):
    return float64(math.atan(x))


def imp_cos(x):
    return float64(math.cos(x))


def imp_sin(x):
    return float64(math.sin(x))


pygame.init()

size = (800, 600)
screen = pygame.display.set_mode(size)
# font = pygame.font.SysFont("helvetica", 36)


def imp_clear_screen():
    screen.fill((0, 0, 0))


def imp_draw_bullet(x, y):
    pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), 2)


def imp_draw_enemy(x, y):
    pygame.draw.circle(screen, (255, 0, 255), (int(x), int(y)), 15, 2)


def imp_draw_particle(x, y, z):
    pygame.draw.circle(screen, (255, 255, 0), (int(x), int(y)), abs(int(z)))


def imp_draw_player(x, y, z):
    pygame.draw.circle(screen, (0, 255, 255), (int(x), int(y)), 10, 2)


def imp_draw_score(s):
    pass
    # print('draw_score', s)
    # text = font.render(f'Score: {int(s)}', True, (200,200, 0))
    # screen.blit(text, (5, 5))


# Declare as imported functions for our "machine"
imported_functions: list = [
    machine.ImportFunction(1, 1, imp_Math_atan),
    machine.ImportFunction(0, 0, imp_clear_screen),
    machine.ImportFunction(1, 1, imp_cos),
    machine.ImportFunction(2, 0, imp_draw_bullet),
    machine.ImportFunction(2, 0, imp_draw_enemy),
    machine.ImportFunction(3, 0, imp_draw_particle),
    machine.ImportFunction(3, 0, imp_draw_player),
    machine.ImportFunction(1, 0, imp_draw_score),
    machine.ImportFunction(1, 1, imp_sin),
]

# Declare "defined" functions
defined_functions: list = []

for typeidx, code in zip(module['func'], module['code']):
    functype = module['type'][typeidx]  # Signature
    func = machine.Function(nparams=len(functype.params),
                            returns=bool(functype.returns),
                            code=wadze.parse_code(code).instructions)
    defined_functions.append(func)

functions = imported_functions + defined_functions

# Declare "exported" functions
exports = {exp.name: functions[exp.ref] for exp in module['export']
           if isinstance(exp, wadze.ExportFunction)}

m = machine.Machine(functions, 20*65536)    # Hack on memory

# Initialize memory
for data in module['data']:
    m.execute(data.offset, None)
    offset = m.pop()
    m.memory[offset:offset+len(data.values)] = data.values


# Call something
width = float64(800.0)
height = float64(600.)

m.call(exports['resize'], width, height)    # Prayer

# Game loop

last = time.time()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit()
        elif event.type == pygame.KEYUP:
            if event.key == 32:
                m.call(exports['toggle_shoot'], int32(0))
            elif event.key == 275:
                m.call(exports['toggle_turn_right'], int32(0))
            elif event.key == 276:
                m.call(exports['toggle_turn_left'], int32(0))
            elif event.key == 273:
                m.call(exports['toggle_boost'], int32(0))

        elif event.type == pygame.KEYDOWN:
            if event.key == 32:
                m.call(exports['toggle_shoot'], int32(1))
            elif event.key == 275:
                m.call(exports['toggle_turn_right'], int32(1))
            elif event.key == 276:
                m.call(exports['toggle_turn_left'], int32(1))
            elif event.key == 273:
                m.call(exports['toggle_boost'], int32(1))

    now = time.time()
    dt = now - last
    last = now
    m.call(exports['update'], float64(dt))
    m.call(exports['draw'])
    pygame.display.flip()
