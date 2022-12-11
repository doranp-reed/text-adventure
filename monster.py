import random
import updater
from names import get_first_name
from item import Weapon, Armor, Coins, Potion


class Monster:
    monster_type = 'monster'

    def __init__(self, health, room):  # TODO: decide on if hints should be in arguments or values
        self.name: str = get_first_name().lower()
        self.health: int = health  # TODO: decide if this is always an int or not
        self.location: 'Room' = room
        
        weapon_damage = random.randint(5, 20)
        weapon = Weapon(f'{self.name}_sword', f'a sword taken from the body of {self.name}', weapon_damage)
        self.weapon: Weapon = weapon
        
        armor_value = random.randint(1, 12)
        armor = Armor(f'{self.name}_armor', f'armor taken from the body of {self.name}', armor_value)
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
    
    def drop_coins(self):
        this_room: 'Room' = self.location
        coins_in_this_room = 0
        for item in this_room.items:
            if item.item_type == 'coins':
                coins_in_this_room += item.value  # sum the coins in the room
                this_room.remove_item(item)  # ...and make sure to not duplicate coins :)
        
        coins_in_this_room += random.randint(1, 7)  # add the monster's dropped coins
        
        self.location.add_item(Coins(coins_in_this_room))
    
    def die(self):
        self.location.add_item(self.weapon)
        self.location.add_item(self.armor)
        self.drop_coins()
        
        if random.random() < 0.4:  # random chance to drop a healing potion
            heal_val = random.choice([15, 20, 25, 30, 35])  # picks a random healing value
            self.location.add_item(Potion(heal_val))
        
        self.location.remove_monster(self)
        updater.deregister(self)
    
    def attack(self, person: 'Player'):
        attack_damage = self.weapon.damage
        person.get_hit(attack_damage)
    
    def get_hit(self, damage_amount: int):
        actual_damage = damage_amount - self.armor.defense
        self.health -= actual_damage
