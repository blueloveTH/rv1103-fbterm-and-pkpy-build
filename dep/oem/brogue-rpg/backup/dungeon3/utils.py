from dataclasses import dataclass
import random
from typing import Callable

from array2d import array2d
from vmath import vec2i, vec2

from .schema import Rect

# 方向定义
DIR_UP = vec2i(0, -1)            # 上
DIR_DOWN = vec2i(0, 1)          # 下
DIR_LEFT = vec2i(-1, 0)         # 左
DIR_RIGHT = vec2i(1, 0)         # 右
DIR_UPPER_RIGHT = vec2i(1, -1)  # 右上
DIR_UPPER_LEFT = vec2i(-1, -1)  # 左上
DIR_LOWER_RIGHT = vec2i(1, 1)   # 右下
DIR_LOWER_LEFT = vec2i(-1, 1)   # 左下


# 四个主要方向
DIRS_4:tuple[vec2i, vec2i, vec2i, vec2i] = (DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT)
OPPO_DIR_4:tuple[vec2i, vec2i, vec2i, vec2i] = (DIR_DOWN, DIR_UP, DIR_RIGHT, DIR_LEFT)

def random_by_freq[T](freq: dict[T, int]) -> T:
    """根据权重随机选择一个元素"""
    return random.choices(
        list(freq.keys()),
        list(freq.values())
    )[0]


# def try_map_room_to_(grid: array2d[int], if_terrain_in_room:Callable[[int], bool], room_grid: array2d[int], delta:vec2i) -> bool:
#     """尝试将`room_grid`中的格子映射到`grid`中

#     设`(x, y)`是房间格子在`room_grid`中的位置, 那么它被映射到`grid`中的位置是`(x+delta_x, y+delta_y)`

#     如果满足条件，且映射后不与其他房间重叠，并距离边界大于一格的距离，则返回`True`，否则返回`False`
#     """

#     f_ = lambda x: x != 0

#     modified_grid = grid.copy()
#     # 预先求出 grid 中每个格子周围的 ZERO 的数量
#     grid_zero_neighbors = grid.count_neighbors(0, "Moore")

#     # 用底层算法求一下外接矩形，减少 python 层面循环的次数
#     room_flag_grid = room_grid.map(lambda x: if_terrain_in_room(x))
#     x_, y_, w_, h_ = room_flag_grid.get_bounding_rect(True)
#     for room_y in range(y_, y_ + h_):
#         for room_x in range(x_, x_ + w_):
#             # 我们只需要挑出属于房间的格子并进行判断, 以保证房间在被移动到 grid 时是完整的并距离边界保持一格的距离
#             t = room_grid[room_x, room_y]
#             if not if_terrain_in_room(room_grid[room_x, room_y]):
#                 continue
#             # 偏移后的房间格子在 grid 中的位置
#             grid_pos = vec2i(room_x, room_y) + delta
#             if not grid.is_valid(grid_pos.x, grid_pos.y):
#                 return False
#             if grid[grid_pos] != 0:
#                 # 房间格子在 grid 中的位置被占用或不合法
#                 return False

#             modified_grid[grid_pos] = t

#     # 房间在 grid 中的位置是合法的
#     grid.copy_(modified_grid)
#     return True

def calc_outerbound_rect(rects:list[Rect]):
    """计算最小能包裹所有rect的大大rect"""
    assert all([rect.x is not None and rect.y is not None for rect in rects])
    
    x_list = [rect.x for rect in rects]
    y_list = [rect.y for rect in rects]
    # w_list = [rect.w for rect in rects]
    # h_list = [rect.h for rect in rects]

    start_x,start_y = min(x_list), min(y_list)
    end_x, end_y = max([rect.x+rect.w for rect in rects]), max([rect.y+rect.h for rect in rects])  #type:ignore

    return Rect(start_x, start_y, end_x-start_x, end_y-start_y)





def try_map_grid_to_(target: array2d[int], if_terrain_in_region: Callable[[int], bool], grid: array2d[int], delta: vec2i) -> bool:
    """尝试将`target`中的格子映射到`grid`中
    
    设`(x, y)`是房间格子在`region_grid`中的位置，那么它被映射到`grid`中的位置是`(x+delta_x, y+delta_y)`

    如果满足条件，不超出`grid`边界且不与已有的非零格子重叠，则返回`True`，否则返回`False`
    """

    # 复制 `grid` 以进行修改
    modified_grid = target.copy()
    
    # 计算 `region_grid` 中房间格子的外接矩形，减少 Python 层面的循环次数
    region_flag_grid = grid.map(lambda x: if_terrain_in_region(x))
    x_, y_, w_, h_ = region_flag_grid.get_bounding_rect(True)

    for region_y in range(y_, y_ + h_):
        for region_x in range(x_, x_ + w_):
            # 跳过不属于房间的格子
            if not if_terrain_in_region(grid[region_x, region_y]):
                continue
            
            # 计算偏移后 `region_grid` 中的房间格子在 `grid` 中的位置
            grid_pos = vec2i(region_x, region_y) + delta
            
            # 检查偏移后的房间格子是否在 `grid` 的有效范围内
            if not target.is_valid(grid_pos.x, grid_pos.y):
                return False
            
            # 检查 `grid` 中的目标位置是否已被非零格子占用
            if target[grid_pos] != 0:
                return False

            # 在 `modified_grid` 中设置该位置
            modified_grid[grid_pos] = grid[region_x, region_y]

    # 所有条件满足，将 `modified_grid` 的更改复制到 `grid` 中
    target.copy_(modified_grid)
    return True


def try_map_anchored_grid_to(target: array2d[int], target_base:vec2i|vec2, if_terrain_in_region: Callable[[int], bool], grid: array2d[int], grid_base: vec2i|vec2):
    """将grid中的房间格子映射到target中, base表示array2d的左上角在全局坐标系中的位置, 因此当两个array2d在全局坐标系中发生重叠才会存在映射。实际上进行了 local -> global -> local 的转换"""
    if isinstance(target_base, vec2):
        target_base = vec2i(int(target_base.x), int(target_base.y))
    if isinstance(grid_base, vec2):
        grid_base = vec2i(int(grid_base.x), int(grid_base.y))
    return try_map_grid_to_(target, if_terrain_in_region, grid, grid_base-target_base)


def add_outline_to_(grid: array2d[int], if_terrain_in_region: Callable[[int], bool], outline_weight: int, outline_value: int):
    """使用outline_vlue为地形增加描边, 描边宽度为 outline_weight"""
    mask = grid.map(if_terrain_in_region)
    
    for _ in range(outline_weight):
        neighbors = mask.count_neighbors(True, "Moore")
        for i in range(mask.width):
            for j in range(mask.height):
                if mask[i, j] == True and neighbors[i, j] > 0:
                    grid[i, j] = outline_value