import random
import updater
from names import get_first_name
from item import Weapon, Armor


class Monster:
    monster_type = 'monster'

    def __init__(self, health, room):  # TODO: decide on if hints should be in arguments or values
        self.name: str = get_first_name().lower()
        self.health: int = health  # TODO: decide if this is always an int or not
        self.location: 'Room' = room
        
        weapon_damage = random.randint(5, 20)
        weapon = Weapon(f'{self.name}\'s sword', f'a sword taken from the body of {self.name}', weapon_damage)
        self.weapon: Weapon = weapon
        
        armor_value = random.randint(1, 12)
        armor = Armor(f'{self.name}\'s armor', f'armor taken from the body of {self.name}', armor_value)
        self.armor: Armor = armor
        
        room.add_monster(self)
        updater.register(self)

    def __repr__(self):
        return f'{self.name} the {self.monster_type}'

    def update(self):
        if random.random() < .5:
            self.move_to(self.location.random_neighbor())

    def move_to(self, room: 'Room'):
        self.location.remove_monster(self)
        self.location = room
        room.add_monster(self)
    
    def die(self):
        # drop items in room
        # TODO: drop random amount of money
        self.location.remove_monster(self)
        updater.deregister(self)
    
    def attack(self, person: 'Player'):
        attack_damage = self.weapon.damage
        person.get_hit(attack_damage)
    
    def get_hit(self, damage_amount: int):
        actual_damage = damage_amount - self.armor.defense
        self.health -= actual_damage
