"""
A collection of common games.
"""

from .game import Game


__all__ = [
    'zero',
    'quarter',
    'half',
    'one',
    'two',
    'star',
    'star2',
    'up',
    'tiny',
    'pm_one',
]


# numbers
zero = Game()
quarter = Game(1/4)
half = Game(1/2)
one = Game(1)
two = Game(2)

# nimbers
star = Game({0}, {0})
star2 = Game({0, star}, {0, star})

# other infinitesimals
up = Game({0}, {star})
upstar = Game({0}, {0, star})
tiny = Game({0}, {Game({0}, {-1})})

# switch
pm_one = Game({1}, {-1})
