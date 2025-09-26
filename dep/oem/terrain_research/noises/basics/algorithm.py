from array2d import array2d, array2d_like
import math

from vmath import vec2i

import random

def lcg_hash(x: int) -> int:
    """简单的 LCG 伪随机哈希（32 位）"""
    return (1103515245 * x + 12345) & 0xFFFFFFFF

def int32_to_float_hash(x):
    # 将 32 位整数转换为 [0, 1) 的浮点数
    return (x & 0x1FFFFF) / (1 << 21)  # 使用 21 位精度

def hash_vec2i_to_f(pos: tuple[int, int], salt: int = 0) -> float:
    """使用 LCG 哈希 2D 坐标到 [0, 1)"""
    x, y = pos
    combined = (x * 0x1f1f1f1f) ^ (y * 0x9e3779b9) ^ salt  # 混合 x, y, salt
    hash_int = lcg_hash(combined)  # 计算 LCG 哈希
    return int32_to_float_hash(hash_int)
    
def advanced_sigmoid(x, k=1, center=0, output_low=0, output_high=1):
    """
    改进版 Sigmoid 函数（可调中心位置和输出区间）
    
    参数:
        x: 输入值（任意实数）
        k: 陡峭度（越大曲线越陡，默认1）
        center: 中心位置（y=0.5的位置，默认0）
        output_low: 输出下限（默认0）
        output_high: 输出上限（默认1）
    
    返回:
        映射到[output_low, output_high]的值
    """
    # 计算Sigmoid基础值
    sig = 1 / (1 + math.exp(-k * (x - center)))
    # 线性映射到目标区间
    return output_low + (output_high - output_low) * sig

def convolve3x3_trimmed_float(
    input: array2d_like[float], kernel: array2d_like[float]
) -> array2d_like[float]:
    """
    Perform 3x3 convolution with float precision, discarding outer edges.
    Ensures input and kernel are converted to float if not already.

    Args:
        input: Input array (H, W)
        kernel: 3x3 convolution kernel

    Returns:
        Convolved array of shape (H-2, W-2), with float dtype.
    """
    input = input.map(float)  # Convert entire array to float
    kernel = kernel.map(float)  # Convert kernel to float

    H, W = input.n_rows, input.n_cols

    output = array2d(W - 2, H - 2)

    k00, k01, k02 = kernel[0, 0], kernel[0, 1], kernel[0, 2]
    k10, k11, k12 = kernel[1, 0], kernel[1, 1], kernel[1, 2]
    k20, k21, k22 = kernel[2, 0], kernel[2, 1], kernel[2, 2]

    for i in range(W - 2):
        for j in range(H - 2):
            output[i, j] = (
                input[i, j] * k00\
                + input[i, j + 1] * k01\
                + input[i, j + 2] * k02\
                + input[i + 1, j] * k10\
                + input[i + 1, j + 1] * k11\
                + input[i + 1, j + 2] * k12\
                + input[i + 2, j] * k20\
                + input[i + 2, j + 1] * k21\
                + input[i + 2, j + 2] * k22\
            )

    return output


def laplace_area(padded_data: array2d[float]) -> array2d[float]:
    """
    Returns the Laplace operator applied to a 2D array.(result.size == padded_data[1:-1, 1:-1].size)
    """
    kernel = type(padded_data).fromlist([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    return convolve3x3_trimmed_float(padded_data, kernel)


def gradient_magnitude_area(padded_data: array2d[float]) -> array2d[float]:
    kernel_x = type(padded_data).fromlist([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    kernel_y = type(padded_data).fromlist([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    return (\
        convolve3x3_trimmed_float(padded_data, kernel_x)\
        + convolve3x3_trimmed_float(padded_data, kernel_y)\
    ) ** 0.5


def filter_components_by_area(
    data: array2d, value, neighborhood_mode: str, min_area: int, max_area: int
) -> array2d:
    """
    将连通域面积在 [min_area, max_area] 范围内的区域保留，其余设为 0。

    Args:
        data: 输入的二维数组
        value: 目标值（要找的连通域的值）
        neighborhood_mode: 邻域类型（4-邻域或8-邻域）
        min_area: 最小连通域面积（含）
        max_area: 最大连通域面积（含），默认为无穷大，即不设上限

    Returns:
        处理后的数组，只保留面积在指定范围内的连通域，其余设为 0
    """
    # Step 1: 获取连通域标记
    visited, count = data.get_connected_components(value, neighborhood_mode)

    # Step 2: 统计每个连通域的面积
    area = {}  # component_id -> pixel count
    for i in range(visited.n_cols):
        for j in range(visited.n_rows):
            component_id = visited[i, j]
            if component_id > 0:
                area[component_id] = area.get(component_id, 0) + 1

    # Step 3: 找出要保留的连通域（面积在 [min_area, max_area] 范围内）
    valid_components = {cid for cid, cnt in area.items() if min_area <= cnt <= max_area}

    # Step 4: 生成结果数组
    result = data.copy()
    mask = visited.map(lambda x: 1 if x in valid_components else 0)
    result = result * mask

    return result
