from vmath import vec2i
from pkpy import TValue

int32 = int

class TileData(TValue[vec2i]):
    def __new__(cls, tileset: int32, index: int32):
        return super().__new__(cls, vec2i(tileset, index))

    @property
    def tileset(self) -> int32:
        return self.value.x
    
    @property
    def index(self) -> int32:
        return self.value.y


class Tile:
    region_id: int

    def __init__(self, region_id: int):
        self.region_id = region_id

    tt_chasm: TileData | None = None
    tt_water: TileData | None = None
    tt_ground: TileData | None = None
    tt_floor: TileData | None = None
    tt_slime: TileData | None = None
    tt_grass: TileData | None = None
    tt_fire: TileData | None = None
    tt_wall: TileData | None = None

    def is_walkable(self) -> bool:
        if self.tt_chasm or self.tt_water or not self.tt_ground or self.tt_wall:
            return False
        return True
