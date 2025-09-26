import random

from array2d import array2d
from vmath import vec2i, vec2

from .schema import Rect, TerrainValues, if_terrain_in_region

from .regions import Region, _Room, dfs
from .builders import Builder, BuildContext, RoomBuilder, CorridorBuilder
from .utils import calc_outerbound_rect, random_by_freq
import random


class DungeonConfig:
    """公共配置"""

    first_room_freq: dict["RoomBuilder", int]  # 第一个房间的概率
    room_freq: dict["RoomBuilder", int]  # 其他房间的概率
    
    corridor_freq: dict["CorridorBuilder", int]


class DungeonIO:
    """地牢由房间和走廊组成"""

    def __init__(
        self, config: DungeonConfig, t_values: TerrainValues, random: random.Random
    ) -> None:
        self.config = config
        self._next_id = 0
        self.t_values = t_values
        self.root = None  # type: Region | None
        self.random = random

    def next_id(self) -> int:
        """返回下一个区域的ID"""
        self._next_id += 1
        return self._next_id

    def first_grow(self) -> Region:
        """第一次生长，返回新增的区域"""
        builder = random_by_freq(self.config.first_room_freq)
        _room = builder.first_build(self)
        _room.m_buildings = array2d[int](_room.m_terrain.width, _room.m_terrain.height, default=0)
        room = _room.to_room()
        self.root = room
        return self.root  # type: ignore
    
    def global_to_local(self, global_pos:vec2i|vec2) -> list[tuple[Region, vec2i|vec2]]:
        '''将地图坐标转换为包含该坐标的所有Region及其本地坐标'''
        _global_pos = global_pos if isinstance(global_pos, vec2) else vec2(global_pos)

        all_regions:set[Region] = set()
        dfs(self.root, all_regions)
        
        found = []
        for region in all_regions:
            rect = region.get_rect()
            local_pos = rect.global_to_local(_global_pos)
            if local_pos.x >= 0 and local_pos.y >= 0 and local_pos.x < rect.w and local_pos.y < rect.h:
                _local_pos = vec2i(int(local_pos.x), int(local_pos.y)) if isinstance(global_pos, vec2i) else local_pos
                found.append((region, _local_pos))
        
        return found
    
    def grow(self, context: BuildContext):
        grow_strategy = context.grow_strategy
        grow_strategy.grow(self, context)
        


    # def grow(self, context: BuildContext) -> Region:
    #     """开始一次生长, 更新IO结构并返回此次新增的区域。生长不会改变已有的区域"""

    #     # 1. 生成房间
    #     builder = random_by_freq(self.config.region_freq)
    #     _region = builder.build(self, context)

    #     # 2. 初筛冲突的房间
    #     conflicted_regions: set[Region] = set()
    #     existing_regions: set[Region] = set()
    #     dfs(self.root, existing_regions)

    #     for existing_region in existing_regions:
    #         overlap_area: Rect | None = _region.get_rect().overlap(
    #             Rect.init_from_(existing_region.bounding_rect)
    #         )
    #         if overlap_area is not None:
    #             conflicted_regions.add(existing_region)

    #     # 3. 精确检测冲突的房间
    #     outerbound_rect = calc_outerbound_rect(
    #         [Rect.init_from_(region.bounding_rect) for region in conflicted_regions]
    #     )
    #     outerbound_region = Region(
    #         -1,
    #         outerbound_rect.xy,
    #         array2d[int](outerbound_rect.w, outerbound_rect.h, default=0),
    #         None,
    #     )

    #     for conflicted_region in conflicted_regions:
    #         try_map_terrain_to_(outerbound_region, lambda x: if_terrain_in_region(x, self.t_values), conflicted_region)
        
    #     # 4. 尝试插入至初筛冲突的区域，如果可以插入， 那么证明实际并没有冲突
    #     if try_map_terrain_to_(outerbound_region, lambda x: if_terrain_in_region(x, self.t_values), _region):
    #         # 成功生成房间, 转换成对外的Rect, 然后链接到其他region， 并返回
    #         region = _region.to_region()
    #         region.connect_to(context.region)
    #     else:
    #         # 失败
    #         raise ValueError("Region conflict")

    #     return region
