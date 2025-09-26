from typing import Sequence

from ..base import Widget, layout
from .text import Text
from .newline import Newline

class _Spacer(Widget):
    def __init__(self, width=-2):
        super().__init__(width, -1)

    def render(self) -> list[str]:
        assert self.width > 0 and self.height > 0
        return [' ' * self.width] * self.height


class Column(Widget):
    children: list[Widget]

    def __init__(self, children: Sequence[Widget | str | ellipsis | None], width=-2, height=-2):
        super().__init__(width, height)
        self.children = []

        for child in children:
            if child is None:
                pass
            elif isinstance(child, str):
                self.children.append(Text(child))
            elif child is ...:
                self.children.append(_Spacer())
            else:
                assert isinstance(child, Widget)
                self.children.append(child)

    def prerender(self, width, height):
        super().prerender(width, height)
        sizes = [c.height for c in self.children]
        extra = layout(sizes, self.height, self.children)
        for i in range(len(self.children)):
            child = self.children[i]
            child.prerender(self.width, sizes[i])
        if extra > 0:
            self.children.append(Newline(self.width, extra))

    def render(self) -> list[str]:
        assert self.width > 0 and self.height > 0
        lines = []
        for child in self.children:
            assert child.width == self.width
            lines.extend(child.render())
        return lines
        # return [textpad(line, self.width) for line in lines]