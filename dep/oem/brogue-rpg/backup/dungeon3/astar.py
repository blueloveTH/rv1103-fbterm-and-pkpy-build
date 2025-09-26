from dataclasses import dataclass
from typing import Callable, Any

from vmath import vec2i, vec2
from array2d import array2d
from .utils import DIRS_4
from .test_tools import *

import heapq

import math


BASE_DEVIATION_PENALTY_FN = lambda now_pos, start_pos, goal_pos, context: point_to_line_distance(vec2(now_pos), vec2(start_pos), vec2(goal_pos)) + (vec2(now_pos)-vec2(goal_pos)).length()

class PriorityQueue[T]:
    def __init__(self):
        self.heap = []
        self.curr_id = 0

    def put(self, item:T):
        self.curr_id += 1
        heapq.heappush(self.heap, item)

    def pop(self):
        return heapq.heappop(self.heap)

    def peek(self):
        return self.heap[0] if self.heap else None

    def is_empty(self):
        return len(self.heap) == 0
    
    def __str__(self):
        self.heap.__repr__()

def point_to_line_distance(point:vec2, line_start:vec2, line_end:vec2)->float:
    '''点到线段的距离, 表现为一个手电筒朝上从线段的一端划到另一端, 其圆锥形光线所形成区域的边界'''
    line_vec = line_end - line_start
    point_vec_start = point - line_start
    point_vec_end = point - line_end
    
    if line_start.x == line_end.x and line_start.y == line_end.y:
        return point_vec_start.length()

    line_length = line_vec.length()
    if line_length == 0:
        return point_vec_start.length()

    # 投影点到线段的距离（比值）
    t = max(0, min(1, (point_vec_start.x * line_vec.x + point_vec_start.y * line_vec.y) / (line_length ** 2)))
    projection = line_start + line_vec * t
    return (point - projection).length()





