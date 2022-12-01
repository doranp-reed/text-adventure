import random
from item import Item
from monster import Monster  # TODO: decide on if I should actually have these imports (right now it's for the IDE)


class Room:
    def __init__(self, description: str):
        self.desc: str = description
        self.monsters: list[Monster] = []
        self.exits: list[list[str, 'Room']] = []
        self.items: list[Item] = []

    def add_exit(self, exit_name: str, destination: 'Room'):
        self.exits.append([exit_name, destination])

    def get_destination(self, direction: str):
        for e in self.exits:
            if e[0] == direction:
                return e[1]
        return self

    @classmethod  # TODO: make sure this works
    def connect_rooms(cls, room1: 'Room', dir1: str, room2: 'Room', dir2: str):
        # creates "dir1" exit from room1 to room2 and vice versa
        room1.add_exit(dir1, room2)
        room2.add_exit(dir2, room1)

    def exit_names(self):
        return [x[0] for x in self.exits]

    def add_item(self, item: Item):
        self.items.append(item)

    def remove_item(self, item: Item):
        self.items.remove(item)

    def add_monster(self, monster: 'Monster'):
        self.monsters.append(monster)

    def remove_monster(self, monster: 'Monster'):
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

    def get_monster_by_name(self, name: str):
        for i in self.monsters:
            if i.name.lower() == name.lower():
                return i
        return False

    def random_neighbor(self):
        return random.choice(self.exits)[1]
