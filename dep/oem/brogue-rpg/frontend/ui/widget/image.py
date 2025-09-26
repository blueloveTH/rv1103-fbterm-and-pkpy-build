from ..base import Widget

class Image(Widget):
    def __init__(self, text: str, width=-2): 
        self.lines = text.split('\n')
        super().__init__(width, len(self.lines))
    
    def render(self):
        assert self.width > 0 and self.height > 0
        return self.lines
