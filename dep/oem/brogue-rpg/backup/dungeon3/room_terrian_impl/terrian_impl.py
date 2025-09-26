import random
from array2d import array2d
from collections import deque
import random



DIRS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
def find_connected_components(grid: array2d, value) -> tuple[array2d[int], int]:
    """获取图的所有连通分量
    
    返回`visited`数组与连通分量个数，其中`0`表示未访问，非`0`表示所在连通分量的索引（从1开始）
    """
    visited = array2d(grid.width, grid.height, default=0)
    queue = deque()
    count = 0       # 以连通分量的索引作为块的id
    for y in range(grid.height):
        for x in range(grid.width):
            if visited[x, y] or grid[x, y] != value:
                continue
            count += 1
            queue.append((x, y))
            visited[x, y] = count
            while queue:
                cx, cy = queue.popleft()
                for dx, dy in DIRS_4:
                    nx, ny = cx+dx, cy+dy
                    if grid.is_valid(nx, ny) and not visited[nx, ny] and grid[nx, ny] == value:
                        queue.append((nx, ny))
                        visited[nx, ny] = count
    return visited, count

def count_connected_components(grid: array2d, value) -> int:
    """计算图的连通分量个数"""
    _, count = find_connected_components(grid, value)
    return count

def find_largest_connected_component(grid: array2d, value) -> array2d[bool] | None:
    """获取图的面积最大的连通分量"""
    visited, count = find_connected_components(grid, value)
    if count == 0:
        return None
    counter = [0] * (count+1)
    for y in range(grid.height):
        for x in range(grid.width):
            counter[visited[x, y]] += 1
    counter[0] = 0  # 不考虑未访问的格子
    max_blob_id = counter.index(max(counter))
    return visited.map(lambda x: x == max_blob_id)

def iter_unordered(grid: array2d, cache: list = None) -> list[tuple[int, int]]:
    if not cache:
        for y in range(grid.height):
            for x in range(grid.width):
                cache.append((x,y))
    assert len(cache) == grid.numel
    random.shuffle(cache)
    return cache.copy()

def fill_circle_(grid: array2d[int], value, center_x: int, center_y: int, radius: int) -> None:
    """逐行扫描圆的外接正方形, 并对距离圆心为`sqrt(r^2 + r)`的点填充为`value`"""

    x_scan_range = range(max(0, center_x - radius - 1), min(grid.width, center_x + radius)+1)
    y_scan_range = range(max(0, center_y - radius - 1), min(grid.height, grid.height + radius)+1)
    
    for x in x_scan_range:
        for y in y_scan_range:
            if not grid.is_valid(x, y):
                continue
            is_in_circle = (x-center_x)**2 + (y-center_y)**2 < radius**2+radius
            if is_in_circle:
                grid[x, y] = value

def fill_rect_(grid: array2d[int], value, conor_x: int, conor_y: int, width: int, height: int) -> None:
    x_scan_range = range(conor_x, conor_x+width)
    y_scan_range = range(conor_y, conor_y+height)
    
    for x in x_scan_range:
        for y in y_scan_range:
            if not grid.is_valid(x,y):
                continue
            grid[x, y] = value

def trim(grid: array2d[int], value) -> array2d[int]:
    """裁剪出包含`value`的最小矩形区域"""
    x, y, w, h = grid.get_bounding_rect(value)
    return grid[x:x+w, y:y+h]



ZERO=0
ONE=1
# 下面是生成房间的逻辑-------------------------------------------
def brogue_designCircularRoom(grid: array2d[int]):
    '''
    在grid中央上绘制一个圆形房间, 有大概率生成实心圆, 有小概率生成甜甜圈样式
    
    圆的半径在2~10之间
    '''
    assert grid.width >= 21 and grid.height >= 21 
    
    grid.fill_(ZERO)  # 以0填充所有的格子

    center_x = grid.width//2
    center_y = grid.height//2
    
    # 确定房间的半径
    if random.random() < 0.5:
        room_radius = random.randint(4, 10)
    else:
        room_radius = random.randint(2, 4)
    
    # 绘制房间
    fill_circle_(grid, ONE, center_x, center_y, room_radius)
    
    # 绘制房间中的空洞
    if room_radius > 6 and random.random() < 0.5:
        hole_radius = random.randint(3, room_radius-3)
        fill_circle_(grid, ZERO, center_x, center_y, hole_radius)


