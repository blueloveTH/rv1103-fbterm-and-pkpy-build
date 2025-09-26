import gyc

def get_input() -> list[int]:
    return gyc.get_input()

def log(level: int, message: str) -> None:
    gyc.log(level, message)

def list_save() -> list[str]:
    return gyc.list_save()

def upload_save(key: str, value: str):
    gyc.upload_save(key, value)

def download_save(key: str) -> str | None:
    return gyc.download_save(key)

def delete_save(key: str) -> bool:
    return gyc.delete_save(key)

from .base import VirtualKey

_codes = {
    'ESC': 11,  '1':  12, '2': 13, '3':  14, 'F1': 15,
    'TAB': 21,  '4':  22, '5': 23, '6':  24, 'F2': 25,
    'MAP': 31,  '7':  32, '8': 33, '9':  34, 'F3': 35,
    'HELP': 41, 'LB': 42, '0': 43, 'RB': 44, 'F4': 45,
}

VKEY_NAMES = {
    VirtualKey.GO_PREV: '1',
    VirtualKey.UP: '2',
    VirtualKey.GO_NEXT: '3',
    VirtualKey.LEFT: '4',
    VirtualKey.OK: '5',
    VirtualKey.RIGHT: '6',
    VirtualKey.DOWN: '8',
    VirtualKey.CURSOR_MODE: '9',
    VirtualKey.TAB: 'TAB',
    VirtualKey.ESCAPE: 'ESC',
    VirtualKey.USE_PET_SKILL: 'LB',
    VirtualKey.SUMMON_PET: 'RB',
    VirtualKey.IDLE: '0',
    VirtualKey.F1: 'F1',
    VirtualKey.F2: 'F2',
    VirtualKey.F3: 'F3',
    VirtualKey.F4: 'F4',
    VirtualKey.MAP: 'MAP',
    VirtualKey.HELP: 'HELP',
}

KEY_MAPPING = {
    _codes[name]: vkey
    for vkey, name in VKEY_NAMES.items()
}