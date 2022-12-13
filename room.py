from random import random as random_random
from random import choice as random_choice
import updater
from monster import Roamer, Entrapper, Guardian


class Room:
    valid_directions: list[str] = ['north', 'n', 'south', 's', 'east', 'e', 'west', 'w']
    room_type = 'room'
    
    def __init__(self, desc: str):
        self.desc: str = desc
        self.monsters: list[type['Monster']] = []
        self.exits: list[list[str, 'Room']] = []
        self.items: list['Item'] = []
        updater.register(self)

    def add_exit(self, exit_name: str, destination: 'Room'):
        self.exits.append([exit_name, destination])

    def get_destination(self, direction: str):
        for e in self.exits:
            if (e[0] == direction) or (e[0][0] == direction):  # so you can do 'n' for 'north'
                return e[1]
        return None

    @classmethod
    def connect_rooms(cls, room1: 'Room', dir1: str, room2: 'Room', dir2: str):
        # creates "dir1" exit from room1 to room2 and vice versa
        room1.add_exit(dir1, room2)
        room2.add_exit(dir2, room1)

    def exit_names(self):
        return [x[0] for x in self.exits]

    def add_item(self, item: 'Item'):
        self.items.append(item)

    def remove_item(self, item: 'Item'):
        self.items.remove(item)

    def add_monster(self, monster: type['Monster']):
        self.monsters.append(monster)

    def remove_monster(self, monster: type['Monster']):
        self.monsters.remove(monster)

    def has_items(self):
        return self.items != []

    def get_item_by_name(self, name: str):
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
        return False

    def has_monsters(self):
        return self.monsters != []

    def get_monster_by_name(self, name: str) -> type['Monster'] | bool:
        for monster in self.monsters:
            if monster.name == name.lower():
                return monster
        return False

    def random_neighbor(self):
        return random_choice(self.exits)[1]
    
    def update(self):
        if random_random() < .1:
            Roamer(10, self)


class Shop(Room):  # monsters can't spawn in here or move here, and has a merchant from whom the player can buy items
    room_type = 'shop'  # TODO: make sure I'm passing 'Gregor's shop' to the __init__
    
    def update(self):
        pass  # monsters don't spawn in shop


class Trap(Room):  # player cannot leave until they've killed all of the entrappers in the room
    room_type = 'trap'
    
    def __init__(self, desc: str):
        super().__init__(desc)
        for _ in range(3):
            Entrapper(30, self)
    
    def update(self):
        pass  # monsters don't spawn in trap room


class Nest(Room):  # spawns way more roamers
    room_type = 'nest'
    
    def update(self):
        if random_random() < 0.6:
            Roamer(10, self)


class Lair(Room):  # location of the Guardian
    room_type = 'lair'
    
    def __init__(self, desc: str):
        super().__init__(desc)
        Guardian(100, self)
