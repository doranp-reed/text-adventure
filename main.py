from room import Room
from player import Player
from item import Item, Potion
from monster import Monster
import updater
from clear import clear
from time import sleep

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
                'insp': '<item> -- inspects an item in the room or inventory',
                'use': '<item> -- uses item in inventory'}


def create_world():
    a = Room("You are in room 1.")
    b = Room("You are in room 2.")
    c = Room("You are in room 3.")
    d = Room("You are in room 4.")
    Room.connect_rooms(a, "east", b, "west")
    Room.connect_rooms(c, "east", d, "west")
    Room.connect_rooms(a, "north", c, "south")
    Room.connect_rooms(b, "north", d, "south")
    i1 = Item("rock", "This is just a rock.")
    i1.put_in_room(b)
    i2 = Item('stick', 'it\'s a stick!')
    i2.put_in_room(c)
    i3 = Item('medal', 'Win the game!')
    i3.put_in_room(d)
    i4 = Potion('medium_potion', 'heal 20 hitpoints', 20)
    i5 = Potion('small_potion', 'heal 10 hitpoints', 10)
    i6 = Potion('large_potion', 'heal 30 hitpoints', 30)
    i4.put_in_room(a)
    i5.put_in_room(b)
    i6.put_in_room(c)
    player.location = a
    Monster(20, b)


def print_situation():
    clear()
    print(player.location.desc)
    print()
    if player.location.has_monsters():
        print("This room contains the following monsters:")
        for m in player.location.monsters:
            print(m)
        print()
    if player.location.has_items():
        print("This room contains the following items:")
        for i in player.location.items:
            print(i.name)
        print()
    print("You can go in the following directions:")
    for e in player.location.exit_names():
        print(e)
    print()


def print_status_update(update: str):
    clear()
    exec(update)
    input('\nPress enter to continue...')


def show_help():
    clear()
    for key in command_help:
        print(key, command_help[key])
    print()
    input("Press enter to continue...")


def show_long_help(comm: str):
    clear()
    match comm:

        case 'help':
            print('The \'help\' command is used to learn more about the different commands.')
            print('Enter \'help\' to see a list of commands,')
            print('or \'help [command]\' to see more information about a command.')

        case 'go':
            print('The \'go\' command is used to move between rooms.')
            print('Enter \'go <direction>\' to move to the room in the given direction.')
            # print('If there is no room in the given direction, you will not be moved anywhere.')

        case 'inv':
            print('The \'inv\' command is used to see your inventory.')
            print('Enter \'inv\' to list its contents.')

        case 'take':
            print('The \'take\' command is used to take an item that is in the room.')
            print('Enter \'take [item]\' to take an item from the room and put it in your inventory, or')
            print('enter \'take\' to take all items from the room.')

        case 'quit':
            print('The \'quit\' command is used to quit the game.')
            print('Note that your state is not saved, so any progress will be lost.')  # TODO: change if this changes

        case 'fight':
            print('The \'fight\' command is used to fight a monster in the room.')
            print('Enter \'fight <monster>\' to fight a monster;')
            print('if you win the monster is killed, if you lose you die.')
            print('Note that you only need to specify the monster\'s first name.')

        case 'drop':
            print('The \'drop\' command is used to drop an item from your inventory.')
            print('Enter \'drop <item>\' to remove the given item from your inventory and put it in the current room.')
        
        case 'wait':
            print('The \'wait\' command is used to wait for a given number of rounds.')
            print('Time passes when you do some things (like move between rooms), so with this you can wait in place.')
            print('Enter \'wait [rounds]\' to wait for the given number of rounds (default 1 round).')
        
        case 'me':
            print('The \'me\' command is used to see information about you, the player.')
            print('Enter \'me\' to see things like your health, items, and other attributes.')  # TODO: add other stuff?
        
        case 'insp':
            print('The \'insp\' command is used to inspect an item and view its properies.')
            print('Enter \'insp <item>\' to see what an item does.')
            print('This can be done on an item in the room or in your inventory.')
        
        case 'use':
            print('The \'use\' command is for using an item in your inventory.')
            print('If given a potion, it will consume the potion and heal you;')
            print('If given a weapon or armor, it will equip that and remove your current weapon or armor (if any).')
            print('Enter \'use <item>\' to use an item. Note that it must be in your inventory first.')

        case _:
            print(f'Sorry, there is no information available for {comm}')

    input('\nPress enter to continue...')


def string_cleaner(com: str) -> str:
    ret = ''
    good_chars = 'abcdefghijklmnopqrstuvwxyz_ 0123456789'  # note that this has a space, so that's not removed
    for symbol in com.lower():
        if symbol in good_chars:
            ret += symbol
    return ret


