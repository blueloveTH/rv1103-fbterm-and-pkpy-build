import terrian_impl
from array2d import array2d
from ..utils import random_by_freq
from vmath import vec2i
from typing import Literal


DEFAULT_FREQ_DICT = {
    "brogue_designCrossRoom": 1,
    "brogue_designSymmetricalCrossRoom": 1,
    "brogue_designSmallRoom": 1,
    "brogue_designCircularRoom": 1,
    "brogue_designChunkyRoom": 1,
    "brogue_design_cave": 1,
    "brogue_designEntranceRoom": 1,
    "brogue_design_compat_cavern": 1,
    "brogue_design_large_north_south_cavern": 1,
    "brogue_design_large_east_west_cavern": 1,
}


def make_terrian_grid(room_wh:vec2i, freq_dict: dict[str, int]|None=None)-> array2d[Literal[0,1]]:

    # 初始化地形array2d
    terrian_grid = array2d(room_wh.x, room_wh.y, default=0)

    # 选择地形生成函数
    impl_func_name = random_by_freq(freq_dict or DEFAULT_FREQ_DICT)

    # 生成地形
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
        terrian_impl.brogue_design_cave(terrian_grid, room_wh.x, room_wh.y)
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

    return terrian_grid