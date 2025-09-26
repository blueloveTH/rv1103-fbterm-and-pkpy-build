from typing import Any, Generator
from vmath import vec2i

from backend import IO
from backend.asyncio import *

from frontend.platform import VirtualKey, Input
from frontend import routes

from .config import Config


class ConsoleIO(IO):
    pages: list[routes.Page]

    def __init__(self) -> None:
        super().__init__()
        self.input = Input()

        self.pages = []
        self.config = Config()

        self.page_startmenu = routes.misc.StartMenuPage()
        self.page_world = routes.world.WorldPage()
        self.page_tab = routes.tab.TabPage()

        # cache
        self.cursor = self.page_world.cursor

    def push[T](self, page: 'routes.Page[T]'):
        self.pages.append(page)
        res = yield from page.poll(self)
        self.pages.pop()
        return res
    
    def begin_frame(self):
        super().begin_frame()

    def end_frame(self):
        super().end_frame()
        w = self.pages[-1](self)
        w.prerender(self.config.width, self.config.height)
        assert w.width == self.config.width
        assert w.height == self.config.height
        print('\x1b[H\x1b[J', end='')
        print(*w.render(), sep='\n', flush=True)
        # update the input state
        self.input.update()

    def wait_for_command(self) -> Future[Task]:
        game = current_game()
        while True:
            state, axis = yield from self.input.wait_for_input()

            if state[VirtualKey.ESCAPE]:
                game.message("暂停菜单")
                continue

            if state[VirtualKey.TAB]:
                if self.cursor.enabled:
                    game.message("光标模式下无法打开背包")
                    # TODO: 特殊处理
                    continue
                game.message("打开背包")
                cmd = yield from self.push(self.page_tab.with_index(0))
                if cmd is not None:
                    return cmd
                continue

            if state[VirtualKey.MAP]:
                raise NotImplementedError
                continue

            if state[VirtualKey.HELP]:
                raise NotImplementedError
                continue

            ###############################################

            if state[VirtualKey.IDLE]:
                return common_tasks.Idle()

            if state[VirtualKey.CURSOR_MODE]:
                if self.cursor.toggle():
                    game.message("开启光标模式")
                else:
                    game.message("关闭光标模式")
                continue

            ###############################################

            if state[VirtualKey.USE_PET_SKILL]:
                raise NotImplementedError
                continue

            if state[VirtualKey.SUMMON_PET]:
                raise NotImplementedError
                continue

            ###############################################

            if state[VirtualKey.OK]:
                target = game.hero.pos + game.hero.facing
                cmd = game.world.interact(game.hero, target)
                if cmd is not None:
                    return cmd
                else:
                    iweapon = game.hero.normal_attack
                    assert iweapon is not None
                    target = iweapon.player_get_auto_target()
                    if target is None:
                        game.message("无法攻击")
                        continue
                    self.cursor.position = target
                    return common_tasks.NormalAttack(game.hero, iweapon, target)
 
            if axis != vec2i.ZERO:
                if self.cursor.enabled:
                    self.cursor.position += axis
                else:
                    self.cursor.reset()
                    target = game.hero.pos + axis
                    game.hero.face_direction(axis)
                    if game.world.is_walkable(target):
                        return common_tasks.Move(game.hero, axis)
                    else:
                        game.message("这里有障碍物，无法前进")
                        return common_tasks.Idle()

    def wait_for_game_start(self):
        yield from self.push(self.page_startmenu)
        self.pages.append(self.page_world)

    def choices(
            self,
            options: list[routes.common.Option],
            title: String | None = None,
            cursor: int = 0
            ) -> Generator[None, Any, int | None]:
        return self.push(routes.common.ChoicesPage(options, title, cursor))

    def wait_for_confirm(self):
        yield
        while True:
            state, _ = yield from self.input.wait_for_input()
            if state[VirtualKey.OK]:
                return
            yield

    def choose_item_slot(self, filter, **kwargs):
        # inventory = current_game().hero.inventory
        # return self.renderer.push(InventoryChoicePage(inventory, filter=filter))
        raise NotImplementedError

