from ..base import Widget

class Padding(Widget):
    def __init__(self, child: Widget, width=-2, height=-2, left_pad=0, right_pad=0):
        super().__init__(width, height)
        self.child = child
        self.left_pad = left_pad
        self.right_pad = right_pad

    def prerender(self, width, height):
        super().prerender(width, height)
        max_width = width - self.left_pad - self.right_pad
        self.child.prerender(max_width, height)
        assert self.child.width <= max_width
        self.right_pad += max_width - self.child.width
        
    def render(self) -> list[str]:
        assert self.width > 0 and self.height > 0
        lines = self.child.render()
        left_spaces = ' ' * self.left_pad
        right_spaces = ' ' * self.right_pad
        return [left_spaces + line + right_spaces for line in lines]
