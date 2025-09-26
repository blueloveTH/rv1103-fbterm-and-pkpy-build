"""
生成整层
"""

from dungeon.test_tools import print_grid
from dungeon2.brogue.rooms.utils import DoorTester, try_map_room_to_
from dungeon2.schema import DIRS_4, IO, OPPO_DIR_4, Door, RoomType, if_terrian_in_room
from array2d import array2d
import random

from vmath import vec2, vec2i

from dungeon2.algorithm.canvas import trim
from dungeon2.brogue.rooms.random_room import make_first_room_randomly, make_basic_room_randomly
from dungeon2.algorithm.grid import count_connected_components, iter_unordered
from dungeon2 import test_tools
from dungeon2.schema import TerrainValues


def register_room(io: IO, room_grid: array2d[int], room_type: RoomType, door_pos_next_to_insert_point:vec2i, delta:vec2i):
    """
    注册房间并更新相关地图数据。

    :param io: 包含地图、房间数据和配置的对象。
    :param room_grid: 当前房间的网格对象。
    :param room_type: 要注册的房间类型。
    :param door_pos_next_to_insert_point: 插入点旁边的其他房间的门坐标
    """
    # 注册 room_id
    if not io.room_type_map:
        room_id = 1
    else:
        room_id = max(io.room_type_map.keys()) + 1
    io.room_type_map[room_id] = room_type

    # 拷贝房间网格并应用 room_id
    room_id_grid = room_grid.copy()
    room_id_grid.apply_(
        lambda val: room_id if if_terrian_in_room(val, io.config.t_values) else val
    )

    # 更新地图的房间 ID
    try_map_room_to_(io.m_room_id, lambda x: x == room_id, room_id_grid, delta)

    # 记录门的位置
    if door_pos_next_to_insert_point is not None:
        io.m_doors.append(Door(door_pos_next_to_insert_point))

        # 设置门的地形
        io.m_terrian[door_pos_next_to_insert_point] = io.config.t_values.BLANK
        io.m_room_id[door_pos_next_to_insert_point] = room_id
        
    

def attach_basic_rooms_loop(io: IO):
    '''
    不断生成房间并连接至地图, 直至达到目标, 最终返回所有门的位置
    '''
    
    
    attempts = 0  # 已经尝试的次数
    unordered_xy = []
    # 不断尝试生成房间, 直到达到房间数量上限或尝试次数上限
    while attempts < io.config.attach_rooms_attempt_count and len(io.room_type_map.keys()) < io.config.attach_rooms_max_count:
        # 确定是否需要生成走廊
        at_least_n_rooms_without_hallway = io.config.attach_rooms_max_count * 0.5
        allow_hallway = attempts <= io.config.attach_rooms_attempt_count - at_least_n_rooms_without_hallway and random.random() < io.config.basic_room_cfg.corridor_chance
        
        # 生成房间
        room_type, room_grid, door_positions = make_basic_room_randomly(io.config, True, allow_hallway)
        
        if all([p is None for _, p in door_positions]):
            
            attempts += 1
            continue
        
        # 确保房间只有一个连通分量
        assert count_connected_components(room_grid.map(lambda x: io.config.t_values.BLANK if if_terrian_in_room(x, io.config.t_values) else x), io.config.t_values.BLANK) == 1

        # 将房间在地图上滑动，直到与墙壁对齐
        # 无序遍历grid, 此处的(x,y)指的是两个房间相互接壤的门的位置
        door_tester = DoorTester(io.config.t_values, io.m_terrian, io.m_doors)
        unordered_xy_copy = iter_unordered(room_grid, cache=unordered_xy)
        
        
        
            
        for door_x, door_y in unordered_xy_copy:

            direction_index = door_tester.test(vec2i(door_x, door_y))
            if direction_index == -1:
                continue

            _, opposite_door_position = door_positions[list(DIRS_4).index(OPPO_DIR_4[direction_index])]
            if opposite_door_position is None:
                # 确保门可以双向打开
                continue

            # 插入点是门的对面 
            delta = vec2i(door_x, door_y) - opposite_door_position
            # 尝试插入房间
            is_success = try_map_room_to_(io.m_terrian, lambda x: if_terrian_in_room(x, io.config.t_values), room_grid, delta)
            if not is_success:
                # (x, y) 不适合插入该房间, 赶紧检测下一个位置
                continue
            else:
                register_room(io, room_grid, room_type, vec2i(door_x, door_y), delta)
                
                # 已经被放置了房间, 那么就不需要继续搜索适合放置该房间的位置了
                
                break
            
            

        

        # 总尝试次数+1
        attempts += 1




def brogue_carveDungeon(io: IO):
    
    room_type, first_room_terrian, first_room_doors = make_first_room_randomly(io.config)
    io.m_terrian = first_room_terrian
    register_room(io, first_room_terrian, room_type, None, vec2i(0,0))
    
    

    # 接着不断生成其余的房间
    # TODO 10/17
    attach_basic_rooms_loop(io)

    if io.config.finish_walls:
        # 给grid进行描边，描边数值为6
        grid = io.m_terrian
        neighbors = grid.count_neighbors(1, "Moore")
        for i in range(grid.width):
            for j in range(grid.height):
                if grid[i, j] == 0 and neighbors[i, j] > 0:
                    grid[i, j] = 6



