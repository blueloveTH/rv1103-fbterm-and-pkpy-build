from vmath import vec2i
from backend.schema.equipments import GearSlot
from frontend.routes.base import Page
from frontend import ui

from .base import TabController, tab_title

class EquipmentsPage(Page):
    def __init__(self, controller: TabController):
        self.controller = controller
        self.cursor = 0

    def move_cursor(self, delta: int):
        length = len(self.equipments)
        self.cursor = (self.cursor + delta) % length

    def poll(self, io):
        while True:
            state, axis = yield from io.input.wait_for_input()
            if axis != vec2i.ZERO:
                self.move_cursor(axis.y)
            elif self.controller.test(state):
                break

    @property
    def equipments(self):
        return current_game().hero.equipments
    
    def _item(self, slot: GearSlot, width: int):
        item = slot.item
        bg = ui.theme.selected_bg if slot.index == self.cursor else None
        if item is None:
            return ui.richtext(" (No Item)", fg=ui.theme.gray, bg=bg, width=width)
        else:
            return ui.richtext(f" {item.name}", bg=bg, width=width)

    def __call__(self, io):
        children: list[ui.Widget | str] = [tab_title("装备界面", io.input)]
        width = io.config.width
        e = self.equipments

        # weapon
        children.append(ui.Text("[武器]"))
        children.append(self._item(e.weapon, width))

        # armor
        children.append(ui.Text("[护甲]"))
        children.append(self._item(e.armor, width))

        # headgear
        children.append(ui.Text("[头饰]"))
        children.append(self._item(e.headgear, width))

        # accessory
        children.append(ui.Text("[饰品]"))
        for accessory in e.accessories:
            children.append(self._item(accessory, width))
        children.append(ui.Newline())

        # artifact
        children.append(ui.Text("[神器]"))
        for artifact in e.artifacts:
            children.append(self._item(artifact, width))

        return ui.VStack([
            self.common_header(io),
            ui.HDivider(),
            ui.Column(
                children,
                height=io.config.body_height_ex
            ),
            ui.HDivider(),
            self.common_footer(io),
        ], width=width)