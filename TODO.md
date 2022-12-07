<!--
# game modifications

## ideas
add/improve error handling for built-in functions
clarity on when a monster moves/something updates

map, or some way of tracking history/not getting lost (map command)
more rooms, more interesting rooms

inconsistency in when screen is cleared, etc: make standard print size? like "two lines for status, one for result..."

one-way doors/rooms?
difficulty levels


## gameplay-wise (what would actually improve the game)
weapons/more complex combat
more rooms
end goal? (find the exit?)
consequences for ignoring monsters?


# code modifications
change how `show-help` works? (generalize)
generalize `match-case` to more commands? is it feasible/reasonable to have a "commands list?"
refactor `command` to split on spaces (and work around that)

change how `command_success` works? seems kind of unintuitive to me
it's for the purpose of `update`, so if I can refactor that then I can mess with `command_success`

clean up how the code is done (not standard or clean in general)

# clean-up
better error messages (e.g. `no such monster 'gary the monster'`)
-->


# Second-half changes!

## code changes
change the 2x `while` loop and how `command_success` is implemented
standardize rest of case handling
modify how commands are accessed/used (extend `command_help` functionality)
better error/command failure handling

## gameplay modifications
**weapons, armor, combat system**
level up? attributes?
different monsters? boss?
**larger world (either random or made by me)**
special rooms? puzzles?
one-way doors? locked doors?
**map/tracking?**
difficulty level?

game save?

## UX cleanup
standardize how printing/clearing is implemented
updates when things change (e.g. monster arrives in room)

## misc.
how do I want to make different rooms? should monsters move around a bunch, or should each room be more like a separate challenge?

## points (goal)
2 - weapons (comabat system as well)
2 - armor
3 - more/different monsters (two or three normal types, maybe boss)
<!-- ? - boss fight (special combat) -->
2 - bigger world
3 - loot
4 - currency/merchant
4 - save/load game
