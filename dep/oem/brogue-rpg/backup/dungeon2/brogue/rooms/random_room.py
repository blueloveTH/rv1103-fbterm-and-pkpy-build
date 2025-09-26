from typing import Callable
from dungeon.brogue.const import RoomProfile
from ...schema import *
from ._cavern_rooms_body import *
from ._simple_rooms_body import *
from .utils import *
from array2d import array2d
import random
from .utils import brogue_chooseRandomDoorSites, brogue_attachHallwayTo
from ._simple_rooms_body import (
    brogue_designChunkyRoom,
    brogue_designCircularRoom,
    brogue_designCrossRoom,
    brogue_designEntranceRoom,
    brogue_designSmallRoom,
    brogue_designSymmetricalCrossRoom
)
from ._cavern_rooms_body import (
    brogue_design_cave,
    brogue_design_compat_cavern,
    brogue_design_large_east_west_cavern,
    brogue_design_large_north_south_cavern
)

"""
所有的房间主体形状的生成算法分布在 .cavern.py 和 .simple.py 中
与房间生成相关的算法在 .utils.py 中
"""


# 所有房间生成算法的调用者, 将根据房间生成权重数组从所有房间中随机选择一个生成, 并生成走廊并返回走廊出口----------------------------
def _make_random_room_body(
    grid_width, grid_height, room_type_freq=None, cave_min_width=50, cave_min_height=20
) -> tuple[RoomType, array2d[int]]:
    """
    在空的grid中就地生成一个随机的房间S

    Args:
        grid_width: 用于生成房间的网格的尺寸
        grid_height: 用于生成房间的网格的尺寸
        room_type_freq (list[float, ROOM_TYPE_COUNT]): 一个长度为ROOM_TYPE_COUNT的列表, 表示每种房间的生成概率权重, 每个权重的值大于等于0即可
        cave_min_width (int): 洞穴房间的最小宽度
        cave_min_height (int): 洞穴房间的最小高度
    """
    room_grid = array2d(grid_width, grid_height, default=0)
    room_type_freq = room_type_freq or (1, 1, 1, 1, 1, 1, 1, 1)
    room_type_list = [
        (RoomType.CROSS_ROOM, "brogue_designCrossRoom"),
        (RoomType.SMALL_SYMMETRICAL_CROSS_ROOM, "brogue_designSymmetricalCrossRoom"),
        (RoomType.SMALL_ROOM, "brogue_designSmallRoom"),
        (RoomType.CIRCULAR_ROOM, "brogue_designCircularRoom"),
        (RoomType.CHUNKY_ROOM, "brogue_designChunkyRoom"),
        (RoomType.MASSIVE_CAVERN, [
            "brogue_design_compat_cavern",
            "brogue_design_large_north_south_cavern",
            "brogue_design_large_east_west_cavern"
        ]),
        (RoomType.CAVE, "brogue_design_cave"),
        (RoomType.ENTRANCE_ROOM, "brogue_designEntranceRoom")
    ]
    # 按权重选取房间生成函数
    
    selected_room: tuple[RoomType, str|list] = random.choices(room_type_list, [room_type_freq[room_type] for room_type, _ in room_type_list])[0]  
    # 选中了cavern, 那么进一步选择生成什么cavern
    if isinstance(selected_room[1], list):
        room_type, design_func = selected_room[0], random.choice(selected_room[1])
    else:
        room_type, design_func = selected_room

    # 生成房间
    if design_func == "brogue_designCrossRoom":
        brogue_designCrossRoom(room_grid)
    elif design_func == "brogue_designSymmetricalCrossRoom":
        brogue_designSymmetricalCrossRoom(room_grid)
    elif design_func == "brogue_designSmallRoom":
        brogue_designSmallRoom(room_grid)
    elif design_func == "brogue_designCircularRoom":
        brogue_designCircularRoom(room_grid)
    elif design_func == "brogue_designChunkyRoom":
        brogue_designChunkyRoom(room_grid)
    elif design_func == "brogue_design_cave":
        brogue_design_cave(room_grid, cave_min_width, cave_min_height)
    elif design_func == "brogue_designEntranceRoom":
        brogue_designEntranceRoom(room_grid)
    elif design_func == "brogue_design_compat_cavern":
        brogue_design_compat_cavern(room_grid)
    elif design_func == "brogue_design_large_north_south_cavern":
        brogue_design_large_north_south_cavern(room_grid)
    elif design_func == "brogue_design_large_east_west_cavern":
        brogue_design_large_east_west_cavern(room_grid)
    else:
        assert False

    return room_type, room_grid


def _make_random_room(config:DungeonConfig, has_doors, allow_hallway, room_type_freq)-> tuple[ RoomType, array2d[int],  tuple[tuple[vec2i, vec2i | None]] ]:

    
    room_type, room_grid = _make_random_room_body(
        config.dungeon_width,
        config.dungeon_height,
        room_type_freq,
        config.cavern_min_width,
        config.cavern_min_height
    )

    door_positions = []
    for dir in DIRS_4:
        door_positions.append((dir, None))
    door_positions = tuple(door_positions)

    if has_doors:
        door_positions = brogue_chooseRandomDoorSites(room_grid, config.t_values)
        if allow_hallway:
            
            # 尝试生成走廊
            new_door_positions = brogue_attachHallwayTo(
                room_grid,
                config.t_values,
                door_positions,
                config.horizontal_corridor_min_length,
                config.horizontal_corridor_max_length,
                config.vertical_corridor_min_length,
                config.vertical_corridor_max_length)
            
            # 如果发现房间的确不适合生成走廊, 那么还是采用无走廊的方案
            if new_door_positions is not None:
                door_positions = new_door_positions
                
        assert not all([p is None for _, p in door_positions])  # 此时无论是否有走廊, 应当都会有至少一扇门
    else:
        door_positions = []
        for dir in DIRS_4:
            door_positions.append((dir, None))
        door_positions = tuple(door_positions)
    
    return room_type, room_grid, door_positions

################ 具体生成不同类型的房间的实现 ##################
def make_first_room_randomly(config:DungeonConfig)-> tuple[RoomType, array2d[int],  tuple[tuple[vec2i, vec2i | None]] ]:
    return _make_random_room(config, False, False, config.first_room_cfg.room_type_freq)

def make_basic_room_randomly(config:DungeonConfig, has_doors, allow_hallway)-> tuple[RoomType, array2d[int],  tuple[tuple[vec2i, vec2i | None]] ]:
    return _make_random_room(config, has_doors, False, config.basic_room_cfg.room_type_freq)