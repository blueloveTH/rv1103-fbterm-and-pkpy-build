from typing import Callable
from noises.basics.perlin import Perlin
from noises.basics.voronoi import Voronoi
from vmath import vec2, vec2i
from geography.schema import NoiseType

def make_noise_func(seed: int, noise_type: str, octaves: int, scale: tuple[float, float], min_amplitude: float) -> Callable[[vec2i], float]:
    """
    生成噪声函数(输出区间为[-0.5, 0.5])
    seed: 随机种子
    noise_type: 噪声类型
    octaves: 多重分形噪声的层数
    scale: 多重分形噪声的尺度范围
    min_amplitude: 最小高度贡献权重
    """
    # print(f"make_noise_func: {seed}, {noise_type}, {octaves}, {scale}, {min_amplitude}")
    
    noise_generator = None
    
    if noise_type == NoiseType.PERLIN:
        noise_generator = Perlin(seed)
    elif noise_type == NoiseType.VORONOI:
        noise_generator = Voronoi(seed)
    else:
        raise ValueError(f"Invalid noise type: {noise_type}")
    
    try:
        assert (isinstance(scale[0], float) or isinstance(scale[0], int)) and (isinstance(scale[1], float) or isinstance(scale[1], int))
        assert scale[0] < scale[1]
        assert 0 < min_amplitude <= 1.0
    except:
        raise ValueError(f"{scale}")
    
    if octaves == 1:
        persistence = 1.0
    else:
        persistence = min_amplitude ** (1.0 / (octaves - 1))
    
    if octaves == 1:
        lacunarity = 1.0
    else:
        lacunarity = (scale[1] / scale[0]) ** (1.0 / (octaves - 1))
    
    base_frequency = 1.0 / scale[1]    
    # print(f"base_frequency: {base_frequency}, lacunarity: {lacunarity}, persistence: {persistence}")
    
    def noise_func(pos: vec2i) -> float:
        # 将原始噪声值乘以0.5，约束在[-0.5, 0.5]范围内
        return noise_generator.noise_ex(
            pos.x * base_frequency, 
            pos.y * base_frequency, 
            0,
            octaves,
            persistence=persistence,
            lacunarity=lacunarity) * 0.5
    
    # 间隔0.5晶格采样1000次, 并且打印最大最小值
    # max_val = -float("inf")
    # min_val = float("inf")
    # for i in range(100000):
    #     pos = vec2(i * 0.1, i * 0.01) / base_frequency
    #     val = noise_func(pos)
    #     max_val = max(max_val, val)
    #     min_val = min(min_val, val)
    # print(f"max_val: {max_val}, min_val: {min_val}")
    
    return noise_func