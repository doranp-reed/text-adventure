from room import Room
from player import Player
from item import Item
from monster import Monster
import updater
from clear import clear

player = Player()
command_help = {'help': '[command] -- prints list of options or help on given command',
                'go': '<direction> -- moves you in the given direction',
                'inv': '-- opens your inventory',
                'take': '<item> -- picks up the given item',
                'quit': '-- quits the game',
                'fight': '<monster name> -- fights the given monster',
                'drop': '<item> -- drops the given item'}


def create_world():
    a = Room("You are in room 1")
    b = Room("You are in room 2")
    c = Room("You are in room 3")
    d = Room("You are in room 4")
    Room.connect_rooms(a, "east", b, "west")
    Room.connect_rooms(c, "east", d, "west")
    Room.connect_rooms(a, "north", c, "south")
    Room.connect_rooms(b, "north", d, "south")
    i = Item("Rock", "This is just a rock.")
    i.put_in_room(b)
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


def show_help():
    clear()
    for key in command_help:
        print(key, command_help[key])
    print()
    input("Press enter to continue...")


def string_cleaner(com: str) -> str:
    ret = ''
    alphabet = 'abcdefghijklm nopqrstuvwxyz'  # note that this has a space, so that's not removed
    for symbol in com.lower():
        if symbol in alphabet:
            ret += symbol
    return ret


def too_many_commands():
    print('Sorry, too many directions given.')
    input("Press enter to continue...")


if __name__ == "__main__":
    create_world()
    playing = True
    clear()
    print('Welcome to the dungeon!')
    print('Be very careful: a single wrong keystroke could end your time here!\n')
    input("Press enter to continue...")

    while playing and player.alive:
        print_situation()
        command_success = False
        time_passes = False

        while not command_success:
            command_success = True
            command = input("What now? ('help' for list of options) ")

            command = string_cleaner(command)

            if len(command) == 0:
                continue

            command_words = command.split()
            if len(command_words) == 0:
                continue

            match command_words[0]:
                case "go":  # now 'go' is well-handled (by my standards)
                    if len(command_words) > 2:
                        too_many_commands()
                        continue
                    okay = player.go_direction(command_words[1]) 
                    if okay:
                        time_passes = True
                    else:
                        print("You can't go that way.")
                        command_success = False

                case "take":
                    if len(command_words) > 2:
                        too_many_commands()
                        continue
                    target_name = command_words[1]
                    target = player.location.get_item_by_name(target_name)
                    if target is not False:
                        player.pickup(target)
                    else:
                        print("No such item.")
                        command_success = False

                case 'drop':  # can handle multi-word objects
                    target_name = command[5:]  # everything after "drop "
                    target = player.get_item_by_name(target_name)
                    if target is not False:
                        player.drop(target)
                    else:
                        print('No such item.')
                        command_success = False

                case "inv":
                    player.show_inventory()

                case "help":
                    show_help()

                case "quit":
                    playing = False

                case "fight":  # TODO: add in description
                    target_name = command[6:]
                    target = player.location.get_monster_by_name(target_name)
                    if target is not False:
                        player.attack_monster(target)
                    else:
                        print("No such monster.")
                        command_success = False
                
                case _:  # other cases
                    print("Not a valid command ('help' for a list of options)")
                    command_success = False  # TODO: see if this is actually error-worthy or not
        if time_passes is True:
            updater.update_all()
