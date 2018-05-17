"""
This module implements functions related to the structure of the partial order of games.
"""

from itertools import combinations, product

import networkx as nx

from .game import Game
from .tools import canonicalize
from .utils import powerset


__all__ = [
    'all_games_gen',
    'build_poset_lattice',
]


def build_poset_lattice(nodes):
    """
    Given a set of nodes with a partial order, construct a lattice of this partial order.

    Parameters
    ----------
    nodes : collection
        The nodes for the lattice.

    Returns
    -------
    lattice : nx.DiGraph
        The lattice of the partial order.
    """
    lattice = nx.DiGraph()

    for u, v in combinations(nodes, 2):
        if u > v and not any(u > a > v for a in nodes):
            lattice.add_edge(u.value, v.value)
        elif v > u and not any(v > a > u for a in nodes):
            lattice.add_edge(v.value, u.value)

    return lattice


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


def all_games_gen(n):
    """
    Construct all games born by day `n`.

    Parameters
    ----------
    n : int >= 0
        The generation of games to construct.

    Returns
    -------
    games : set
        The set of all games born by day `n`.
    """
    if n == 0:
        return {Game()}
    else:
        priors = all_games_gen(n-1)
        antichains = {games for games in powerset(priors) if is_antichain(games)}
        news = {canonicalize(Game(a, b)) for a, b in product(antichains, repeat=2)}
        return priors | news
