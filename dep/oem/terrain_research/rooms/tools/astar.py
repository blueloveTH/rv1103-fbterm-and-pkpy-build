from dataclasses import dataclass
from typing import Callable, Any

from vmath import vec2i, vec2
from array2d import array2d

# 四个基本方向：上、右、下、左
DIRS_4 = [vec2i(0, 1), vec2i(1, 0), vec2i(0, -1), vec2i(-1, 0)]

# 类型别名（注释）
# Position = vec2i
# Path = list[Position]
# CostMap = dict[Position, float]
# PathMap = dict[Position, Position | None]

class PathFinder:
    """
    A*寻路算法的封装类
    
    泛型参数:
    P: 位置类型，必须支持加减操作
    """
    
    def __init__(self, 
                 heuristic_fn=None,
                 neighbors_fn=None,
                 cost_fn=None):
        """
        初始化寻路器
        
        参数:
        heuristic_fn (Callable[[P, P], float] | None): 启发式函数，估计从当前位置到目标的成本
        neighbors_fn (Callable[[P], list[P]] | None): 获取邻居节点的函数
        cost_fn (Callable[[P, P], float] | None): 计算两个相邻节点间移动成本的函数
        """
        self.heuristic_fn = heuristic_fn or self._default_heuristic
        self.neighbors_fn = neighbors_fn or self._default_neighbors
        self.cost_fn = cost_fn or self._default_cost
    
    def _default_heuristic(self, current, goal):
        """
        默认启发式函数：使用曼哈顿距离
        
        参数:
        current (P): 当前位置
        goal (P): 目标位置
        
        返回:
        float: 估计的距离成本
        """
        current_vec = vec2(current)
        goal_vec = vec2(goal)
        return (current_vec - goal_vec).length()
    
    def _default_neighbors(self, pos):
        """
        默认邻居函数：返回四个相邻位置
        
        参数:
        pos (P): 当前位置
        
        返回:
        list[P]: 邻居位置列表
        """
        return [pos + d for d in DIRS_4]
    
    def _default_cost(self, current, next_pos):
        """
        默认成本函数：所有移动成本为1
        
        参数:
        current (P): 当前位置
        next_pos (P): 下一个位置
        
        返回:
        float: 移动成本
        """
        return 1.0
    
    def find_path(self, start, goal, max_iterations=10000):
        """
        寻找从起点到终点的路径
        
        参数:
        start (P): 起始位置
        goal (P): 目标位置
        max_iterations (int): 最大迭代次数，防止无限循环
        
        返回:
        list[P] | None: 路径列表，如果没有找到路径则返回None
        """
        # 特殊情况：起点就是终点
        if start == goal:
            return [start]
        
        # 初始化优先队列
        frontier = PriorityQueue()
        frontier.put((0, 0, frontier.curr_id, start))
        
        # 路径记录和成本记录
        came_from = {start: None}  # Dict[P, P | None]
        cost_so_far = {start: 0}   # Dict[P, float]
        
        iterations = 0
        
        # A*主循环
        while not frontier.is_empty() and iterations < max_iterations:
            iterations += 1
            
            # 获取当前成本最低的节点
            _, _, _, current = frontier.pop()
            
            # 如果到达目标，结束搜索
            if current == goal:
                break
            
            # 检查所有邻居节点
            for next_pos in self.neighbors_fn(current):
                # 计算到达邻居节点的成本
                new_cost = cost_so_far[current] + self.cost_fn(current, next_pos)
                
                # 如果找到更优路径，更新成本和路径
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    
                    # 计算优先级（f = g + h）
                    priority = new_cost + self.heuristic_fn(next_pos, goal)
                    
                    # 将邻居节点加入优先队列
                    frontier.put((priority, new_cost, frontier.curr_id, next_pos))
                    
                    # 记录路径
                    came_from[next_pos] = current
        
        # 路径回溯
        if goal in came_from:
            path = self._reconstruct_path(came_from, start, goal)
            return path
        else:
            # 没有找到路径
            return None
    
    def _reconstruct_path(self, came_from, start, goal):
        """
        重建从起点到终点的路径
        
        参数:
        came_from (Dict[P, P | None]): 路径映射
        start (P): 起始位置
        goal (P): 目标位置
        
        返回:
        list[P]: 从起点到终点的路径
        """
        path = [goal]
        current = goal
        
        while current != start:
            current = came_from[current]
            path.append(current)
        
        # 反转路径，从起点到终点
        return path[::-1]

class PriorityQueue:
    """
    优先队列实现
    
    泛型参数:
    T: 队列元素类型
    """
    def __init__(self):
        """初始化空的优先队列"""
        self.elements = []  # list[T]
        self.curr_id = 0    # 用于打破优先级相同时的平局

    def put(self, item):
        """
        添加元素到优先队列
        
        参数:
        item (T): 要添加的元素
        """
        self.curr_id += 1
        self.elements.append(item)
        self._sift_up(len(self.elements) - 1)

    def pop(self):
        """
        移除并返回优先级最高的元素
        
        返回:
        T: 优先级最高的元素
        
        异常:
        IndexError: 当队列为空时抛出
        """
        if self.is_empty():
            raise IndexError("从空优先队列中弹出元素")
        
        result = self.elements[0]
        last_element = self.elements.pop()
        
        if self.elements:
            self.elements[0] = last_element
            self._sift_down(0)
            
        return result

    def peek(self):
        """
        查看优先级最高的元素但不移除
        
        返回:
        T | None: 优先级最高的元素，如果队列为空则返回None
        """
        return self.elements[0] if self.elements else None

    def is_empty(self):
        """
        检查队列是否为空
        
        返回:
        bool: 如果队列为空则返回True，否则返回False
        """
        return len(self.elements) == 0
    
    def _sift_up(self, idx):
        """
        上移操作，用于维护优先队列性质
        
        参数:
        idx (int): 要上移的元素索引
        """
        parent = (idx - 1) // 2
        if idx > 0 and self.elements[parent] > self.elements[idx]:
            self.elements[parent], self.elements[idx] = self.elements[idx], self.elements[parent]
            self._sift_up(parent)
    
    def _sift_down(self, idx):
        """
        下移操作，用于维护优先队列性质
        
        参数:
        idx (int): 要下移的元素索引
        """
        smallest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2
        
        if left < len(self.elements) and self.elements[left] < self.elements[smallest]:
            smallest = left
            
        if right < len(self.elements) and self.elements[right] < self.elements[smallest]:
            smallest = right
            
        if smallest != idx:
            self.elements[idx], self.elements[smallest] = self.elements[smallest], self.elements[idx]
            self._sift_down(smallest)

