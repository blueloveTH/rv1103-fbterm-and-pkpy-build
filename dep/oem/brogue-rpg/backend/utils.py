from vmath import vec2i

DIRS_4_CW = [vec2i.LEFT, vec2i.UP, vec2i.RIGHT, vec2i.DOWN]

DIRS_8_CW = [
    vec2i.LEFT,
    vec2i.LEFT + vec2i.UP,
    vec2i.UP,
    vec2i.RIGHT + vec2i.UP,
    vec2i.RIGHT,
    vec2i.RIGHT + vec2i.DOWN,
    vec2i.DOWN,
    vec2i.LEFT + vec2i.DOWN,
]


class FacingTransform:
    def __init__(self, dir_i: vec2i, dir_j: vec2i):
        cw_i = DIRS_4_CW.index(dir_i)
        cw_j = DIRS_4_CW.index(dir_j)
        self.n_rots = (cw_j - cw_i) % 4

    def __call__(self, v: vec2i) -> vec2i:
        if self.n_rots == 0:
            return v                    # (1, 3)
        if self.n_rots == 1:
            return vec2i(-v.y, v.x)     # (-3, 1)
        if self.n_rots == 2:
            return vec2i(-v.x, -v.y)    # (-1, -3)
        if self.n_rots == 3:
            return vec2i(v.y, -v.x)     # (3, -1)
        assert False

def border_pos_clockwise(width: int, height: int):
    res: list[vec2i] = []
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