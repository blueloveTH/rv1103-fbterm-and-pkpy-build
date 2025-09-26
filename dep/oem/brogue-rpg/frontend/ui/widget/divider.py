from typing import Optional
from vmath import color32

from ..base import Widget, theme

class HDivider(Widget):
    def __init__(self, color: Optional[color32] = None, fillchar='⎯', width=-2):
        super().__init__(width, 1)
        self.color = color or theme.hdivider_fg
        self.fillchar = fillchar

    def render(self):
        assert self.width > 0 and self.height > 0
        line = self.fillchar * self.width
        if self.color is not None:
            line = self.color.ansi_fg(line)
        return [line]
    
class VDivider(Widget):
    def __init__(self, color: Optional[color32] = None, fillchar='|', height=-2):
        super().__init__(1, height)
        self.color = color or theme.vdivider_fg
        self.fillchar = fillchar

    def render(self):
        assert self.width > 0 and self.height > 0
        line = self.fillchar
        if self.color is not None:
            line = self.color.ansi_fg(line)
        return [line] * self.height
