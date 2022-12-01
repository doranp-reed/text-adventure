import random
import updater
from room import Room


class Monster:
    def __init__(self, name, health, room: Room):  # TODO: decide on where I should put the hints (input, value, both)
        self.name: str = name
        self.health: int = health  # TODO: decide if this is always an int or not
        self.room: Room = room
        room.add_monster(self)
        updater.register(self)

    def update(self):
        if random.random() < .5:
            self.move_to(self.room.random_neighbor())

    def move_to(self, room: Room):
        self.room.remove_monster(self)
        self.room = room
        room.add_monster(self)
    
    def die(self):
        self.room.remove_monster(self)
        updater.deregister(self)
