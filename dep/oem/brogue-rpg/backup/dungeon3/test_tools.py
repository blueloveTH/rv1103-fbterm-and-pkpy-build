from array2d import array2d
from vmath import vec2i

from .io import *
from .utils import try_map_grid_to_


def print_grid(grid: array2d[int], message="------------------------"):
# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
# Color Name	    Foreground Color Code	Background Color Code
# Black	            30	                    40
# Red	            31	                    41
# Green	            32	                    42
# Yellow	        33	                    43
# Blue	            34	                    44
# Magenta	        35	                    45
# Cyan	            36	                    46
# White	            37	                    47
# Default	        39	                    49
# Reset	            0	                    0
# Bright Black	    90	                    100
# Bright Red	    91	                    101
# Bright Green	    92	                    102
# Bright Yellow	    93	                    103
# Bright Blue	    94	                    104
# Bright Magenta	95	                    105
# Bright Cyan	    96	                    106
# Bright White	    97	                    107
    
    # (symbol, fg, bg)
    palette = {
        0: (". ", 37, 0),
        1: ("1 ", 30, 41),
        2: ("2 ", 30, 42),
        3: ("3 ", 30, 43),
        4: ("4 ", 30, 44),
        5: ("5 ", 30, 45),
        6: ("6 ", 30, 46),
        7: ("7 ", 30, 47),
        8: ("8 ", 30, 101),
        9: ("9 ", 30, 102),
        10: ("10", 30, 103),
        11: ("11", 30, 104),
        12: ("12", 30, 105),
        13: ("13", 30, 106),
        14: ("14", 30, 107)
    }
    
    max_value = max(palette.keys())-1

    grid = grid.map(int)
    
    print(message)
    for y in range(grid.height):
        for x in range(grid.width):
            value = grid[x, y]
    
            if value in palette:
                symbol, fg, bg = palette[value]
            else:
                remainder = (value % (max_value + 1))+1
                _, fg, bg = palette[remainder]
                symbol = str(value)  # Keep the number for printing
    
            data = f"\x1b[2;{fg};{bg}m"
            data += symbol
            data += "\x1b[0m"
            print(data, end="")
        print()
    
    # get non-zero count
    print("sparsity:", grid.count(0), "/", grid.numel)

def dfs(node: "Region", visited: set["Region"]):
    if node in visited:
        return
    visited.add(node)
    for neighbor in node.neighbors:
        dfs(neighbor, visited)

def print_regions_terrain(regions, margin=5):
    all_regions = set(regions)
    rects = [region.bounding_rect for region in all_regions]
    print(rects)
    now_xy = rects[0][0]
    for new_rect in rects[1:]:
        now_xy = vec2i(min(now_xy.x, new_rect[0].x), min(now_xy.y, new_rect[0].y))
    
        
    now_end_xy = rects[0][0] + rects[0][1]
    for new_rect in rects[1:]:
        new_end_xy = new_rect[0] + new_rect[1]
        now_end_xy = vec2i(max(now_end_xy.x, new_end_xy.x), max(now_end_xy.y, new_end_xy.y))    
    margin_vec = vec2i(margin,margin)
    dungeon_rect = (now_xy-margin_vec, (now_end_xy - now_xy) + margin_vec + margin_vec)
    dungeon_terrain = array2d(dungeon_rect[1].x, dungeon_rect[1].y, default=0)
    
    for region in all_regions:
        delta = region.base - dungeon_rect[0]
        success = try_map_grid_to_(dungeon_terrain, lambda x: x==1, region.m_terrain, delta)
    print_grid(dungeon_terrain)
        
# 从根区域开始遍历
def print_all_regions_terrain(io: DungeonIO, margin=5):
    all_regions = set()
    dfs(io.root, all_regions)
    rects = [region.bounding_rect for region in all_regions]
    
    now_xy = rects[0][0]
    for new_rect in rects[1:]:
        now_xy = vec2i(min(now_xy.x, new_rect[0].x), min(now_xy.y, new_rect[0].y))
    
        
    now_end_xy = rects[0][0] + rects[0][1]
    for new_rect in rects[1:]:
        new_end_xy = new_rect[0] + new_rect[1]
        now_end_xy = vec2i(max(now_end_xy.x, new_end_xy.x), max(now_end_xy.y, new_end_xy.y))    
    margin_vec = vec2i(margin,margin)
    dungeon_rect = (now_xy-margin_vec, (now_end_xy - now_xy) + margin_vec + margin_vec)
    dungeon_terrain = array2d(dungeon_rect[1].x, dungeon_rect[1].y, default=0)
    
    for region in all_regions:
        delta = region.base - dungeon_rect[0]
        success = try_map_grid_to_(dungeon_terrain, lambda x: x!=0, region.m_terrain.map(lambda x: x+region.id if x!=0 else 0), delta)
    print_grid(dungeon_terrain)
        