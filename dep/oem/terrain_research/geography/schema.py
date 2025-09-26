from dataclasses_dbg import dataclass
from enum import Enum
from typing import Callable
from vmath import vec2, vec2i

from array2d import array2d

class NoiseType(Enum):
    PERLIN = "perlin"
    VORONOI = "voronoi"


class WorldScaleTag(Enum):
    TECTONIC = "TECTONIC"
    CLIMATE = "CLIMATE"
    DRAINAGE = "DRAINAGE"
    LANDMASS = "LANDMASS"
    TOPOGRAPHY = "TOPOGRAPHY"
    SURFACE = "SURFACE"

@dataclass
class NoiseConfig:
    """噪声配置
    noise_type: 噪声类型
    octaves: 多重分形噪声的层数
    scale: 多重分形噪声的尺度范围
    min_amplitude: 最小高度贡献权重
    """
    noise_type: NoiseType
    octaves: int
    scale: tuple[WorldScaleTag, WorldScaleTag] | WorldScaleTag
    min_amplitude: float = 0.1



#######################
# 外部配置
#######################
@dataclass
class GeoConfig:
    seed: int
    # 世界尺度定义（现在是字典）
    world_scale: dict[WorldScaleTag, float]
    # 对应驱动层
    primary_forces: 'PrimaryForceConfig'  
    # 对应中间层
    material_flux: 'MaterialFluxConfig'  
    # 对应生物群系决定层  
    surface_expressions: 'SurfaceExpressionsConfig'
    

    
    @staticmethod
    def get_scale(world_scale: dict[WorldScaleTag, float], tags: tuple[WorldScaleTag, ...]|WorldScaleTag) -> float|tuple[float, ...]:
        assert isinstance(world_scale, dict)
        assert isinstance(tags, WorldScaleTag) or isinstance(tags, tuple)
        if isinstance(tags, tuple):
            assert all([isinstance(tag, WorldScaleTag) for tag in tags])
            
        if isinstance(tags, WorldScaleTag):
            return world_scale[tags]
        else:
            result = []
            for tag in tags:
                if not isinstance(tag, WorldScaleTag):
                    raise TypeError()
                result.append(world_scale[tag])
            return result
    #
    #
    #
    #
    #
@dataclass
class PrimaryForceConfig:
    # 风场图
    planetary_wind: 'PlanetaryWindConfig'
    local_wind: 'LocalWindConfig'
    # 地壳运动（含地震带/地形生成）
    geothermal_activity: 'GeothermalActivityConfig'  
    # 太阳辐射标量场
    solar_radiation: 'SolarRadiationConfig'  
    # 水汽场
    planetary_humidity: 'PlanetaryHumidityConfig'
        #
        #
        #
        #
        #
@dataclass
class PlanetaryWindConfig:
    """行星风场配置
    wind_noise: 风场噪声配置
    wind_speed: 风速最大值
    """
    wind_noise: NoiseConfig = NoiseConfig(
        noise_type=NoiseType.PERLIN,
        octaves=6,
        scale=(WorldScaleTag.TOPOGRAPHY, WorldScaleTag.CLIMATE),
        min_amplitude=0.1
    )
    wind_speed: WorldScaleTag = WorldScaleTag.CLIMATE
            #
            #
            #
@dataclass
class LocalWindConfig:
    """局部风场配置(还需负责搬运水汽)
    wind_noise: 风场噪声配置
    wind_speed: 风速最大值
    """
    wind_noise: NoiseConfig = NoiseConfig(
        noise_type=NoiseType.PERLIN,
        octaves=6,
        scale=(WorldScaleTag.SURFACE, WorldScaleTag.TOPOGRAPHY),
        min_amplitude=0.1
    )
    wind_speed: WorldScaleTag = WorldScaleTag.SURFACE
            #
            #
            #
@dataclass 
class PlanetaryHumidityConfig:
    """行星级湿度配置
    humidity_noise: 湿度噪声配置
    humidity_level_max: 最大湿度(0~100%)
    """
    humidity_noise: NoiseConfig = NoiseConfig(
        noise_type=NoiseType.PERLIN,
        octaves=6,
        scale=(WorldScaleTag.TOPOGRAPHY, WorldScaleTag.CLIMATE),
        min_amplitude=0.1
    )
    humidity_level_max: float = 100.0
            #
            #
            #
