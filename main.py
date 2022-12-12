from room import Room
from player import Player
from item import Item, WinCondition
from monster import Monster
import updater
from time import sleep
from os import system as os_system  # only import what you need
from os import name as os_name


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
                'use': '<item> -- uses item in inventory'}


def create_world():
    a = Room("room 1")
    b = Room("room 2")
    c = Room("room 3")
    d = Room("room 4")
    Room.connect_rooms(a, "east", b, "west")
    Room.connect_rooms(c, "east", d, "west")
    Room.connect_rooms(a, "north", c, "south")
    Room.connect_rooms(b, "north", d, "south")
    i1 = Item("rock", "This is just a rock.")
    i1.put_in_room(b)
    i2 = Item('stick', 'it\'s a stick!')
    i2.put_in_room(c)
    i3 = WinCondition('medal', 'Win the game!')
    i3.put_in_room(d)
    player.location = a
    Monster(20, b)


def clear():
    os_system('cls' if os_name == 'nt' else 'clear')


def enter_to_continue():  # If I ever decide to change the message, I only need to change one thing
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
            # print('If there is no room in the given direction, you will not be moved anywhere.')

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
            print('Enter \'use <item>\' to use an item. Note that it must be in your inventory first.')

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
    sleep(2)
    clear()

    while player.alive:
        print_situation()
        # I removed the `command_success` and second while loop in favor of a bunch of continue statements

        original_command: str = input("What now? ('help' for list of options) ")  # sometimes this value is still needed
        clean_command: str = string_cleaner(original_command)
        if len(clean_command) == 0:
            continue  # error handling so I don't call `split()` on an empty string

        command_words: list[str] = clean_command.split()
        if len(command_words) == 0:
            continue
        
        if len(command_words) > 2:  # no commands are more than two words total (verb and object)
            print_status_update("print('Sorry, too many directions given.')")
            continue

        match command_words[0]:
            case 'g' | "go":
                okay = player.go_direction(command_words[1])
                if not okay:
                    print_status_update('print("You can\'t go that way.")')
                    continue

            case 't' | "take":                
                if len(command_words) == 2:  # take a specific item
                    target_name = command_words[1]
                    item: Item | bool = player.location.get_item_by_name(target_name)
                    if item is not False:
                        player.pickup(item)
                    else:
                        print_status_update(f'print("There is no item named \"{target_name}\" in this room.")')
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
                target_name = command_words[1]
                item: Item | bool = player.get_item_by_name(target_name)
                if item is not False:
                    player.drop(item)
                else:
                    print_status_update(f'print("There is no item named \"{target_name}\" in your inventory.")')
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
                continue

            case 'i' | 'inv':
                clear()
                if len(player.items) != 0:
                    print("You are currently carrying:\n")
                    for i in player.items:
                        print(i.name)
                else:
                    print('You are currently carrying no items.')
                enter_to_continue()
                continue

            case 'h' | 'help':
                if len(command_words) == 1:
                    show_help()
                else:
                    show_long_help(command_words[1])
                continue

            case 'q' | "quit":
                break  # breaks out of the `while player.alive` loop

            case 'f' | "fight":
                target_name = command_words[1]
                monster: Monster | bool = player.location.get_monster_by_name(target_name)
                if monster is False:
                    print_status_update(f'print("There is no monster named \"{target_name}\" in this room.")')
                    continue
                # else...  # TODO: modify if I change how I deal with `continue`
                while True:
                    clear()
                    print(f'You are fighting {monster}.')
                    print(f'You have {player.health} health, {monster} has {monster.health} health.')
                    player.attack(monster)
                    if monster.health <= 0:
                        monster.die()
                        print(f'You attack {monster}. It dies!')
                        enter_to_continue()
                        break
                    monster.attack(player)
                    if player.health <= 0:
                        player.die()
                        print(f'Oh no! {monster} killed you!')
                        enter_to_continue()
                        break
                    # else...
                    print(f'You attack {monster}. It attacks back!')
                    # TODO: add a way of escaping combat, and make it clearer how much damage you take/deal
                    enter_to_continue()
            
            case 'dev':  # for my testing (so I can see in real-time stuff like the player's hp)
                my_command = original_command[4:]
                exec(my_command)
                enter_to_continue()
                continue
            
            case 'l' | 'look':
                if len(command_words) < 2:
                    print_status_update('print("No item given to look at.")')
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
                target_name = command_words[1]
                item: 'Item | Potion | bool' = player.get_item_by_name(target_name)
                if not item:  # so it's not in the inventory
                    print_status_update(f'print("There is no item named {target_name} in your inventory.")')
                    continue
                # else...
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
                        print('Congratulations! You win!')  # TODO: change if victory condition changes (story-wise)
                        break
                    
                    case _:
                        error_message = 'print(\"Not a valid target: please select a weapon, armor, potion, or medal.")'
                        # TODO: change above line if win con changes
                        print_status_update(error_message)  # this is so my lines aren't too long
                        continue

            case _:  # other cases
                print("Not a valid command ('help' for a list of options)")
                enter_to_continue()
                continue

        # outside of the `match-case` block, but still in the `while` loop
        updater.update_all()  # TODO: decide on how I want to do updating
    
    # outside of the `while` loop, but still in the `if __name__ == "__main__"` block
    if player.alive:
        print('Goodbye!\n')
    else:
        print('You died. The end!\n')
