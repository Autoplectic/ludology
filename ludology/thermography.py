"""
"""

from fractions import Fraction
from functools import lru_cache

import numpy as np
from scipy.optimize import brentq

from .game import Game


__al__ = [
    'mean',
    'temperature',
    'cool',
    'heat',
    'overheat',
    'thermograph',
]


@lru_cache(maxsize=None)
def mean(G):
    """
    """
    value = G.value
    if G.is_number:
        return float(Fraction(value))
    elif G.is_switch:
        m, _ = value.split('±')
        if m:
            m = float(Fraction(m))
        else:
            m = 0.0
        return m
    else:
        return float(_cooled_left_stop(G)(temperature(G)))


@lru_cache(maxsize=None)
def temperature(G):
    """
    """
    if G.is_number:
        return 0.0
    elif G.is_switch:
        _, temp = G.value.split('±')
        temp = float(Fraction(temp))
        return temp
    else:
        fl = _cooled_left_stop(G)
        fr = _cooled_right_stop(G)
        def f(t):
            return fl(t) - fr(t)
        upper = 1
        while f(upper) > 0:
            upper *= 2
        return float(brentq(f, 0, upper + 1))


@lru_cache(maxsize=None)
def cool(G, t):
    """
    """
    if t <= temperature(G):
        t = Game(t)
        lefts = {cool(G_L, t) - t for G_L in G._left}
        rights = {cool(G_R, t) + t for G_R in G._right}
        return Game(lefts, rights)
    else:
        return Game(mean(G))


@lru_cache(maxsize=None)
def heat(G, t):
    """
    """
    if G.is_number:
        return G
    else:
        if not isinstance(t, Game):
            t = Game(t)
        lefts = {heat(G_L, t) + t for G_L in G._left}
        rights = {heat(G_R, t) - t for G_R in G._right}
        return Game(lefts, rights)


@lru_cache(maxsize=None)
def overheat(G, t):
    """
    """
    if not isinstance(t, Game):
        t = Game(t)
    lefts = {overheat(G_L, t) + t for G_L in G._left}
    rights = {overheat(G_R, t) - t for G_R in G._right}
    return Game(lefts, rights)


def cooled_left_stop(G):  # pragma: no cover
    """
    The left stop of `G` cooled down.

    Parameters
    ----------
    G : Game
        The game of interest.

    Returns
    -------
    cls : func
        A function which returns the left stop of `G` cooled by `t`.
    """
    m = mean(G)
    crss = [cooled_right_stop(G_L) for G_L in G._left]
    @np.vectorize
    def inner(t):
        return max([crs(t) - t for crs in crss] + [m])
    return inner


def cooled_right_stop(G):  # pragma: no cover
    """
    """
    m = mean(G)
    clss = [cooled_left_stop(G_R) for G_R in G._right]
    @np.vectorize
    def inner(t):
        return min([cls(t) + t for cls in clss] + [m])
    return inner


def _cooled_left_stop(G):  # pragma: no cover
    """
    """
    crss = [cooled_right_stop(G_L) for G_L in G._left]
    @np.vectorize
    def inner(t):
        return np.max([crs(t) - t for crs in crss])
    return inner


def _cooled_right_stop(G):  # pragma: no cover
    """
    """
    clss = [cooled_left_stop(G_R) for G_R in G._right]
    @np.vectorize
    def inner(t):
        return np.min([cls(t) + t for cls in clss])
    return inner


@lru_cache(maxsize=None)
def integer_height(G):  # pragma: no cover
    """
    """
    if G.is_number:
        return 1
    else:
        return max(integer_height(g) for g in G._left | G._right) + 1


def _thermograph(G, ax, T, lw):  # pragma: no cover
    """
    """
    ts = np.linspace(0, T, 101)
    ls, rs = cooled_left_stop(G), cooled_right_stop(G)

    line, = ax.plot(ls(ts), ts, lw=2*lw, label=G.value)
    ax.plot(rs(ts), ts, lw=2*lw, c=line.get_color())


def thermograph(G, with_options=True, ax=None, T=None):  # pragma: no cover
    """
    """
    if ax is None:
        import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(10, 5))
        ax = fig.gca()

    if T is None:
        T = 1.1 * temperature(G)

    if with_options:
        lw = integer_height(G)
    else:
        lw = 2

    _thermograph(G, ax, T, lw)

    if with_options:
        options = G._left | G._right
        i = 1
        while any(not g.is_number for g in options):
            new_options = set()
            for g in options:
                _thermograph(g, ax, T, lw=i)
                g_opts = g._left | g._right
                if any(not _.is_number for _ in g_opts):
                    new_options |= g_opts
            i += 1
            options = new_options

    xlims = ax.get_xlim()
    ax.set_xlim(xlims[1], xlims[0])

    ax.grid(True)

    ax.legend(loc='best')

    return ax
