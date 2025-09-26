from dataclasses import dataclass
from enum import Enum
import random
from array2d import array2d
from tileset_data import TileIndex
from vmath import vec2i
from geography.schema import GeoConfig, DEFAULT_GEO_CONFIG, GeothermalActivityConfig, HumidityConfig, LocalWindConfig, MaterialFluxConfig, NoiseConfig, NoiseType, PlanetaryHumidityConfig, PlanetaryWindConfig, PrimaryForceConfig, RainShadowConfig, SurfaceExpressionsConfig, TemperatureConfig, WorldScaleTag, SolarRadiationConfig

@dataclass
class EnvironmentObjectSeed:
    env_obj_id: TileIndex
    shape: vec2i

@dataclass
class StructureSeed:
    structure_id: TileIndex
    shape: vec2i

@dataclass
class TerrainCell:
    position: vec2i
    ground_tile_id: TileIndex
    env_obj_seed: EnvironmentObjectSeed | None
    structure_seed: StructureSeed | None


class EnvType(Enum):
    WASTELAND = "WASTELAND"
    FOREST = "FOREST"

class TileTag(Enum):
    # 荒漠-地面
    WASTELAND_CHASM = TileIndex(5,0)
    WASTELAND_CLIFF = TileIndex(5,1)
    WASTELAND_GROUND = TileIndex(5,2)
    WASTELAND_FLOWINGSAND = TileIndex(5,3)
    WASTELAND_WATER = TileIndex(5,4)
    
    # 荒漠-灌木
    WASTELAND_HERBS_1 = TileIndex(6,0)
    WASTELAND_HERBS_2 = TileIndex(6,1)
    WASTELAND_CACTUS_1 = TileIndex(6,2)
    WASTELAND_WEEDS_3 = TileIndex(6,3)
    WASTELAND_WEEDS_2 = TileIndex(6,4)
    WASTELAND_WEEDS_1 = TileIndex(6,5)
    
    # debug
    DEBUG_PATH = TileIndex(2, 4)

TILE_NOT_PASSABLE = [TileTag.WASTELAND_CHASM.value, TileTag.WASTELAND_CLIFF.value, TileTag.WASTELAND_WATER.value]


@dataclass
class RoomRequestConfig:
    env_type: EnvType  # 环境类型
    seed: int  # 随机种子
    layout: array2d[int]  # 0表示地面, 1表示墙壁
    exits: list[tuple[vec2i, vec2i]]  # 要求相互联通的出口区域列表, 每一个区域都是长方形, list[tuple[在layout坐标系中的坐标表示出口左下角, 形状]]


def upsample_array(arr, scale_factor):
    """将二维数组超采样扩大
    
    Args:
        arr: 原始数组
        scale_factor: 扩大倍数
        
    Returns:
        扩大后的数组
    """
    new_cols = arr.n_cols * scale_factor
    new_rows = arr.n_rows * scale_factor
    result = array2d(new_cols, new_rows)
    
    for row in range(new_rows):
        for col in range(new_cols):
            # 计算对应的原始数组坐标
            orig_col = col // scale_factor
            orig_row = row // scale_factor
            # 复制原始值到新位置
            result[col, row] = arr[orig_col, orig_row]
    
    return result


_wasteland_layout_small = array2d.fromlist([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
])
# 超采样扩大10倍
_wasteland_layout = upsample_array(_wasteland_layout_small, 10)


WASTELAND_ROOM_REQUEST_CONFIG = RoomRequestConfig(
    env_type=EnvType.WASTELAND,
    seed=random.randint(0, 10000000),
    layout=_wasteland_layout,
    exits=[
        (vec2i(11, 30), vec2i(5, 11)),
        (vec2i(11, 110), vec2i(5, 11)),
        (vec2i(134, 30), vec2i(5, 11)),
    ]
)


WASTELAND_GEO_CONFIG = GeoConfig(
    seed=None,
    world_scale={
        WorldScaleTag.LANDMASS: 100,
        WorldScaleTag.TOPOGRAPHY: 10,
        WorldScaleTag.SURFACE: 1,
    },
    primary_forces=PrimaryForceConfig(
        planetary_wind = PlanetaryWindConfig(
            wind_noise = NoiseConfig(
                NoiseType.PERLIN,
                1,
                (WorldScaleTag.TOPOGRAPHY, WorldScaleTag.LANDMASS),
                0.01
            ),
            wind_speed = WorldScaleTag.LANDMASS,
        ),
        local_wind = LocalWindConfig(
            wind_noise = NoiseConfig(
                NoiseType.PERLIN,
                1,
                (WorldScaleTag.SURFACE, WorldScaleTag.TOPOGRAPHY),
                0.5
            ),
            wind_speed = WorldScaleTag.TOPOGRAPHY,
        ),
        geothermal_activity = GeothermalActivityConfig(
            height_noise = NoiseConfig(
                NoiseType.PERLIN,
                5,
                (WorldScaleTag.TOPOGRAPHY, WorldScaleTag.LANDMASS),
                0.5
            ),
            tectonic_activity_noise = NoiseConfig(
                NoiseType.PERLIN,
                3,
                (WorldScaleTag.SURFACE, WorldScaleTag.LANDMASS),
                0.1
            ),
            tectonic_activity_max = WorldScaleTag.TOPOGRAPHY,
            height_max = 100,
            height_post_process = None,
        ),
        solar_radiation = SolarRadiationConfig(
            solar_radiation_noise = NoiseConfig(
                NoiseType.PERLIN,
                1,
                (WorldScaleTag.SURFACE, WorldScaleTag.LANDMASS),
                0.01
            ),
            solar_radiation_max = 10000,
        ),
        planetary_humidity = PlanetaryHumidityConfig(
            humidity_noise = NoiseConfig(
                NoiseType.PERLIN,
                1,
                (WorldScaleTag.SURFACE, WorldScaleTag.LANDMASS),
                0.01
            ),
            humidity_level_max = 100,
        ),
    ),
    material_flux=MaterialFluxConfig(
            humidity=HumidityConfig(),
            temperature=TemperatureConfig(),
            rain_shadow=RainShadowConfig()
    ),
    surface_expressions=SurfaceExpressionsConfig()
)