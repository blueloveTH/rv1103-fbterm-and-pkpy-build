import math
from array2d import array2d
from vmath import vec2, vec2i
from geography.tools.field_processing import compute_gaussian_blur, compute_gradient, gradient_3x3
from .tools.math import float_mod
from noises.basics.perlin import Perlin
from noises.basics.voronoi import Voronoi

from geography.schema import DEFAULT_GEO_CONFIG, GeoCell, GeoConfig
from geography.tools.debug import show_height_map, show_vector_field
from geography.tools.noise import make_noise_func

from dev_tools.progress_tracker import *

# -----驱动层

# 大尺度风场
def calc_planetary_wind(origin:vec2i, width:int, height:int, config:GeoConfig) -> array2d[vec2]:
    noise_func_x = make_noise_func(
        config.seed-10,
        config.primary_forces.planetary_wind.wind_noise.noise_type,
        config.primary_forces.planetary_wind.wind_noise.octaves,
        GeoConfig.get_scale(config.world_scale, config.primary_forces.planetary_wind.wind_noise.scale),
        config.primary_forces.planetary_wind.wind_noise.min_amplitude
    )
    noise_func_y = make_noise_func(
        config.seed+10,
        config.primary_forces.planetary_wind.wind_noise.noise_type,
        config.primary_forces.planetary_wind.wind_noise.octaves,
        GeoConfig.get_scale(config.world_scale, config.primary_forces.planetary_wind.wind_noise.scale),
        config.primary_forces.planetary_wind.wind_noise.min_amplitude
    )
    return array2d(
        width, height,
        lambda pos: vec2(
            noise_func_x(pos + origin),
            noise_func_y(pos + origin)
        )
    ) * GeoConfig.get_scale(config.world_scale, config.primary_forces.planetary_wind.wind_speed)

# 小尺度风场
def calc_local_wind(origin:vec2i, width:int, height:int, config:GeoConfig) -> array2d[vec2]:
    noise_func_x = make_noise_func(
        config.seed+20,
        config.primary_forces.local_wind.wind_noise.noise_type,
        config.primary_forces.local_wind.wind_noise.octaves,
        GeoConfig.get_scale(config.world_scale, config.primary_forces.local_wind.wind_noise.scale),
        config.primary_forces.local_wind.wind_noise.min_amplitude
    )
    noise_func_y = make_noise_func(
        config.seed-20,
        config.primary_forces.local_wind.wind_noise.noise_type,
        config.primary_forces.local_wind.wind_noise.octaves,
        GeoConfig.get_scale(config.world_scale, config.primary_forces.local_wind.wind_noise.scale),
        config.primary_forces.local_wind.wind_noise.min_amplitude
    )
    return array2d(
        width, height,
        lambda pos: vec2(noise_func_x(pos + origin), noise_func_y(pos + origin))
    ) * GeoConfig.get_scale(config.world_scale, config.primary_forces.local_wind.wind_speed)

# 大尺度基础水汽场
def calc_planetary_humidity(origin:vec2i, width:int, height:int, config:GeoConfig) -> array2d[float]:
    noise_func = make_noise_func(
        config.seed+30,
        config.primary_forces.planetary_humidity.humidity_noise.noise_type,
        config.primary_forces.planetary_humidity.humidity_noise.octaves,
        GeoConfig.get_scale(config.world_scale, config.primary_forces.planetary_humidity.humidity_noise.scale),
        config.primary_forces.planetary_humidity.humidity_noise.min_amplitude
    )
    return array2d(width, height,
        lambda pos: noise_func(pos + origin)
    ).map(lambda x: (x+0.5) * config.primary_forces.planetary_humidity.humidity_level_max)

# 太阳辐射
def calc_solar_radiation(origin:vec2i, width:int, height:int, config:GeoConfig) -> array2d[float]:
    noise_func = make_noise_func(
        config.seed+40,
        config.primary_forces.solar_radiation.solar_radiation_noise.noise_type,
        config.primary_forces.solar_radiation.solar_radiation_noise.octaves,
        GeoConfig.get_scale(config.world_scale, config.primary_forces.solar_radiation.solar_radiation_noise.scale),
        config.primary_forces.solar_radiation.solar_radiation_noise.min_amplitude
    )
    return array2d(width, height,
        lambda pos: noise_func(pos + origin)
    ).map(lambda x: (x+0.5) * config.primary_forces.solar_radiation.solar_radiation_max)


