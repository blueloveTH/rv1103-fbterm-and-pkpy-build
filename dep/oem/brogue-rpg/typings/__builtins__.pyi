from backend import Game, World, IO
from frontend import i18n
import builtins

# injected functions
def current_game() -> Game: ...
def current_world() -> World: ...
def current_io() -> IO: ...

# type aliases
String = str | i18n.string
ellipsis = builtins.ellipsis

