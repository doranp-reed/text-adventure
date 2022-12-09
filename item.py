from clear import clear
from random import randint


class Item:
    item_type = 'nothing special'
    
    def __init__(self, name, desc):
        self.name: str = name
        self.desc: str = desc
    
    def __repr__(self):
        return f'{self.name}: {self.desc}'

    def describe(self):
        clear()
        print(self.desc)
        print()
        input("Press enter to continue...")
    
    def put_in_room(self, room: 'Room'):
        room.add_item(self)


class Potion(Item):
    item_type = 'potion'
    
    def __init__(self, name, desc, hp):
        super().__init__(name, desc)
        self.heal_value = hp


class Weapon(Item):
    item_type = 'weapon'
    
    def __init__(self, name, desc, damage):
        super().__init__(name, desc)
        self.damage: int = damage
    
    def __repr__(self):
        return f'{self.name}: {self.damage} damage'


class Armor(Item):
    item_type = 'armor'
    
    def __init__(self, name, desc, defense):
        super().__init__(name, desc)
        self.defense: int = defense  # defense is flat reduction, not percentage reduction
    
    def __repr__(self):
        return f'{self.name}: {self.defense} defense'


class Coins(Item):
    item_type = 'coins'
    
    def __init__(self):
        self.name: str = 'coins'
        self.desc: str = 'a pile of coins'
        self.value = randint(1, 7)
