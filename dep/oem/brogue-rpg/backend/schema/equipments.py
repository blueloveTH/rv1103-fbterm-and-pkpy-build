from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.item import Item


class GearSlot:
    item: Item | None
    index: int

    def __init__(self, index: int = 0):
        self.item = None
        self.index = index

    def is_empty(self) -> bool:
        return self.item is None
    
    def set(self, item: Item) -> None:
        self.item = item
    

class Equipments:
    def __init__(self):
        self.slots = [GearSlot(i) for i in range(9)]

        self.weapon = self.slots[0]    # 武器
        self.armor = self.slots[1]     # 护甲
        self.headgear = self.slots[2]
        self.accessories = [
            self.slots[3], # 饰品1
            self.slots[4], # 饰品2
        ]
        self.artifacts = [
            self.slots[5], # 神器1
            self.slots[6], # 神器2
            self.slots[7], # 神器3
            self.slots[8], # 神器4
        ]

    def __iter__(self):
        return iter(self.slots)

    def __len__(self):
        return len(self.slots)
    
    def __getitem__(self, index: int) -> GearSlot:
        return self.slots[index]