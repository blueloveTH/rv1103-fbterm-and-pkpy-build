from typing import TYPE_CHECKING

from array2d import array2d
from vmath import vec2, vec2i


from .schema import Rect

from .regions import dfs

from .regions import _Region, _Corridor, Region, Corridor, Room

from .astar import base_astar_in_grid

from .utils import (
    add_outline_to_,
    calc_outerbound_rect,
    try_map_anchored_grid_to,
    try_map_grid_to_,
    random_by_freq
)

from .test_tools import *

from .grow import GrowStrategy

import math


if TYPE_CHECKING:
    from .io import DungeonIO


class Builder[T: _Region]:
    def first_build(self, io: "DungeonIO") -> T:
        raise NotImplementedError

    def build(self, io: "DungeonIO", context: "BuildContext") -> T:
        raise NotImplementedError


class BuildContext:
    """生长上下文"""

    region: Region  # 通常是玩家当前所在的房间，或者是准备进行分支的房间
    direction: vec2  # 指引房间Builder生成的方向
    grow_strategy: GrowStrategy

    # ----以下是内部维护的字段
    _corridor_start_pos: vec2i|None = None  # 走廊builder必要的参数
    _corridor_end_pos: vec2i|None = None
    _new_room: Room|None = None  # 寄存grow策略中新生成的新房间


    def __init__(self):
        pass




class BaseCorridorTerrianBuilder():
    def __init__(self):
        pass
    def build_terrian(self, corridor:_Corridor, io: DungeonIO, context: BuildContext) -> None:
        raise NotImplementedError

    
class CorridorBuilder():
    def __init__(self, t_builder: BaseCorridorTerrianBuilder):
        self.t_builder = t_builder
    def build(self, io: DungeonIO, context: BuildContext) -> _Corridor:
        assert context._corridor_start_pos is not None and context._corridor_end_pos is not None
        start_pos = context._corridor_start_pos
        end_pos = context._corridor_end_pos
        assert isinstance(start_pos, vec2i) and isinstance(end_pos, vec2i)
        assert io.global_to_local(start_pos)
        corridor = _Corridor(start_pos, end_pos, io.next_id(), None, None, None)
        self.t_builder.build_terrian(corridor, io, context)
        return corridor
        

class AncientAstarTerrianBuilder(BaseCorridorTerrianBuilder):

    def build_terrian(self, corridor:_Corridor, io: DungeonIO, context: BuildContext) -> None:

        is_blank_fn = lambda x: x == io.t_values.BLANK

        
        # 确定两个房间的外接矩形与其他与该外接矩形重叠的region所一起形成的大外接矩形, 然后放大至2倍
        all_regions: set[Region] = set()
        dfs(context._new_room, all_regions)
        astar_searching_regions = [\
                region\
                for region in all_regions.union(set([context._new_room, context.region]))\
                ]
        astar_searching_rect = calc_outerbound_rect([region.get_rect() for region in astar_searching_regions]).up_scaled(2).floor_align()
        astar_searching_grid = array2d(int(astar_searching_rect.w), int(astar_searching_rect.h), default=0)

        # 生成该矩形所框出的地形array2d
        for region in astar_searching_regions:
            result = try_map_anchored_grid_to(astar_searching_grid, vec2i(int(astar_searching_rect.x), int(astar_searching_rect.y)), is_blank_fn, region.m_terrain, region.base)
            assert result == True
    
        start_pos = astar_searching_rect.global_to_local(context._corridor_start_pos)
        end_pos = astar_searching_rect.global_to_local(context._corridor_end_pos)
        path = base_astar_in_grid(astar_searching_grid.map(is_blank_fn), start_pos, end_pos)
        assert path is not None
        
        # 根据路径确定其最小包围盒，也作为corridor的尺寸
        temp_grid = array2d(astar_searching_grid.width, astar_searching_grid.height, default=0)
        corridor.path = path
        for pos in path:
            temp_grid[pos] = io.t_values.BLANK
        x,y,w,h = temp_grid.get_bounding_rect(io.t_values.BLANK)
        
        # 将path映射到corridor内
        corridor_rect = Rect(x+astar_searching_rect.x,y+astar_searching_rect.y,w,h)
        corridor.base = vec2i(int(corridor_rect.x), int(corridor_rect.y))
        corridor.m_terrain = array2d(w,h,0)
        for pos in path:
            pos_in_corridor = corridor_rect.global_to_local(astar_searching_rect.local_to_global(pos))
            corridor.m_terrain[vec2i(int(pos_in_corridor.x), int(pos_in_corridor.y))] = io.t_values.BLANK
        
        
        corridor.m_buildings = array2d(corridor.m_terrain.width, corridor.m_terrain.height, default=0)
        
        