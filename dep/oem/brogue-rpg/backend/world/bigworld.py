from array2d import chunked_array2d
from vmath import vec2i, vec2
from collections import deque
import random
from typing import TYPE_CHECKING, Iterable

from backend.models.actor import Actor
from backend.battle.damage import DamageInfo, DamageFlow
from backend.asyncio import Task
from backend.utils import DIRS_4_CW, DIRS_8_CW
from backend.dungeon.perlin import Perlin

from .tile import Tile, TileData

class ChunkContext:
    def __init__(self, chunk_pos: vec2i):
        self.chunk_pos = chunk_pos
        self.ttl = 5

    def reset_ttl(self):
        self.ttl = 5

class World:
    def __init__(self):
        self.a = chunked_array2d[Tile, ChunkContext](
            8,
            default=Tile(0),
            context_builder=ChunkContext,
        )
        self.actors = dict[vec2i, Actor]()
        self.perlin = Perlin(seed=7)
        self.rand = random.Random(7)
    
    def init_chunk(self, chunk_pos: vec2i):
        context = self.a.get_context(chunk_pos)
        if context is None:
            context = self.a.add_chunk(chunk_pos)
            chunk = self.a.view_chunk(chunk_pos)
            # initialize the chunk
            for local_pos, _ in chunk:
                tile = Tile(0)
                tile.tt_ground = TileData(2, 0)

                pos = vec2(chunk.origin + local_pos + vec2i.ONE * 65536) / 5
                if self.perlin.noise_ex(pos.x, pos.y, 0, 1) > 0.2:
                    tile.tt_grass = TileData(5, 0)
                chunk[local_pos] = tile
        context.reset_ttl()

    def refresh_actor_chunks(self, actor: Actor):
        return
        radius = actor.bigworld_loading_radius
        if radius == 0:
            return
        chunk_pos, _ = self.a.world_to_chunk(actor.pos)
        for x in range(-(radius-1), radius):
            for y in range(-(radius-1), radius):
                dst_chunk_pos = chunk_pos + vec2i(x, y)
                self.init_chunk(dst_chunk_pos)

    def refresh_chunks(self):
        return
        for pos, context in self.a:
            context.ttl -= 1
            if context.ttl <= 0:
                assert self.a.remove_chunk(pos)

    def spawn_actor[T: Actor](self, t: type[T], pos: vec2i) -> T:
        actor = t()
        actor.pos = pos
        self.refresh_actor_chunks(actor)
        # don't modify default!!! e.g. get an inexistent key (default object) and modify it
        self.actors[pos] = actor
        return actor

    def destroy_actor(self, actor: Actor) -> None:
        del self.actors[actor.pos]

    def move_actor(self, actor: Actor, delta: vec2i) -> None:
        self.teleport_actor(actor, actor.pos + delta)

    def teleport_actor(self, actor: Actor, target: vec2i) -> None:
        del self.actors[actor.pos]
        actor.pos = target
        self.actors[actor.pos] = actor
        self.refresh_actor_chunks(actor)

    def interact(self, actor: Actor, target: vec2i) -> Task | None:
        """让actor和target位置的单位进行交互，如果可行的话，返回一个命令"""
        for pos, fg in self.actors.items():
            if pos == target:
                return fg.interact(actor)

    def is_walkable(self, pos: vec2i) -> bool:
        """检查坐标是否是可行走的"""
        return self.a[pos].is_walkable() and pos not in self.actors

    def bfs(self, pos: vec2i, filter=None) -> Iterable[tuple[vec2i, int]]:
        """由近及远地搜索满足条件的坐标，迭代地返回一个包含坐标和距离的元组"""
        filter = filter or self.is_walkable
        q = deque[tuple[vec2i, int]]()
        visited = set[vec2i]()
        q.appendleft((pos, 0))
        visited.add(pos)
        while len(q) > 0:
            pos, dist = q.pop()
            yield pos, dist
            for delta in DIRS_4_CW:
                next_pos = pos + delta
                if next_pos in visited:
                    continue
                if not filter(next_pos):
                    continue
                q.appendleft((next_pos, dist+1))
                visited.add(next_pos)
