from array2d import array2d
import random

from vmath import vec2i

from ...schema import DIR_DOWN, DIR_UP, DIR_LEFT, DIR_RIGHT, DIRS_4, TerrainValues, Door, if_terrian_in_room

from typing import Callable, Literal

from dungeon2.test_tools import print_grid

'''
utils.py 包含了生成房间的小部分相关算法
'''



"""生成门的四种情况
上(0)   下(1)   左(2)   右(3)
? . ?   ? 1 ?   ? . ?   ? . ?
. √ .   . √ .   . √ 1   1 √ .
? 1 ?   ? . ?   ? . ?   ? . ?
"""
# 我倾向于让对侧的门满足某种数学关系，例如 (i+2)%4

class DoorTester:
    def __init__(self, t_values:TerrainValues, m_terrian:array2d[int], doors_list: list[Door]):
        self.grid_neighbors_ZERO = m_terrian.count_neighbors(0, 'von Neumann')
        self.grid_neighbors_BLANK = m_terrian.count_neighbors(t_values.BLANK, 'von Neumann')
        self.m_terrian = m_terrian
        self.t_values = t_values
        
        door_map = array2d(m_terrian.width, m_terrian.height,default=0)
        for door in doors_list:
            door_map[door.pos] = 1
        
        self.grid_neighbors_DOOR = door_map.count_neighbors(1, 'Moore')

        
    def test(self, pos:vec2i) -> Literal[-1, 0, 1, 2, 3]:
        # 目标点必须是 ZERO
        if self.m_terrian[pos] != 0:
            return -1
        # 目标点的 4-邻域中必须有且仅有一个 blank
        if self.grid_neighbors_BLANK[pos] != 1:
            return -1
        # 目标点的 4-邻域中必须有且仅有三个 ZERO
        if self.grid_neighbors_ZERO[pos] != 3:
            return -1
        # 目标点的 8-邻域中不能有 门
        if self.grid_neighbors_DOOR[pos] > 0:
            return -1
        
        if self.m_terrian[pos + DIR_DOWN] == self.t_values.BLANK:
            return 0
        if self.m_terrian[pos + DIR_UP] == self.t_values.BLANK:
            return 1
        if self.m_terrian[pos + DIR_RIGHT] == self.t_values.BLANK:
            return 2
        if self.m_terrian[pos + DIR_LEFT] == self.t_values.BLANK:
            return 3
        
        # 什么情况都没有, 说明有问题
        assert False



# 在本文件中, 完全复刻自brogue的算法将使用 "brogue_<brogue中该函数的原名>" 命名
def clamp(x, a, b):
    if a > b: a, b = b, a
    if x < a: return a
    if x > b: return b
    return x


def brogue_chooseRandomDoorSites(room_terrian: array2d[int], t_values: TerrainValues) -> tuple[tuple[vec2i, vec2i | None]]:
    '''
    对于上下左右四个方向, 在提供的房间grid中, 分别寻找1个能够满足"可以向本方向打开门"的格子的位置, 当某个方向找不到符合要求的格子时, 将使用`None`表示
    
    - 对于"可以向本方向打开门"的判断标准:
        - 1. 需要首先满足 DoorTester 中对格子的要求
        - 2. 其次需要保证向门打开的方向上延伸10格, 不能遇到房间格子
    '''
    door_tester = DoorTester(t_values, room_terrian, [])
    results: list[list[vec2i]] = [[] for _ in range(4)]
    
    for y in range(room_terrian.height):
        for x in range(room_terrian.width):
            # 首先判断本格是否满足"可以向本方向打开门"的判断标准的第一点
            direction_index = door_tester.test(vec2i(x, y))
            if direction_index == -1:  # no direction  表示本格无法满足条件
                continue

            # 下面的循环会判断是否满足标准的第二点
            direction_delta_x, direction_delta_y = DIRS_4[direction_index].x, DIRS_4[direction_index].y

            
            can_open = True
            for detect_length in range(1, 10+1):
                # 将门打开的方向(通过第一重判断得到的direction_index)作为探测方向依次延申10格
                detect_x = x + detect_length * direction_delta_x
                detect_y = y + detect_length * direction_delta_y
                # 忽略出界的探测点
                if not room_terrian.is_valid(detect_x, detect_y):
                    break
                # 如果发现探测途中遇到了房间格子, 则说明无法向该方向打开门
                if room_terrian[detect_x, detect_y] != 0:
                    can_open = False
                    break

            # 标记完全符合判断标准的位置为可以打开门的方向的标签
            if can_open:
                results[direction_index].append(vec2i(x, y))


    
    ret = []
    for d, r in zip(DIRS_4, results):
        if r:
            ret.append((d, random.choice(r)))
    
    assert not all([p is None for _, p in ret])  # 应该不可能出现没有生成任何门的情况
    return tuple(ret)


