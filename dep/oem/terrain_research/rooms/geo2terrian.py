from random import Random
from array2d import array2d
from geography.schema import GeoCell
from .tools.probability import sigmoid_probability
from ..geography.tools.debug import show_height_map
from .nosie import wasteland_rift_noise
from tileset_data import DEFAULT_TILE_GALLERY, Tile
from vmath import vec2i
from .schema import EnvType, EnvironmentObjectSeed, TileTag, TerrainCell







def geo_area_to_terrain(geo_area:array2d[GeoCell], seed: int, env_type: EnvType) -> array2d[TerrainCell]:
    origin = geo_area[0, 0].position
    if env_type == EnvType.WASTELAND:
        return geo_area_to_terrain_in_wasteland(geo_area, seed)
    elif env_type == EnvType.FOREST:
        return geo_area_to_terrain_in_forest(geo_area, seed)
    else:
        raise ValueError(f"Invalid env type: {env_type}")



def geo_area_to_terrain_in_wasteland(geo_area:array2d[GeoCell], seed: int) -> array2d[TerrainCell]:
    origin = geo_area[0, 0].position
    result: array2d[TerrainCell] = array2d(geo_area.n_cols, geo_area.n_rows)
    random = Random(seed)
    # ======地面, 环境物体(点映射)=======
    for i in range(geo_area.n_cols):
        for j in range(geo_area.n_rows):
            geo_cell = geo_area[i, j]

            ground_tile_id = None
            env_obj_seed = None
            structure_seed = None
            
            # =====地面====
            if geo_cell.humidity < 40:  # 流沙区域
                ground_tile_id = TileTag.WASTELAND_FLOWINGSAND.value
            else:  # 普通地面
                ground_tile_id = TileTag.WASTELAND_GROUND.value
            
            # =====灌木====
            if geo_cell.slope < 45:
                # 仙人掌：在高湿度高辐射区域
                if sigmoid_probability(
                    [geo_cell.humidity, geo_cell.solar_radiation], 
                    [50, 2000],  # 参考值：湿度50，辐射2000
                    0.01,         # 参考概率
                    random_generator=random,
                    slope=[0.1, 0.0005]
                ):
                    env_obj_seed = EnvironmentObjectSeed(TileTag.WASTELAND_CACTUS_1.value, vec2i(1, 1))
                # 草药：在中等湿度和中等辐射区域
                elif sigmoid_probability(
                    [geo_cell.humidity, geo_cell.solar_radiation], 
                    [40, 3500],  # 参考值：湿度40，辐射3500
                    0.02,         # 参考概率
                    random_generator=random,
                    max_probability=0.3,
                    slope=[0.1, -0.0005]  # 湿度正相关，辐射负相关
                ):
                    env_obj_seed = EnvironmentObjectSeed(TileTag.WASTELAND_HERBS_1.value, vec2i(1, 1))
                # 杂草：在低湿度低辐射区域
                elif sigmoid_probability(
                    [geo_cell.humidity, geo_cell.solar_radiation], 
                    [30, 5000],  # 参考值：湿度30，辐射5000
                    0.1,         # 参考概率
                    random_generator=random,
                    max_probability=0.3,
                    slope=[0.3, -0.0005]  # 湿度正相关，辐射负相关
                ):
                    if random.random() < 0.5:
                        env_obj_seed = EnvironmentObjectSeed(TileTag.WASTELAND_WEEDS_1.value, vec2i(1, 1))
                    elif random.random() < 0.5:
                        env_obj_seed = EnvironmentObjectSeed(TileTag.WASTELAND_WEEDS_2.value, vec2i(1, 1))
                    else:
                        env_obj_seed = EnvironmentObjectSeed(TileTag.WASTELAND_WEEDS_3.value, vec2i(1, 1))
                
            # =====悬崖====
            else :  # 陡峭的悬崖
                ground_tile_id = TileTag.WASTELAND_CLIFF.value
            # =====水体====
            if geo_cell.altitude < -5:  # 水体
                ground_tile_id = TileTag.WASTELAND_WATER.value
            
            result[i, j] = TerrainCell(
                position=vec2i(i, j) + origin,
                ground_tile_id=ground_tile_id,
                env_obj_seed=env_obj_seed,
                structure_seed=structure_seed
            )
    # show_height_map(geo_area.map(lambda x: x.solar_radiation), 1)
    # show_height_map(geo_area.map(lambda x: x.humidity), 1)
    # show_height_map(result.map(lambda x: 0 if x.env_obj_seed is None else x.env_obj_seed.env_obj_id.x + x.env_obj_seed.env_obj_id.y), 1)
    # ======裂谷(区域请求)=======
    rift = wasteland_rift_noise(origin, geo_area.n_cols, geo_area.n_rows, random.randint(0, 1000000))
    is_rift = rift.map(lambda x: 1 if x > 1 else 0)
    for i in range(geo_area.n_cols):
        for j in range(geo_area.n_rows):
            if is_rift[i, j] == 1:
                result[i, j].ground_tile_id = TileTag.WASTELAND_CHASM.value
    return result
    




def geo_area_to_terrain_in_forest(geo_area:array2d[GeoCell], seed: int) -> array2d[TerrainCell]:
    pass