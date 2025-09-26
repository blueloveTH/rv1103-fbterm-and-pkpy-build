from vmath import vec2i
from backend.asyncio import Task
from frontend import i18n
from typing import TYPE_CHECKING

from .expr import Expr
from .affix import *

if TYPE_CHECKING:
    from backend.battle.attack import IWeapon


class ItemAction:
    def __init__(self, name: String, task: Task):
        self.name = name
        self.task = task

    def __call__(self, user, item: 'Item'):
        context: dict = item.environ.copy()
        context[Item.CTX_USER] = user
        context[Item.CTX_ITEM] = item
        return self.task.with_context(context)


class Item:
    CTX_USER = 'user'
    CTX_ITEM = 'item'

    def __init__(self, name: String = '', icon: str = '', desc: String = ''):
        self.name = name
        self.icon = icon
        self.desc = desc
        self.affixes_equip = AffixGroup()
        self.affixes_backpack = AffixGroup()
        self.actions = []           # type: list[ItemAction]
        self.environ = {}           # type: dict[str, Expr]

        self.is_equipped = False
        self.iweapon = None         # type: IWeapon | None

        self.durability = None      # type: vec2i | None
        self.quantity = 1

    def is_equippable(self) -> bool:
        return bool(self.affixes_equip)
    
    def on_equip(self, *affixes: Affix):
        for a in affixes:
            self.affixes_equip.append(a)
        return self
    
    def on_backpack(self, *affixes: Affix):
        for a in affixes:
            self.affixes_backpack.append(a)
        return self
    
    def on_action(self, name: String, task: Task):
        self.actions.append(ItemAction(name, task))
        return self
    
    def on_attack(self, weapon: IWeapon):
        assert self.iweapon is None
        self.iweapon = weapon
        return self
    
    def with_durability(self, value: vec2i | None):
        self.durability = value
        return self
    
    def with_quantity(self, value: int):
        self.quantity = value
        return self
    
    def with_environ(self, **kwargs):
        self.environ.update(kwargs)
        return self
    
    #######################################################

    def render_desc(self) -> str:
        kv = {k: e(self.environ) for k, e in self.environ.items()}
        return str(self.desc).format(**kv)

    def get_actions(self):
        actions = self.actions.copy()
        if self.is_equippable():
            if self.is_equipped:
                actions.insert(0, action_unequip()) # type: ignore
            else:
                actions.insert(0, action_equip())   # type: ignore
        return actions
    

# class ChooseGearSlot(Task):
#     def __init__(self, output: str = 'slot'):
#         self.output = output

#     def call_async(self, context: dict):
#         from backend.schema.inventory import GearSlot
#         game = current_game()
#         game.message("Choose a gear slot to equip")
#         filter = lambda slot: (isinstance(slot, GearSlot) and slot.item is None)
#         slot = yield from game.io.choose_item_slot(filter)
#         context[self.output] = slot
#         return 0


# def action_equip():
#     def extra_step(ctx):
#         from backend.schema.inventory import GearSlot

#         slot: GearSlot | None = ctx["slot"]
#         if slot is None:
#             raise TaskInterrupt("No slot selected")
        
#         inventory = current_game().hero.inventory
#         item: Item = ctx[Item.CTX_ITEM]
#         inventory.remove(item)
#         slot.item = item
#         slot.item.is_equipped = True

#         ctx[Item.CTX_USER].update_stats()

#     return ItemAction(ui.Equip, Task.pipeline([
#         ChooseGearSlot(output='slot'),
#         Task.callback(extra_step)
#     ]))


# def action_unequip():
#     def extra_step(ctx):
#         inventory = current_game().hero.inventory
#         item: Item = ctx[Item.CTX_ITEM]
#         item_slot = inventory.first_empty_slot()
#         if item_slot is None:
#             raise TaskInterrupt("No empty slot")
#         inventory.remove(item)
#         item_slot.item = item
#         item.is_equipped = False

#         ctx[Item.CTX_USER].update_stats()

#     return ItemAction(ui.Unequip, Task.callback(extra_step))
