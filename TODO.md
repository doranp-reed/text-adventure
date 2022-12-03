# game modifications
add/improve error handling for built-in functions
welcome screen, `about` command, help for specific commands
clarity on when a monster moves/something updates

map, or some way of tracking history/not getting lost (map command)
more rooms, more interesting rooms

inconsistency in when screen is cleared, etc: make standard print size? like "two lines for status, one for result..."

one-way doors/rooms?
difficulty levels

## Eddie
take all command

# code modifications
change how `show-help` works? (generalize)
generalize `match-case` to more commands? is it feasible/reasonable to have a "commands list?"
refactor `command` to split on spaces (and work around that)

change how `command_success` works? seems kind of unintuitive to me
it's for the purpose of `update`, so if I can refactor that then I can mess with `command_success`

clean up how the code it done (not standard or clean in general)
