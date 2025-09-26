
from dataclasses import dataclass

from .base import TileIndex, EnvironmentObjectSeed, StructureSeed


@dataclass
class TerrianCell:
    tile_id: TileIndex
    env_obj_seed: EnvironmentObjectSeed | None
    structure_seed: StructureSeed | None
        
        

    