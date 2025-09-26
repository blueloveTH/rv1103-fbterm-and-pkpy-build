from typing import Iterator
from vmath import vec2i, color32


TileIndex = vec2i


class Tile:
    def __init__(self, index: TileIndex, char: str, fg: str | None, bg: str | None):
        self.index = index
        self.char = char
        self.fg = fg or None
        self.bg = bg or None
    
    def __str__(self):
        return self.wrap_str_with_background(self.get_frontground_str())
    
    def __repr__(self):
        return f"Tile(index={self.index}, char={self.char}, fg={self.fg}, bg={self.bg})"
    
    def get_frontground_str(self) -> str:
        if self.fg is None:
            return self.char
        return color32.from_hex(self.fg).ansi_fg(self.char)
    
    def wrap_str_with_background(self, s: str) -> str:
        if self.bg is None:
            return s
        return color32.from_hex(self.bg).ansi_bg(s)

class Tileset:
    def __init__(self, id: int, name: str, tiles: list[Tile]):
        self.id = id
        self.name = name
        self.tiles = tiles
    
    def __iter__(self) -> Iterator[Tile]:
        return iter(self.tiles)
    
    def __len__(self) -> int:
        return len(self.tiles)
    
    def __getitem__(self, index: int) -> Tile:
        return self.tiles[index]
    
class TileGallery:
    def __init__(self, version: str, created_at: str, tilesets: list[Tileset]):
        self.version = version
        self.created_at = created_at
        self.tilesets = {ts.id: ts for ts in tilesets}
    
    def __iter__(self) -> Iterator[Tileset]:
        return iter(self.tilesets.values())
    
    def __getitem__(self, index: int|TileIndex) -> Tileset|Tile:
        if isinstance(index, int):
            return self.tilesets[index]
        elif isinstance(index, TileIndex):
            for tileset in self.tilesets.values():
                if index.x == tileset.id:
                    return tileset[index.y]
            raise IndexError(f"Tile index out of range: {index}")
        else:
            raise ValueError(f"Invalid index type: {type(index)}")




