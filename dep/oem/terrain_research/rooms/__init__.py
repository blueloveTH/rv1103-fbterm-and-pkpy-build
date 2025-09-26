from array2d import array2d
from ..dev_tools.progress_tracker import step
from geography import request_area
from geography.schema import GeoConfig, DEFAULT_GEO_CONFIG, GeothermalActivityConfig, LocalWindConfig, NoiseConfig, NoiseType, PlanetaryWindConfig, PrimaryForceConfig, WorldScaleTag
from vmath import vec2i

from ..geography.tools.debug import show_height_map

from .geo2terrian import geo_area_to_terrain
from ..tileset_data import Tile
from .schema import TILE_NOT_PASSABLE, WASTELAND_GEO_CONFIG, WASTELAND_ROOM_REQUEST_CONFIG, EnvType, RoomRequestConfig, TerrainCell, TileTag
from random import Random
from .tools.astar import base_astar_in_grid


MAX_TRY_COUNT = 1000




def generate_room(room_config: RoomRequestConfig) -> array2d[TerrainCell]:
    try_count = 0
    random = Random(room_config.seed)
    while try_count < MAX_TRY_COUNT:
        origin = vec2i(random.randint(0, 10000000), random.randint(0, 10000000))
        width, height = room_config.layout.n_cols, room_config.layout.n_rows
        
        # ====生成初始地理信息====
        if room_config.env_type == EnvType.WASTELAND:
            geo_config = WASTELAND_GEO_CONFIG
        else:
            raise ValueError(f"Invalid env type: {room_config.env_type}")
        
        geo_config.seed = room_config.seed
        geo_config.primary_forces.geothermal_activity.height_post_process = [lambda world_pos, local_pos, height: height + 50 if room_config.layout.is_valid((world_pos-origin).x, (world_pos-origin).y) and room_config.layout[world_pos-origin] == 1 else height]  # 墙壁区域高度+50
        geo_area = request_area(origin, width, height, geo_config)
        # ====生成TerrainCell====
        step("生成TerrainCell")
        terrain_area = geo_area_to_terrain(geo_area, room_config.seed, room_config.env_type)
        
        # ====检查连通性====
        # 计算每一个出口的中心, 然后使用astar生成路径, 确保每一个出口组合都可以联通, 最后将路径位置的ground替换成debug颜色
        # 生成出口组合
        step("检查连通性")
        exit_combinations:list[tuple[vec2i, vec2i]] = []
        for i in range(len(room_config.exits)):
            for j in range(i+1, len(room_config.exits)):
                exit_combinations.append((room_config.exits[i], room_config.exits[j]))
        
        # 检查每一个出口组合是否可以联通
        try:
            path_list = []
            for exit_combination in exit_combinations:
                exit_1, exit_2 = exit_combination
                exit_1_center = exit_1[0] + exit_1[1] // 2
                exit_2_center = exit_2[0] + exit_2[1] // 2
                # 将出口区域标记为可通行区域
                def is_passable(cell):
                    # 如果位置在出口区域内, 则视为可通行
                    for exit_pos, exit_shape in [exit_1, exit_2]:
                        local_pos = cell.position - origin
                        if (local_pos.x >= exit_pos.x and local_pos.x < exit_pos.x + exit_shape.x and \
                            local_pos.y >= exit_pos.y and local_pos.y < exit_pos.y + exit_shape.y):
                            return False
                    # 否则检查是否是障碍物
                    return cell.ground_tile_id in TILE_NOT_PASSABLE
                path = base_astar_in_grid(terrain_area.map(is_passable), exit_1_center, exit_2_center)
                if path is None:
                    raise ValueError(f"出口{exit_combination}无法联通")
                
                for pos in path:
                    if pos not in path_list:
                        path_list.append(pos)
        except ValueError as e:
            print(e)
            try_count += 1
            continue
        
        for pos in path_list:
            terrain_area[pos].ground_tile_id = TileTag.DEBUG_PATH.value
            # 还需要标记出口区域
            for exit_pos, exit_shape in room_config.exits:
                for _, pos in array2d(exit_shape.x, exit_shape.y, lambda pos: exit_pos + pos):
                    terrain_area[pos].ground_tile_id = TileTag.DEBUG_PATH.value
        
        
        
        return terrain_area
        
        
        
    raise ValueError("Failed to generate room, retry too many times")