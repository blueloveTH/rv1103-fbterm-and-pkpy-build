from dungeon3 import *
from dungeon3.astar import *
from dungeon3.utils import *
from vmath import *
from dungeon3.test_tools import *
import math

def to_array2d(list2d):
    a = array2d(len(list2d[0]), len(list2d))
    for y, row in enumerate(list2d):
        for x, val in enumerate(row):
            a[x, y] = val
    return a


maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

maze = to_array2d(maze)
print_grid(maze)

start = vec2i(1, 1)
end = vec2i(9, 9)

path = astar(start, end, 
                    terrain_cost_fn=lambda pos, context: 1, 
                    obstacle_penalty_fn=lambda pos, context: context["maze"][pos]*999,
                    deviation_penalty_fn=None,
                    context_for_terrain_cost_fn=None,
                    context_for_obstacle_penalty_fn={'maze':maze},
                    context_for_deviation_penalty_fn=None
                    )

m1 = maze.copy()
for v in path:
    m1[v] += 2

print_grid(m1)





def projection_height(point, center, radius):
    # 提取坐标
    x, y = point.x, point.y
    cx, cy = center.x, center.y
    
    # 计算点到球心的水平距离
    horizontal_distance = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    
    # 检查点是否在球的范围内
    if horizontal_distance > radius:
        return 1
    
    # 计算投影高度
    height = math.sqrt(radius ** 2 - horizontal_distance ** 2) * 0.2
    
    return max(height, 1)


maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

maze = to_array2d(maze)
print_grid(maze)

start = vec2i(1, 1)
end = vec2i(9, 9)

path = astar(start, end, 
                    terrain_cost_fn=lambda pos, context: projection_height(pos, vec2i(5,0), 3), 
                    obstacle_penalty_fn=lambda pos, context: context["maze"][pos]*999,
                    deviation_penalty_fn=None,
                    context_for_terrain_cost_fn=None,
                    context_for_obstacle_penalty_fn={'maze':maze},
                    context_for_deviation_penalty_fn=None
                    )

m2 = maze.copy()
for v in path:
    m2[v] += 2


maze = array2d(30, 30, default = 0)
# for i in range(20):
#     maze[i+5, 15] = 1

start = vec2i(3,3)
end = vec2i(27,27)


path = astar(start, end, 
                    terrain_cost_fn=lambda pos, context: projection_height(pos, vec2i(10,7), 10) + projection_height(pos, vec2i(21,21), 5), 
                    obstacle_penalty_fn=lambda pos, context: context["maze"][pos]*999 + 999*int(pos.x==0 or pos.y==0 or pos.x==context["maze"].width-1 or pos.y==context["maze"].height-1),
                    deviation_penalty_fn=lambda pos, start, goal, context: point_to_line_distance(vec2(pos), vec2(start), vec2(goal)) + vec2(pos-goal).length(),
                    context_for_terrain_cost_fn=None,
                    context_for_obstacle_penalty_fn={'maze':maze},
                    context_for_deviation_penalty_fn=None
                    )

m3 = maze.copy()
for v in path:
    m3[v] += 2


path = base_astar_in_grid(maze.map(lambda x: {1:True, 0:False}[x]), start, end)

m4 = maze.copy()
for v in path:
    m4[v] += 2


print_grid(m1)
print_grid(m2)
print_grid(m3)
print_grid(m4)