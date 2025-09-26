from .casting import CastingMethod

class SpellModifier:
    power: int
    range: int
    multicast: int
    cost_sp: int
    cost_time: float
    recharge_time: float

class Spell:
    method: CastingMethod
    tier: int
    dmg_type: str
    modifiers: list[SpellModifier]

