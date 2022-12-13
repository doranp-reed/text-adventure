from room import Room, Shop, Trap, Nest, Lair
from player import Player
from item import Item, Weapon, Armor, Potion
from monster import Monster
import updater
from time import sleep
from os import system as os_system  # only import what you need
from os import name as os_name
from random import random as random_random


player = Player()
command_help = {'help': '[command] -- prints list of options or help on given command',
                'go': '<direction> -- moves you in the given direction',
                'inv': '-- opens your inventory',
                'take': '[item] -- picks up the given item (default takes all items)',
                'quit': '-- quits the game',
                'fight': '<monster name> -- fights the given monster',
                'drop': '<item> -- drops the given item',
                'wait': '[rounds] -- waits the given number of rounds (default 1)',
                'me': '-- shows information about you: name, health, items, etc.',
                'look': '<item> -- looks at an item in the room or inventory',
                'use': '-- uses an item in inventory',
                'about': '-- gives information about the game',
                'shop': '-- shows items for purchase from the merchant (if in the room)'}


def create_world():
    # temp names are location: 3x3 grid, 'sw' = southwest room
    
    nw = Shop('Gregor\'s shop!')
    n = Room('the north room.')
    ne = Lair('the scroll guardian\'s lair!')
    w = Room('the west room.')
    c = Room('the central room.')
    e = Room('the east room.')
    sw = Nest('the roamer\'s nest!')
    s = Room('the south room.')
    se = Trap('an entrapping room!')  # TODO: better name?
    
    # now I connect a lot of rooms...
    Room.connect_rooms(nw, 'south', w, 'north')
    Room.connect_rooms(w, 'south', sw, 'north')
    Room.connect_rooms(w, 'east', c, 'west')
    
    Room.connect_rooms(ne, 'west', n, 'east')
    Room.connect_rooms(n, 'south', c, 'north')
    
    Room.connect_rooms(se, 'north', e, 'south')
    Room.connect_rooms(e, 'west', c, 'east')
    
    Room.connect_rooms(c, 'south', s, 'north')
    
    # dud items for the fun of it
    Item('rock', 'just a rock').put_in_room(w)
    Item('stick', 'it\'s a stick').put_in_room(n)
    
    player.location = s
    
    for _ in range(2):
        updater.update_all()  # spawn a couple of random roamers to start the game


def clear():
    os_system('cls' if os_name == 'nt' else 'clear')


def enter_to_continue():  # If I ever decide to change the message, I only need to change one thing
    """Press enter to continue..."""
    input('\nPress enter to continue...')


def print_situation():
    clear()
    print(f'You are in {player.location.desc}\n')
    if player.location.has_monsters():
        print("This room contains the following monsters:")
        for m in player.location.monsters:
            print(m)
        print()
    if player.location.has_items():
        print("This room contains the following items:")
        for each_item in player.location.items:
            print(each_item.name)
        print()
    print("You can go in the following directions:")
    for e in player.location.exit_names():
        print(e)
    print()


def print_status_update(update: str):
    clear()
    exec(update)
    enter_to_continue()


def show_help():
    clear()
    for key in command_help:
        print(key, command_help[key])
    print('\nYou can also use the first letter of any command instead of the full name (e.g. i for inv).')
    enter_to_continue()


