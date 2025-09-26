from typing import Iterable
from vmath import color32

from ..base import Widget, Span
from ..span import RowSpan

class Row(Widget):
    def __init__(self, children: Iterable[Span | str | ellipsis | None], width=-2, fg: color32 | None = None, bg: color32 | None = None):
        super().__init__(width, 1)
        self.span = RowSpan(children)
        self.fg = fg
        self.bg = bg

    def render(self) -> list[str]:
        assert self.width > 0 and self.height > 0
        self.span.prerender(self.width)
        text = self.span.render()
        if self.fg is not None:
            text = self.fg.ansi_fg(text)
        if self.bg is not None:
            text = self.bg.ansi_bg(text)
        return [text]