# 地质运动
def calc_geothermal_activity(origin:vec2i, width:int, height:int, config:GeoConfig) -> array2d[float]:
    height_noise_func = make_noise_func(
        config.seed+50,
        config.primary_forces.geothermal_activity.height_noise.noise_type,
        config.primary_forces.geothermal_activity.height_noise.octaves,
        GeoConfig.get_scale(config.world_scale, config.primary_forces.geothermal_activity.height_noise.scale),
        config.primary_forces.geothermal_activity.height_noise.min_amplitude
    )
    tectonic_activity_noise_func_x = make_noise_func(
        config.seed+55,
        config.primary_forces.geothermal_activity.tectonic_activity_noise.noise_type,
        config.primary_forces.geothermal_activity.tectonic_activity_noise.octaves,
        GeoConfig.get_scale(config.world_scale, config.primary_forces.geothermal_activity.tectonic_activity_noise.scale),
        config.primary_forces.geothermal_activity.tectonic_activity_noise.min_amplitude
    )
    tectonic_activity_noise_func_y = make_noise_func(
        config.seed-55,
        config.primary_forces.geothermal_activity.tectonic_activity_noise.noise_type,
        config.primary_forces.geothermal_activity.tectonic_activity_noise.octaves,
        GeoConfig.get_scale(config.world_scale, config.primary_forces.geothermal_activity.tectonic_activity_noise.scale),
        config.primary_forces.geothermal_activity.tectonic_activity_noise.min_amplitude
    )
    
    result = array2d(width, height,
        lambda pos: height_noise_func(
            # 先计算全局坐标，再施加扭曲
            (vec2(pos) + vec2(origin)) + \
            vec2(
                tectonic_activity_noise_func_x(vec2(pos) + vec2(origin)),
                tectonic_activity_noise_func_y(vec2(pos) + vec2(origin))
            ) * GeoConfig.get_scale(config.world_scale, config.primary_forces.geothermal_activity.tectonic_activity_max)
        ) * config.primary_forces.geothermal_activity.height_max
    )
    
    for func in config.primary_forces.geothermal_activity.height_post_process:
        mapper = lambda local_pos: func(local_pos + origin, local_pos, result[local_pos])
        result = array2d(width, height, mapper)
    
    return result
    

# -----中间层
# 雨影效应
def calc_rain_shadow(planetary_wind:array2d[vec2], padded_geothermal_activity:array2d[float], geo_config: GeoConfig) -> array2d[float]:
    assert planetary_wind.shape - padded_geothermal_activity.shape == vec2i(1,1)
    pass
# 平均温度
def calc_temperature(solar_radiation:array2d[float], geothermal_activity:array2d[float], geo_config: GeoConfig) -> array2d[float]:
    assert solar_radiation.shape == geothermal_activity.shape
    pass
# 基础含水量
def calc_basic_humidity(padded_geothermal_activity:array2d[float], request_shape:vec2i, geo_config: GeoConfig) -> array2d[float]:
    assert request_shape + 2*vec2i(geo_config.material_flux.humidity.gaussian_size//2, geo_config.material_flux.humidity.gaussian_size//2) == padded_geothermal_activity.shape
    pass

# 静态水汽分布图
def calc_static_humidity(basic_humidity:array2d[float], temperature:array2d[float], solar_radiation:array2d[float]) -> array2d[float]:
    pass

# 水汽分布图
def calc_humidity(static_humidity:array2d[float], planetary_wind:array2d[vec2], geo_config: GeoConfig) -> array2d[float]:
    pass



OFFSET = 20
# 请求入口
def request_area(origin:vec2i, width:int, height:int, geo_config:GeoConfig|None=None) -> array2d[GeoCell]:
    """
    请求一个区域的地理信息
    """

    geo_config = geo_config if geo_config else DEFAULT_GEO_CONFIG
    
    # 计算总共需要的padding
    padding_d = sum(
        [
            geo_config.world_scale[geo_config.primary_forces.local_wind.wind_speed], # 风场padding
            1  # 地形梯度计算需要额外padding
        ]
    )
    padding = vec2i(padding_d, padding_d)
    # 根据padding修正origin
    origin_padded = origin - padding
    padded_width = width + 2*padding.x
    padded_height = height + 2*padding.y
    
    # ====驱动层====
    step("计算行星风场")
    planetary_wind_layer = calc_planetary_wind(origin_padded, padded_width, padded_height, geo_config)
    step("计算局部风场")
    local_wind_layer = calc_local_wind(origin_padded, padded_width, padded_height, geo_config)
    step("计算行星湿度场")
    planetary_humidity_layer = calc_planetary_humidity(origin, width, height, geo_config)
    step("计算太阳辐射场")
    solar_radiation_layer = calc_solar_radiation(origin, width, height, geo_config)
    step("计算地质活动场")
    geothermal_activity_layer = calc_geothermal_activity(origin_padded, padded_width, padded_height, geo_config)
    # ====中间层====
    
    # ====计算GeoCell====
    result = array2d(width, height, None)
    
    step("计算坡度")
    slope_origin = origin_padded + vec2i(1, 1)
    slope_layer = gradient_3x3(geothermal_activity_layer)
    
    wind_layer = planetary_wind_layer + local_wind_layer
    
    step("计算GeoCell")
    for i in range(width):
        for j in range(height):
            world_pos = vec2i(i, j) + origin
            result[i, j] = GeoCell(
                        position=world_pos,
                        altitude=geothermal_activity_layer[world_pos-origin_padded],
                        solar_radiation=solar_radiation_layer[world_pos-origin],
                        temperature=None,
                        humidity=planetary_humidity_layer[i, j],
                        wind_speed=wind_layer[i, j].length(),
                        wind_direction=float_mod(90 - math.degrees(vec2.angle(wind_layer[i, j], vec2(0, 1))), 360),
                        precipitation=planetary_humidity_layer[i, j],
                        slope=math.degrees(math.atan2(slope_layer[world_pos-slope_origin].length(), 1)),
                        aspect=float_mod(90 - math.degrees(vec2.angle(slope_layer[world_pos-slope_origin], vec2(0, 1))), 360)
                        )
    return result


def request_point(pos:vec2i, geo_config:GeoConfig) -> GeoCell:
    return request_area(pos, 1, 1, geo_config)[0, 0]

