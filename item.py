from clear import clear
from typing import Optional


class Item:
    item_type = 'nothing special'
    
    def __init__(self, name, desc):
        self.name: str = name
        self.desc: str = desc  # TODO: actually use this value
        self.location: Optional['Room | Player'] = None  # TODO: do I need quotes or no?
    
    def __repr__(self):
        return f'{self.name}: {self.desc}'

    def describe(self):
        clear()
        print(self.desc)
        print()
        input("Press enter to continue...")
    
    def put_in_room(self, room: 'Room'):
        self.location = room
        room.add_item(self)


class Potion(Item):
    item_type = 'potion'
    
    def __init__(self, name, desc, hp):
        super().__init__(name, desc)
        self.heal_value = hp
