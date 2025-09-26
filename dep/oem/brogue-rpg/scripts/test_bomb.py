from array2d import *
from vmath import *

import os
os.system('cls')

import random
# random.seed(7)

a = chunked_array2d[str, None](4, default=' ')

rect_width = 32
rect_height = 20

a.view_rect(vec2i.ZERO, rect_width, rect_height)[:, :] = '.'

def border_pos_clockwise(width: int, height: int):
    res = []
    # up
    for x in range(width - 1):
        res.append(vec2i(x, 0))
    # right
    for y in range(height - 1):
        res.append(vec2i(width-1, y))
    # down
    for x in range(width - 1, 0, -1):
        res.append(vec2i(x, height-1))
    # left
    for y in range(height - 1, 0, -1):
        res.append(vec2i(0, y))
    return res

def roll(pct: int):
    return random.randint(1, 100) <= pct

last_index = -1
border_pos = border_pos_clockwise(rect_width, rect_height)

for index, pos in enumerate(border_pos):
    if index - last_index > 10 and roll(15):
        bomb_width = random.randint(3, rect_width//2)
        bomb_height = random.randint(3, rect_height//2)
        bomb_view = a.view_rect(
            pos - vec2i(bomb_width // 2, bomb_height // 2),
            bomb_width,
            bomb_height
        )

        if bomb_view.count('#') == 0:
            last_index = index
            bomb_view[:, :] = '#'


for pos in border_pos:
    a[pos] = '#'

a_view = a.view()
nb_cnt = a_view.count_neighbors('.', 'Moore')
a_view[nb_cnt == 0] = ' '

print(a_view.render())
