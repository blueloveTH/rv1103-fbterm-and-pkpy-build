import os
from conio import _kbhit, _getch

from .base import VirtualKey

def get_input() -> list[int]:
    keys = []
    while _kbhit():
        keys.append(_getch())
    return keys

def log(level: int, message: str):
    pass

def list_save() -> list[str]:
    if not os.path.exists("save"):
        return []
    return os.listdir("save")

def upload_save(key: str, value: str):
    if not os.path.exists("save"):
        os.mkdir("save")
    with open(f"save/{key}", "w") as f:
        f.write(value)

def download_save(key: str) -> str | None:
    filename = f"save/{key}"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return f.read()

def delete_save(key: str) -> bool:
    filename = f"save/{key}"
    if os.path.exists(filename):
        os.remove(filename)
        return True
    return False

KEY_MAPPING = {
    ord('w'): VirtualKey.UP, ord('W'): VirtualKey.UP,
    ord('a'): VirtualKey.LEFT, ord('A'): VirtualKey.LEFT,
    ord('s'): VirtualKey.DOWN, ord('S'): VirtualKey.DOWN,
    ord('d'): VirtualKey.RIGHT, ord('D'): VirtualKey.RIGHT,
    ord('q'): VirtualKey.GO_PREV, ord('Q'): VirtualKey.GO_PREV,
    ord('e'): VirtualKey.GO_NEXT, ord('E'): VirtualKey.GO_NEXT,
    ord(' '): VirtualKey.OK, ord('f'): VirtualKey.OK, ord('F'): VirtualKey.OK,
    ord('x'): VirtualKey.IDLE, ord('X'): VirtualKey.IDLE,
    ord('c'): VirtualKey.CURSOR_MODE, ord('C'): VirtualKey.CURSOR_MODE,
    ord('1'): VirtualKey.F1,
    ord('2'): VirtualKey.F2,
    ord('3'): VirtualKey.F3,
    ord('4'): VirtualKey.F4,
    ord('['): VirtualKey.USE_PET_SKILL,
    ord(']'): VirtualKey.SUMMON_PET,
    27: VirtualKey.ESCAPE,
    9: VirtualKey.TAB,
    ord('m'): VirtualKey.MAP, ord('M'): VirtualKey.MAP,
    ord('h'): VirtualKey.HELP, ord('H'): VirtualKey.HELP,
}

VKEY_NAMES = {
    VirtualKey.UP: 'W',
    VirtualKey.LEFT: 'A',
    VirtualKey.DOWN: 'S',
    VirtualKey.RIGHT: 'D',
    VirtualKey.GO_PREV: 'Q',
    VirtualKey.GO_NEXT: 'E',
    VirtualKey.OK: 'F',
    VirtualKey.IDLE: 'X',
    VirtualKey.CURSOR_MODE: 'C',
    VirtualKey.F1: '1',
    VirtualKey.F2: '2',
    VirtualKey.F3: '3',
    VirtualKey.F4: '4',
    VirtualKey.USE_PET_SKILL: '[',
    VirtualKey.SUMMON_PET: ']',
    VirtualKey.ESCAPE: 'ESC',
    VirtualKey.TAB: 'TAB',
    VirtualKey.MAP: 'M',
    VirtualKey.HELP: 'H',
}
