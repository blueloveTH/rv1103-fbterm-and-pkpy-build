from .builder_config import BuilderConfig
from .terrianer import BaseRoomTerrainer
from ..builders import Builder
from ..regions import _Room
from .placer import BaseRoomPlacer
from ..io import DungeonIO, BuildContext
from vmath import *

class RoomBuilder(Builder[_Room]):

    def __init__(self, builder_cfg:BuilderConfig):
        self.t_builder = t_builder
        self.placer = placer

    def first_build(self, io: DungeonIO) -> _Room:
        room = _Room(io.next_id(), vec2i(0, 0), None, None)
        self.t_builder.build_terrain(room, io)
        return room

    def build(self, io: DungeonIO, context: BuildContext) -> _Room:
        # 1. 初始化空房间
        room = _Room(io.next_id(), None, None, None)
        # 2. 初始化地形和建筑地图, 生成scale和地形
        self.t_builder.build_terrain(room, io, context)
        return room