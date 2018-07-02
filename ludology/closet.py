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
    'g1',
    'g2',
    'g3',
    'g4',
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

# more complex examples
g1 = Game({5/2, Game({4}, {2})}, {Game({0}, {-4}), Game({-1}, {-2})})
g2 = Game({Game({4}, {2})}, {Game({Game({0}, {-2})}, {Game({-4}, {-6})})})
g3 = Game({Game({3}, {one + star})}, {Game({-one + star}, {-two + star}), Game({0}, {-3})})
g4 = Game({5}, {Game({1}, {-9})})
