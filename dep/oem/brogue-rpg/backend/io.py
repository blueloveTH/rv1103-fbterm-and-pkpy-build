from typing import Generator, TYPE_CHECKING
import pkpy
import time

if TYPE_CHECKING:
    from backend.asyncio import *

class IO:
    def __init__(self):
        self.delta_time = 0.0
        self.time = 0.0
        self.is_first_frame = True

    def begin_frame(self) -> None:
        pkpy.watchdog_begin(1000)
        now = time.time()
        if self.is_first_frame:
            self.delta_time = 0.0
            self.is_first_frame = False
        else:
            self.delta_time = now - self.time
        self.time = now

    def end_frame(self) -> None:
        pkpy.watchdog_end()

    def wait_for_command(self) -> Future[Task]:
        """获取玩家的命令"""
        raise NotImplementedError
    
    def wait_for_game_start(self) -> Generator:
        """等待游戏开始"""
        raise NotImplementedError