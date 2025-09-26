from array2d import array2d
from vmath import vec2, vec2i
from .regions import _Region, Region, Corridor, Room, dfs
from .io import *
from .builders import *
from .utils import (
    add_outline_to_,
    calc_outerbound_rect,
    try_map_anchored_grid_to,
    try_map_grid_to_,
    random_by_freq
)
from .astar import astar, base_astar_in_grid
from .schema import Rect
from .test_tools import *

class GrowStrategy:
    def grow(self, io: DungeonIO, context: BuildContext) -> None:
        raise NotImplementedError


class TwoHopsGrowStrategy(GrowStrategy):
    """
    总结一下, 就是我需要修改io.grow为策略模式, 先实现两跳的grow策略。
    两跳grow采用走廊和房间交替的形式,
    走廊是指基于外部传入的若干其余房间地形边缘的粘合点来生成矩形区域和具体地形的region,
    房间是指让房间builder自由确定矩形区域和具体地形的region。
    在两跳grow策略中,  先生成下一个房间,
    再通过下一个房间和上一个房间构成的局部array2d来确认两个走廊粘合点,
    由于粘合点必须要在房间地形的边缘,
    我目前想到的是使用一次“以两个房间的中心点作为起点和终点的A*”所生成的路径与两房间各自的地形边缘的交点
    来确定。在确定走廊粘合点后, 就可以用走廊的builder来生成走廊了。
    回到房间的生成, 在房间builder生成了一个房间之后（包括地形和坐标）, grow需要判断该房间是否合法,
    具体来说就是需要考虑该房间是否与其他房间重叠, 利用矩形区域是否重叠进行初筛,  再对重叠的情况精确判断。
    同时grow还需要留出走廊的空间, 尽可能确保走廊builder可以生成走廊。由于走廊也是region,
    它也需要在地形外部留出一圈wall的空间,  因此无论是初筛还是精确判断的步骤,
    都需要每个房间各自向外扩2格来确保走廊可以从4格宽的缝隙中钻来钻去, 确保粘合点与粘合点之间必定可以生成走廊。
    """

    def grow(self, io: DungeonIO, context: BuildContext) -> None:
        is_blank_fn = lambda x: x == io.t_values.BLANK
        
        start_region = context.region  # 基于该节点生长

        # 第一跳是走廊,  第二跳一定是房间
        if isinstance(start_region, Corridor):
            start_rooms = start_region.extras.out_bound_neighbors
            # 由于可以保证(走廊, 房间)一定成对生成, 因此任意走廊的下一跳房间均在其上一步和走廊一起成对生成了
            pass

        # 第一跳是房间, 第二三跳可能是走廊+房间, 也可能是第二跳就生成房间
        elif isinstance(start_region, Room):
            # 情况1: 走廊+房间
            # ------- 生成房间 ------
            max_attemp_count = 10
            assert max_attemp_count > 0
            context._new_room = None
            global_path = None  # 如果通过走廊检测，那么暂存走廊检测所计算出的路径点, 并交给下一步用以计算走廊的起点和终点
            for attemped in range(max_attemp_count):

                # test1初筛 test2精确检测 test3走廊检测
                
                test_opens: list[bool|str] = ["?", "?", "?"]
                test_passed: list[bool|str] = ["?", "?", "?"]

                # {test_passd: test_opens}
                test_opening_rules = {
                    # init -> test1
                    ("?", "?", "?"): (True, "?", "?"),
                    # test1 -> test2
                    (True, "?", "?"): ("?", False, "?"),
                    (False, "?", "?"): ("?", True, "?"),
                    # test2 -> test3
                    (True, "?", "?"): ("?", "?", True),  # test1 passed, ignore test2
                    (False, True, "?"): ("?", "?", True),  # test1 not passed, but test2 passed 
                    (False, False, "?"): ("?", "?", True),  # test1 not passed, and test2 not passed 
                    
                }

                # {test_passed: is room building successful}
                all_tests_passed_rules = {
                    (True, "?", True): True,
                    (False, True, True): True,
                    (False, False, True): True,
                    
                    (True, "?", False): False,
                    (False, True, False): False,
                    (False, False, False): False
                }
                
                #   1. 先生成房间, 然后放置
                room_builder: RoomBuilder = random_by_freq(io.config.room_freq)
                _region = room_builder.build(io, context)
                room_builder.placer.place_room(_region, io, context)
                _region.m_buildings = array2d(_region.m_terrain.width, _region.m_terrain.height)
                context._new_room = _region.to_room()

                all_regions: set[Region] = set()
                dfs(context._new_room, all_regions)
                
                new_room_rect = context._new_room.get_rect()
                last_center = new_room_rect.center
                new_room_rect.wh += vec2(8,8)
                new_room_rect.center = last_center
                
                conflict_regions = [
                        region
                        for region in all_regions
                        if new_room_rect.overlap(region.get_rect()) is not None
                    ]
                
                # 2.1 粗筛 ------------------------
                # 确定冲突检测区域(周围必须空出4格)
                test_opens = test_opening_rules[tuple(test_passed)]
                if test_opens[0]:
                    new_room_rect = context._new_room.get_rect()
                    test_passed[0] = (conflict_regions == [])

                #   2.2 精确地形检测 ------------------------
                test_opens = test_opening_rules[tuple(test_passed)]
                if test_opens[1]:
                    # 冲突区域的外接矩形
                    outbound_rect_for_conflict_regions = calc_outerbound_rect(
                        [region.get_rect() for region in conflict_regions]
                    )
                    # 转换成网格
                    target = array2d(
                        outbound_rect_for_conflict_regions.w,
                        outbound_rect_for_conflict_regions.h,
                        default=0,
                    )
                    # 网格的锚点
                    target_base = vec2i(outbound_rect_for_conflict_regions.x, outbound_rect_for_conflict_regions.y)
                    # 将已经存在的区域的地形映射到该外接矩形网格
                    for region in conflict_regions:
                        try_map_anchored_grid_to(target, target_base, is_blank_fn, region.m_terrain, region.base)
                    
                    # 最后映射新生成的房间, 看看有没有冲突
                    outlined_new_room_terrain = context._new_room.m_terrain
                    add_outline_to_(outlined_new_room_terrain, is_blank_fn, 2, io.t_values.BLANK)
                    
                    new_room_is_valid = try_map_anchored_grid_to(target, target_base, is_blank_fn, outlined_new_room_terrain, context._new_room.base)
                    
                    # 通过精确检测
                    test_passed[1] = new_room_is_valid 
                
                # 2.3 走廊检测 ------------------------------------
                test_opens = test_opening_rules[tuple(test_passed)]
                if test_opens[2]:
                    # ------- 生成房间后生成走廊, 如果走廊无法生成则打回重新生成房间 ------
                    # 1. 确定房间中心点（离rect.center最近的房间格子）
                    start_room_center = start_region.get_terrian_center(is_blank_fn)
                    start_room_center = start_region.get_rect().local_to_global(start_room_center)
                    new_room_center = context._new_room.get_terrian_center(is_blank_fn)
                    new_room_center = context._new_room.get_rect().local_to_global(new_room_center)
                    
                    # 2. 确定两个房间的外接矩形与其他与该外接矩形重叠的region所一起形成的大外接矩形, 然后放大至2倍
                    all_regions: set[Region] = set()
                    dfs(context._new_room, all_regions)
                    astar_searching_regions = [
                            region
                            for region in all_regions.union(set([context._new_room, start_region]))
                            if calc_outerbound_rect([context._new_room.get_rect(), start_region.get_rect()]).overlap(region.get_rect()) is not None
                        ]
                    astar_searching_rect = calc_outerbound_rect([region.get_rect() for region in astar_searching_regions]).up_scaled(2).floor_align()
                    astar_searching_grid = array2d(int(astar_searching_rect.w), int(astar_searching_rect.h), default=0)
                    
                    # 生成该矩形所框出的地形array2d
                    for region in astar_searching_regions:
                        if region is not start_region and region is not context._new_room:
                            result = try_map_anchored_grid_to(astar_searching_grid, vec2i(int(astar_searching_rect.x), int(astar_searching_rect.y)), is_blank_fn, region.m_terrain, region.base)
                            assert result == True
                    
                    # 将房间的中心点(全局坐标系)转换为相对于该矩形的坐标(局部)
                    start_pos = astar_searching_rect.global_to_local(start_room_center)
                    end_pos = astar_searching_rect.global_to_local(new_room_center)

                    
                    # 得到的path从context.region开始至context._new_room结束
                    path = base_astar_in_grid(astar_searching_grid.map(is_blank_fn), start_pos, end_pos)
                    
                    if path is not None:
                        for pos in path:
                            astar_searching_grid[pos] = 1
                        global_path = list(map(astar_searching_rect.local_to_global, path))
                        test_passed[2] = True
                    else:
                        test_passed[2] = False

                    
                    
                # 3. 该房间是否成功通过检测
                success = all_tests_passed_rules[tuple(test_passed)]
                if success:
                    # 跳出循环，得到新房间
                    break
                
                io._next_id -= 1
                
                if attemped == max_attemp_count:
                    # 超出尝试次数, 说明很大程度上无法生成房间
                    raise Exception("grow failed")
                else:
                    # 重试其他的builder尝试处理冲突
                    continue
            
            
            # ------- 生成走廊 ------
            assert context._new_room.base is not None and context._new_room.m_terrain is not None
            assert global_path is not None
            ''' 求 A B
                                  1-1-1-1-1-1 
                                1-1-1-1-1-1-1-1-1
                                1-1-1-1-x-1-1-1-1
                                  1-1-x-x-1-1
                                    x B
                                  x x
                  1-1-1-1-1-1 A x x
                1-1-1-1-x-x-x-x-1
                1-1-1-x-x-1-1-1-1
                1-1-1-1-1-1-1
                  1-1-1
                
                "1": 房间格子BLANK
                "x": 路径点pos
                "A": 走廊的起点
                "B": 走廊的终点
            '''

            # ----计算A点（全局坐标）
            room_A = context.region
            room_A_grid = context.region.m_terrain
            room_A_rect = context.region.get_rect()
            #   由于房间的rect可能紧贴在房间边缘，因此需要扩大1格
            outlined_room_A_rect = Rect(room_A_rect.x - 1, room_A_rect.y - 1, room_A_rect.w + 2, room_A_rect.h + 2)
            outlined_room_A_grid = array2d(outlined_room_A_rect.w, outlined_room_A_rect.h, default=0)
            _reult = try_map_anchored_grid_to(outlined_room_A_grid, outlined_room_A_rect.xy, is_blank_fn, room_A_grid, room_A_rect.xy)
            assert _reult == True

            A = None
            local_path = list(map(outlined_room_A_rect.global_to_local, global_path))
            for pos in local_path:
                if outlined_room_A_grid[vec2i(int(pos.x), int(pos.y))] == 0:
                    A = outlined_room_A_rect.local_to_global(pos)
                    break
            
            # ----计算B点（全局坐标）
            room_B = context._new_room
            room_B_grid = context._new_room.m_terrain
            room_B_rect = context._new_room.get_rect()
            outlined_room_B_rect = Rect(room_B_rect.x - 1, room_B_rect.y - 1, room_B_rect.w + 2, room_B_rect.h + 2)
            outlined_room_B_grid = array2d(outlined_room_B_rect.w, outlined_room_B_rect.h, default=0)
            _reult = try_map_anchored_grid_to(outlined_room_B_grid, vec2i(outlined_room_B_rect.x, outlined_room_B_rect.y), is_blank_fn, room_B_grid, room_B_rect.xy)
            assert _reult == True

            B = None
            local_path = list(map(outlined_room_B_rect.global_to_local, global_path))
            for pos in local_path[::-1]:
                if outlined_room_B_grid[vec2i(int(pos.x), int(pos.y))] == 0:
                    B = outlined_room_B_rect.local_to_global(pos)
                    break
            

            
            # ---- 创建走廊
            # print("----")
            # print_regions_terrain([room_A, room_B])
            assert A is not None and B is not None
            context._corridor_start_pos, context._corridor_end_pos = vec2i(int(A.x), int(A.y)), vec2i(int(B.x), int(B.y))
            corridor_builder: CorridorBuilder = random_by_freq(io.config.corridor_freq)
            corridor = corridor_builder.build(io, context)
            corridor = corridor.to_corridor()
            corridor.connect_to(context._new_room)  # 链接新房间
            context.region.connect_to(corridor)  # 将走廊－新房间连接到region树
        
        else:
            raise Exception(f"无法处理的房间类型: {type(context.region)}")