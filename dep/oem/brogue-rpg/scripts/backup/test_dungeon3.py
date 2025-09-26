from dungeon3 import *
from vmath import vec2, vec2i
from array2d import array2d
from dungeon3.regions import dfs
from dungeon3.room_builders.terrianer import SquareRoomTerrainer
from dungeon3.test_tools import *
from dungeon3.schema import *
from dungeon3.regions import dfs
from dungeon3.builders import *
from dungeon3.grow import *
    


# class TestRegionBuilder(RoomBuilder):
    
#     def __init__(self, direction:vec2, distance_ratio:float, side_length:int):
#         super().__init__(
#             LinearRoomPlacer(direction, distance_ratio),   # 沿着一条射线放置房间
#             SquareRegionTerrianBuilder(side_length)  # 房间的形状是正方形
#             )
    
    

# if __name__ == "__main__":
#     config = DungeonConfig()

#     import random
#     rnd = random.Random()
#     io = DungeonIO(config, TerrainValues(BLANK=1, WALL=6), rnd)
#     io.config.first_room_freq = { TestRegionBuilder(vec2(1,1), 1.1, rnd.randint(3,10)): 1 }
#     io.config.room_freq = { 
#                         TestRegionBuilder(vec2(1,1),2, rnd.randint(5,10)): 1,
#                         TestRegionBuilder(vec2(1,-1),2, rnd.randint(5,10)): 1,
#                         TestRegionBuilder(vec2(1,0),1.5, rnd.randint(15,20)): 1
#                         }

#     region = io.first_grow()
#     for _ in range(4):
#         ctx = BuildContext(region)
#         region = io.grow(ctx)

#     path = set()
#     dfs(io.root, path)
#     print(path)
#     print_all_regions_terrian(io)



class TestRegionBuilder(RoomBuilder):
    
    def __init__(self, direction:vec2, distance_ratio:float, side_length:int):
        super().__init__(
            LinearRoomPlacer(direction, distance_ratio),   # 沿着一条射线放置房间
            SquareRoomTerrainer(side_length)  # 房间的形状是正方形
            )

class TestCorridorBuilder(CorridorBuilder):

    def __init__(self):
        super().__init__(AncientAstarTerrianBuilder())
    



if __name__ == "__main__":
    config = DungeonConfig()

    import random
    rnd = random.Random()
    io = DungeonIO(config, TerrainValues(BLANK=1, WALL=6), rnd)
    io.config.first_room_freq = { TestRegionBuilder(vec2(1,1), 1.1, rnd.randint(3,10)): 1 }
    io.config.room_freq = { 
                        TestRegionBuilder(vec2(1.5,1),1.5, rnd.randint(5,10)): 1,
                        TestRegionBuilder(vec2(1,-1.5),1.5, rnd.randint(5,10)): 1,
                        TestRegionBuilder(vec2(1,0),1.5, rnd.randint(5,10)): 1,
                        TestRegionBuilder(vec2(-1.5,1),1.5, rnd.randint(5,10)): 1,
                        TestRegionBuilder(vec2(-1,-1.5),1.5, rnd.randint(5,10)): 1,
                        TestRegionBuilder(vec2(-1,0),1.5, rnd.randint(5,10)): 1,
                        TestRegionBuilder(vec2(0,1),1.5, rnd.randint(5,10)): 1,
                        TestRegionBuilder(vec2(0,-1),1.5, rnd.randint(5,10)): 1,
                        }
    io.config.corridor_freq = { TestCorridorBuilder(): 1 }

    first_room = io.first_grow()
    ctx = BuildContext()
    ctx.region = first_room
    for _ in range(4):
        print_all_regions_terrain(io)
        ctx.grow_strategy = TwoHopsGrowStrategy()
        io.grow(ctx)
        print(ctx._new_room)
        ctx.region = ctx._new_room

    path = set()
    dfs(io.root, path)
    print(len(path))
    print_all_regions_terrain(io)