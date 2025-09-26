from typing import TYPE_CHECKING
from vmath import vec2i

from .base import Task

if TYPE_CHECKING:
    from backend.models import Actor
    from backend.battle.attack import IWeapon

class Idle(Task):
    def call(self, context: dict) -> float:
        return 1.0

class Move(Task):
    def __init__(self, actor: Actor, delta: vec2i) -> None:
        self.actor = actor
        self.delta = delta

    def call(self, context: dict):
        current_world().move_actor(self.actor, self.delta)
        if self.actor.is_hero:
            current_game().events.broadcast('on_hero_move', None)
        return 1.0
    
class NormalAttack(Task):
    def __init__(self, actor: Actor, weapon: IWeapon, target: vec2i) -> None:
        self.actor = actor
        self.weapon = weapon
        self.target = target

    def call_async(self, context: dict):
        return self.weapon.attack(context, self.actor, self.target)


__all__ = ['Idle', 'Move', 'NormalAttack']