import math
from typing import Callable, List, Union, Tuple
import random as random_module

from vmath import color32, vec2, vec2i

from array2d import array2d

from tileset_data import *
from rooms.schema import *



def sample_grid(
    area_origin: vec2i,
    area_shape: vec2i,
    dx_dy: vec2i,
    align_point: vec2i|None
) -> array2d[vec2i]:
    """生成基于对齐点的采样坐标网格
    
    Args:
        area_origin: 区域左下角坐标 (x, y)
        area_shape: 区域尺寸 (width, height)
        dx_dy: 采样间距 (dx, dy)
        align_point: 对齐点坐标(如果采样网格无限延申, 则align_point一定会成为采样点)
    
    Returns:
        二维数组存储采样点坐标，数组形状自动计算
    """
    align_point = align_point or vec2i(0,0)
    # 参数校验
    if dx_dy.x <= 0 or dx_dy.y <= 0:
        raise ValueError("Sampling intervals must be positive")
    if area_shape.x <= 0 or area_shape.y <= 0:
        return array2d(0, 0)  # 空区域返回空数组

    # 计算有效采样范围
    area_end = area_origin + area_shape
    grid_min = ((area_origin - align_point) + dx_dy - 1) // dx_dy  # 向上取整
    grid_max = (area_end - align_point - 1) // dx_dy              # 向下取整

    # 采样网格的coordinates
    kx = range(grid_min.x, grid_max.x + 1)
    ky = range(grid_min.y, grid_max.y + 1)
    
    
    # 创建采样网格
    return array2d(len(kx), len(ky)).map(
        lambda pos: align_point + dx_dy * vec2i(kx[pos[0]], ky[pos[1]])
    )

##################################
# Debug
##################################





_structure_seed_map: list[list[int | None, str]] = [
    [None, '🔴'],
    [None, '🟡'],
    [None, '🟢'],
    [None, '🔵'],
    [None, '🟣'],
    [None, '🟤']
][::-1]


def structure_seed_to_str(structure_seed: StructureSeed) -> str:
    # 检查是否已存在映射
    for entry in _structure_seed_map:
        if entry[0] == structure_seed.structure_id:
            return entry[1]
    
    # 寻找空槽位
    for entry in _structure_seed_map:
        if entry[0] is None:
            entry[0] = structure_seed.structure_id
            return entry[1]
    
    # 映射已满
    return color32.from_vec3i("#e60012").ansi_bg("Ｆ")

def show_terrain(array: array2d[TerrainCell], show_grid: bool):
    width = array.width
    height = array.height
    
    # 创建三个层：地形层、结构层、环境物件层
    terrain_layer = array2d(width, height, lambda _: " ")
    structure_layer = array2d(width, height, lambda _: None)
    env_layer = array2d(width, height, lambda _: None)
    env_fg_colors = array2d(width, height, lambda _: None)  # 新增：存储环境物体的前景色
    
    # 预处理各层数据
    for y in range(height):
        for x in range(width):
            cell = array[x, y]
            
            # 地形层
            tile_str_with_bg, bg = str(DEFAULT_TILE_GALLERY[cell.ground_tile_id]), DEFAULT_TILE_GALLERY[cell.ground_tile_id].bg
            terrain_layer[x, y] = (tile_str_with_bg, bg or color32(0, 0, 0, 0).to_hex())
            
            # 结构层
            if cell.structure_seed is not None:
                symbol = structure_seed_to_str(cell.structure_seed)
                shape = cell.structure_seed.shape
                for dx in range(shape.x):
                    for dy in range(shape.y):
                        px = x + dx
                        py = y - dy  # 从当前位置向上扩展
                        if 0 <= px < width and 0 <= py < height:
                            structure_layer[px, py] = symbol
            
            # 环境物件层
            if cell.env_obj_seed is not None:
                # 修复：正确获取环境物体的字符
                env_obj_id = cell.env_obj_seed.env_obj_id
                # 确保使用正确的索引方式获取tile
                tile = DEFAULT_TILE_GALLERY[env_obj_id]
                symbol = tile.char
                fg_color = tile.fg  # 获取前景色
                shape = cell.env_obj_seed.shape
                for dx in range(shape.x):
                    for dy in range(shape.y):
                        px = x + dx
                        py = y - dy  # 从当前位置向上扩展
                        if 0 <= px < width and 0 <= py < height:
                            env_layer[px, py] = symbol
                            env_fg_colors[px, py] = fg_color  # 存储前景色

    # 打印顶部边框
    print('-' * (width * 2 + 2))
    
    for y in range(height):
        for x in range(width):
            if x == 0:
                print('|', end='')
            
            tile_str_with_bg, bg = terrain_layer[x, y]
            
            # 处理网格线
            if show_grid:
                if (x > 0 and x % 22 == 0) or (y > 0 and y % 14 == 0):
                    tile_str_with_bg = color32.from_hex(bg).ansi_bg("➕")
            # 应用覆盖区域（结构优先于环境物件）
            if structure_layer[x, y] is not None:
                tile_str_with_bg = color32.from_hex(bg).ansi_bg(structure_layer[x, y])
            elif env_layer[x, y] is not None:
                # 确保环境物体字符正确显示，并应用前景色
                char = env_layer[x, y]
                fg_color = env_fg_colors[x, y]
                
                # 先应用背景色
                colored_char = color32.from_hex(bg).ansi_bg(char)
                
                # 如果有前景色，再应用前景色
                if fg_color is not None:
                    colored_char = color32.from_hex(fg_color).ansi_fg(colored_char)
                
                tile_str_with_bg = colored_char
            else:
                # 普通区域也需要应用背景色
                tile_str_with_bg = color32.from_hex(bg).ansi_bg(tile_str_with_bg)
            
            print(tile_str_with_bg, end='')
        print('|')
    
    # 打印底部边框
    print('-' * (width * 2 + 2))
    print("Structure Map:", _structure_seed_map)
