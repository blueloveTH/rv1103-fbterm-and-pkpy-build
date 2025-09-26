# TODO


from array2d import array2d
from vmath import vec2i, vec2

downsample_GRID_ORIGIN = vec2i(0, 0)  # world origin


def aligning_downsample_grid(
    input_field_shape: vec2i,
    input_field_pos: vec2i,
    delta: int,
    align_to: vec2i|None = None
) -> tuple[array2d[vec2i], vec2i]:
    if align_to is None:
        align_to = downsample_GRID_ORIGIN
    assert input_field_shape.x >= align_to.x + delta
    assert input_field_shape.y >= align_to.y + delta
    
    start_x = input_field_pos.x + (align_to.x - input_field_pos.x) % delta
    start_y = input_field_pos.y + (align_to.y - input_field_pos.y) % delta
    grid = array2d(input_field_shape.x//delta, input_field_shape.y//delta, vec2i(0, 0)) # 采样网格
    for i in range(grid.n_cols):
        for j in range(grid.n_rows):
            x = start_x + i * delta
            y = start_y + j * delta
            grid[i, j] = vec2i(x, y)
    return grid, vec2i(start_x, start_y) # 采样网格, 采样网格世界坐标



def aligned_downsample_field(
    input_field: array2d[float],
    input_field_pos: vec2i,
    delta: int,
    align_to: vec2i|None = None
) -> tuple[array2d[float], vec2i]:
    """
    对齐采样网格的前提下, 对某一片区域进行降采样
    
    Args:
        input_field: 输入场
        input_field_pos: 输入场世界坐标
        delta: 采样间隔
        align_to: 对齐位置
    Returns:
        采样后的场, 大小为 (input_field.n_cols//delta) x (input_field.n_rows//delta)
        采样场的世界坐标
    """
    if align_to is None:
        align_to = downsample_GRID_ORIGIN
    assert input_field.n_cols >= input_field_pos.x + delta
    assert input_field.n_rows >= input_field_pos.y + delta
    
    downsample_positions, downsample_positions_pos = aligning_downsample_grid(input_field.shape, input_field_pos, delta, align_to)
    downsampled_field = array2d(downsample_positions.n_cols, downsample_positions.n_rows, 0.0)
    for i in range(downsampled_field.n_cols):
        for j in range(downsampled_field.n_rows):
            downsampled_field[i, j] = input_field[downsample_positions[i, j]]

    return downsampled_field, downsample_positions_pos



sobel_x = array2d[int].fromlist([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
sobel_y = array2d[int].fromlist([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

def _bilinear_interpolate_vec2(field: array2d[vec2], x_idx_float: float, y_idx_float: float) -> vec2:
    """Helper function for bilinear interpolation on a field of vec2."""
    x1 = int(x_idx_float)
    y1 = int(y_idx_float)
    
    fx = x_idx_float - x1
    fy = y_idx_float - y1

    # Clamp indices to valid range to handle boundaries
    x1_clamped = max(0, min(x1, field.n_cols - 1))
    y1_clamped = max(0, min(y1, field.n_rows - 1))
    x2_clamped = max(0, min(x1 + 1, field.n_cols - 1))
    y2_clamped = max(0, min(y1 + 1, field.n_rows - 1))

    p00 = field[x1_clamped, y1_clamped]
    p10 = field[x2_clamped, y1_clamped]
    p01 = field[x1_clamped, y2_clamped]
    p11 = field[x2_clamped, y2_clamped]

    # Interpolate along x-axis for y1 and y2
    interp_y1_x = p00.x * (1 - fx) + p10.x * fx
    interp_y1_y = p00.y * (1 - fx) + p10.y * fx
    
    interp_y2_x = p01.x * (1 - fx) + p11.x * fx
    interp_y2_y = p01.y * (1 - fx) + p11.y * fx

    # Interpolate along y-axis
    final_x = interp_y1_x * (1 - fy) + interp_y2_x * fy
    final_y = interp_y1_y * (1 - fy) + interp_y2_y * fy
    
    return vec2(final_x, final_y)

def _bilinear_interpolate_float(field: array2d[float], x_idx_float: float, y_idx_float: float) -> float:
    """Helper function for bilinear interpolation on a field of float."""
    x1 = int(x_idx_float)
    y1 = int(y_idx_float)
    
    fx = x_idx_float - x1
    fy = y_idx_float - y1

    # Clamp indices to valid range to handle boundaries
    x1_clamped = max(0, min(x1, field.n_cols - 1))
    y1_clamped = max(0, min(y1, field.n_rows - 1))
    x2_clamped = max(0, min(x1 + 1, field.n_cols - 1))
    y2_clamped = max(0, min(y1 + 1, field.n_rows - 1))

    p00 = field[x1_clamped, y1_clamped]
    p10 = field[x2_clamped, y1_clamped]
    p01 = field[x1_clamped, y2_clamped]
    p11 = field[x2_clamped, y2_clamped]

    # Interpolate along x-axis for y1 and y2
    interp_y1 = p00 * (1 - fx) + p10 * fx
    interp_y2 = p01 * (1 - fx) + p11 * fx

    # Interpolate along y-axis
    final = interp_y1 * (1 - fy) + interp_y2 * fy
    
    return final

def _calculate_upsampled_meta(
    downsampled_field_shape: vec2i,
    downsampled_field_pos: vec2i,
    delta: int
) -> tuple[vec2i, vec2i]:
    """
    计算超采样后场的目标形状和世界坐标位置
    
    Args:
        downsampled_field_shape: 降采样场的形状
        downsampled_field_pos: 降采样场的世界坐标
        delta: 原始的降采样间隔，现在作为上采样因子
    
    Returns:
        upsampled_field_shape: 超采样后场的形状
        upsampled_field_pos: 超采样后场的世界坐标
    """
    # 计算超采样后的场的形状（每个低分辨率单元格变为 delta x delta 个高分辨率单元格）
    upsampled_field_shape = vec2i(
        downsampled_field_shape.x * delta,
        downsampled_field_shape.y * delta
    )
    
    # 超采样后场的世界坐标与降采样场相同
    upsampled_field_pos = downsampled_field_pos
    
    return upsampled_field_shape, upsampled_field_pos

def aligned_upsample_field_float(
    downsampled_field: array2d[float],
    downsampled_field_pos: vec2i,
    delta: int
) -> tuple[array2d[float], vec2i]:
    """
    对浮点型场进行超采样（使用双线性插值）
    
    Args:
        downsampled_field: 降采样后的场
        downsampled_field_pos: 降采样场的世界坐标
        delta: 原始的降采样间隔，现在作为上采样因子
    
    Returns:
        upsampled_field: 超采样后的场
        upsampled_field_pos: 超采样后场的世界坐标
    """
    # 计算超采样后场的形状和世界坐标
    upsampled_shape, upsampled_pos = _calculate_upsampled_meta(
        vec2i(downsampled_field.n_cols, downsampled_field.n_rows),
        downsampled_field_pos,
        delta
    )
    
    # 创建超采样后的场
    upsampled_field = array2d(upsampled_shape.x, upsampled_shape.y, 0.0)
    
    # 对每个高分辨率单元格进行双线性插值
    for i in range(upsampled_field.n_cols):
        for j in range(upsampled_field.n_rows):
            # 计算对应的低分辨率场中的浮点索引
            x_idx_float = i / delta
            y_idx_float = j / delta
            
            # 使用双线性插值计算该位置的值
            upsampled_field[i, j] = _bilinear_interpolate_float(downsampled_field, x_idx_float, y_idx_float)
    
    return upsampled_field, upsampled_pos

def aligned_upsample_field_vec2(
    downsampled_field: array2d[vec2],
    downsampled_field_pos: vec2i,
    delta: int
) -> tuple[array2d[vec2], vec2i]:
    """
    对vec2型场进行超采样（使用双线性插值）
    
    Args:
        downsampled_field: 降采样后的场
        downsampled_field_pos: 降采样场的世界坐标
        delta: 原始的降采样间隔，现在作为上采样因子
    
    Returns:
        upsampled_field: 超采样后的场
        upsampled_field_pos: 超采样后场的世界坐标
    """
    # 计算超采样后场的形状和世界坐标
    upsampled_shape, upsampled_pos = _calculate_upsampled_meta(
        vec2i(downsampled_field.n_cols, downsampled_field.n_rows),
        downsampled_field_pos,
        delta
    )
    
    # 创建超采样后的场
    upsampled_field = array2d(upsampled_shape.x, upsampled_shape.y, vec2(0.0, 0.0))
    
    # 对每个高分辨率单元格进行双线性插值
    for i in range(upsampled_field.n_cols):
        for j in range(upsampled_field.n_rows):
            # 计算对应的低分辨率场中的浮点索引
            x_idx_float = i / delta
            y_idx_float = j / delta
            
            # 使用双线性插值计算该位置的值
            upsampled_field[i, j] = _bilinear_interpolate_vec2(downsampled_field, x_idx_float, y_idx_float)
    
    return upsampled_field, upsampled_pos

def gradient_3x3(
    input_field: array2d[float],
    accuracy: float = 1e-5
) -> array2d[vec2]:
    """
    计算3x3窗口内的梯度，使用整型卷积近似浮点计算。
    
    Args:
        input_field: 输入场（浮点型）
        accuracy: 精度控制参数（缩放因子 = 1/accuracy）
    
    Returns:
        梯度场, 大小为 (input_field.n_cols - 2) x (input_field.n_rows - 2)
        每个点为 vec2(gradient_x, gradient_y)
    """
    # 1. 缩放输入和卷积核
    scale = int(1 / accuracy)  # 确保缩放因子为整数
    input_field_scaled = (input_field * float(scale)).map(int)  # 放大后取整
    
    # 3. 执行整型卷积
    gradient_x_scaled = input_field_scaled.convolve(sobel_x, 0)
    gradient_y_scaled = input_field_scaled.convolve(sobel_y, 0)
    
    # 4. 恢复梯度值（考虑归一化因子8和缩放因子）
    gradient_x = (gradient_x_scaled / (8 * scale))[1:-1, 1:-1]
    gradient_y = (gradient_y_scaled / (8 * scale))[1:-1, 1:-1]
    
    # 5. 合并为向量场
    return array2d(
        gradient_x.n_cols, 
        gradient_x.n_rows, 
        lambda p: vec2(gradient_x[p], gradient_y[p])
    )


def compute_gradient(
    input_field: array2d[float],
    input_field_pos: vec2i,
    delta: int,
    align_to: vec2i|None = None
) -> tuple[array2d[vec2], vec2i]:
    
    # 1. 降采样
    downsampled_field, downsample_field_pos = aligned_downsample_field(input_field, input_field_pos, delta, align_to=align_to)
    
    # 2. 计算梯度
    gradient_field = gradient_3x3(downsampled_field)
    actual_gradient_field_world_pos = downsample_field_pos + vec2i(1,1) * delta
    
    if gradient_field.n_cols == 0 or gradient_field.n_rows == 0:
        return array2d(0, 0, vec2(0.0, 0.0)), actual_gradient_field_world_pos

    # 3. 超采样(双线性插值)
    upsampled_gradient_field, upsampled_pos = aligned_upsample_field_vec2(gradient_field, actual_gradient_field_world_pos, delta)
    
    return upsampled_gradient_field, upsampled_pos

def compute_gaussian_blur(
    input_field: array2d[float],
    input_field_pos: vec2i,
    delta: int,
    align_to: vec2i|None = None
) -> tuple[array2d[float], vec2i]:
    """
    使用降采样+超采样的方式实现高斯模糊效果
    
    Args:
        input_field: 输入场
        input_field_pos: 输入场世界坐标
        delta: 采样间隔
        align_to: 对齐位置
    
    Returns:
        blurred_field: 模糊后的场
        blurred_field_pos: 模糊后场的世界坐标
    """
    # 1. 降采样 (相当于平均池化，降低分辨率)
    downsampled_field, downsample_field_pos = aligned_downsample_field(
        input_field, input_field_pos, delta, align_to=align_to
    )
    
    # 2. 超采样 (双线性插值，恢复分辨率，同时产生平滑效果)
    upsampled_field, upsampled_pos = aligned_upsample_field_float(
        downsampled_field, downsample_field_pos, delta
    )
    
    return upsampled_field, upsampled_pos
    
