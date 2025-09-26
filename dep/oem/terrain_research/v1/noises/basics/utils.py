import math

import math
from typing import Callable, Tuple, Union

from array2d import array2d
import random

from .voronoi import Voronoi
from .perlin import Perlin

from noises.basics.algorithm import gradient_magnitude_area, laplace_area


def apply_operations_area(
    padded_data: array2d[float], operations: list[Tuple[str, float]]
) -> array2d[float]:
    """
    Returns the result of applying a list of operations to a 2D array of floats.
    * result.size == padded_data[p:-p, p:-p].size
    * p = sum(op in ['Laplace(pos)', 'GradientMagnitude(pos)'] for op in operations)
    """
    result = padded_data.copy()
    min_shape_x = result.shape.x - 2

    for op, param in operations:
        if op == "Power(x, param)":
            result = result**param
        elif op == "Power(param, x)":
            result = param**result
        elif op == "Log(x, param)":
            result = result.map(lambda x: math.log(abs(x) + 1e-9))
        elif op == "Sigmoid(x, param)":
            result = result.map(lambda x: 1 / (1 + math.exp(-param * x)))
        elif op == "Threshold(x, param)":
            result = (result > param).map(lambda x: 1 if x else 0)
        elif op == "Add(x, param)":
            result = result + param
        elif op == "Multiply(x, param)":
            result = result * param
        elif op == "Laplace(pos)":
            result = laplace_area(result)
            min_shape_x = min(min_shape_x, result.shape.x)
        elif op == "GradientMagnitude(pos)":
            result = gradient_magnitude_area(result)
            min_shape_x = min(min_shape_x, result.shape.x)

    padding = (result.shape.x - min_shape_x) // 2
    if padding == 0:
        return result
    return result[padding:-padding, padding:-padding]


def terrain_to_ascii(terrain, chars=(".", "*", "#"), size=(40, 40)):

    if not chars:
        raise ValueError("字符列表不能为空")

    # 获取地形数据的最小和最大值
    max_h_pos, max_h = max(terrain, key=lambda pos_value_pair: pos_value_pair[1])
    min_h_pos, min_h = min(terrain, key=lambda pos_value_pair: pos_value_pair[1])

    if min_h is None or max_h is None:
        return ""  # 空地形

    # 计算高度分段阈值
    num_chars = len(chars)
    if num_chars == 0:
        raise ValueError("字符列表不能为空")
    thresholds = []
    for i in range(1, num_chars):
        fraction = i / num_chars
        thresholds.append(min_h + fraction * (max_h - min_h))

    # 创建高度到字符的映射函数
    def height_to_char(h):
        for i, t in enumerate(thresholds):
            if h <= t:
                return chars[i]
        return chars[-1]

    # 处理采样尺寸
    original_cols = terrain.n_cols
    original_rows = terrain.n_rows
    step = 1
    if size is not None:
        output_width, output_height = size
        if output_width <= 0 or output_height <= 0:
            raise ValueError("输出尺寸必须大于0")
        x_scale = original_cols / output_width
        y_scale = original_rows / output_height
        scale = max(x_scale, y_scale)
        step = max(int(scale), 1)

    # 采样原始地形
    sampled_terrain = terrain[::step, ::step]
    sampled_data = sampled_terrain.tolist()

    # 转换为ASCII字符
    ascii_art = []
    for row in sampled_data:
        ascii_row = " ".join([height_to_char(h) for h in row])
        ascii_art.append(ascii_row)

    # 添加垂直填充保持比例
    if size is not None:
        target_width, target_height = size
        current_lines = len(ascii_art)
        if current_lines < target_height:
            padding_needed = target_height - current_lines
            padding = random.choices(ascii_art, k=padding_needed)
            ascii_art.extend(padding)

    return "\n".join(ascii_art)


def generate_layer_noise(pos: vec2i, layer: dict, perlin:perlin.Perlin|None = None, voronoi:voronoi.Voronoi|None = None) -> float:
    if layer['noise_type'] == 'Perlin':
        return perlin.noise_ex(
            pos.x/layer['scale'], pos.y/layer['scale'], 0,
            layer['octaves'],
            persistence=layer['persistence'],
            lacunarity=layer['lacunarity'])
    elif layer['noise_type'] == 'Voronoi':
        return voronoi.noise_ex(
            pos.x/layer['scale'], pos.y/layer['scale'], 0,
            layer['radius'],
            layer['falloff'],
            layer['octaves'],
            persistence=layer['persistence'],
            lacunarity=layer['lacunarity'])