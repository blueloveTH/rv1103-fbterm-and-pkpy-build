from typing import Iterable
from ..base import Widget
from .text import Text

def clip_range(window: int, cursor: int, length: int) -> tuple[int, int]:
    assert window < length
    start = cursor - window // 2
    end = start + window
    if start < 0:
        start = 0
        end = window
    if end > length:
        end = length
        start = length - window
    return start, end


class ListView(Widget):
    children: list[Widget]

    def __init__(self, children: Iterable[Widget | str | None], width=-2, height=-2, item_height=1, scroll_index=0):
        super().__init__(width, height)
        self.children = []

        for child in children:
            if child is None:
                pass
            elif isinstance(child, str):
                self.children.append(Text(child))
            else:
                assert isinstance(child, Widget)
                self.children.append(child)

        assert 0 <= scroll_index < len(self.children)
        self.item_height = item_height
        self.scroll_index = scroll_index

    def prerender(self, width: int, height: int) -> None:
        super().prerender(width, height)
        for child in self.children:
            child.prerender(width, self.item_height)
            assert child.width == width
            assert child.height == self.item_height

    def render(self) -> list[str]:
        assert self.width > 0 and self.height > 0
        assert self.height % self.item_height == 0
        lines = []
        items_per_page = self.height // self.item_height
        start, end = clip_range(items_per_page, self.scroll_index, len(self.children))
        for i in range(start, end):
            child = self.children[i]
            assert child.width == self.width
            assert child.height == self.item_height
            lines.extend(child.render())
        if len(lines) < self.height:
            empty_line = ' ' * self.width
            lines.extend([empty_line] * (self.height - len(lines)))
        return lines