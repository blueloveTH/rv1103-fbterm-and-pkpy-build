from dataclasses import dataclass
from vmath import vec2i
from array2d import array2d
from .schema import Rect
from typing import Callable
from .utils import DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT, DIRS_4
from .test_tools import print_grid



class _Region:
    """内部类, 仅用于组织构造真正的Region需要用到的对象, 不包含外部其他房间的信息"""

    def __init__(
        self, id: int, base: vec2i, m_terrain: array2d[int], m_buildings: array2d[int]
    ):
        self.id = id  # 区域ID
        self.base = base  # 房间左上角原点在地牢中的位置
        self.m_terrain = m_terrain  # 区域内部的地形
        self.m_buildings = m_buildings  # 区域内部的建筑（包括门）
        
    
    def get_rect(self) -> Rect:
        if self.base is None:
            x,y = None, None
        else:
            x, y = self.base
        return Rect(x, y, self.m_terrain.width, self.m_terrain.height)


    def validate(self):
        assert isinstance(self.id, int)
        assert isinstance(self.base, vec2i)
        assert isinstance(self.m_terrain, array2d)
        assert isinstance(self.m_buildings, array2d)
        assert self.m_terrain.width == self.m_buildings.width
        assert self.m_terrain.height == self.m_buildings.height


    def reset_from_rect(self, rect: Rect):
        """设置base, 重置m_terrain, m_buildings并赋予wh"""
        self.base = rect.xy
        self.m_terrain = array2d(rect.w, rect.h, 0)
        self.m_buildings = array2d(rect.w, rect.h, 0)

    def to_region(self):
        self.validate()
        return Region(self.id, self.base, self.m_terrain, self.m_buildings)

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id}, base={self.base}, shape={self.get_rect().wh})"

class _Room(_Region):
    def to_room(self):
        self.validate()
        return Room(self.id, self.base, self.m_terrain, self.m_buildings)
    
class _Corridor(_Region):
    def __init__(self, start_pos:vec2i, end_pos:vec2i, id: int, base: vec2i, m_terrain: array2d[int], m_buildings: array2d[int]
    ):
        super().__init__(id, base, m_terrain, m_buildings)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.path = []
    def to_corridor(self):
        self.validate()
        return Corridor(self.id, self.base, self.m_terrain, self.m_buildings, self.start_pos, self.end_pos)

class Region:
    """地牢的区域"""

    def __init__(self, id: int, base: vec2i, m_terrain: array2d[int], m_buildings: array2d[int]):
        assert (
            isinstance(id, int)\
            and isinstance(base, vec2i)\
            and isinstance(m_terrain, array2d)\
            and isinstance(m_buildings, array2d)\
        )
        self.id = id  # 区域ID
        self.base = base  # 房间左上角原点在地牢中的位置
        self.m_terrain = m_terrain  # 区域内部的地形
        self.m_buildings = m_buildings  # 区域内部的建筑（包括门）
        self.neighbors = set()  # 相邻区域  type: set[Region]
        self.extras = RegionExtras()

    @property
    def base(self):
        return self._base
    @base.setter
    def base(self, base: vec2i):
        assert isinstance(base, vec2i)
        self._base = base

    def get_rect(self) -> Rect:
        assert self.m_terrain.width == self.m_buildings.width and self.m_terrain.height == self.m_buildings.height
        return Rect(self.base.x, self.base.y, self.m_terrain.width, self.m_terrain.height)

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id}, base={self.base}, shape={self.get_rect().wh})"

    @property
    def bounding_rect(self) -> tuple[vec2i | None, vec2i]:
        """返回区域的包围盒"""
        xy = self.base

        if self.m_terrain is not None:
            wh = vec2i(self.m_terrain.width, self.m_terrain.height)
            return xy, wh
        else:
            wh = vec2i(self.m_buildings.width, self.m_buildings.height)
            return xy, wh

    def connect_to(self, other: "Region") -> None:
        """连接两个区域 让self指向other"""
        self.neighbors.add(other)
        self.extras.out_bound_neighbors.add(other)
        other.neighbors.add(self)
        other.extras.in_bound_neighbors.add(self)
        


@dataclass
class RegionExtras:
    in_bound_neighbors: set[Region] = set()
    out_bound_neighbors: set[Region] = set()


class Room(Region):
    def get_terrian_center(self, t_in_room_fn: Callable[[int], bool])->vec2i:
        '''获取房间地形外接矩形的中心（局部坐标）, 参与计算的地形值需要满足t_in_room_fn
        
        1. 取地形包围盒的中心点, 如果命中地形且不在边缘, 那么返回该点
        
        2. 如果矩形中心没有命中房间地形格子, 那么向四个方向发射探测线, 每一轮探测, 四个探测线的长度先后增长1, 直到探测到非边缘的房间地形, 返回探测线的最后一个点。
        
        3. 如果所有探测线都没有命中非边缘格子, 那么返回房间中心点。(因为是包围盒，因此从矩形中央发出的四条射线中至少会存在两条探测到地形格子，但因为少数是地形边缘的格子，因此他们会被探测线忽略)
        
        '''
        mask: array2d[bool] = self.m_terrain.map(t_in_room_fn)
        mask = mask.count_neighbors(True, "Moore").map(lambda x: x==8)  # 非地形边缘的格子地图
        
        rect: tuple[int, int, int, int] = mask.get_bounding_rect(True)
        assert rect is not None
        x,y,w,h = rect
        fcenter = Rect(x,y,w,h).center  # 地形包围盒的中心点坐标（相对于整个房间的左上角）
        center = vec2i(int(fcenter.x), int(fcenter.y))
        
        # 终止条件
        dir4_are_not_valid: dict[vec2i, bool] = {DIR_UP:False, DIR_DOWN:False, DIR_LEFT:False, DIR_RIGHT:False}
        
        detecting_line_length:int = 0
        while not all(dir4_are_not_valid.values()):  # 直到所有方向的探测线都超出array2d才跳出循环
            for dir_delta in DIRS_4:
                current_pos = center + vec2i(detecting_line_length * dir_delta.x, detecting_line_length * dir_delta.y)
                if not mask.is_valid(current_pos):
                    dir4_are_not_valid[dir_delta] = True
                    continue
                else:
                    # 探测点在array2d内部
                    if mask[current_pos] is True:
                        # 当第一次探测到存在房间地形, 则返回探测点坐标
                        return current_pos
            detecting_line_length += 1
        
        # 四个方向的探测线都超出了array2d
        return center


class Corridor(Region):
    start_pos: vec2i
    end_pos: vec2i

    def __init__(self, id: int, base: vec2i, m_terrain: array2d[int], m_buildings: array2d[int], start_pos: vec2i, end_pos: vec2i):
        super().__init__(id, base, m_terrain, m_buildings)
        self.start_pos = start_pos
        self.end_pos = end_pos
    def __repr__(self):
        return f"{type(self).__name__}(id={self.id}, base={self.base}, shape={self.get_rect().wh}, start_pos={self.start_pos}, end_pos={self.end_pos})"


def dfs(node: "Region", visited: set["Region"]):
    if node in visited:
        return
    visited.add(node)
    for neighbor in node.neighbors:
        dfs(neighbor, visited)
