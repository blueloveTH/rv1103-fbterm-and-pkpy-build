from typing import TYPE_CHECKING
from vmath import vec2i
from array2d import array2d

from backend.utils import FacingTransform

if TYPE_CHECKING:
    from backend.models import Actor, Expr
    from backend.asyncio import Future
    from backend.battle.damage import DamageInfo


from .damage import DamageFlow

def pattern_to_offsets(pattern: str):
    lines = [
        list(line.strip())
        for line in pattern.split('\n')
        if line.strip()
    ]
    offsets: list[vec2i] = []
    a = array2d[str].fromlist(lines)
    center = a.index('P')
    for pos, val in a:
        if val == '#':
            offsets.append(pos - center)
    offsets.sort(key=lambda v: v.dot(v))
    return offsets


class IWeapon:
    min_dmg: Expr[int]
    max_dmg: Expr[int]
    dmg_info: DamageInfo

    def with_damage(self, min_dmg, max_dmg, info: DamageInfo):
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.dmg_info = info
        return self

    def player_get_auto_target(self) -> vec2i | None:
        game = current_game()
        valid_targets = self.get_valid_targets(game.hero)
        actors = game.world.actors
        for target in valid_targets:
            a = actors.get(target)
            if a is not None and a.is_mob:
                return target
        if len(valid_targets) == 0:
            return None
        return valid_targets[0]

    def get_valid_targets(self, src: Actor) -> list[vec2i]:
        raise NotImplementedError(type(self))

    def attack(self, ctx: dict, src: Actor, target: vec2i) -> Future[float]:
        raise NotImplementedError(type(self))


class NormalWeapon(IWeapon):
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.offsets = pattern_to_offsets(pattern)

    @staticmethod
    def default():
        pattern = """
        ....
        P#..
        ....
        """
        return NormalWeapon(pattern)

    def get_valid_targets(self, src):
        targets: list[vec2i] = []
        facing = src.facing
        if facing == vec2i.ZERO:
            return targets
        trans = FacingTransform(vec2i.RIGHT, facing)
        for offset in self.offsets:
            dst_pos = src.pos + trans(offset)
            targets.append(dst_pos)
        return targets
    
    def attack(self, ctx, src, target):
        yield  # TODO: 动画播放
        import random
        dmg = random.randint(self.min_dmg(ctx), self.max_dmg(ctx))
        world = current_world()
        dst = world.actors.get(target)
        if dst is not None:
            flow = DamageFlow(src, dst, dmg, self.dmg_info)
            flow()
        return 1.0

