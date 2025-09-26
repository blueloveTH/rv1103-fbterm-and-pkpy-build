from enum import Enum

from typing import Literal

from array2d import array2d
from dataclasses import dataclass
from vmath import vec2i



# 方向定义
DIR_UP = vec2i(0, -1)            # 上
DIR_DOWN = vec2i(0, 1)          # 下
DIR_LEFT = vec2i(-1, 0)         # 左
DIR_RIGHT = vec2i(1, 0)         # 右
DIR_UPPER_RIGHT = vec2i(1, -1)  # 右上
DIR_UPPER_LEFT = vec2i(-1, -1)  # 左上
DIR_LOWER_RIGHT = vec2i(1, 1)   # 右下
DIR_LOWER_LEFT = vec2i(-1, 1)   # 左下


# 四个主要方向
DIRS_4:tuple[vec2i, vec2i, vec2i, vec2i] = (DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT)
OPPO_DIR_4:tuple[vec2i, vec2i, vec2i, vec2i] = (DIR_DOWN, DIR_UP, DIR_RIGHT, DIR_LEFT)

@dataclass
class TerrainValues:
    # 默认0是"虚空"
    BLANK: int
    WALL: int


def if_terrian_in_room(terrian_value: int, t_values: TerrainValues) -> bool:
    if terrian_value == t_values.BLANK:
        return True # 目前只有 BLANK 地形算作房间内部的地形, 这里的 BLANK 在本包内被视作是可通行区域, 具体值由外部调用者传入
    
    return False
    

class RoomType(Enum):
    UNKNOWN = -1
    CROSS_ROOM = 0                       # 十字房间 (Cross room)
    SMALL_SYMMETRICAL_CROSS_ROOM = 1     # 小型对称十字房间 (Small symmetrical cross room)
    SMALL_ROOM = 2                       # 小房间 (Small room)
    CIRCULAR_ROOM = 3                    # 圆形房间 (Circular room)
    CHUNKY_ROOM = 4            # 不规则块状房间 (Chunky room)
    CAVE = 5                             # 洞穴 (各种Cave)
    MASSIVE_CAVERN = 6                   # 巨大洞穴 (填满整个地下层的那种大洞穴，Cavern)
    ENTRANCE_ROOM = 7                    # 入口房间 (位于第一层的大倒 “T” 形房间，Entrance room)


@dataclass
class RoomsConfig:
    room_type_freq: dict["RoomType", int]
    corridor_chance: float

    @staticmethod
    def create_default_basic_room_config():
        return RoomsConfig(
            room_type_freq={
                RoomType.CROSS_ROOM: 2,
                RoomType.SMALL_SYMMETRICAL_CROSS_ROOM: 1,
                RoomType.SMALL_ROOM: 1,
                RoomType.CIRCULAR_ROOM: 1,
                RoomType.CHUNKY_ROOM: 7,
                RoomType.CAVE: 1,
                RoomType.MASSIVE_CAVERN: 0,
                RoomType.ENTRANCE_ROOM: 0
            },
            corridor_chance=1
        )

    @staticmethod
    def create_default_first_room_config():
        return RoomsConfig(
            room_type_freq={
                RoomType.CROSS_ROOM: 10,
                RoomType.SMALL_SYMMETRICAL_CROSS_ROOM: 0,
                RoomType.SMALL_ROOM: 0,
                RoomType.CIRCULAR_ROOM: 3,
                RoomType.CHUNKY_ROOM: 7,
                RoomType.CAVE: 10,
                RoomType.MASSIVE_CAVERN: 10,
                RoomType.ENTRANCE_ROOM: 0
            },
            corridor_chance=0
        )

@dataclass
class DungeonConfig:
    t_values: "TerrainValues"
    basic_room_cfg: RoomsConfig
    first_room_cfg: RoomsConfig
    dungeon_width: int = 79
    dungeon_height: int = 29
    horizontal_corridor_min_length: int = 5
    horizontal_corridor_max_length: int = 15
    vertical_corridor_min_length: int = 2
    vertical_corridor_max_length: int = 9
    room_type_count: int = 8
    cavern_min_width: int = 50
    cavern_min_height: int = 20
    attach_rooms_attempt_count: int = 35
    attach_rooms_max_count: int = 35
    finish_walls: bool = True

    @staticmethod
    def create_default(t_values: TerrainValues):
        return DungeonConfig(
            t_values=t_values,
            basic_room_cfg=RoomsConfig.create_default_basic_room_config(),
            first_room_cfg=RoomsConfig.create_default_first_room_config()
        )

@dataclass
class Door:
    pos: vec2i

@dataclass
class Monster:
    pos: vec2i

@dataclass
class IO:
    config: DungeonConfig
    m_terrian: array2d[int]
    m_room_id: array2d[int]
    room_type_map: dict[int, RoomType]
    m_doors: list[Door]
    m_monsters: list[Monster]

    @staticmethod
    def create_default(t_values: TerrainValues):
        config=DungeonConfig.create_default(t_values)
        
        io = IO(
            config=config,
            m_terrian=array2d(config.dungeon_width, config.dungeon_height, default=0),
            m_room_id=array2d(config.dungeon_width, config.dungeon_height, default=0),
            room_type_map={},
            m_doors=[],
            m_monsters=[]
        )
        return io