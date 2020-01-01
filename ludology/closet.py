# -*- coding: utf-8 -*-

"""
A collection of common games.
"""

from .games import Game, Nimber, Surreal, Switch
from .tools import canonicalize


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
    'g5',
]


# numbers
zero = Surreal(0)
one = Surreal(1)
two = Surreal(2)
half = Surreal(1 / 2)
quarter = Surreal(1 / 4)

# nimbers
star = Nimber(1)
star2 = Nimber(2)

# other infinitesimals
up = Game({zero}, {star})
upstar = Game({zero}, {zero, star})

# switch
pm_one = Switch(mean=zero, temp=one)

# more complex examples
g1 = canonicalize(Game({5 / 2, Game({4}, {2})}, {Game({0}, {-4}), Game({-1}, {-2})}))
g2 = canonicalize(Game({Game({4}, {2})}, {Game({Game({0}, {-2})}, {Game({-4}, {-6})})}))
g3 = canonicalize(Game({Game({3}, {one + star})}, {Game({-one + star}, {-two + star}), Game({0}, {-3})}))
g4 = canonicalize(Game({5}, {Game({1}, {-9})}))
g5 = canonicalize(Game({Game({2}, {0}), Game({2}, {star})}, {Game({0}, {-2 + star}), Game({star}, {-2 + star})}))


# Factories for specific game types.
def tiny(G):
    """
    Construct a Tiny Game: {0 || 0 | G}

    Parameters
    ----------
    G : Game
        The Game to make Tiny.

    Returns
    -------
    T : Game
        {0 || 0 | G}
    """
    return canonicalize(Game({0}, {Game({0}, {G})}))


def miny(G):
    """
    Construct a Miny Game: {-G | 0 || 0}

    Parameters
    ----------
    G : Game
        The Game to make Miny.

    Returns
    -------
    M : Game
        {-G | 0 || 0}
    """
    return -tiny(G)


def uptimal(*nums):
    """
    Construct an Uptimal.

    Parameters
    ----------
    nums : [int]
        The uptimal values

    Returns
    -------
    U : Game
        The uptimal.
    """
    raise NotImplementedError
