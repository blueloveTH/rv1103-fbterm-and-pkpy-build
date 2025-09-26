import math
from typing import Callable, List, Union, Tuple
import random as random_module

def sigmoid_probability(x: Union[float, List[float], Tuple[float, ...]], 
                       reference_value: Union[float, List[float], Tuple[float, ...]], 
                       reference_probability: float, 
                       random_generator=None, 
                       max_probability: float = 1.0, 
                       slope: Union[float, List[float], Tuple[float, ...]] = 1.0) -> bool:
    """使用sigmoid函数计算概率并根据该概率返回布尔值
    
    Args:
        x: 当前值或当前值列表
        reference_value: 参考值或参考值列表，当x等于此值时，概率为reference_probability
        reference_probability: 参考值对应的概率
        random_generator: 随机数生成器，默认使用random模块
        max_probability: 最大概率，默认为1.0
        slope: sigmoid曲线的斜率或斜率列表，较大的值使曲线更陡峭，默认为1.0
    
    Returns:
        根据计算出的概率随机决定的布尔值
    """
    # 使用默认的random模块如果没有提供random_generator
    random_gen = random_generator or random_module
    
    # 确保参考概率在有效范围内
    reference_probability = max(0.0, min(reference_probability, max_probability))
    
    # 将单个值转换为列表以统一处理
    x_list = [x] if isinstance(x, (int, float)) else list(x)
    ref_list = [reference_value] if isinstance(reference_value, (int, float)) else list(reference_value)
    slope_list = [slope] if isinstance(slope, (int, float)) else list(slope)
    
    # 确保所有列表长度一致
    max_len = max(len(x_list), len(ref_list), len(slope_list))
    
    # 扩展列表到相同长度
    if len(x_list) < max_len:
        repeat_times = max_len // len(x_list) + (1 if max_len % len(x_list) else 0)
        x_list = (x_list * repeat_times)[:max_len]
    
    if len(ref_list) < max_len:
        repeat_times = max_len // len(ref_list) + (1 if max_len % len(ref_list) else 0)
        ref_list = (ref_list * repeat_times)[:max_len]
    
    if len(slope_list) < max_len:
        repeat_times = max_len // len(slope_list) + (1 if max_len % len(slope_list) else 0)
        slope_list = (slope_list * repeat_times)[:max_len]
    
    # 计算每个条件的概率
    probabilities = []
    # 使用单独的循环代替zip
    for i in range(max_len):
        xi = x_list[i]
        ref = ref_list[i]
        s = slope_list[i]
        
        # 从参考概率计算sigmoid的中点位置
        if reference_probability <= 0:
            midpoint = float('inf')  # 如果参考概率为0，则中点设为无穷大
        elif reference_probability >= max_probability:
            midpoint = float('-inf')  # 如果参考概率为最大值，则中点设为负无穷大
        else:
            # 解方程得到中点
            midpoint = ref + math.log((max_probability / reference_probability) - 1) / s
        
        # 使用sigmoid函数计算概率
        if xi <= midpoint and s > 0:
            prob = max_probability / (1 + math.exp(-s * (xi - midpoint)))
        elif xi >= midpoint and s < 0:
            prob = max_probability / (1 + math.exp(-s * (xi - midpoint)))
        elif s > 0:
            prob = max_probability
        else:
            prob = 0.0
        
        probabilities.append(prob)
    
    # 取所有条件概率的平均值作为最终概率
    final_probability = sum(probabilities) / len(probabilities)
    
    # 基于计算出的概率返回布尔值
    return random_gen.random() < final_probability

def get_probability(x: Union[float, List[float], Tuple[float, ...]], 
                   reference_value: Union[float, List[float], Tuple[float, ...]], 
                   reference_probability: float, 
                   max_probability: float = 1.0, 
                   slope: Union[float, List[float], Tuple[float, ...]] = 1.0) -> float:
    """仅计算sigmoid概率值而不进行随机决策
    
    Args:
        x: 当前值或当前值列表
        reference_value: 参考值或参考值列表，当x等于此值时，概率为reference_probability
        reference_probability: 参考值对应的概率
        max_probability: 最大概率，默认为1.0
        slope: sigmoid曲线的斜率或斜率列表，较大的值使曲线更陡峭，默认为1.0
    
    Returns:
        计算出的概率值（0.0到max_probability之间）
    """
    # 确保参考概率在有效范围内
    reference_probability = max(0.0, min(reference_probability, max_probability))
    
    # 将单个值转换为列表以统一处理
    x_list = [x] if isinstance(x, (int, float)) else list(x)
    ref_list = [reference_value] if isinstance(reference_value, (int, float)) else list(reference_value)
    slope_list = [slope] if isinstance(slope, (int, float)) else list(slope)
    
    # 确保所有列表长度一致
    max_len = max(len(x_list), len(ref_list), len(slope_list))
    
    # 扩展列表到相同长度
    if len(x_list) < max_len:
        repeat_times = max_len // len(x_list) + (1 if max_len % len(x_list) else 0)
        x_list = (x_list * repeat_times)[:max_len]
    
    if len(ref_list) < max_len:
        repeat_times = max_len // len(ref_list) + (1 if max_len % len(ref_list) else 0)
        ref_list = (ref_list * repeat_times)[:max_len]
    
    if len(slope_list) < max_len:
        repeat_times = max_len // len(slope_list) + (1 if max_len % len(slope_list) else 0)
        slope_list = (slope_list * repeat_times)[:max_len]
    
    # 计算每个条件的概率
    probabilities = []
    # 使用单独的循环代替zip
    for i in range(max_len):
        xi = x_list[i]
        ref = ref_list[i]
        s = slope_list[i]
        
        # 从参考概率计算sigmoid的中点位置
        if reference_probability <= 0:
            midpoint = float('inf')  # 如果参考概率为0，则中点设为无穷大
        elif reference_probability >= max_probability:
            midpoint = float('-inf')  # 如果参考概率为最大值，则中点设为负无穷大
        else:
            # 解方程得到中点
            midpoint = ref + math.log((max_probability / reference_probability) - 1) / s
        
        # 使用sigmoid函数计算概率
        if xi <= midpoint and s > 0:
            prob = max_probability / (1 + math.exp(-s * (xi - midpoint)))
        elif xi >= midpoint and s < 0:
            prob = max_probability / (1 + math.exp(-s * (xi - midpoint)))
        elif s > 0:
            prob = max_probability
        else:
            prob = 0.0
        
        probabilities.append(prob)
    
    # 取所有条件概率的平均值作为最终概率
    return sum(probabilities) / len(probabilities) 