from typing import Literal

FieldCpnt = Literal['base', 'from_gear', 'from_talent', 'from_buff', 'value']

class Field:
    def __init__(self):
        self.base = 0
        self.from_gear = 0
        self.from_talent = 0
        self.from_buff = 0

    @property
    def value(self):
        return self.base + self.from_gear + self.from_talent + self.from_buff
    
    def reset(self):
        self.from_gear = 0
        self.from_talent = 0
        self.from_buff = 0


class Stats:
    def __init__(self):
        self.max_hp = Field()
        self.max_sp = Field()

        self.min_dmg = Field()
        self.max_dmg = Field()

        self.dodge = Field()
        self.block = Field()

        self.defense = Field()
        self.elemental_resist = Field()
        self.curse_resist = Field()
        # 环境抗性
        self.env_fire_resist = Field()
        self.env_cold_resist = Field()

    def reset(self):
        for k, v in self.__dict__.items():
            if isinstance(v, Field):
                v.reset()

    def copy_with_base(self):
        new = Stats()
        for k, v in new.__dict__.items():
            if isinstance(v, Field):
                old_field: Field = getattr(self, k)
                v.base = old_field.base
        return new