def point_to_line_distance(point, line_start, line_end):
    '''
    计算点到线段的距离
    
    参数:
    point (vec2): 点的位置
    line_start (vec2): 线段起点
    line_end (vec2): 线段终点
    
    返回:
    float: 点到线段的距离
    '''
    line_vec = line_end - line_start
    point_vec_start = point - line_start
    
    # 处理特殊情况：起点和终点相同
    if line_start.x == line_end.x and line_start.y == line_end.y:
        return point_vec_start.length()

    line_length = line_vec.length()
    if line_length == 0:
        return point_vec_start.length()

    # 计算投影点到线段的距离
    t = max(0, min(1, (point_vec_start.x * line_vec.x + point_vec_start.y * line_vec.y) / (line_length ** 2)))
    projection = line_start + line_vec * t
    return (point - projection).length()

# 为了保持向后兼容性，提供与原始API相同的函数

def astar(start, 
          goal, 
          terrain_cost_fn=None, 
          obstacle_penalty_fn=None, 
          deviation_penalty_fn=None,
          context_for_terrain_cost_fn=None,
          context_for_obstacle_penalty_fn=None,
          context_for_deviation_penalty_fn=None,
          max_wh=None
          ):
    '''
    A* 寻路算法实现（兼容旧接口）。
    
    参数：
    start (vec2i): 网格中的起始位置。
    goal (vec2i): 网格中的目标位置。
    terrain_cost_fn (Callable[[vec2i, Any], float] | None): 计算当前位置地形成本的函数。
    obstacle_penalty_fn (Callable[[vec2i, Any], float] | None): 计算当前位置障碍惩罚的函数。
    deviation_penalty_fn (Callable[[vec2i, vec2i, vec2i, Any], float] | None): 计算偏离惩罚的函数。
    context_for_* (Any): 传递给各函数的附加上下文。
    
    返回值：
    list[vec2i] | None: 从起点到目标点的路径，作为位置列表返回；如果未找到路径，则返回 None。
    '''
    # 设置默认函数
    terrain_cost_fn = terrain_cost_fn or (lambda now_pos, context: 1)
    obstacle_penalty_fn = obstacle_penalty_fn or (lambda now_pos, context: 0)
    
    # 创建成本函数
    def cost_fn(current, next_pos):
        return (
            terrain_cost_fn(next_pos, context_for_terrain_cost_fn) + \
            obstacle_penalty_fn(next_pos, context_for_obstacle_penalty_fn)
        )
    
    # 创建启发式函数
    def heuristic_fn(current, goal):
        if deviation_penalty_fn:
            return deviation_penalty_fn(current, start, goal, context_for_deviation_penalty_fn)
        else:
            return (vec2(current) - vec2(goal)).length()
    
    # 创建邻居函数
    def neighbors_fn(pos):
        return [pos + d for d in DIRS_4]
    
    # 使用新接口
    path_finder = PathFinder(
        heuristic_fn=heuristic_fn,
        neighbors_fn=neighbors_fn,
        cost_fn=cost_fn
    )
    
    return path_finder.find_path(start, goal)

def base_astar_in_grid(
    grid, 
    start, 
    goal, 
    search_intensity=2
):
    """
    在布尔网格上使用A*寻路的简化版本
    
    参数:
    grid (array2d[bool]): 布尔类型的网格，True表示障碍物
    start (vec2i): 起始位置
    goal (vec2i): 目标位置
    search_intensity (float): 搜索强度，影响路径的直线性
    
    返回:
    list[vec2i] | None: 从起点到终点的路径，如果没有找到则返回None
    """
    # 确保坐标是整数
    start = vec2i(int(start.x), int(start.y))
    goal = vec2i(int(goal.x), int(goal.y))
    
    # 验证起点和终点在网格内
    assert grid.is_valid(start) and grid.is_valid(goal), "起点或终点不在网格内"
    
    # 确保网格元素是布尔类型
    def _assert_bool(x):
        assert isinstance(x, bool), "网格元素必须是布尔类型"
    grid.map(_assert_bool)
    
    # 创建成本函数
    def cost_fn(current, next_pos):
        return 1.0 if grid.is_valid(next_pos) and not grid[next_pos] else float('inf')
    
    # 创建启发式函数
    def heuristic_fn(current, goal):
        base_distance = (vec2(current) - vec2(goal)).length()
        deviation = point_to_line_distance(vec2(current), vec2(start), vec2(goal))
        return base_distance + search_intensity * deviation
    
    # 创建邻居函数
    def neighbors_fn(pos):
        return [pos + d for d in DIRS_4 if grid.is_valid(pos + d)]
    
    # 使用新接口
    path_finder = PathFinder(
        heuristic_fn=heuristic_fn,
        neighbors_fn=neighbors_fn,
        cost_fn=cost_fn
    )
    
    return path_finder.find_path(start, goal)