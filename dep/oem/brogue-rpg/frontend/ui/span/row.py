from typing import Iterable
from ..base import Span, layout, textwidth
from .text import TextSpan

class _Spacer(Span):
    def __init__(self):
        super().__init__(-1)

    def render(self) -> str:
        assert self.width > 0
        return ' ' * self.width


class RowSpan(Span):
    children: list[Span]

    def __init__(self, children: Iterable[Span | str | ellipsis | None], width=-2):
        super().__init__(width)
        self.children = []

        for child in children:
            if child is None:
                pass
            elif isinstance(child, str):
                self.children.append(TextSpan(child))
            elif child is ...:
                self.children.append(_Spacer())
            else:
                assert isinstance(child, Span)
                self.children.append(child)

    def prerender(self, width):
        super().prerender(width)
        sizes = [c.width for c in self.children]
        extra = layout(sizes, self.width, self.children)
        for i in range(len(self.children)):
            child = self.children[i]
            child.prerender(sizes[i])
        if extra > 0:
            self.children.append(TextSpan(' ' * extra))

    def render(self) -> str:
        assert self.width > 0
        cpnts = []
        for span in self.children:
            cpnts.append(span.render())
        return ''.join(cpnts)

