from vmath import vec2i
from typing import TypeVar
from backend.schema.inventory import ItemSlot
from backend.asyncio import *

from frontend.platform import VirtualKey
from frontend.routes.base import Page
from frontend import ui

from .base import TabController, tab_title

from ..common import Option

T = TypeVar('T')

class InventoryBase[T](Page[T]):
    def __init__(self, cursor: int = 0):
        self.cursor = cursor

    @property
    def inventory(self):
        return current_game().hero.inventory

    @property
    def selected_slot(self) -> ItemSlot:
        return self.inventory.items[self.cursor]

    def move_cursor(self, delta: int):
        length = len(self.inventory.items)
        self.cursor = (self.cursor + delta) % length
    
    def build_item(self, slot: ItemSlot, width: int):
        prefix = f'[{(slot.index + 1):02}]'
        bg = ui.theme.selected_bg if slot.index == self.cursor else None
        if slot.item is None:
            text = ui.richtext(
                f'{prefix} (No Item)',
                fg=ui.theme.gray,
                bg=bg,
                width=width,
            )
        else:
            text = ui.richtext(
                f'{prefix} {slot.item.name}',
                bg=bg,
                width=width,
            )
        return ui.Text(text)
    
    def __call__(self, io):
        body = ui.ListView(
            [
                self.build_item(slot, io.config.width)
                for slot in self.inventory.items
            ],
            height=io.config.body_height_ex - 1,
            scroll_index=self.cursor
        )
        return ui.VStack([
            self.common_header(io),
            ui.HDivider(),
            tab_title("背包界面", io.input),
            body,
            ui.HDivider(),
            self.common_footer(io),
        ], width=io.config.width)


class InventoryPage(InventoryBase[Task]):
    def __init__(self, controller: TabController, cursor: int = 0):
        super().__init__(cursor)
        self.controller = controller

    def poll(self, io):
        game = current_game()
        while True:
            state, axis = yield from io.input.wait_for_input()
            if axis != vec2i.ZERO:
                self.move_cursor(axis.y)
            elif state[VirtualKey.OK]:
                slot = self.selected_slot
                if slot.item is None:
                    continue
                else:
                    item = slot.item
                    game.message("选中物品")
                    title = f'{item.name}'
                    desc = title + '\n\n' + item.render_desc()
                    actions = item.get_actions()
                    options = [Option(str(op.name), desc, True) for op in actions]
                    index = yield from io.choices(options)
                    if index is not None:
                        game.message(f"选择了{options[index].name}")
                        return actions[index](game.hero, item)
                    else:
                        game.message("你取消了选择")
            elif self.controller.test(state):
                break


class InventoryChoicePage(InventoryBase[ItemSlot | None]):
    def __init__(self, cursor: int, filter=None):
        super().__init__(cursor)
        self.filter = filter or (lambda slot: True)

    def poll(self, io):
        while True:
            state, axis = yield from io.input.wait_for_input()
            if axis != vec2i.ZERO:
                self.move_cursor(axis.y)
            elif state[VirtualKey.OK]:
                slot = self.selected_slot
                if self.filter(slot):
                    return slot
            elif state[VirtualKey.ESCAPE]:
                break