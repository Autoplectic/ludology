"""
This module implements functions related to the structure of the partial order of games.
"""

from itertools import combinations, product

from .game import Game
from .tools import canonicalize
from .utils import powerset


__all__ = [
    'all_games',
    'companion',
    'is_lonely',
]

def is_antichain(stuff):
    """
    Whether the elements of `stuff` form an antichain or not. An antichain is a set where no two
    elements are comparable.

    Parameters
    ----------
    stuff : collection
        The collection of elements to test.

    Returns
    -------
    antichain : bool
        Whether `stuff` forms an antichain or not.
    """
    return all(g | h for g, h in combinations(stuff, 2))


def all_games(generation):
    """
    Construct all games born by day `generation`.

    Parameters
    ----------
    generation : int >= 0
        The generation of games to construct.

    Returns
    -------
    games : set
        The set of all games born by day `n`.
    """
    if generation == 0:
        return {Game()}
    else:
        priors = all_games(generation-1)
        antichains = {games for games in powerset(priors) if is_antichain(games)}
        news = {canonicalize(Game(a, b)) for a, b in product(antichains, repeat=2)}
        return priors | news


def companion(G):
    """
    The companion of a Game G is the dual of G under the unique order-preserving automorphism of
    Games born by day n.

    Parameters
    ----------
    G : Game
        The Game of interest.

    Returns
    -------
    c : Game
        G's companion.
    """
    cleft = {companion(G_L) for G_L in G._left}
    cright = {companion(G_R) for G_R in G._right}
    if G == 0:
        c = Game({0} | cleft, {0} | cright)
    elif G > 0:
        c = Game({0} | cleft, cright)
    elif G < 0:
        c = Game(cleft, {0} | cright)
    else:
        c = Game(cleft, cright)
    return canonicalize(c)


def is_lonely(G):
    """
    A Game is lonely if it is its own companion.

    Parameters
    ----------
    G : Game
        The Game of interest.

    Returns
    -------
    lonely : bool
        Whether G is lonely or not.
    """
    return G == companion(G)