_data = {
    "version": "terrian_test_0.1",
    "created_at": "2025-06-01 00:41:34.901641",
    "tilesets": [
        {
            "id": 1,
            "name": "debug-height-ground",
            "tiles": [
                {
                    "id": 0,
                    "char": "　",
                    "fg": None,
                    "bg": "#be5c37"
                },
                {
                    "id": 1,
                    "char": "　",
                    "fg": None,
                    "bg": "#d78851"
                },
                {
                    "id": 2,
                    "char": "　",
                    "fg": None,
                    "bg": "#dbbf92"
                },
                {
                    "id": 3,
                    "char": "　",
                    "fg": None,
                    "bg": "#f3e1af"
                },
                {
                    "id": 4,
                    "char": "　",
                    "fg": None,
                    "bg": "#f7f7e9"
                }
            ]
        },
        {
            "id": 2,
            "name": "debug-height-sea",
            "tiles": [
                {
                    "id": 0,
                    "char": "　",
                    "fg": None,
                    "bg": "#507aaf"
                },
                {
                    "id": 1,
                    "char": "　",
                    "fg": None,
                    "bg": "#8197c6"
                },
                {
                    "id": 2,
                    "char": "　",
                    "fg": None,
                    "bg": "#afb7db"
                },
                {
                    "id": 3,
                    "char": "　",
                    "fg": None,
                    "bg": "#dedcea"
                },
                {
                    "id": 4,
                    "char": "　",
                    "fg": None,
                    "bg": "#fbf9fa"
                }
            ]
        },
        {
            "id": 3,
            "name": "debug-height-all",
            "tiles": [
                {
                    "id": 0,
                    "char": "　",
                    "fg": None,
                    "bg": "#831a21"
                },
                {
                    "id": 1,
                    "char": "　",
                    "fg": None,
                    "bg": "#a13d3b"
                },
                {
                    "id": 2,
                    "char": "　",
                    "fg": None,
                    "bg": "#c16d58"
                },
                {
                    "id": 3,
                    "char": "　",
                    "fg": None,
                    "bg": "#dba27d"
                },
                {
                    "id": 4,
                    "char": "　",
                    "fg": None,
                    "bg": "#ecd0b4"
                },
                {
                    "id": 5,
                    "char": "　",
                    "fg": None,
                    "bg": "#f2ebe5"
                },
                {
                    "id": 6,
                    "char": "　",
                    "fg": None,
                    "bg": "#e8edf1"
                },
                {
                    "id": 7,
                    "char": "　",
                    "fg": None,
                    "bg": "#c8d6e7"
                },
                {
                    "id": 8,
                    "char": "　",
                    "fg": None,
                    "bg": "#9ebcdb"
                },
                {
                    "id": 9,
                    "char": "　",
                    "fg": None,
                    "bg": "#7091c7"
                },
                {
                    "id": 10,
                    "char": "　",
                    "fg": None,
                    "bg": "#4e70af"
                },
                {
                    "id": 11,
                    "char": "　",
                    "fg": None,
                    "bg": "#375093"
                }
            ]
        },
        {
            "id": 4,
            "name": "debug-direction",
            "tiles": [
                {
                    "id": 0,
                    "char": "→ ",
                    "fg": "#ff3b30",
                    "bg": None
                },
                {
                    "id": 1,
                    "char": "↗ ",
                    "fg": "#ff9500",
                    "bg": None
                },
                {
                    "id": 2,
                    "char": "↑ ",
                    "fg": "#34c759",
                    "bg": None
                },
                {
                    "id": 3,
                    "char": "↖ ",
                    "fg": "#00c7be",
                    "bg": None
                },
                {
                    "id": 4,
                    "char": "← ",
                    "fg": "#00b0ff",
                    "bg": None
                },
                {
                    "id": 5,
                    "char": "↙ ",
                    "fg": "#5856d6",
                    "bg": None
                },
                {
                    "id": 6,
                    "char": "↓ ",
                    "fg": "#af52ff",
                    "bg": None
                },
                {
                    "id": 7,
                    "char": "↘ ",
                    "fg": "#ff2d55",
                    "bg": None
                }
            ]
        },
        {
            "id": 5,
            "name": "background-wasteland",
            "tiles": [
                {
                    "id": 0,
                    "char": "　",
                    "fg": None,
                    "bg": "#100906"
                },
                {
                    "id": 1,
                    "char": "　",
                    "fg": None,
                    "bg": "#3b3b3b"
                },
                {
                    "id": 2,
                    "char": "　",
                    "fg": None,
                    "bg": "#d29723"
                },
                {
                    "id": 3,
                    "char": "﹒",
                    "fg": None,
                    "bg": "#a4771c"
                },
                {
                    "id": 4,
                    "char": "　",
                    "fg": None,
                    "bg": "#1ca498"
                }
            ]
        },
        {
            "id": 6,
            "name": "foreground-wasteland-shrub",
            "tiles": [
                {
                    "id": 0,
                    "char": "🌿",
                    "fg": None,
                    "bg": None
                },
                {
                    "id": 1,
                    "char": "☘️",
                    "fg": None,
                    "bg": None
                },
                {
                    "id": 2,
                    "char": "🌵",
                    "fg": None,
                    "bg": None
                },
                {
                    "id": 3,
                    "char": "茻",
                    "fg": "#147313",
                    "bg": None
                },
                {
                    "id": 4,
                    "char": "芔",
                    "fg": "#147313",
                    "bg": None
                },
                {
                    "id": 5,
                    "char": "艹",
                    "fg": "#147313",
                    "bg": None
                }
            ]
        }
    ]
}




DEFAULT_TILE_GALLERY = TileGallery(
    _data["version"],
    _data["created_at"],
    [Tileset(ts["id"], ts["name"], [Tile(vec2i(t["id"], 0), t["char"], t["fg"], t["bg"]) for t in ts["tiles"]]) for ts in _data["tilesets"]]
)

