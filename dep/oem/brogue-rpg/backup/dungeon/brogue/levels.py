"""
生成整层
"""

from array2d import array2d
import random

from vmath import vec2, vec2i

from dungeon.algorithm import grid
from dungeon.brogue.const import ONE,TWO,THREE,FOUR,FIVE,SIX,SEVEN,EIGHT,NINE,ZERO,LevelProfile
from dungeon.brogue import rooms as Rooms
from dungeon.algorithm.grid import count_connected_components, iter_unordered
from dungeon.brogue.doors import DoorTester
from dungeon import test_tools


Door = tuple[vec2i, bool]  # [坐标, 方向]    方向: true水平, false垂直


def try_map_room_to_grid_(grid: array2d[int], room_grid: array2d[int], delta_x: int, delta_y: int) -> bool:
    """尝试将`room_grid`中的格子映射到`grid`中

    设`(x, y)`是房间格子在`room_grid`中的位置, 那么它被映射到`grid`中的位置是`(x+delta_x, y+delta_y)`

    如果满足条件，且映射后不与其他房间重叠，并距离边界大于一格的距离，则返回`True`，否则返回`False`
    """
    modified_grid = grid.copy()
    # 预先求出 grid 中每个格子周围的 ZERO 的数量
    grid_zero_neighbors = grid.count_neighbors(ZERO, "Moore")

    # 用底层算法求一下外接矩形，减少 python 层面循环的次数
    rect = room_grid.get_bounding_rect(ONE)
    assert rect is not None
    x_, y_, w_, h_ = rect
    for room_y in range(y_, y_ + h_):
        for room_x in range(x_, x_ + w_):
            # 我们只需要挑出属于房间的格子并进行判断, 以保证房间在被移动到 grid 时是完整的并距离边界保持一格的距离
            if room_grid[room_x, room_y] != ONE:
                continue
            # 偏移后的房间格子在 grid 中的位置
            grid_x = room_x + delta_x
            grid_y = room_y + delta_y
            if grid.get(grid_x, grid_y) != ZERO:
                # 房间格子在 grid 中的位置被占用或不合法
                return False
            if grid_zero_neighbors[grid_x, grid_y] < 8:
                # 房间格子在距离边界小于一格
                return False

            modified_grid[grid_x, grid_y] = ONE

    # 房间在 grid 中的位置是合法的
    grid.copy_(modified_grid)
    return True


def brogue_attachRooms(
    grid: array2d[int],
    level_profile: LevelProfile,
    corridor_chance,
    room_frequencies,
    max_attempts: int,
    max_rooms: int)->list[Door]:
    '''
    不断生成房间并连接至地图, 直至达到目标, 最终返回所有门的位置
    '''
    
    
    attempts = 0  # 已经尝试的次数
    rooms = 0  # 已经生成的房间数量

    unordered_xy = []
    doors_list:list[Door] = []
    # 不断尝试生成房间, 直到达到房间数量上限或尝试次数上限
    while attempts < max_attempts and rooms < max_rooms:
        # 生成一个房间并暂存在 roomMap 中
        room_grid = array2d(grid.width, grid.height, default=0)
        # 确定是否需要生成走廊
        has_hallway = attempts <= max_attempts - 5 and random.random() < corridor_chance
        #    door_positions 是一个 list[list[int,2], 4], 其中每个元素是 [x,y], 表示朝一个方向上打开的门的位置, 门打开的方向取决于[x,y]在 door_positions 中的位置
        door_positions = Rooms.brogue_designRandomRoom(
            room_grid, level_profile, room_frequencies, has_hallway=has_hallway, has_doors=True  # ?
        )

        # 确保房间只有一个连通分量
        assert count_connected_components(room_grid, ONE) == 1

        # 将房间在地图上滑动，直到与墙壁对齐
        # 无序遍历grid, 此处的(x,y)指的是两个房间相互接壤的门的位置
        opposite_map = {0: 1, 1: 0, 2: 3, 3: 2}
        door_tester = DoorTester(grid)
        
        for x, y in iter_unordered(room_grid, unordered_xy):
            direction_index = door_tester.test(x, y)
            if direction_index == -1:
                continue

            opposite_direction_index = opposite_map[direction_index]
            opposite_door_position = door_positions[opposite_direction_index]
            if opposite_door_position is None:
                # 确保门可以双向打开
                continue

            # opposite_door_position 与 (x, y) 最终映射为同一个点，即门的位置
            delta_x = x - opposite_door_position[0]
            delta_y = y - opposite_door_position[1]
            # 尝试插入房间
            if not try_map_room_to_grid_(grid, room_grid, delta_x, delta_y):
                continue

            # 并将位置(x,y)标记为房间的门, 使用2表示门
            # grid[x, y] = TWO
            
            # 这里替换为记录门的位置, 而不是直接在地图中标记门
            door: Door = (vec2i(x, y), bool(direction_index in [2, 3]))
            doors_list.append(door)
            grid[x, y] = ONE
            
            rooms += 1
            # 已经经被放置了房间, 那么就不想需要继续搜索适合放置该房间的位置了
            break

        test_tools.print_grid_debug(grid)

        # 总尝试次数+1
        attempts += 1
        
    return doors_list





def brogue_carveDungeon(level_profile: LevelProfile) -> tuple[array2d[int], list[Door]]:
    grid = array2d[int](
        level_profile.dungeon_width, level_profile.dungeon_height, default=None
    )

    # 生成第一个房间
    Rooms.brogue_designRandomRoom(
        grid,
        level_profile,
        level_profile.first_room_profile.room_frequencies,
        has_doors=False,
        has_hallway=False,
    )

    test_tools.print_grid_debug(grid)

    # 接着不断生成其余的房间
    doors_list = brogue_attachRooms(
        grid,
        level_profile,
        level_profile.basic_room_profile.corridor_chance,
        level_profile.basic_room_profile.room_frequencies,
        level_profile.attach_rooms_attempt_count,
        level_profile.attach_rooms_max_count,
    )

    if level_profile.finish_walls:
        grid = grid.copy()
        # 给grid进行描边，描边数值为6
        neighbors = grid.count_neighbors(1, "Moore")
        for i in range(grid.width):
            for j in range(grid.height):
                if grid[i, j] == 0 and neighbors[i, j] > 0:
                    grid[i, j] = 6

    return grid, doors_list