@dataclass
class GeothermalActivityConfig:
    """地形生成配置
    height_noise: 基础地形噪声配置
    height_max: 高度/深度最大值(m)
    tectonic_activity_noise: 地壳运动噪声配置(域扭曲)
    tectonic_activity_max: 扭曲矢量的最大模长
    gaussian_delta: 高斯模糊采样距离(m)
    height_post_process: 高度后处理函数(Callable[[vec2i, float], float])
    """
    height_noise: NoiseConfig = NoiseConfig(
        noise_type=NoiseType.PERLIN,
        octaves=3,
        scale=(WorldScaleTag.SURFACE, WorldScaleTag.LANDMASS),
        min_amplitude=0.01
    )
    tectonic_activity_noise: NoiseConfig = NoiseConfig(
        noise_type=NoiseType.PERLIN,
        octaves=3,
        scale=(WorldScaleTag.SURFACE, WorldScaleTag.LANDMASS),
        min_amplitude=0.01
    )
    tectonic_activity_max: WorldScaleTag = WorldScaleTag.TOPOGRAPHY
    height_max: float = 100
    gaussian_delta: float = 1.0
    height_post_process: list[Callable[[vec2i, vec2i, float], float]] = [lambda world_pos, local_pos, height: height]
            #
            #
            #
@dataclass
class SolarRadiationConfig:
    """太阳辐射配置
    solar_radiation_noise: 太阳辐射噪声配置
    solar_radiation_max: 太阳辐射最大值
    """
    solar_radiation_noise: NoiseConfig = NoiseConfig(
        noise_type=NoiseType.PERLIN,
        octaves=6,
        scale=(WorldScaleTag.CLIMATE, WorldScaleTag.TECTONIC),
        min_amplitude=0.1
    )
    solar_radiation_max: float = 1000
            #
            #
            #
    #
    #
    #
@dataclass
class MaterialFluxConfig:
    # 水汽分布相关
    humidity: 'HumidityConfig'  
    # 温度相关
    temperature: 'TemperatureConfig'  
    # 雨影效应
    rain_shadow: 'RainShadowConfig'  
        #
        #
        #
        #
        #
@dataclass
class HumidityConfig:
    # ----高斯核配置, 用于计算基础含水量
    gaussian_size: int = 5  # 高斯核边长(实际边长=gaussian_size*sample_scale)
    gaussian_sigma_ratio: float = 1.0/3  # 高斯核标准差与边长比
    sample_scale: WorldScaleTag = WorldScaleTag.CLIMATE  # 采样尺度
    
            #
            #
            #
@dataclass
class TemperatureConfig:
    pass
            #
            #
            #
@dataclass
class RainShadowConfig:
    pass
            #
            #
            #
    #
    #
    #
@dataclass
class SurfaceExpressionsConfig:
    pass
        #
        #
        #
        #

@dataclass
class BiomeConfig:
    humidity_variance: float = 0.3    # 湿度高斯模糊强度
    diurnal_temp_range: float = 0.15  # 昼夜温差系数
            #
            #
            #
@dataclass
class TerrainConfig:
    slope_effect: float = 1.5      # 坡度对侵蚀的放大系数
    aspect_modifier: float = 0.8   # 朝向修正系数


# -------------默认配置
default_world_scale: dict[WorldScaleTag, float] = {
    WorldScaleTag.TECTONIC: 1000000,   # 构造级
    WorldScaleTag.CLIMATE: 100000,     # 气候级
    WorldScaleTag.DRAINAGE: 10000,     # 流域级
    WorldScaleTag.LANDMASS: 100,      # 地形级
    WorldScaleTag.TOPOGRAPHY: 10,      # 地貌级
    WorldScaleTag.SURFACE: 1            # 地表级
}


DEFAULT_GEO_CONFIG = GeoConfig(
    seed=123456,
    world_scale=default_world_scale.copy(),
    primary_forces=PrimaryForceConfig(
        planetary_wind=PlanetaryWindConfig(),
        local_wind=LocalWindConfig(),
        geothermal_activity=GeothermalActivityConfig(),
        solar_radiation=SolarRadiationConfig(),
        planetary_humidity=PlanetaryHumidityConfig()
    ),
    material_flux=MaterialFluxConfig(
        humidity=HumidityConfig(),
        temperature=TemperatureConfig(),
        rain_shadow=RainShadowConfig()
    ),
    surface_expressions=SurfaceExpressionsConfig()
)


#######################
# 返回值
#######################
@dataclass
class GeoCell:
    position: vec2i  # 坐标
    altitude: float  # 海拔(m)
    solar_radiation: float  # 太阳辐射(MJ/m^2/year)
    temperature: float  # 温度(℃)
    humidity: float  # 湿度(%)
    wind_speed: float  # 风速(m/s)
    wind_direction: float  # 风向(°)正北方向吹来的风为0°
    precipitation: float  # 降水量(mm)
    slope: float  # 坡度(°)
    aspect: float  # 朝向(°)山脚指向山顶的方向
    
