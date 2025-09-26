from backend.world import Tile, TileData
from backend.utils import border_pos_clockwise

from array2d import array2d

def build_region():
    a = array2d[Tile](16, 8, default=lambda _: Tile(0))
    border_pos_set = set(border_pos_clockwise(a.width, a.height))
    for pos, tile in a:
        tile.tt_ground = TileData(2, 0)
        if pos in border_pos_set:
            tile.tt_wall = TileData(7, 0)
    return a
