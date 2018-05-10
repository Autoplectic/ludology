"""
"""

from itertools import combinations, product

import networkx as nx

from .game import Game
from .tools import canonicalize
from .utils import powerset


def build_poset_lattice(nodes):
    """
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
    """
    return all(g | h for g, h in combinations(stuff, 2))


def all_games_gen(n):
    """
    """
    if n == 0:
        return {Game()}
    else:
        priors = all_games_gen(n-1)
        antichains = {games for games in powerset(priors) if is_antichain(games)}
        news = {canonicalize(Game(a, b)) for a, b in product(antichains, repeat=2)}
        return priors | news