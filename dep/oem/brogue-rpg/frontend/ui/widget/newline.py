from ..base import Widget

class Newline(Widget):
    def __init__(self, width=-2, height=1):
        super().__init__(width, height)

    def render(self):
        assert self.width > 0 and self.height > 0
        return [' ' * self.width] * self.height