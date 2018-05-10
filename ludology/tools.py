"""
"""

from copy import copy, deepcopy
from functools import lru_cache

import networkx as nx


__all__ = [
    'canonicalize',
    'left_incentives',
    'right_incentives',
    'left_stop',
    'right_stop',
]


@lru_cache(maxsize=None)
def left_incentives(G):
    """
    """
    return {simplify(G_L - G) for G_L in G._left}


@lru_cache(maxsize=None)
def right_incentives(G):
    """
    """
    return {simplify(G - G_R) for G_R in G._right}


def stop_order(item):
    """
    if x > y:
        x_- > x_+ > y_- > y_+

    since L is lexicographically less than R, we
    can't rely on natural ordering.
    """
    g, s = item
    return (g, s == '-')


@lru_cache(maxsize=None)
def left_stop(G):
    """
    """
    if G.is_number:
        return (G, '+')
    else:
        return max((right_stop(G_L) for G_L in G._left), key=stop_order)


@lru_cache(maxsize=None)
def right_stop(G):
    """
    """
    if G.is_number:
        return (G, '-')
    else:
        return min((left_stop(G_R) for G_R in G._right), key=stop_order)


@lru_cache(maxsize=None)
def remove_dominated(G):
    """
    """
    old_left = list(G._left)
    G._left = set()
    while old_left:
        G_L = old_left.pop()
        if not any(G_L < g for g in old_left):
            G._left.add(G_L)

    old_right = list(G._right)
    G._right = set()
    while old_right:
        G_R = old_right.pop()
        if not any(G_R > g for g in old_right):
            G._right.add(G_R)

    # G._left = {g for g in G._left if not any(g < G_L for G_L in G._left)}
    # G._right = {g for g in G._right if not any(g > G_R for G_R in G._right)}


@lru_cache(maxsize=None)
def replace_reversible(G):
    """
    """
    old_left = list(G._left)
    G._left = set()
    while old_left:
        G_L = old_left.pop()
        for G_LR in G_L._right:
            if G >= G_LR:  # G_L is reversible through G_LR
                G._left |= G_LR._left
                break
        else:  # Not reversible
            G._left.add(G_L)

    old_right = list(G._right)
    G._right = set()
    while old_right:
        G_R = old_right.pop()
        for G_RL in G_R._left:
            if G_RL >= G:  # G_R is reversible through G_RL
                G._right |= G_RL._right
                break
        else:  # Not reversible
            G._right.add(G_R)


@lru_cache(maxsize=None)
def simplify(G):
    """
    """
    G = copy(G)

    G._left = {simplify(G_L) for G_L in G._left}
    G._right = {simplify(G_R) for G_R in G._right}

    old_left, old_right = set(), set()
    while G._left != old_left or G._right != old_right:
        old_left, old_right = G._left, G._right
        remove_dominated(G)
        replace_reversible(G)

    return(G)


canonicalize = simplify


def game_tree(G):
    """
    """
    tree = nx.DiGraph()