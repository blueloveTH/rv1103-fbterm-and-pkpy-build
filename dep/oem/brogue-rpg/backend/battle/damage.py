from typing import Literal, TYPE_CHECKING
from random import Random
from dataclasses import dataclass

if TYPE_CHECKING:
    from backend.models import Actor
    from backend.game import Game


DamageType = Literal[
    'normal',
    'fire',
    'cold',
    'lightning',
    'poison',
    'curse',
]

ELEMENTAL_DAMAGE_TYPES = ('fire', 'cold', 'lightning', 'poison')

DamageSource = Literal[
    'normal',           # 普通攻击
    'environmental',    # 环境
    'spell',            # 法术
    'others',           # 其他
]

@dataclass
class DamageInfo:
    type: DamageType = 'normal'
    source: DamageSource = 'normal'
    is_melee: bool = False
    is_projectile: bool = False

    @property
    def is_elemental(self) -> bool:
        return self.type in ELEMENTAL_DAMAGE_TYPES



DamageOutcome = Literal[
    'miss',
    'block',
    'hit',
    'death_hit',
]

class DamageFlow:
    def __init__(self, src: Actor, dst: Actor, dmg: int, dmg_info: DamageInfo, rand: Random | None = None):
        self.src = src
        self.dst = dst
        self.dmg = dmg
        self.dmg_info = dmg_info
        self.rand = rand or Random()
        self.outcome = None     # type: DamageOutcome | None

    def reduce_dmg_fixed(self, dmg: int, value: int) -> int:
        return max(0, dmg - value)

    def reduce_dmg_percent(self, dmg: int, percent: int) -> int:
        percent = min(percent, 100)
        return dmg * (100 - percent) // 100

    def roll(self, chance: int) -> bool:
        return self.rand.randint(0, 100) < chance

    def __call__(self):
        game = current_game()
        self.call_impl(game)
        match self.outcome:
            case 'miss':
                game.message(f'{self.src.char}攻击{self.dst.char}失败，未命中！')
            case 'block':
                game.message(f'{self.src.char}攻击{self.dst.char}被格挡！')
            case 'hit':
                game.message(f'{self.src.char}攻击{self.dst.char}，造成{self.dmg}点伤害！')
            case 'death_hit':
                game.message(f'{self.src.char}攻击{self.dst.char}，造成{self.dmg}点伤害，击杀了对方！')
            case _:
                assert False, self.outcome

    def call_impl(self, game: 'Game'):
        if self.roll(self.dst.stats.dodge.value):
            # 闪避判定
            self.outcome = 'hit'
            return
        
        game.events.send(self.dst, 'on_pre_hit', self)
        if self.outcome is not None:
            return
        
        if self.dmg_info.is_projectile:
            # 格挡判定
            if self.roll(self.dst.stats.block.value):
                self.outcome = 'block'
                return

        # 伤害减免
        defense = self.dst.stats.defense.value
        if self.dmg_info.type == 'normal':
            self.dmg = self.reduce_dmg_fixed(self.dmg, defense)
        elif self.dmg_info.type in ELEMENTAL_DAMAGE_TYPES:
            if self.dmg_info.type == 'fire' and self.dmg_info.source == 'environmental':
                self.dmg = self.reduce_dmg_percent(self.dmg, self.dst.stats.env_fire_resist.value)
            if self.dmg_info.type == 'cold' and self.dmg_info.source == 'environmental':
                self.dmg = self.reduce_dmg_percent(self.dmg, self.dst.stats.env_cold_resist.value)
            self.dmg = self.reduce_dmg_percent(self.dmg, self.dst.stats.elemental_resist.value)
        elif self.dmg_info.type == 'curse':
            self.dmg = self.reduce_dmg_percent(self.dmg, self.dst.stats.curse_resist.value)
        else:
            assert False

        assert self.dmg >= 0
        self.dst.add_hp(-self.dmg)

        if self.dst.hp > 0:
            game.events.send(self.dst, 'on_post_hit', self)
            self.outcome = 'hit'
        else:
            current_world().destroy_actor(self.dst)
            game.events.send(self.dst, 'on_death_hit', self)
            self.outcome = 'death_hit'
