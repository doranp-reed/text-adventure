import random
import updater
from names import get_first_name


class Monster:
    monster_type = 'monster'

    def __init__(self, health, room: 'Room'):  # TODO: decide on where I should put the hints (input, value, both)
        self.name: str = get_first_name().lower()
        self.health: int = health  # TODO: decide if this is always an int or not
        self.location: 'Room' = room
        room.add_monster(self)
        updater.register(self)

    def __repr__(self):
        return f'{self.name} the {self.class_name}'

    def update(self):
        if random.random() < .5:
            self.move_to(self.location.random_neighbor())

    def move_to(self, room: 'Room'):
        self.location.remove_monster(self)
        self.location = room
        room.add_monster(self)
    
    def die(self):
        self.location.remove_monster(self)
        updater.deregister(self)
        # drop loot and stuff
    
    def attack(self, person):  # TODO: do this
        pass