def show_long_help(comm: str):
    clear()
    match comm:

        case 'help':
            print('The \'help\' or \'h\' command is used to learn more about the different commands.')
            print('Enter \'help\' to see a list of commands,')
            print('or \'help [command]\' to see more information about a command.')

        case 'go':
            print('The \'go\' or \'g\' command is used to move between rooms.')
            print('Enter \'go <direction>\' to move to the room in the given direction.')
            print('The direction can either be a full name, like \'north\', or a single letter, like \'n\'.')

        case 'inv':
            print('The \'inv\' or \'i\' command is used to see your inventory.')
            print('Enter \'inv\' to list its contents.')

        case 'take':
            print('The \'take\' or \'t\' command is used to take an item that is in the room.')
            print('Enter \'take [item]\' to take an item from the room and put it in your inventory, or')
            print('enter \'take\' to take all items from the room.')

        case 'quit':
            print('The \'quit\' or \'q\' command is used to quit the game.')
            print('Note that your state is not saved, so any progress will be lost.')  # TODO: change if this changes

        case 'fight':
            print('The \'fight\' or \'f\' command is used to fight a monster in the room.')
            print('Enter \'fight <monster>\' to fight a monster;')
            print('both you and the monster will attack each other, and if the monster dies they\'ll drop their stuff.')
            print('Note that you only need to specify the monster\'s first name.')

        case 'drop':
            print('The \'drop\' or \'d\' command is used to drop an item from your inventory.')
            print('Enter \'drop <item>\' to remove the given item from your inventory and put it in the current room.')
        
        case 'wait':
            print('The \'wait\' or \'w\' command is used to wait for a given number of rounds.')
            print('Time passes when you do some things (like move between rooms), so with this you can wait in place.')
            print('Enter \'wait [rounds]\' to wait for the given number of rounds (default 1 round).')
        
        case 'me':
            print('The \'me\' or \'m\' command is used to see information about you, the player.')
            print('Enter \'me\' to see things like your health, items, and other attributes.')  # TODO: add other stuff?
        
        case 'look':
            print('The \'look\' or \'l\' command is used to look at an item and view its properies.')
            print('Enter \'look <item>\' to see what an item does.')
            print('This can be done on an item in the room or in your inventory.')
        
        case 'use':
            print('The \'use\' or \'u\' command is for using an item in your inventory.')
            print('If given a potion, it will consume the potion and heal you;')
            print('If given a weapon or armor, it will equip that and remove your current weapon or armor.')
            print('Enter \'use\' to see usable items in your inventory, then enter the item\'s name to use it.')
            print('Note that the item must be in your inventory to be used.')
        
        case 'about':
            print('The \'about\' or \'a\' command is used to see information about the game.')
            print('Enter \'about\' to see why you\'re here, as well as credits to all who helped!')
        
        case 'shop':
            print('The \'shop\' or \'s\' command is used to purchase items from a merchant.')
            print('Enter \'shop\' to open a menu where you can see what the merchant has available and select an item.')
            print('If you have enough money the merchant will take your money and give you the requested item.')

        case _:
            print(f'Sorry, there is no information available for {comm}')

    enter_to_continue()


def string_cleaner(com: str) -> str:
    ret = ''
    good_chars = 'abcdefghijklmnopqrstuvwxyz_ 0123456789'  # note that this has a space, so that's not removed
    for symbol in com.lower():
        if symbol in good_chars:
            ret += symbol
    return ret


