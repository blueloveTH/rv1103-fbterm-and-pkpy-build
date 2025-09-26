from vmath import color32, vec2i
from ..base import Span, textwidth

class StatBarSpan(Span):
    def __init__(self, title: str, bar_width: int, fg: color32, value: vec2i, fill_char='='):
        bar = fill_char * int(bar_width * value.x / value.y)
        bar = bar.ljust(bar_width)
        self.text = f'{title}: [{bar}] {value.x}/{value.y}'
        self.fg = fg
        super().__init__(textwidth(self.text))

    def render(self):
        assert self.width > 0
        return self.fg.ansi_fg(self.text)
    

class ChargeBarSpan(Span):
    def __init__(self, value: float, n_ticks: int, width=-2):
        self.value = min(max(0.0, value), 1.0)
        self.n_ticks = n_ticks
        assert n_ticks >= 1
        super().__init__(width)

    def render(self):
        assert self.width > 0
        fill_char = '#'
        tick_char = '|'

        fill_width = self.width - 2
        progress = int(fill_width * self.value)
        tick_indices = calc_ticks(fill_width, self.n_ticks)

        chars = []
        for i in range(fill_width):
            if i in tick_indices:
                chars.append(tick_char)
            else:
                chars.append(fill_char if i < progress else ' ')
        return f'[{"".join(chars)}]'


def calc_ticks(width: int, n_ticks: int):
    """在`width`宽度的字符数组中插入`n_ticks`个刻度线，尽可能均匀分割，返回每个刻度线的下标"""
    n_splits = n_ticks + 1
    indices = []
    q, r = divmod(width - n_ticks, n_splits)
    # 逐步计算每个刻度线的位置
    indices = []
    current_index = 0
    for i in range(1, n_ticks + 1):
        current_index += q  # 增加基础长度
        if i <= r:  # 分配余数到前 r 个分割线
            current_index += 1
        indices.append(current_index)  # 添加分割线位置
        current_index += 1  # 分割线占据1个空间
    return indices