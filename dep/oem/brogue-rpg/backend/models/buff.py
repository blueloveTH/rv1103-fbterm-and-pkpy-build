from .affix import AffixGroup

class Buff:
    def __init__(self, duration: int):
        self.affixes = AffixGroup()
        self.duration = duration