from backend.battle.attack import IWeapon
from .base import Actor, PRIORITY_HERO

class Hero(Actor):
    def __init__(self) -> None:
        super().__init__()

        self.level = 1
        self.hp = 5
        self.sp = 0

        self.stats.max_hp.base = 20
        self.stats.max_sp.base = 10

        self.tb_info.priority = PRIORITY_HERO

        self.bigworld_loading_radius = 2

        from backend.schema.inventory import Inventory
        from backend.schema.equipments import Equipments
        self.inventory = Inventory()
        self.equipments = Equipments()

    @property
    def is_hero(self) -> bool:
        return True
    
    @property
    def char(self) -> str:
        return '🙂'
    
    @property
    def normal_attack(self):
        item = self.equipments.weapon.item
        assert item is not None
        return item.iweapon
    
    def wait_for_command(self):
        return current_io().wait_for_command()
    
    def update_stats(self):
        super().update_stats()
        for slot in self.equipments:
            if slot.item is not None:
                affixes = slot.item.affixes_equip
                affixes.apply_modifiers(self.stats, 'from_gear')
        for slot in self.inventory:
            if slot.item is not None:
                affixes = slot.item.affixes_backpack
                affixes.apply_modifiers(self.stats, 'from_gear')

    def collect_triggers(self):
        triggers = super().collect_triggers()
        for slot in self.equipments:
            if slot.item is not None:
                triggers.extend(slot.item.affixes_equip.triggers)
        for slot in self.inventory:
            if slot.item is not None:
                triggers.extend(slot.item.affixes_backpack.triggers)
        return triggers

