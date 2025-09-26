from array2d import array2d
from ..builders import BuildContext
from ..io import DungeonIO
from ..regions import _Room
from ..test_tools import BuildContext, DungeonIO, array2d, vec2i
from ..utils import random_by_freq
import terrian_impl

from vmath import vec2i


class BaseRoomTerrainer:
    """提供自定义房间地形的接口"""
    def build_terrain(
        self, region: _Room, io: DungeonIO, context: BuildContext | None = None
    ):
        raise NotImplementedError

class BrogueRoomTerrainer(BaseRoomTerrainer):
    """构造Brogue风格的房间地形"""
    def __init__(self, impl_func_name_or_freq_dict: str|dict[str, int], room_wh: vec2i):
        if isinstance(impl_func_name_or_freq_dict, str):
            self.room_freq = {impl_func_name_or_freq_dict: 1}
        elif isinstance(impl_func_name_or_freq_dict, dict):
            self.room_freq = impl_func_name_or_freq_dict
        else:
            raise TypeError
        
        self.room_wh = room_wh
        
    def _make_terrian_grid(self, io:DungeonIO)-> array2d[int]:
        # 初始化地形array2d
        terrian_grid = array2d(self.room_wh.x, self.room_wh.y, default=0)

        # 选择地形生成函数
        impl_func_name = random_by_freq(self.room_freq)

        # 生成房间
        if impl_func_name == "brogue_designCrossRoom":
            terrian_impl.brogue_designCrossRoom(terrian_grid)
        elif impl_func_name == "brogue_designSymmetricalCrossRoom":
            terrian_impl.brogue_designSymmetricalCrossRoom(terrian_grid)
        elif impl_func_name == "brogue_designSmallRoom":
            terrian_impl.brogue_designSmallRoom(terrian_grid)
        elif impl_func_name == "brogue_designCircularRoom":
            terrian_impl.brogue_designCircularRoom(terrian_grid)
        elif impl_func_name == "brogue_designChunkyRoom":
            terrian_impl.brogue_designChunkyRoom(terrian_grid)
        elif impl_func_name == "brogue_design_cave":
            terrian_impl.brogue_design_cave(terrian_grid, self.room_wh.x, self.room_wh.y)
        elif impl_func_name == "brogue_designEntranceRoom":
            terrian_impl.brogue_designEntranceRoom(terrian_grid)
        elif impl_func_name == "brogue_design_compat_cavern":
            terrian_impl.brogue_design_compat_cavern(terrian_grid)
        elif impl_func_name == "brogue_design_large_north_south_cavern":
            terrian_impl.brogue_design_large_north_south_cavern(terrian_grid)
        elif impl_func_name == "brogue_design_large_east_west_cavern":
            terrian_impl.brogue_design_large_east_west_cavern(terrian_grid)
        else:
            raise ValueError(f"Unknown impl_func_name: {impl_func_name}")

        return terrian_grid.map(lambda x: io.t_values.BLANK if x==1 else 0)


    def build_terrain(self, region, io, context = None):
        region.m_terrain = self._make_terrian_grid(io)
        
        



class SquareRoomTerrainer(BaseRoomTerrainer):
    """构造正方形的房间地形"""

    wh: vec2i
    side_length: int

    def __init__(self, side_length: int):
        assert side_length >= 2
        self.side_length = side_length
        self.wh = vec2i(side_length+2, side_length+2)

    def _make_terrian_grid(self, io: DungeonIO)-> array2d[int]:
        terrian_grid = array2d(self.wh.x, self.wh.y, default=0)
        terrian_impl.fill_rect_(
            terrian_grid, io.t_values.BLANK, (self.wh.x-self.side_length)//2, (self.wh.y-self.side_length)//2, self.side_length, self.side_length
        )
        return terrian_grid

    def build_terrain(
        self, region: _Room, io: DungeonIO, context: BuildContext | None = None
    ):
        # context: BuildContext|None 意味着可被用于first_build环节

        region.m_terrain = self._make_terrian_grid(io)