if __name__ == "__main__":
    create_world()
    clear()

    print('Welcome to the dungeon!')
    print('Be very careful: a single wrong keystroke could end your time here!\n')
    player.name = input("What is your name? ")
    print('\nWelcome, ' + player.name + '!')
    sleep(1.5)
    clear()

    while player.alive:
        print_situation()
        # I removed the `command_success` and second while loop in favor of a bunch of continue statements
        # the updater triggers after a successful command, even if the command doesn't affect anything (like 'me')
        # exceptions are 'help', 'about', and 'dev'

        original_command: str = input("What now? ('help' for list of options) ")  # sometimes this value is still needed
        clean_command: str = string_cleaner(original_command)
        if len(clean_command) == 0:
            continue  # error handling so I don't call `split()` on an empty string

        command_words: list[str] = clean_command.split()
        if len(command_words) == 0:
            continue
        
        # no commands are more than two words total (verb and object), except for 'dev' commands (which are special)
        if (len(command_words) > 2) and command_words[0] != 'dev':
            print_status_update("print('Sorry, too many directions given.')")
            continue
        
        def has_more_than_one_word(message: str):  # check if enough words were used for a command
            if len(command_words) < 2:
                print_status_update(f'print("{message}")')  # ths string combination here is a bit wacky, but it works
                return False
            return True

        match command_words[0]:
            case 'g' | "go":
                if has_more_than_one_word('Please enter a direction to go.') is False:
                    continue
                
                if (player.location.room_type == 'trap') and player.location.has_monsters():  # trap room with monsters
                    print_status_update('print("You can\'t leave - the entrappers are blocking your way!")')
                    continue
                
                if not (command_words[1] in player.location.valid_directions):
                    print_status_update('print("That\'s not a valid direction! Go north, south, east, or west.")')
                    continue
                
                okay = player.go_direction(command_words[1])
                if not okay:
                    print_status_update('print("There\'s a wall there!")')
                    continue

            case 't' | "take":                
                if len(command_words) == 2:  # take a specific item
                    target_name = command_words[1]
                    item: Item | bool = player.location.get_item_by_name(target_name)
                    if item is not False:
                        player.pickup(item)
                    else:
                        # the triple-backslash is so that the string passed to `exec` will have `\"`
                        # (I need to escape the backslash, then escape the quote. `exec` is weird)
                        print_status_update(f'print("There is no item named \\\"{target_name}\\\" in this room.")')
                        continue
                else:  # only 'take' was given, so take all
                    if len(player.location.items) == 0:
                        print_status_update('print(There are no items in this room.)')
                        continue
                    else:
                        clear()
                        while len(player.location.items) > 0:  # while the room has at least one item
                            item: Item = player.location.items[0]
                            player.pickup(item)
                            print(f'took {item.name}')
                        enter_to_continue()

            case 'd' | 'drop':
                if has_more_than_one_word('Please enter an item to drop.') is False:
                    continue
                
                target_name = command_words[1]
                item: Item | bool = player.get_item_by_name(target_name)
                if item is not False:
                    player.drop(item)
                else:
                    print_status_update(f'print("There is no item named \\\"{target_name}\\\" in your inventory.")')
                    continue

            case 'w' | 'wait':
                numb_of_turns = 1
                if len(command_words) > 1:
                    numb_of_turns = int(command_words[1])  # TODO: error handling here
                for time in range(numb_of_turns):
                    updater.update_all()
                    continue  # this is because we already waited the necessary number of rounds

            case 'm' | 'me':
                print_status_update('print(player)')

            case 'i' | 'inv':
                clear()
                if len(player.items) != 0:
                    print("You are currently carrying:\n")
                    for i in player.items:
                        print(i.name)
                else:
                    print('You are currently carrying no items.')
                enter_to_continue()

            case 'h' | 'help':
                if len(command_words) == 1:
                    show_help()
                else:
                    show_long_help(command_words[1])
                continue

            case 'q' | 'quit':
                print('Goodbye!\n')
                break  # breaks out of the `while player.alive` loop

            case 'f' | 'fight':
                if has_more_than_one_word('Please enter a monster to fight.') is False:
                    continue
                
                target_name = command_words[1]
                monster: Monster | bool = player.location.get_monster_by_name(target_name)
                if monster is False:
                    print_status_update(f'print("There is no monster named \\\"{target_name}\\\" in this room.")')
                    continue
                # else...  # TODO: modify if I change how I deal with `continue`
                
                if monster.name == 'doran':  # easter egg! (small chance that monster spawns with name 'doran') :)
                    print('\nWait, what? You\'re trying to fight the creator of this game?')
                    input('As you wish...')
                
                fighting = True
                while fighting:
                    clear()
                    print(f'You are fighting {monster}.')
                    print(f'You have {player.health} health, {monster} has {monster.health} health.')
                    player.attack(monster)
                    if monster.health <= 0:
                        monster.die()
                        print(f'You attack {monster}. It dies!')
                        if monster.name == 'doran':
                            print('\nDid you just... kill him? How can this be? What have you done?')
                        enter_to_continue()
                        break
                    monster.attack(player)
                    if player.health <= 0:
                        player.die()
                        if monster.name == 'doran':
                            print('\nHa! That\'ll teach you to never mess with your maker!\n')
                        print(f'Oh no! {monster} killed you!')
                        enter_to_continue()
                        break
                    # else...
                    print(f'You attack {monster}. It attacks back!\n')
                    print(f'You now have {player.health} health, {monster} has {monster.health} health.')
                    if player.location.room_type == 'trap':
                        print('You must keep fighting: the entrapper won\'t let you get away!')
                        enter_to_continue()
                    else:
                        while True:
                            keep_fighting = input('Do you want to keep fighting? (Y/n) ')
                            if keep_fighting.lower() == 'y' or keep_fighting.lower() == '':
                                break  # this breaks out of the 'want to keep fighting?' loop, not the outer fight loop
                            if keep_fighting.lower() == 'n':
                                fighting = False
                                break  # same comment here
                    # TODO: add a way of escaping combat, and make it clearer how much damage you take/deal
            
            case 'dev':  # for my testing (so I can see in real-time stuff like the player's hp)
                my_command = original_command[4:]
                exec(my_command)
                enter_to_continue()
                continue
            
            case 'l' | 'look':
                if has_more_than_one_word('Please enter an item to look at.') is False:
                    continue
                
                target_name = command_words[1]
                item: type[Item] | bool = player.get_item_by_name(target_name)
                if not item:  # so it's not in the inventory
                    item = player.location.get_item_by_name(target_name)
                if not item:  # so it's not in the room either
                    print_status_update(f'print("There is no item named {target_name} in the room or your inventory.")')
                    continue
                else:
                    print_status_update('print(item)')
            
            case 'u' | 'use':
                clear()
                usable_items: list[type[Item]] = [i for i in player.items if i.usable]  # list of all the `usable` items
            
                if not usable_items:  # if the list is empty (no usable items)
                    clear()
                    print('There are no usable items in your inventory.')
                    print('Usable items include: potions, armor, weapons, and scrolls.')
                    enter_to_continue()
                    continue
                
                # else...
                for index, item in enumerate(usable_items):
                    print(str(index+1), item)  # note that this starts at 1, so other numbers are modified as such
                target_item_index: str = input('\nWhat would you like to use? (enter the item number) ')
                
                # this next part I had to do because if you call `int` on a non-int it'll throw an error, so instead
                # I decided to compare the input to other strings
                valid_options: list[str] = [str(x+1) for x in range(len(usable_items))]
                
                if target_item_index not in valid_options:  # so it's not a number within the required range
                    print(f'\"{target_item_index}\" is not a valid item number.')
                    enter_to_continue()
                    continue
                
                # else...                
                item: type[Item] = usable_items[int(target_item_index) - 1]  # minus 1 because input is 1-n
                item_type: str = item.item_type
                match item_type:
                    case 'potion':
                        old_hp = player.health  # this is for the status update
                        player.heal(item.heal_value)
                        player.remove_item(item)
                        print_status_update("print(f'You healed from {old_hp} health to {player.health} health!')")
                    
                    case 'armor':
                        old_armor = player.armor
                        new_armor = item
                        
                        player.remove_item(new_armor)  # removes new_armor from standard inventory
                        player.armor = new_armor
                        
                        player.add_item(old_armor)  # adds old_armor to standard inventory
                        print_status_update("print(f'You equipped {new_armor.name}.')")
                    
                    case 'weapon':
                        old_weapon = player.weapon
                        new_weapon = item
                        
                        player.remove_item(new_weapon)  # removes new_weapon from standard inventory
                        player.weapon = new_weapon
                        
                        player.add_item(old_weapon)  # adds old_weapon to standard inventory
                        print_status_update("print(f'You equipped {new_weapon.name}.')")
                    
                    case 'victory':
                        print('You unwind the scroll and begin to read its contents.')
                        sleep(3)
                        print('A blue mist begins to swirl around you and your eyes move across the lines,')
                        sleep(2)
                        print('faster and faster as you begin to understand,')
                        sleep(1)
                        print('to learn this knowledge forbidden to mortals...\n')
                        sleep(5)
                        print('Congratulations! You have conquered the dungeon and learned the secrets of immortality!')
                        sleep(1)
                        print('You win the game!')
                        sleep(1)
                        print('\nThe End')
                        break
                    
                    case _:  # this should never trigger
                        print('Oops! Something went wrong, contact your local developer to get it fixed!')  # :)
                        break

            case 'a' | 'about':
                clear()
                print('Welcome to the dungeon!')
                print('You are a brave adventurer, here to defeat monsters in your path')
                print('and find the legendary scroll of wisdom, said to give the knowledge')
                print('of immortality to any who reads it.\n')
                print('This game was made by Doran with help from TaiyuC,')
                print('as an assignment for professor Dylan McNamee\'s class.')
                print('See all who helped make this game possible on the GitHub page:')
                print('https://github.com/doranp-reed/text-adventure')
                enter_to_continue()
                continue
            
            case 's' | 'shop':
                if player.location.room_type != 'shop':
                    print_status_update("print('You are not in a room with a merchant, you cannot shop!')")
                    continue
                # else...
                
                clear()
                print('Gregor: Welcome to my humble store! You\'re lucky you found me in this dark place.')
                print('Gregor: Here you can buy some weapons and armor, as well as potions for the road ahead.')
                print('And don\'t think of trying to sell me anything: I ain\'t dumb enough to buy what you\'ve got!')
                print('Here\'s what I\'ve got!\n')
                # maybe sometime later I'd add the ability to sell to him, but right now you can just buy
                
                shop_weapon = Weapon('generic_sword', 'a sword bought from Gregor the merchant', 20)
                shop_armor = Armor('generic_armor', 'armor bought from Gregot the merchant', 10)
                pot_15 = Potion(15)
                pot_25 = Potion(25)
                pot_35 = Potion(35)
                
                item_list: list[list[Item, int]] = [[shop_weapon, 50],
                                                    [shop_armor, 50],
                                                    [pot_15, 15],
                                                    [pot_25, 25],
                                                    [pot_35, 35]]
                
                for index, item in enumerate(item_list):
                    print(f'{index+1} {item[0]}: {item[1]} coins')  # getting type error here, but seems to be fine?
                
                request = input(f'\nYou have {player.coins} coins.\nWhat would you like to buy? (enter item number) ')
                
                valid_options: list[str] = [str(x+1) for x in range(len(item_list))]  # this is like in 'use' section
                
                if request not in valid_options:
                    print(f'Are you crazy? There\'s no item numbered \"{request}\"!')
                    enter_to_continue()
                    continue
                
                # else...
                request_index = int(request) - 1
                requested_item: list = item_list[request_index]  # note that this is the item-cost list, not the item
                
                item_cost = requested_item[1]
                
                if item_cost > player.coins:
                    print(f'What are you trying to pull? You only have {player.coins} coins! You need {item_cost}!')
                    enter_to_continue()
                    continue
                # else...
                player.remove_coins(item_cost)
                player.add_item(requested_item[0])  # TODO: make sure this works!
                print(f'Gregor: Here\'s your {requested_item[0]}! Good doing business with you!')
                enter_to_continue()
            
            case _:  # other cases
                print("Not a valid command ('help' for a list of options)")
                enter_to_continue()
                continue

        # outside of the `match-case` block, but still in the `while` loop
        if random_random() < 0.5:  # decide to make updates less frequent
            updater.update_all()
    
    # outside of the `while` loop, but still in the `if __name__ == "__main__"` block
    if not player.alive:
        print('You died. The end!\n')
