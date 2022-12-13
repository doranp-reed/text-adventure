import random
import updater
from names import get_first_name
from item import Weapon, Armor, Coins, Potion, WinCondition


class Monster:
    monster_type = 'monster'

    def __init__(self, health: int, room: 'Room'):  # TODO: decide on if hints should be in arguments or values        
        self.name: str = get_first_name().lower()
        self.health: int = health  # TODO: decide if this is always an int or not
        self.location: 'Room' = room
        
        weapon_damage = random.randint(5, 12)
        weapon = Weapon(f'{self.name}_sword', f'a sword taken from the body of {self.name}', weapon_damage)
        self.weapon: Weapon = weapon
        
        armor_value = random.randint(1, 8)
        armor = Armor(f'{self.name}_armor', f'armor taken from the body of {self.name}', armor_value)
        self.armor: Armor = armor
        
        room.add_monster(self)
        updater.register(self)

    def __repr__(self):
        return f'{self.name} the {self.monster_type}'

    def update(self):
        pass  # generic monsters have no update & don't roam by default
    
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
        if random.random() < 0.3:  # random chance to drop weapon
            self.location.add_item(self.weapon)
        
        if random.random() < 0.3:  # same for armor
            self.location.add_item(self.armor)
        
        if random.random() < 0.3:  # ...and same for potions
            heal_val = random.choice([15, 20, 25, 30, 35])  # picks a random healing value
            self.location.add_item(Potion(heal_val))
        
        self.drop_coins()
        
        self.location.remove_monster(self)
        updater.deregister(self)
    
    def attack(self, person: 'Player'):
        attack_damage = self.weapon.damage
        person.get_hit(attack_damage)
    
    def get_hit(self, damage_amount: int):
        actual_damage = damage_amount - self.armor.defense
        self.health -= max(actual_damage, 0)  # so there's no "healing"


class Roamer(Monster):  # roamers are lower-health and move around
    monster_type = 'roamer'
    
    def move_to(self, room: 'Room'):
        if room.has_merchant:  # monsters can't move into merchant room
            return  # this does mean that monsters may "pile up" outside the merchant room , but I like that idea

        self.location.remove_monster(self)
        self.location = room
        room.add_monster(self)
    
    def update(self):  # defining feature is that they move from room to room
        self.move_to(self.location.random_neighbor())


class Guardian(Monster):  # there is only one guardian, and it holds the win condition
    def __init__(self, health, room):
        self.health = health
        self.location: 'Room' = room
        self.name = get_first_name().lower()
        
        weapon_damage = random.randint(15, 25)  # TODO: balance this (this seems really unbalanced)
        weapon = Weapon(f'{self.name}_sword', f'a sword taken from the body of the scroll\'s guardian', weapon_damage)
        self.weapon: Weapon = weapon

        armor_value = random.randint(10, 15)
        armor = Armor(f'{self.name}_armor', f'armor taken from the body of the scroll\'s guardian', armor_value)
        self.armor: Armor = armor

        room.add_monster(self)
        updater.register(self)
    
    def die(self):
        # the item drops are big because this is the final boss: if the player wants to they can continue to play
        # with these powerful items, but they've already won the game so it's fine to make the items too strong
        
        self.location.add_item(self.weapon)
        self.location.add_item(self.armor)
        for _ in range(3):
            self.location.add_item(Potion(100))

        self.drop_coins()
        
        self.location.add_item(WinCondition('scroll', 'This scroll contains potentially wonderous knowledge...'))

        self.location.remove_monster(self)
        updater.deregister(self)


class Entrapper(Monster):
    pass  # TODO
