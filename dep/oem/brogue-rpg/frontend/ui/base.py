from vmath import color32

from .rich import *
from . import theme

class Widget:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def prerender(self, width: int, height: int):
        if self.width < 0:
            self.width = width
        if self.height < 0:
            self.height = height

    def render(self) -> list[str]:
        raise NotImplementedError

class Span:
    def __init__(self, width: int):
        self.width = width

    def prerender(self, width: int):
        if self.width < 0:
            self.width = width

    def render(self) -> str:
        raise NotImplementedError


def richtext(
        text: str,
        fg: color32 | None = None,
        bg: color32 | None = None,
        italic: bool = False,
        width: int | None = None,
        align: Align = 'left'
        ) -> str:
    if width is not None:
        text = textpad(text, width, align)
    if fg is not None:
        text = fg.ansi_fg(text)
    if bg is not None:
        text = bg.ansi_bg(text)
    if italic:
        text = ansi_italic(text)
    return text


def layout(sizes: list[int], total_size: int, debug_objects: list):
    assert total_size > 0
    fixed_size = 0
    spacers = []

    # Step 1: Collect fixed widths and flexible spacers
    for index, child_size in enumerate(sizes):
        if child_size == -1:
            spacers.append(index)
        elif child_size == -2:
            obj = debug_objects[index]
            raise ValueError(f"child_size of {obj} was unset")
        else:
            fixed_size += child_size

    # Step 2: Distribute remaining space to flexible spacers
    remaining = total_size - fixed_size
    num_flexible = len(spacers)
    flexible_size = 0
    if num_flexible > 0:
        if remaining < 0:
            raise ValueError(f"No enough space: sizes={sizes}, total_size={total_size}")
        per_spacer = remaining // num_flexible
        extra = remaining % num_flexible  # distribute the remainder
        for i, spacer in enumerate(spacers):
            sizes[spacer] = per_spacer + (1 if i < extra else 0)
            flexible_size += sizes[spacer]
    return remaining - flexible_size
    # elif remaining != 0:
    #     # No flexible spacers, but width doesn't match
    #     raise ValueError("Extra space left but no spacers to fill it")