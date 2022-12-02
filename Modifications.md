# TOTAL POINTS
1 - 'drop' command
1 - command abbreviations
? - access everything by single word (1) (somewhat part of comm. abbrev.)
1 - 'wait' command (2)
? - player name (1)
? - hidden dev command (?)
? - welcome screen (1)
? - detailed help commands (2/3) (UNFINISHED)
2 - 'me' command

# starter code modification
added type hinting, good-practice spacing between functions
extracted `clear()` function to its own file

# improved help menu
easier to add to

# command abbreviations/modifications
some of these are just for clarity
`inventory` -> `inv`
`pickup` -> `take`
`attack` -> `fight`
changing functionality so everything is accessible by a single word (e.g. monsters by their name, items have 1 word)

# drop command
added drop command

# misc. 3:15 pm 1 Dec (not comprehensive)
gave monsters random names from `names` package
added `__repr__` for monsters
began to add better command parsing (string cleaning)
added small intro screen
updated TODO, Modificaations
