import os
from typing import Optional


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


class Player:
    def __init__(self):
        self.location: Optional["Room"] = None  # TODO: see if I can stop the linter from warning here
        self.items = []
        self.health: int = 50  # TODO: decide if this will always be an int
        self.alive: bool = True
    # goes in specified direction if possible, returns True
    # if not possible returns False

    def go_direction(self, direction: str):
        new_location = self.location.get_destination(direction.lower())
        if new_location is not None:
            self.location = new_location
            return True
        return False

    def pickup(self, item):
        self.items.append(item)
        item.loc = self
        self.location.remove_item(item)

    def show_inventory(self):
        clear()
        print("You are currently carrying:")
        print()
        for i in self.items:
            print(i.name)
        print()
        input("Press enter to continue...")

    def attack_monster(self, mon):
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
