"""
Functions related to the calculation of thermographic properties.
"""

from collections import namedtuple
from copy import copy
from fractions import Fraction
from functools import lru_cache

import numpy as np
from scipy.optimize import brentq, minimize

from .game import Game
from .tools import canonicalize


__al__ = [
    'is_cold',
    'is_tepid',
    'is_hot',
    'mean',
    'temperature',
    'cool',
    'heat',
    'overheat',
    'thermal_dissociation',
    'thermograph',
]


###############################################################################
# hot, cold, or tepid? [Siegel pg. 112]


def is_cold(G):
    """
    A Game is cold if it is a number.

    Parameters
    ----------
    G : Game
        The Game of interest.

    Returns
    -------
    cold : bool
        Whether the Game is cold or not.
    """
    return G.is_number


def is_tepid(G):
    """
    A Game is tepid if it is numberish, but not a number; that is, it differs from a number by an
    infinitesimal amount.

    Parameters
    ----------
    G : Game
        The Game of interest.

    Returns
    -------
    tepid : bool
        Whether the Game is tepid or not.
    """
    return G.is_numberish and not G.is_number


def is_hot(G):
    """
    A Game is hot if it is not numberish; that is, it's left and right stops do not coincide.

    Parameters
    ----------
    G : Game
        The Game of interest.

    Returns
    -------
    hot : bool
        Whether the Game is hot or not.
    """
    return not G.is_numberish


###############################################################################
# mean and temperature


@lru_cache(maxsize=None)
def mean(G):
    """
    Compute the mean value of a Game. The mean value is defined as the value to which a Game cools
    to. It is, by definition, a surreal number.

    Parameters
    ----------
    G : Game
        The Game of interest.

    Returns
    -------
    m : float
        The mean value of G.
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
        return float(_left_scaffold(G)(temperature(G)))


@lru_cache(maxsize=None)
def temperature(G):
    """
    Compute the temperature of a game. It is the amount by which a Game must be cooled in order to
    become a number.

    Parameters
    ----------
    G : Game
        The Game of interest.

    Returns
    -------
    temp : float
        The temperature of G.
    """
    if G.is_number:
        return -1/Fraction(G.value).denominator
    elif G.is_switch:
        _, temp = G.value.split('±')
        temp = float(Fraction(temp))
        return temp
    else:
        fl = _left_scaffold(G)
        fr = _right_scaffold(G)

        def f1(t):
            return fl(t) - fr(t)

        def f2(t):
            return abs(fl(t) - fr(t)) + t/2

        upper = 1
        while f1(upper) > 0:
            upper *= 2

        root = float(brentq(f1, 0, upper + 1))

        return round(float(minimize(f2, root).x), 4)


###############################################################################
# heating and cooling of games


@lru_cache(maxsize=None)
def cool(G, t):
    """
    Cool a game down. To cool a game, one taxes each player for the right to play. This results in
    both players having less incentive to play. At some point both the left stop and the right stop
    of the game coincide, at which point the game has become tepid (infinitesimally close to a
    number) and cooling by any more will make the game cold (a number).

    Parameters
    ----------
    G : Game
        The Game of interest.
    t : Game, float
        The amount to cool G by.

    Returns
    -------
    CG : Game
        The Game resulting from cooling G by t.
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
    Heat up a game. In some sense, heating is the opposite of cooling.

    Parameters
    ----------
    G : Game
        The Game of interest.
    t : Game, float
        The amount to heat G by.

    Returns
    -------
    HG : Game
        The Game resulting from heating G by t.
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
    Overheat a game. This is similar to heating, except applies to numbers also.

    Parameters
    ----------
    G : Game
        The Game of interest.
    t : Game, float
        The amount to overheat G by.

    Returns
    -------
    HG : Game
        The Game resulting from overheating G by t.
    """
    if not isinstance(t, Game):
        t = Game(t)
    lefts = {overheat(G_L, t) + t for G_L in G._left}
    rights = {overheat(G_R, t) - t for G_R in G._right}
    return Game(lefts, rights)


###############################################################################
# thermal dissociation


Particle = namedtuple('Particle', ['particle', 'critical_temperature'])


def thermal_dissociation(G):
    """
    The thermal dissociation of a Game G is its mean value, plus a series of
    heated infinitesimals.

    Parameters
    ----------
    G : Game
        The Game of interest.

    Returns
    -------
    td : tuple
        A tuple consisting of the mean value, followed by Particles.
    """
    g = copy(G)

    m = mean(g)

    particles = []

    while not g.is_infinitesimal and g != 0:
        t = temperature(g)
        p = canonicalize(cool(g, t) - mean(g))
        particles.append(Particle(p, t))
        g = canonicalize(g - heat(p, t))

    return tuple([m] + particles)


###############################################################################
# scaffolds, mostly helpers for thermograph plotting


def cooled_left_stop(G):  # pragma: no cover
    """
    The left stop of `G` cooled down. Useful for plotting thermographs.

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
        """
        Compute the cooled left stop.

        Parameters
        ----------
        t : float
            The amount to cool by.

        Returns
        -------
        cls : float
            The left stop of the cooled Game.
        """
        return max([crs(t) - t for crs in crss] + [m])

    return inner