def brogue_attachHallwayTo(
    dungeon_terrian: array2d[int],
    t_values: TerrainValues,
    door_positions: tuple[tuple[vec2i, vec2i | None]],
    horizontal_corridor_min_length,
    horizontal_corridor_max_length,
    vertical_corridor_min_length,
    vertical_corridor_max_length
) -> tuple[tuple[vec2i, vec2i | None]] | None:
    """
    在grid上绘制走廊。并返回走廊的出口坐标, 大多数情况下出口坐标会是在走廊方向继续延伸一格的位置, 在小部分情况下(15%)会返回排除走廊延伸方向的对向方向外的其余3个方向上的坐标
    ```
    如算法选择了door_positions中表示向右打开的门,并生成了走廊:  #表示房间, +表示走廊, 实际上它们的存储值都是1,但这里使用不同的符号加以区分
        # #
        # # + + + + +
        # #
    此时算法将返回的位置绝大多数是:
        # #
        # # + + + + + @ <---- @表示出口,假设此处坐标是(3, 4), 而因为它向右侧延伸,因此返回值是[None, None, None, (3, 4)]
        # #
    有小部分情况下是:
        # #         @
        # # + + + + + @ <---- 返回值是[(2, 3), (2, 5), (3, 4), None]
        # #         @
    ```
    Args:
        grid (array2d[int]): 二维数组表示地图的网格，应当为地牢的总地图尺寸。
        door_positions: 4个方向的门的位置列表。
            一个包含4个二元列表的列表，每个二元列表分别表示朝向"上,下,左,右"打开的门的位置。
            当门的位置为 None 时表示没有朝向该方向打开的门。
    Returns:
        4个方向的走廊出口的位置列表。

    """

    # 选择一个合适的方向
    shuffled_door_positions = list(door_positions)
    random.shuffle(shuffled_door_positions)

    direction_index = None  # None表示没有找到合适的方向
    door_pos = None
    for _direction_index, _door_pos in shuffled_door_positions:
        # 首先排除没有门的方向的坐标
        if _door_pos is None:
            continue

        door_x, door_y = _door_pos.x, _door_pos.y 

        # 探测当前开门方向上将生成走廊的最远位置,是否超出了地图边界
        direction_delta_x, direction_delta_y = _direction_index.x, _direction_index.y
        detect_x = door_x + horizontal_corridor_max_length * direction_delta_x
        detect_y = door_y + vertical_corridor_max_length * direction_delta_y

        if dungeon_terrian.is_valid(detect_x, detect_y):
            # 该方向上可以生成走廊
            direction_index = _direction_index
            door_pos = _door_pos
            break

    # assert door_pos is not None
    
    # 四个方向的门都不符合条件,那么就返回吧
    if direction_index == None:
        return None
    
    # 生成垂直方向的走廊
    if direction_index in (DIR_UP, DIR_DOWN):  # 0,1表示"上,下"方向的direction_index
        corridor_length = random.randint(vertical_corridor_min_length, vertical_corridor_max_length)
    # 生成水平方向的走廊
    else:
        corridor_length = random.randint(horizontal_corridor_min_length, horizontal_corridor_max_length)

    # 绘制和房间相连的走廊, 走廊的地块使用1表示,和房间地块相同
    direction_delta_x, direction_delta_y = direction_index.x, direction_index.y

    
    start_x, start_y = door_pos.x, door_pos.y
    end_x = start_x + direction_delta_x*(corridor_length-1)
    end_y = start_y + direction_delta_y*(corridor_length-1)

    step_x = -1 if end_x < start_x else 1
    step_y = -1 if end_y < start_y else 1

    for x in range(start_x, end_x+step_x, step_x):
        for y in range(start_y, end_y+step_y, step_y):
            dungeon_terrian[x, y] = t_values.BLANK

    # 随机决定是否允许拐弯的走廊出口, 并更新走廊结束处的门位信息
    end_x = clamp(end_x, 0, dungeon_terrian.width-1)
    end_y = clamp(end_y, 0, dungeon_terrian.height-1)
    allow_oblique_hallway_exit = random.random() < 0.15  # 决定走廊出口是否允许拐弯
    
    if not allow_oblique_hallway_exit:
        # 单个出口
        delta = vec2i(direction_delta_x*1, direction_delta_y*1)
        conn_pos = vec2i(end_x, end_y) + delta
        new_door_positions = [(d, conn_pos if d == delta else None) for d in DIRS_4]
    else:
        # 多个出口
        exclude_delta = vec2i(-direction_delta_x*1, -direction_delta_y*1)
        new_door_positions = [(d, vec2i(end_x, end_y) + d if d != exclude_delta else None) for d in DIRS_4]

    assert not all([p is None for _, p in new_door_positions])  # 应当不可能出现没有门的情况
    return tuple(new_door_positions)  # type: ignore



def try_map_room_to_(grid: array2d[int], if_terrian_in_room:Callable[[int], bool], room_grid: array2d[int], delta:vec2i) -> bool:
    """尝试将`room_grid`中的格子映射到`grid`中

    设`(x, y)`是房间格子在`room_grid`中的位置, 那么它被映射到`grid`中的位置是`(x+delta_x, y+delta_y)`

    如果满足条件，且映射后不与其他房间重叠，并距离边界大于一格的距离，则返回`True`，否则返回`False`
    """
    
    f_ = lambda x: x != 0
    
    modified_grid = grid.copy()
    # 预先求出 grid 中每个格子周围的 ZERO 的数量
    grid_zero_neighbors = grid.count_neighbors(0, "Moore")

    # 用底层算法求一下外接矩形，减少 python 层面循环的次数
    room_flag_grid = room_grid.map(lambda x: if_terrian_in_room(x))
    x_, y_, w_, h_ = room_flag_grid.get_bounding_rect(True)
    for room_y in range(y_, y_ + h_):
        for room_x in range(x_, x_ + w_):
            # 我们只需要挑出属于房间的格子并进行判断, 以保证房间在被移动到 grid 时是完整的并距离边界保持一格的距离
            t = room_grid[room_x, room_y]
            if not if_terrian_in_room(room_grid[room_x, room_y]):
                continue
            # 偏移后的房间格子在 grid 中的位置
            grid_pos = vec2i(room_x, room_y) + delta
            if not grid.is_valid(grid_pos.x, grid_pos.y):
                return False
            if grid[grid_pos] != 0:
                # 房间格子在 grid 中的位置被占用或不合法
                return False
            if grid_zero_neighbors[grid_pos] < 8:
                # 房间格子在距离边界小于一格
                return False

            modified_grid[grid_pos] = t

    # 房间在 grid 中的位置是合法的
    grid.copy_(modified_grid)
    return True