from clear import clear
from typing import Optional
from names import get_first_name
import updater


class Player:
    def __init__(self):
        self.location: Optional['Room'] = None  # TODO: see if I can stop the linter from warning here
        self.items: list['Item'] = []  # TODO: decide on if I need the quotes or not
        self.health: int = 50  # TODO: decide if this will always be an int
        self.alive: bool = True
        self.name: str = get_first_name().lower()  # random name
        updater.register(self)

    def __repr__(self):
        ret_str = f'{self.name}, {self.health}HP\n'

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
        self.items.append(item)
        item.location = self
        self.location.remove_item(item)

    def get_item_by_name(self, name: str):
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
            return False

    def drop(self, item: 'Item'):  # TODO: implement error handling
        self.items.remove(item)
        item.location = self.location
        self.location.add_item(item)

    def show_inventory(self):
        clear()
        if len(self.items) != 0:
            print("You are currently carrying:\n")
            for i in self.items:
                print(i.name)
        else:
            print('You are currently carrying no items.')
        input("\nPress enter to continue...")

    def attack_monster(self, mon: 'Monster'):
        clear()
        print("You are attacking " + mon.name)
        print()
        print("Your health is " + str(self.health) + ".")
        print(mon.name + "'s health is " + str(mon.health) + ".")
        print()
        if self.health > mon.health:
            self.health -= mon.health
            print("You win. Your health is now " + str(self.health) + ".")
            mon.die()
        else:
            print("You lose.")
            self.alive = False
        print()
        input("Press enter to continue...")
    
    def update(self):
        if self.health < 50:
            self.health += 1
