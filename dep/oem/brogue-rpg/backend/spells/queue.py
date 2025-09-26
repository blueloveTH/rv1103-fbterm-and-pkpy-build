from dataclasses import dataclass
from typing import Literal
from vmath import vec2i

@dataclass
class Wand:
    mana: vec2i             # 法力值
    mana_regen: int         # 每回合恢复的法力值
    capacity: int           # 法杖容量，可以放多少格法术

    cast_delay: float       # 释放完一个法术组后，等待多少回合才能释放下一个法术组
    recharge_time: float    # 所有法术组释放完后，等待多少回合才会刷新
    hit_rate: int           # 基础命中率
    crit_rate: int          # 基础暴击率

    affixes: list[str]      # 附加词条

    spells: list['Spell']

    state: 'WandState | None'

    def compile(self) -> list['SpellGroup']:
        ...

SpellType = Literal['projectile']

@dataclass
class WandState:
    index: int
    spell_groups: list['SpellGroup']

class Spell:
    cast_delay: float
    recharge_time: float
    hit_rate: int
    crit_rate: int

    uses: int             # 使用次数，-1表示无限
    mana_cost: int        # 法力消耗
    radius: int
    damage: int

class SpellGroup:
    spell: Spell
    indices: list[int]


