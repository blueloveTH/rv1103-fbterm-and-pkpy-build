from vmath import vec2i

class Incremental:
    def __init__(self):
        self.value = -1

    def __call__(self):
        self.value += 1
        return self.value
    
incr = Incremental()

class VirtualKey:
    # 数字键
    UP = incr()
    DOWN = incr()
    LEFT = incr()
    RIGHT = incr()
    GO_PREV = incr()
    GO_NEXT = incr()
    OK = incr()
    IDLE = incr()
    CURSOR_MODE = incr()
    # 快捷道具
    F1 = incr()
    F2 = incr()
    F3 = incr()
    F4 = incr()
    # 特殊动作
    USE_PET_SKILL = incr()
    SUMMON_PET = incr()
    # 功能键
    ESCAPE = incr()
    TAB = incr()
    MAP = incr()
    HELP = incr()
    __count__ = incr()
