from vmath import vec2i
from .base import Actor, PRIORITY_MOB


class Mob(Actor):
    def __init__(self) -> None:
        super().__init__()
        self.level = 0
        self.tb_info.priority = PRIORITY_MOB

    @property
    def char(self) -> str:
        return '👹'
    
    @property
    def is_mob(self) -> bool:
        return True
    
    def wait_for_command(self):
        raise NotImplementedError(type(self))
    
    def with_level(self, level: int):
        assert level >= 1
        self.level = level

        self.hp = (10 + level * 4)
        self.stats.max_hp.base = self.hp
        return self