def too_many_commands():
    print('Sorry, too many directions given.')
    input("Press enter to continue...")


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

        original_command = input("What now? ('help' for list of options) ")  # sometimes this string is still needed
        clean_command = string_cleaner(original_command)
        if len(clean_command) == 0:
            continue

        command_words = clean_command.split()  # note that, although it's called `command_words`, it includes others too
        if len(command_words) == 0:
            continue

        match command_words[0]:
            case "go":  # now 'go' is well-handled (by my standards)
                if len(command_words) > 2:  # TODO: decide if *any* commands will use more than 2 words, and if so
                    too_many_commands()     # move this functionality outside of the individual cases
                    continue
                okay = player.go_direction(command_words[1])
                if not okay:
                    print("You can't go that way.")
                    print('\nPress enter to continue...')
                    continue

            case "take":
                if len(command_words) > 2:  # too many keywords
                    too_many_commands()
                    continue
                
                if len(command_words) == 2:  # take a specific item
                    target_name = command_words[1]
                    monster = player.location.get_item_by_name(target_name)
                    if monster is not False:
                        if monster.name == 'medal':
                            print('Congradulations! You win!')
                            playing = False
                        player.pickup(monster)
                    else:
                        print_status_update('print("No such item.")')
                        # clear()
                        # print_situation()  # TODO: figure out if this is a mistake or what
                        continue
                else:  # take all
                    total_items = len(player.location.items)
                    if total_items != 0:
                        clear()
                        print()
                        for _ in range(total_items):  # this is to avoid modifying the iterated list while iterating
                            item: Item = player.location.items[0]
                            if item.name == 'medal':
                                print('Congradulations! You win!')
                                playing = False
                            player.pickup(item)
                            print(f'took {item.name}')
                        input('Press enter to continue...')
                    else:
                        print_status_update('print(There are no items in this room.)')
                        continue

            case 'drop':  # TODO: change to how I like it
                target_name = clean_command[5:]  # everything after "drop "
                monster = player.get_item_by_name(target_name)
                if monster is not False:
                    player.drop(monster)
                else:
                    print('No such item.')
                    continue

            case 'wait':
                numb_of_turns = 1
                if len(command_words) > 1:
                    numb_of_turns = int(command_words[1])
                for time in range(numb_of_turns):
                    updater.update_all()
                    continue  # this is because we already waited the necessary number of rounds

            case 'me':
                print_status_update('print(player)')
                continue

            case "inv":
                player.show_inventory()
                continue

            case "help":
                if len(command_words) == 1:
                    show_help()
                else:
                    show_long_help(command_words[1])
                continue

            case "quit":
                break

            case "fight":  # TODO: update description
                target_name = command_words[1]
                monster: Monster | bool = player.location.get_monster_by_name(target_name)
                if monster is False:
                    print("No such monster.")
                    continue
                # else...
                fighting = True
                while fighting:
                    print(f'You are fighting {monster}.')
                    print(f'You have {player.health} health, {monster} has {monster.health} health.')
                    player.attack_monster(monster)
                    if monster.health <= 0:
                        monster.die()
                        print(f'You attack {monster}. It dies!')
                        input('\nPress enter to continue...')
                    monster.attack(player)
                    if player.health <= 0:
                        player.die()
                        print(f'Oh no! {monster} killed you!')
                        break
                    # else...
                    print(f'You attack {monster}. It attacks back!')
                    input('\nPress enter to continue...')
            
            case 'dev':  # for my testing (so I can see in real-time stuff like the player's hp)
                my_command = original_command[4:]
                exec(my_command)
                input('\nPress enter to continue...')
                continue
            
            case 'insp':
                target_name = command_words[1]
                monster: Item | bool = player.get_item_by_name(target_name)
                if not monster:  # so it's not in the inventory
                    monster = player.location.get_item_by_name(target_name)
                if not monster:  # so it's not in the room either
                    print('No such item.')
                    continue
                else:
                    print_status_update('print(target)')
            
            case 'use':
                target_name = command_words[1]
                monster: Item | Potion | bool = player.get_item_by_name(target_name)
                if not monster:  # so it's not in the inventory
                    print('No such item.')
                    continue
                # else...
                item_type: str = monster.item_type
                match item_type:
                    case 'potion':
                        old_hp = player.health
                        player.heal(monster.heal_value)
                        player.remove_item(monster)
                        clear()
                        print(f'You healed from {old_hp} health to {player.health} health!')
                        input('\nPress enter to continue...')
                    
                    case 'armor':
                        pass
                    
                    case 'weapon':
                        pass
                    
                    case _:
                        error_message = 'print(\"Not a valid target: please select a weapon, armor, or potion.")'
                        print_status_update(error_message)  # this is so my lines aren't too long
                        continue

            case _:  # other cases
                print("Not a valid command ('help' for a list of options)")
                print('\nPress enter to continue...')
                continue

        updater.update_all()
    
    if player.alive:
        print('Goodbye!')
    else:
        print('You died. The end!')
