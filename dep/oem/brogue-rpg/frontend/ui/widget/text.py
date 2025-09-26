from ..base import Widget, textpad, textpad2d, textwrap, theme
from .row import Row

class Text(Widget):
    def __init__(self, text: str, width=-2):
        if '\n' in text:
            raise ValueError("'\\n' is not allowed in Text widget")
        self.text = text
        super().__init__(width, 1)

    def render(self) -> list[str]:
        assert self.width > 0 and self.height > 0
        return [textpad(self.text, self.width)]


class MultiLineText(Widget):
    lines: list[str]

    def __init__(self, text: str, width=-2, height=-2):
        assert width != -2
        self.lines = textwrap(text, width)
        if height == -2:
            height = len(self.lines)
        super().__init__(width, height)

    def render(self) -> list[str]:
        assert self.width > 0 and self.height > 0
        return textpad2d(self.lines, self.width, self.height)
