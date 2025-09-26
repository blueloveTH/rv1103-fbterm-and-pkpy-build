from vmath import vec2i
from backend.models.actor import Mob, Actor
from backend.asyncio import *

# def welcome(context: dict) -> Future[int]:
#     io = current_io()
#     idx = yield from io.choices([i18n.ui.Talk, i18n.ui.Trade, i18n.ui.Leave])
#     if idx == 0:
#         yield from io.monologue([
#             i18n.string(
#                 "Welcome, adventurer. My name is Elia, a mage from the BorderTown. I know you're here to seek powerful magic.",
#                 "你好，冒险者。我是艾莉亚，一位来自边境小镇的魔导师。我知道你是来寻找强大的魔法的。"
#             ),
#             i18n.string(
#                 "Take this wand, it would be useful.",
#                 "收下这个新手法杖，它会派上用场的。",
#             )
#         ])
#     return 0


# class TestNpc(Actor):
#     def __init__(self) -> None:
#         super().__init__()
#         self.hp = vec2i(20, 20)

#     def wait_for_command(self):
#         import backend
#         for d in backend.utils.DIRS_8_CW:
#             current_world().a[self.pos + d].tt_ground = backend.world.TileData(2, 1)

#         return common_tasks.Idle()

#     @property
#     def char(self) -> str:
#         return "🔮"
    
#     def interact(self, actor: Actor) -> Task | None:
#         assert isinstance(actor, Actor)
#         if actor.is_hero:
#             return Task.future_callback(welcome)


class TestMob(Mob):
    def __init__(self) -> None:
        super().__init__()
        self.with_level(5)

    def wait_for_command(self):
        return common_tasks.Idle()

    @property
    def char(self) -> str:
        # return "🪳"
        return "🐍"