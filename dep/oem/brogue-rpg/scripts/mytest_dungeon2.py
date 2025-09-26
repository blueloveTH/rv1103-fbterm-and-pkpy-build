from dungeon2.test_tools import print_grid
from dungeon2.levels import brogue_carveDungeon
from dungeon2.schema import IO, DungeonConfig, TerrainValues
import json

io = IO.create_default(TerrainValues(BLANK=1, WALL=6))
brogue_carveDungeon(io)
print_grid(io.m_room_id)

for k, v in io.room_type_map.items():
    print(k, v.name, end=", ")
print()

print_grid(io.m_terrian)
print(io)