def astar(start: vec2i, 
          goal: vec2i, 
          terrain_cost_fn: Callable[[vec2i, Any], float] = None, 
          obstacle_penalty_fn: Callable[[vec2i, Any], float] = None, 
          deviation_penalty_fn: Callable[[vec2i, vec2i, vec2i, Any], float] = None,
          context_for_terrain_cost_fn:Any=None,
          context_for_obstacle_penalty_fn:Any=None,
          context_for_deviation_penalty_fn:Any=None,
          max_wh:vec2i|None = None
          )->list[vec2i]|None:
    '''
    A* 寻路算法实现。

    参数：
    start (vec2i): 网格中的起始位置。
    goal (vec2i): 网格中的目标位置。
    terrain_cost_fn (Callable[[vec2i, Any], float]): 启发函数之一, 计算当前位置地形成本的函数。（这里可以人为的设置一些崎岖的地形，返回值越大意味着通过此处越是艰难）
        - now_pos (vec2i): 当前的位置。
        - context (Any): 地形成本函数的附加上下文。
    obstacle_penalty_fn (Callable[[vec2i, Any], float]): 启发函数之一, 计算当前位置障碍惩罚的函数。（在这里设置所有的障碍物，返回一个极大的值来表示此处有障碍）
        - now_pos (vec2i): 当前的位置。
        - context (Any): 障碍惩罚函数的附加上下文。
    deviation_penalty_fn (Callable[[vec2i, vec2i, vec2i, Any], float]): 启发函数之一, 计算偏离惩罚的函数。（在这里让路径的覆盖范围不要太大，离期望的最优路径越远，则惩罚越大）
        - now_pos (vec2i): 当前的位置。
        - start_pos (vec2i): 起始位置。
        - goal_pos (vec2i): 目标位置。
        - context (Any): 偏离惩罚函数的附加上下文。
    context_for_terrain_cost_fn (Any): 传递给地形成本函数的附加上下文。
    context_for_obstacle_penalty_fn (Any): 传递给障碍惩罚函数的附加上下文。
    context_for_deviation_penalty_fn (Any): 传递给偏离惩罚函数的附加上下文。

    返回值：
    从起点到目标点的路径，作为位置列表返回；如果未找到路径，则返回 None。
    '''
    terrain_cost_fn = terrain_cost_fn or (lambda now_pos, context: 1)
    obstacle_penalty_fn = obstacle_penalty_fn or (lambda now_pos, context: 0)
    deviation_penalty_fn = deviation_penalty_fn or BASE_DEVIATION_PENALTY_FN 
    assert isinstance(start, vec2i) and isinstance(goal, vec2i)
    
    if start == goal:
        return [start]


    
    frontier:PriorityQueue[tuple[float,vec2i]] = PriorityQueue()  # 存储待访问的node  {cost: pos}
    
    start_point_cost = \
        terrain_cost_fn(start, context_for_terrain_cost_fn) + \
        obstacle_penalty_fn(start, context_for_obstacle_penalty_fn) + \
        deviation_penalty_fn(start, start, goal, context_for_deviation_penalty_fn)
    
    
    frontier.put((start_point_cost, (vec2(start-goal) + vec2(0,0.001)).length(), frontier.curr_id, start)) 
    path: dict[vec2i, vec2i|None] = {}  # {next_pos: pos}
    path[start] = None
    
    terrain_cost_map: dict[vec2i, float] = {}  # 抵达某格的所有路径的地形开销之和
    terrain_cost_map[start] = start_point_cost
    #---
    maze:array2d = list(context_for_obstacle_penalty_fn.items())[0][1].copy()
    count = 0
    #---

    while not frontier.is_empty():

        current_cost, _, _, current_pos = frontier.pop()
        
        if current_pos == goal:
            break
        
        for neighbor_delta in DIRS_4:
            next_pos = current_pos + neighbor_delta
            t_cost = terrain_cost_map[current_pos] + terrain_cost_fn(next_pos, context_for_terrain_cost_fn) + obstacle_penalty_fn(next_pos, context_for_obstacle_penalty_fn)
            if next_pos not in terrain_cost_map or t_cost < terrain_cost_map[next_pos]:
                terrain_cost_map[next_pos] = t_cost
                cost = \
                    t_cost + \
                    deviation_penalty_fn(next_pos, start, goal, context_for_deviation_penalty_fn)
                frontier.put((cost, (vec2(next_pos - goal) + vec2(0,0.01)).length(), frontier.curr_id, next_pos))
                #----
                if maze.is_valid(current_pos):
                    try:
                        # maze[next_pos] = math.log10(cost)
                        maze[next_pos] = int(cost) % 99+1
                    except:
                        pass
                    if count % max(int(maze.width*maze.height*0.01), 1) == 0:
                        print(start, goal, len(terrain_cost_map))
                        print(cost, deviation_penalty_fn(next_pos, start, goal, context_for_deviation_penalty_fn))
                        print_grid(maze)
                count += 1
                #----
                path[next_pos] = current_pos
    if path.get(goal):
        correct_path = [goal]
        parent = goal
        while path.get(parent):
            parent = path[parent]
            correct_path.append(parent)
        return correct_path[::-1]
    else:
        print(path)
        return None



def base_astar_in_grid(grid:array2d[bool], start:vec2i, goal:vec2i, search_intensity:float=2)->list[vec2i]|None:
    def _assert_bool(x):
        assert isinstance(x, bool)  # 确保输入的grid元素都是bool类型
    
    start = vec2i(int(start.x), int(start.y))
    goal = vec2i(int(goal.x), int(goal.y))
    assert grid.is_valid(start) and grid.is_valid(goal)
    grid.map(_assert_bool)

    longest_path_length = grid.width * grid.height
    t_cost = 1
    
    def terrain_cost_fn(now_pos:vec2i, context:Any)->float:
        return t_cost
        
    def obstacle_penalty_fn(now_pos:vec2i, context:Any)->float:
        return 0 if context['grid'].is_valid(now_pos) and context['grid'][now_pos] != True else longest_path_length
    
    def deviation_penalty_fn(now_pos:vec2i, start_pos:vec2i, goal_pos:vec2i, context:Any)->float:
        return search_intensity*t_cost*BASE_DEVIATION_PENALTY_FN(now_pos, start_pos, goal_pos, context)
    
    return astar(start, goal, terrain_cost_fn, obstacle_penalty_fn, deviation_penalty_fn, context_for_terrain_cost_fn={'grid':grid}, context_for_obstacle_penalty_fn={'grid':grid}, context_for_deviation_penalty_fn={"grid":grid})