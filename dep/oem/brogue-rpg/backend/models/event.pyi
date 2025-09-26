from typing import Literal, overload
from backend.battle.damage import DamageFlow
from backend.models.actor import Actor
from backend.models.affix import Trigger

Event = Literal[
    'on_hero_move',
    'on_hero_attack',
]

LocalEvent = Literal[
    'on_pre_hit',
    'on_post_hit',
    'on_death_hit',
]

class EventDispatcher:
    @overload
    def broadcast(self, event: Literal['on_hero_move'], params: None): ...
    @overload
    def broadcast(self, event: Literal['on_hero_attack'], params: None): ...

    @overload
    def send(self, actor: Actor, event: Literal['on_pre_hit'], params: DamageFlow): ...
    @overload
    def send(self, actor: Actor, event: Literal['on_post_hit'], params: DamageFlow): ...
    @overload
    def send(self, actor: Actor, event: Literal['on_death_hit'], params: DamageFlow): ...

    def add_trigger(self, trigger: Trigger) -> None: ...
