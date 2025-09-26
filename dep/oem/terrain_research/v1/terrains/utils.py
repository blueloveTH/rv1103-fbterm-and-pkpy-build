import math
from typing import Callable

from vmath import color32, vec2, vec2i

from array2d import array2d
from schema.base import AsciiSprite, EnvironmentObjectSeed, StructureSeed, TileIndex, TilesetId, get_sprite, tile_to_str
from schema.terrian import TerrianCell




#################################
#  Math
#################################

def sigmoid(x: float, a:float, b:float) -> float:
    return 1 / (1 + math.exp(-(a*x-b)))

def gradient_point(pos: vec2, noise_func: Callable[[vec2], float], d: float = 0.5) -> vec2:
    x, y = pos
    k = 1/(2 * d)
    k_diag = 1/(2 * d * math.sqrt(2))
    
    n_right = noise_func(vec2(x + d, y))
    n_left = noise_func(vec2(x - d, y))
    n_top = noise_func(vec2(x, y + d))
    n_bottom = noise_func(vec2(x, y - d))
    
    dx = (n_right - n_left) * k * 0.5
    dy = (n_top - n_bottom) * k * 0.5
    
    n_tr = noise_func(vec2(x + d, y + d))
    n_tl = noise_func(vec2(x - d, y + d))
    n_br = noise_func(vec2(x + d, y - d))
    n_bl = noise_func(vec2(x - d, y - d))
    
    dx += (n_tr - n_tl + n_br - n_bl) * k_diag * 0.5
    dy += (n_tr - n_br + n_tl - n_bl) * k_diag * 0.5
    
    return vec2(dx, dy)

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

def get_dir_tile(dir:vec2) -> TileIndex:
    # Calculate angle in [-π, π]
    angle = math.atan2(dir.y, dir.x)
    
    # Normalize to [0, 2π)
    if angle < 0:
        angle += 2 * math.pi
    
    # Define 8 directions (π/4 radians per sector)
    sector = int(round(angle / (math.pi / 4))) % 8
    
    # Map sector to arrow emoji
    arrows = [TileIndex(TilesetId.Direction, 2), # r
              TileIndex(TilesetId.Direction, 1), # ur
              TileIndex(TilesetId.Direction, 0), # u
              TileIndex(TilesetId.Direction, 7), # ul
              TileIndex(TilesetId.Direction, 6), # l
              TileIndex(TilesetId.Direction, 5), # dl
              TileIndex(TilesetId.Direction, 4), # d
              TileIndex(TilesetId.Direction, 3)  # dr
              ]
    return arrows[sector]

def get_contour_tile(height: float, height_range: tuple[float, float]) -> TileIndex:
    """
    根据高度值和范围获取等高线TileIndex
    
    参数:
        height: 当前高度值
        height_range: (min_height, max_height) 高度范围
        
    返回:
        TileIndex 对应等高线的瓦片索引
    """
    min_height, max_height = height_range
    
    # 计算高度在范围内的归一化值 [0, 1]
    normalized = (height - min_height) / (max_height - min_height)
    
    # 将归一化值映射到等高线瓦片索引 (假设有8个等高线等级)
    contour_levels = 8
    level = int(normalized * contour_levels)
    
    # 确保level在有效范围内
    level = max(0, min(contour_levels - 1, level))
    
    # 返回对应等高线的TileIndex (假设等高线瓦片在TilesetId.Height中连续排列)
    return TileIndex(TilesetId.Height, level)

_env_obj_seed_map: list[list[int | None, str]] = [
    [None, '🟥'],
    [None, '🟨'],
    [None, '🟩'],
    [None, '🟦'],
    [None, '🟪'],
    [None, '🟫']
]

_structure_seed_map: list[list[int | None, str]] = [
    [None, '🔴'],
    [None, '🟡'],
    [None, '🟢'],
    [None, '🔵'],
    [None, '🟣'],
    [None, '🟤']
][::-1]

def env_obj_seed_to_str(env_obj_seed: EnvironmentObjectSeed) -> str:
    # 检查是否已存在映射
    for entry in _env_obj_seed_map:
        if entry[0] == env_obj_seed.env_obj_id:
            return entry[1]
    
    # 寻找空槽位
    for entry in _env_obj_seed_map:
        if entry[0] is None:
            entry[0] = env_obj_seed.env_obj_id
            return entry[1]
    
    # 映射已满
    return color32.from_vec3i("#e60012").ansi_bg("Ｆ")

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
    
    # 预处理各层数据
    for y in range(height):
        for x in range(width):
            cell = array[x, y]
            
            # 地形层
            tile_str, bg = tile_to_str(get_sprite(cell.tile_id.x, cell.tile_id.y))
            terrain_layer[x, y] = (tile_str, bg or color32(0, 0, 0, 0).to_vec3i())
            
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
                symbol = env_obj_seed_to_str(cell.env_obj_seed)
                shape = cell.env_obj_seed.shape
                for dx in range(shape.x):
                    for dy in range(shape.y):
                        px = x + dx
                        py = y - dy  # 从当前位置向上扩展
                        if 0 <= px < width and 0 <= py < height:
                            env_layer[px, py] = symbol

    # 打印顶部边框
    print('-' * (width * 2 + 2))
    
    for y in range(height):
        for x in range(width):
            if x == 0:
                print('|', end='')
            
            tile_str, bg = terrain_layer[x, y]
            
            # 处理网格线
            if show_grid:
                if (x > 0 and x % 22 == 0) or (y > 0 and y % 14 == 0):
                    tile_str = color32.from_vec3i(bg).ansi_bg("➕")
            
            # 应用覆盖区域（结构优先于环境物件）
            if structure_layer[x, y] is not None:
                tile_str = color32.from_vec3i(bg).ansi_bg(structure_layer[x, y])
            elif env_layer[x, y] is not None:
                tile_str = color32.from_vec3i(bg).ansi_bg(env_layer[x, y])
            
            print(tile_str, end='')
        print('|')
    
    # 打印底部边框
    print('-' * (width * 2 + 2))
    print("Structure Map:", _structure_seed_map)
    print("Environment Map:", _env_obj_seed_map)