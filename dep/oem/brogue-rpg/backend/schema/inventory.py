from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.item import Item

class ItemSlot:
    item: Item | None
    index: int

    def __init__(self, index: int):
        self.item = None
        self.index = index
    
    def set(self, item: Item) -> None:
        self.item = item


class Inventory:
    def __init__(self) -> None:
        self.items = [ItemSlot(i) for i in range(20)]

    def first_empty_slot(self) -> ItemSlot | None:
        for slot in self.items:
            if slot.item is None:
                return slot

    def remove(self, item: Item):
        for slot in self.items:
            if slot.item == item:
                slot.item = None
                return
    
    def __iter__(self):
        return iter(self.items)
