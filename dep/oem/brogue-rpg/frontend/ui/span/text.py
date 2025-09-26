from ..base import Span, textwidth

class TextSpan(Span):
    def __init__(self, text: str):
        self.text = text
        super().__init__(textwidth(text))

    def render(self) -> str:
        assert self.width > 0
        return self.text

