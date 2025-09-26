from vmath import vec2i

import backend
import random

from frontend import ConsoleIO, platform
from backend.models import Actor

# 生成地图
# if 0:
#     from dungeon.brogue.levels import brogue_carveDungeon
#     from dungeon.brogue.const import LevelProfile
#     m_terrain, doors = brogue_carveDungeon(LevelProfile(5, 10))
#     zone = backend.Zone(m_terrain.width, m_terrain.height)
#     zone.m_terrain = m_terrain.map({0: T.Void(), 1: T.Empty(), 6: T.Wall()}.__getitem__)
#     for door in doors:
#         zone.m_building[door[0]] = B.ClosedDoor()
# else:
#     from backend.dungeon.example import build
#     zone = backend.Zone.from_primed(build(50, 30, 2024))

world = backend.World()

playground = backend.levels.Playground.build_region()
target = world.a.view_rect(vec2i(-5, -5), playground.width, playground.height)
target[:, :] = playground

hero = world.spawn_actor(backend.Hero, vec2i.ZERO)

# 在主角附近随机位置放置一个怪物
def random_place(T: type[Actor]):
    for pos, dist in world.bfs(hero.pos):
        if dist < 3:
            continue
        if dist > 10 or random.random() < 0.1:
            world.spawn_actor(T, pos)
            return pos
    assert False, "No place to spawn"

random_place(backend.levels.BorderTown.test_actors.TestMob)

############################################################
from backend.models import *
from backend.asyncio import Task
from frontend.i18n import string, ui


class ChooseTarget(Task):
    def __init__(self, output='target'):
        self.output = output

    def call(self, context):
        context[self.output] = ...
        return 0.0


class DeleteItem(Task):
    def call(self, context):
        item = context['item']
        game.hero.inventory.remove(item)
        return 0.0


from backend.battle.attack import NormalWeapon
from backend.battle.damage import DamageInfo

ShortSword = Item(
        name=string('Short Sword', '短剑'),
        desc=string('Deal 2-4 damage.', '造成 2-4 点伤害。')
    ).on_equip(
        Modifier('max_sp', 10),
        # 当玩家移动，恢复1点HP
        MethodTrigger(
            'on_hero_move',
            MethodCall(
                Expr.eval('current_game().hero'),
                'add_hp',
                Expr.value(1),
            )
        )
    ).on_attack(
        NormalWeapon.default().with_damage(
            Expr.value(2), Expr.value(4),
            DamageInfo(is_melee=True)
        )
    )

SmallHealingPotion = Item(
        name=string('Small Healing Potion', '小型治疗药水'),
        desc=string('Restore 15% health.', '恢复 15% 生命值。')
    ).on_action(
        ui.Drink, Task.pipeline([
            Task.callback(
                MethodCall(
                    Expr.context(Item.CTX_USER),
                    'add_hp',
                    Expr.context(Item.CTX_USER, 'stats.max_hp.value') * 15 // 100
                ),
            ),
            DeleteItem()
        ])
    ).on_action(
        ui.Drop, DeleteItem()
    )

if 0:
    from backend.checkpoint import dumps, dumps_json, loads
    from vmath import vec2i
    __obj = {
        'item_1': ShortSword,
        'item_2': SmallHealingPotion,
    }
    print(__obj)
    data = dumps_json(__obj)
    with open('test.json', 'w') as f:
        f.write(data)
    print(data)
    print(loads(data))
    assert dumps_json(loads(data)) == data
    exit()

hero.inventory.items[0].set(SmallHealingPotion)
# hero.inventory.items[1].set(ShortSword)
hero.equipments.weapon.set(ShortSword)

# 创建游戏
io = ConsoleIO()
game = backend.Game(io, world, hero)
game_iterator = iter(game)

import pkpy
pkpy.enable_full_buffering_mode()

print('\x1bc', flush=True)

def step_game():
    """Step the game and render the result.
    
    Return `False` if the game is over, otherwise `True`.
    """
    io.begin_frame()
    res = next(game_iterator, StopIteration)
    io.end_frame()
    return res is not StopIteration
