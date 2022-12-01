from os import system as os_system
from os import name as os_name


def clear():
    os_system('cls' if os_name == 'nt' else 'clear')
