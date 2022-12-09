from clear import clear
from typing import Optional
from names import get_first_name
import updater
from item import Weapon, Armor


class Player:
    def __init__(self):
        self.location: Optional['Room'] = None  # TODO: see if I can stop the linter from warning here
        self.items: list['Item'] = []  # TODO: decide on if I need the quotes or not
        self.health: int = 50  # TODO: decide if this will always be an int
        self.max_health = 50
        self.alive: bool = True
        self.name: str = get_first_name().lower()  # random name
        self.weapon = Weapon('Doran_blade', 'a basic sword', 10)  # TODO: balance damage and stuff
        self.armor = Armor('Doran_shield', 'a basic shield strapped to your body', 5)
        self.coins: int = 5
        updater.register(self)

    def __repr__(self):
        ret_str = f'{self.name}, {self.health} health\n'
        ret_str += f'{self.weapon}\n{self.armor}\n'

        if len(self.items) > 0:
            ret_str += 'Items:'
            for item in self.items:
                ret_str += f' {item.name}'
        else:
            ret_str += 'No items in inventory.'

        return ret_str

    # goes in specified direction if possible, returns True
    # if not possible returns False
    def go_direction(self, direction: str):
        new_location = self.location.get_destination(direction.lower())
        if new_location is not None:
            self.location = new_location
            return True
        return False

    def pickup(self, item: 'Item'):
        self.add_item(item)
        self.location.remove_item(item)
    
    def remove_item(self, item):
        self.items.remove(item)
    
    def add_item(self, item: 'Item'):
        self.items.append(item)
    
    def heal(self, amount: int):
        # old_hp = self.health
        self.health += amount
        self.health = min(self.health, self.max_health)  # there's an instant where you're over max hp, but whatever

    def get_item_by_name(self, name: str):
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
            return False

    def drop(self, item: 'Item'):  # TODO: implement error handling
        self.remove_item(item)
        self.location.add_item(item)

    def show_inventory(self):  # TODO: make cleaner
        clear()
        if len(self.items) != 0:
            print("You are currently carrying:\n")
            for i in self.items:
                print(i.name)
        else:
            print('You are currently carrying no items.')
        input("\nPress enter to continue...")

    def attack(self, mon: 'Monster'):
        attack_damage = self.weapon.damage
        mon.get_hit(attack_damage)
    
    def get_hit(self, damage_amount: int):
        actual_damage = damage_amount - self.armor.defense
        self.health -= actual_damage
    
    def update(self):
        self.heal(1)
    
    def die(self):
        self.alive = False
        updater.deregister(self)  # TODO: is this actually necessary? and does it matter either way?
