"""
Computing the canonical form of a Game.
"""

from functools import lru_cache

from .games import Game


__all__ = [
    'canonical_form',
    'make_specific',
]


@lru_cache(maxsize=None)
def remove_dominated(G):
    """
    Remove the dominated options of G.

    A left option is dominated if there exists another left option greater than
    it. A right option is dominated if there exists another right option less
    than it. In essence, it would always be a "bad idea" to move to a dominated
    option, because there exists a different option which was objectively and
    strictly superior.

    Parameters
    ----------
    G : Game
        The Game of interest.
    """
    left = G.left
    for g in G.left:
        if any(g < G_L for G_L in left):
            left.remove(g)

    right = G.right
    for g in G.right:
        if any(g > G_R for G_R in right):
            right.remove(g)

    return Game(left=left, right=right)


@lru_cache(maxsize=None)
def replace_reversible(G):
    """
    Remove the reversable options of G.

    A left option is reversible if it has a right option which is less than G.
    In this case, that left option can be replaced with it's right option's left
    options. Essentially, this means that if left were to make a move to an
    option from which right has the ability to move to a position which is
    strictly better for her than G, it is a "no brainer" to do so, and so that
    left option might as well be replaced with the options available after right
    makes the obvious responce.

    Parameters
    ----------
    G : Game
        The Game of interest.
    """
    left = set()
    for G_L in G.left:
        for G_LR in G_L.right:
            if G_LR <= G:  # G_L is reversible through G_LR
                left |= G_LR.left
                break
        else:  # Not reversible
            left.add(G_L)

    right = set()
    for G_R in G.right:
        for G_RL in G_R.left:
            if G_RL >= G:  # G_R is reversible through G_RL
                right |= G_RL.right
                break
        else:  # Not reversible
            right.add(G_R)

    return Game(left=left, right=right)


@lru_cache(maxsize=None)
def make_specific(G):
    """
    Return G as a more specific subtype of Game, if possible.

    Parameters
    ----------
    G : Game
        The game to make specific.

    Returns
    -------
    G : [Game, Nimber, Surreal, Switch]
        G as a subclass of Game.
    """
    from .games import Nimber, Surreal, Switch

    if G.is_number:
        return Surreal(left=G.left, right=G.right)
    elif G.is_impartial:
        return Nimber(left=G.left, right=G.right)
    elif G.is_switch:
        return Switch(left=G.left, right=G.right)
    else:
        left = {make_specific(G_L) for G_L in G.left}
        right = {make_specific(G_R) for G_R in G.right}
        return Game(left=left, right=right)


@lru_cache(maxsize=None)
def canonical(G):
    """
    Compute the canonical form of the game G.

    Parameters
    ----------
    G : Game
        The Game of interest.

    Returns
    -------
    K : Game
        The Game G in canonical form.
    """
    left = {canonical(G_L) for G_L in G.left}
    right = {canonical(G_R) for G_R in G.right}
    cG = Game(left=left, right=right)

    old_left, old_right = set(), set()
    while cG.left != old_left or cG.right != old_right:
        old_left, old_right = cG.left, cG.right
        cG = remove_dominated(cG)
        cG = replace_reversible(cG)

    return cG  # noqa: R504


@lru_cache(maxsize=None)
def canonical_form(G, specify=True):
    """
    Compute the canonical form of the game G.

    Parameters
    ----------
    G : Game
        The Game of interest.

    Returns
    -------
    K : Game
        The Game G in canonical form.
    """
    cG = canonical(G)

    return make_specific(cG) if specify else cG