def brogue_designSmallRoom(grid: array2d[int]):
    '''
    在grid中央上绘制一个矩形房间
    
    矩形宽度在3~6之间, 高度在2~4之间
    '''
    assert grid.width >= 6 and grid.height >= 4 
    
    grid.fill_(ZERO)  # 以0填充所有的格子
    
    room_width = random.randint(3, 6)
    room_height = random.randint(2, 4)
    room_x = (grid.width - room_width) // 2  # 确保房间的中心和grid中心对齐
    room_y = (grid.height - room_height) // 2
    
    fill_rect_(grid, ONE, room_x, room_y, room_width, room_height)
    
    
def brogue_designCrossRoom(grid: array2d[int]):
    '''
    在房间偏左下的位置生成两个矩形交叉而成的房间
    '''
    assert grid.width >= 30 and grid.height >= 15
    grid.fill_(ZERO)  # 以0填充所有的格子

    # 确定两个房间的x坐标和宽度
    room1_width = random.randint(3, 12)
    room1_x =                                           \
        random.randint(
            max(0, grid.width//2 - (room1_width - 1)),
            grid.width//2
        )
    
    room2_width = random.randint(4, 20)
    room2_x =                                           \
        random.choice([-1, 0,0, 1,1,1, 2,2, 3]) +       \
        room1_x +                                       \
        (room1_width - room2_width)//2
    
    
    # 确定两个房间的y坐标和高度
    room1_height = random.randint(3, 7)
    room1_y = grid.height//2 - room1_height
    
    room2_height = random.randint(2, 5)
    room2_y =                                           \
        grid.height//2 -                                \
        room2_height +                                  \
        random.choice([0, -1,-1, -2,-2, -3])            
    
    # 将房间整体向左下角偏移
    room1_x -= 5
    room2_x -= 5
    room1_y += 5
    room2_y += 5
    
    # 绘制
    fill_rect_(grid, ONE, room1_x, room1_y, room1_width, room1_height)
    fill_rect_(grid, ONE, room2_x, room2_y, room2_width, room2_height)


def brogue_designSymmetricalCrossRoom(grid: array2d[int]):
    '''
    在房间中央生成两个矩形交叉而成的房间
    
    将不会生成"L"形房间
    '''
    assert grid.width >= 8 and grid.height >= 5 
    grid.fill_(ZERO)  # 以0填充所有的格子

    # 确定房间1的规格
    room1_width = random.randint(4, 8)
    room1_height = random.randint(4, 5)
    
    # 根据房间1规格的奇偶性, 确定房间2的规格, 为了避免生成"L"型房间
    room2_width = random.randint(3, 4) - 1 if room1_height % 2 == 0 else random.randint(3, 4)
    room2_height = 3 - 1 if room1_width % 2 == 0 else 3
    
    # 根据两个房间的规格, 确定格子的位置, 为了使得它们落在grid中央
    room1_x = (grid.width - room1_width) // 2
    room1_y = (grid.height - room1_height) // 2
    room2_x = (grid.width - room2_width) // 2
    room2_y = (grid.height - room2_height) // 2
    
    # 绘制
    fill_rect_(grid, ONE, room1_x, room1_y, room1_width, room1_height)
    fill_rect_(grid, ONE, room2_x, room2_y, room2_width, room2_height)


def brogue_designChunkyRoom(grid: array2d[int]):
    '''
    生成若干连续的小圆(下面称作chunk)拼成的房间, 首个圆生成在grid中央
    '''
    assert grid.width >= 14 and grid.height >= 15
    
    grid.fill_(ZERO) # 以0填充所有的格子

    chunk_count = random.randint(2, 8)  # 即将生成的小圆数量
    radius = 2  # 所有小圆的半径
    
    # 定义并绘制首个圆, 并寄存到表示"上一个圆"的变量
    last_circle = {
        'x': grid.width // 2, 
        'y': grid.height // 2,
        'next_min_x': grid.width // 2 - 3,  # 下一个圆的圆心随机生成范围
        'next_max_x': grid.width // 2 + 3,
        'next_min_y': grid.height // 2 - 3,
        'next_max_y': grid.height // 2 + 3,
    }
    fill_circle_(grid, ONE, last_circle['x'], last_circle['y'], radius)
    
    for _ in range(chunk_count):
        # 确定圆的位置, 必须让所有的圆的圆心落在已绘制的区域上
        while True:
            x = random.randint(last_circle['next_min_x'], last_circle['next_max_x'])
            y = random.randint(last_circle['next_min_y'], last_circle['next_max_y'])
            if grid[x,y] == 1:
                break
            
        
        # 确定当前的圆
        circle = {
            'x': x, 
            'y': y,
            'next_min_x': max(1, min(x-3, last_circle['next_min_x'])),
            'next_max_x': min(grid.width-2, max(x+3, last_circle['next_max_x'])),
            'next_min_y': max(1, min(y-3, last_circle['next_min_y'])),
            'next_max_y': min(grid.height-2, max(y+3, last_circle['next_max_y']))
        }
        
        last_circle = circle

        #绘制
        fill_circle_(grid, ONE, circle['x'], circle['y'], radius)


def brogue_designEntranceRoom(grid: array2d[int]):
    assert grid.width >= 22 and grid.height >= 12 
    
    grid.fill_(ZERO)
    
    room1_width = 8
    room1_height = 10
    room2_width = 20
    room2_height = 5
    room1_x = grid.width // 2 - room1_width // 2 - 1
    room1_y = grid.height - room1_height - 2
    room2_x = grid.width // 2 - room2_width // 2 - 1
    room2_y = grid.height - room2_height - 2

    fill_rect_(grid, ONE, room1_x, room1_y, room1_width, room1_height)
    fill_rect_(grid, ONE, room2_x, room2_y, room2_width, room2_height)







# ---------------------------------洞穴---------------------------------
# 关于洞穴的生成算法, 程序将不断尝试在max_width, max_height内随机生成块, 而直到块的规格符合要求时才会停止
# 根据经验, 它们的规格多数集中在max_width/2, max_height/2附近, 因此当块的下限min_width, min_height大于max_width/2, max_height/2时, 将很难在短时间内生成洞穴
# 因此对于下列预设的函数, 传入的grid的规格需要尽可能大(我已经基于大量测试设定了合适的assert限制), 以防止生成速度变慢, 甚至是超出1000次的重新生成限制报AssertionError

def brogue_design_compat_cavern(grid: array2d):
    _brogue_designCavern(grid, 3, 12, 4, 8)

def brogue_design_large_north_south_cavern(grid: array2d):
    assert grid.width >= 4 and grid.height >= 18
    _brogue_designCavern(grid, 3, 12, 15, grid.height-2)

def brogue_design_large_east_west_cavern(grid: array2d):
    assert grid.width >= 22 and grid.height >= 22
    _brogue_designCavern(grid, 20, grid.height-2, 4, 8)

def brogue_design_cave(grid: array2d, cave_min_width, cave_min_height):
    assert grid.width >= cave_min_width and grid.height >= cave_min_height
    _brogue_designCavern(grid, cave_min_width, grid.width-2, cave_min_height, grid.height-2)



# ----------- _brogue_designCavern 为原作函数, 以上为原作中调用该函数的四个地方
def _brogue_designCavern(grid: array2d[int], min_width: int, max_width: int, min_height: int, max_height: int):
    """
    使用元胞自动机生成限定规格的一块洞穴样式的房间
    """
    assert min_width <= max_width and min_height <= max_height
    
    grid.fill_(ZERO)
    
    blob_grid = array2d(max_width, max_height, default=None)  # 用来培育块的网格, 尺寸为块的最大尺寸
    round_count = 2  # 当它被设定地很高时, 生成将非常耗时, 当它越大, 房间越大,但是边缘越粗糙, 反之, 当它越小,房间越小,边缘越光滑
    noise_probability = 0.55
    birth_parameters = "ffffffttt"
    survival_parameters = "ffffttttt"
    blob_grid = _brogue_createBlobOnGrid(blob_grid, min_width, max_width, min_height, max_height, round_count, noise_probability, birth_parameters, survival_parameters)
    
    # 下面将生成的块从blob_grid中复制到grid中
    blob_w, blob_h = blob_grid.width, blob_grid.height

    # 把blob_grid复制到grid的中心
    grid_x = (grid.width - blob_w) // 2
    grid_y = (grid.height - blob_h) // 2
    grid[grid_x: grid_x+blob_w, grid_y: grid_y+blob_h] = blob_grid



# _brogue_designCavern 的一部分, 用于构造房间, _brogue_designCavern会将该房间插入到大的grid
def _brogue_createBlobOnGrid(
    grid: array2d[int], 
    blob_min_width: int, 
    blob_max_width: int, 
    blob_min_height: int,  
    blob_max_height: int,  
    round_count = 5, 
    noise_probability = 0.55, 
    birth_parameters = 'ffffffttt',  
    survival_parameters = 'ffffttttt' \
    ) -> array2d[int]:
    '''
    本函数利用细胞自动机按照培育参数在给定的空网格之内生成图案, 并返回最大的块在网格中的位置和规格
    
    参数列表:
        grid:  
            用于培育块的网格
        blob_min_width:  
            用于限制块的规格
        blob_max_width:  
            用于限制块的规格
        blob_min_height:  
            用于限制块的规格
        blob_max_height:   
            用于限制块的规格
        round_count = 10:  
            细胞自动机的迭代次数
        noise_probability = 0.55 :
            初始噪声的生成率 
        birth_parameters = 'ffffffttt' :
            长度为9的字符串, 表示当前格子附近3x3区域内存在index个细胞时, birth_parameters[index]的值(t/f)将决定本格子是否在下一轮迭代时生成细胞, 或使本格子细胞存活
        survival_parameters = 'ffffttttt' :
            同上, 假如本格子不会诞生新细胞, 那么这个参数将判定周围细胞的密度以决定下一轮迭代时本格子的细胞是否会被销毁, 't'表示存活, 'f'表示销毁
    
    返回值:
        四元组, 其中每个元素分别表示最大块外接矩形的 (左上角x坐标, 左上角y坐标, 宽度, 高度)
    '''
    
    survival_value, dead_value = -1, -2
    TIME_OUT_LOOP = 2000
    loop_count = 0
    while True:
        loop_count += 1
        assert loop_count <= TIME_OUT_LOOP
        
        # ---- 生成初始噪声
        grid.apply_(lambda _: survival_value if random.random() < noise_probability else dead_value)
        
        # ---- 细胞自动机开始数轮迭代
        for _ in range(round_count):
            # 每轮迭代遍历并修改 blob_grid 所有格子
            last_grid = grid.copy()  # 记录上一轮迭代的最终结果, 接下来将就地修改blob_grid

            # 计算当前格子的周围中存在活细胞的数量
            live_neighbors = grid.count_neighbors(survival_value, 'Moore')
            
            for cell_x in range(grid.width):
                for cell_y in range(grid.height):
                    # 计算本轮迭代中该格子的细胞的命运
                    nb_count = live_neighbors[cell_x, cell_y]
                    last_value = last_grid[cell_x, cell_y]
                    # 原作实现：
                    # if (!buffer2[i][j] && birthParameters[nbCount] == 't') {
                    #     grid[i][j] = 1; // birth
                    # } else if (buffer2[i][j] && survivalParameters[nbCount] == 't') {
                    #      // survival
                    # } else {
                    #     grid[i][j] = 0; // death
                    # }
                    if last_value == dead_value and birth_parameters[nb_count] == 't':
                        grid[cell_x, cell_y] = survival_value   # birth
                    elif last_value == survival_value and survival_parameters[nb_count] == 't':
                        pass    # survival
                    else:
                        grid[cell_x, cell_y] = dead_value
        
        largest = find_largest_connected_component(grid, survival_value)
        if largest is not None:
            rect = largest.get_bounding_rect(True)
            assert rect is not None  # 如果没有在地图中找到Ture, 说明前面的代码存在问题
            blob_x, blob_y, blob_w, blob_h = rect
            # 检测是否满足对块的规格限制
            if (blob_min_width <= blob_w <= blob_max_width) and (blob_min_height <= blob_h <= blob_max_height):
                largest = largest[blob_x: blob_x+blob_w, blob_y: blob_y+blob_h]
                return largest.map(lambda x: ONE if x else ZERO)
