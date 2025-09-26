from typing import TYPE_CHECKING, Literal, Iterable

from .models.actor import Hero, TurnBasedActor
from .models.event import EventDispatcher


if TYPE_CHECKING:
    from .world import World
    from .io import IO

Locale = Literal["en_US", "zh_CN"]

class Game:
    instance: 'Game'

    def __init__(self, io: IO, world: World, hero: Hero) -> None:
        Game.instance = self
        self.io = io
        self.locale = "zh_CN"       # type: Locale
        self.world = world
        self.hero = hero
        self.messages = []          # type: list[str]
        self.events = EventDispatcher()

    def message(self, msg: str):
        self.messages.insert(0, msg)
        if len(self.messages) > 10:
            self.messages.pop()

    def __iter__(self):
        yield from self.io.wait_for_game_start()

        from backend.asyncio import Task

        while True:
            tb_actors: Iterable[TurnBasedActor] = self.world.actors.values()
            # determine the next actor to act
            # 1. the actor with the smallest time acts first
            # 2. if multiple actors have the same time, the actor with the highest priority acts first
            actor = min(tb_actors, key=lambda u: (u.tb_info.time, -u.tb_info.priority))

            while True:
                cmd = actor.wait_for_command()
                if not isinstance(cmd, Task):
                    cmd = yield from cmd
                break

            duration = yield from cmd({})
            actor.tb_info.time += duration


# inject to builtins
import builtins

setattr(builtins, 'current_game', lambda: Game.instance)
setattr(builtins, 'current_world', lambda: Game.instance.world)
setattr(builtins, 'current_io', lambda: Game.instance.io)