def cooled_right_stop(G):  # pragma: no cover
    """
    The right stop of `G` cooled down. Useful for plotting thermographs.

    Parameters
    ----------
    G : Game
        The game of interest.

    Returns
    -------
    crs : func
        A function which returns the right stop of `G` cooled by `t`.
    """
    m = mean(G)
    clss = [cooled_left_stop(G_R) for G_R in G._right]

    @np.vectorize
    def inner(t):
        """
        Compute the cooled right stop.

        Parameters
        ----------
        t : float
            The amount to cool by.

        Returns
        -------
        cls : float
            The right stop of the cooled Game.
        """
        return min([cls(t) + t for cls in clss] + [m])

    return inner


def _left_scaffold(G):
    """
    Compute the left scaffold of the thermograph of G.

    Parameters
    ----------
    G : Game
        The Game of interest.

    Returns
    -------
    ls : func
        The left scaffold as a function of temperature.
    """
    crss = [cooled_right_stop(G_L) for G_L in G._left]

    @np.vectorize
    def inner(t):
        """
        Compute the left scaffold of G as a function t.

        Parameters
        ----------
        t : float
            The temperature.

        Returns
        -------
        ls : float
            The left scaffold of G at temperature t.
        """
        return np.max([crs(t) - t for crs in crss])

    return inner


def _right_scaffold(G):
    """
    Compute the right scaffold of the thermograph of G.

    Parameters
    ----------
    G : Game
        The Game of interest.

    Returns
    -------
    rs : func
        The right scaffold as a function of temperature.
    """
    clss = [cooled_left_stop(G_R) for G_R in G._right]

    @np.vectorize
    def inner(t):
        """
        Compute the right scaffold of G as a function t.

        Parameters
        ----------
        t : float
            The temperature.

        Returns
        -------
        rs : float
            The right scaffold of G at temperature t.
        """
        return np.min([cls(t) + t for cls in clss])

    return inner


@lru_cache(maxsize=None)
def number_height(G):  # pragma: no cover
    """
    Return the height of the game tree truncated at numbers.

    Parameters
    ----------
    G : Game
        The Game of interest.

    Returns
    -------
    height : int
        The hight of the number-truncated game tree.
    """
    if G.is_number:
        return 1
    else:
        return max(number_height(g) for g in G._left | G._right) + 1


###############################################################################
# plotting of thermographs


def _thermograph(G, ax, t_min, t_max, lw):  # pragma: no cover
    """
    Plot a single thermograph.

    Parameters
    ----------
    G : Game
        The Game whose thermograph is to be plotted.
    ax : plt.axis
        The matplotlib axis to plot on.
    t_min : float
        The minimum temperature to plot.
    t_max : float
        The maximum temperature to plot.
    lw : float
        The line width to plot with.
    """
    temp = temperature(G)
    ts = np.linspace(t_min, temp, 101)
    ls, rs = cooled_left_stop(G), cooled_right_stop(G)
    mast_height = t_max - temp

    line, = ax.plot(ls(ts), ts, lw=lw, label=G.value)
    color = line.get_color()
    ax.plot(rs(ts), ts, lw=lw, c=color)

    ax.arrow(mean(G), temp, 0, mast_height, lw=lw, color=color, length_includes_head=True)


def thermograph(G, with_options=True, ax=None):  # pragma: no cover
    """
    Plot a thermograph of G.

    Parameters
    ----------
    G : Game
        The Game to plot the thermograph of.
    with_options : bool
        If True, plot the thermographs of the options of G as well. Defaults to True.
    ax : plt.axis, None
        The axis to plot on. If not provided, construct one.

    Returns
    -------
    ax : plt.axis
        The axis with the thermograph plotted.
    """
    if ax is None:
        import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(10, 5))
        ax = fig.gca()

    t_min = -1.0 if G.is_number else 0.0
    t_max = max([0.25 + temperature(G), 1.0])

    if with_options:
        lw = 2 * number_height(G)
    else:
        lw = 2

    _thermograph(G, ax, t_min, t_max, lw)

    if with_options:
        options = G._left | G._right
        i = 2
        while any(not g.is_number for g in options):
            new_options = set()
            for g in options:
                _thermograph(g, ax, t_min, t_max, lw - i)
                g_opts = g._left | g._right
                if any(not _.is_number for _ in g_opts):
                    new_options |= g_opts
            i += 2
            options = new_options

    ax.invert_xaxis()
    ax.set_ylim(t_min, t_max + 0.1 * (t_max - t_min))

    ax.grid(True)

    ax.legend(loc='best')

    return ax
