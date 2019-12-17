# -*- coding: utf-8 -*-

"""
Nicely formatting game values.
"""

from collections import namedtuple
from copy import copy
from fractions import Fraction
from functools import lru_cache

from .game import Game
from .tools import canonicalize

__all__ = [
    'value_str',
]

Symbol = namedtuple('Symbol', ['unicode', 'latex'])


_SYMBOLS = {
    'star': Symbol('∗', r'\ensuremath{\ast}'),
    'up': Symbol('↑', r'\ensuremath{\uparrow}'),
    'down': Symbol('↓', r'\ensuremath{\downarrow}'),
    '2up': Symbol('⇑', r'\ensuremath{\Uparrow}'),
    '2down': Symbol('⇓', r'\ensuremath{\Downarrow}'),
    '3up': Symbol('⤊', r'\ensuremath{3\uparrow}'),
    '3down': Symbol('⤋', r'\ensuremath{3\downarrow}'),
    '4up': Symbol('⟰', r'\ensuremath{4\uparrow}'),
    '4down': Symbol('⟱', r'\ensuremath{4\downarrow}'),
    'cdot': Symbol('·', r'\ensuremath{\cdot}'),
    'pm': Symbol('±', r'\ensuremath{\pm}'),
    'frac': Symbol((lambda n, d: unicode_fraction(n, d)), (lambda n, d: f'\\ensuremath{{\\nicefrac{{{n}}}{{{d}}}}}')),
    'miny': Symbol((lambda g: '⧿_' + g), (lambda g: r'\ensuremath{\tminus}_{' + g + '}')),
    'tiny': Symbol((lambda g: '⧾_' + g), (lambda g: r'\ensuremath{\tplus}_{' + g + '}')),
}

_SPECIFIC_FRACTIONS = {
    (1, 2): "½",
    (1, 3): "⅓",
    (2, 3): "⅔",
    (1, 4): "¼",
    (3, 4): "¾",
    (1, 5): "⅕",
    (2, 5): "⅖",
    (3, 5): "⅗",
    (4, 5): "⅘",
    (1, 6): "⅙",
    (5, 6): "⅚",
    (1, 7): "⅐",
    (1, 8): "⅛",
    (3, 8): "⅜",
    (5, 8): "⅝",
    (7, 8): "⅞",
    (1, 9): "⅑",
    (1, 10): "⅒",
}

_SUPERSCRIPTS = "⁰ⁱ²³⁴⁵⁶⁷⁸⁹"
_SUBSCRIPTS   = "₀₁₂₃₄₅₆₇₈₉"
_SLASH        = "⁄"


def unicode_fraction(numerator, denominator):
    """
    Nicely format a faction in unicode.

    Parameters
    ----------
    numerator : int
        The numerator.
    denominator : int
        The denominator.

    Returns
    -------
    frac : str
        The fraction.
    """
    if denominator == 1:
        return str(numerator)

    sign = "" if numerator >= 0 else "-"
    numerator = abs(numerator)
    if (numerator, denominator) in _SPECIFIC_FRACTIONS:
        return sign + _SPECIFIC_FRACTIONS[(numerator, denominator)]
    else:
        n = ''.join(_SUPERSCRIPTS[int(i)] for i in str(numerator))
        d = ''.join(_SUBSCRIPTS[int(i)] for i in str(denominator))
        return sign + n + _SLASH + d


def switch(mean, temp, latex):
    """
    Return the value of a switch with mean value `mean` and temperature `temp`.

    Parameters
    ----------
    mean : Fraction
        The mean value.
    temp : Fraction
        The temperature.
    latex : bool
        If false, unicode. If true, LaTeX.

    Returns
    -------
    switch : str
        The value of the switch.
    """
    if mean:
        a = _SYMBOLS['frac'][latex](mean.numerator, mean.denominator)
    else:
        a = ''
    b = _SYMBOLS['frac'][latex](temp.numerator, temp.denominator)
    return a + _SYMBOLS['pm'][latex] + b


@lru_cache(maxsize=None)
def value_str(G, latex=False):
    """
    A string representation of the game, accounting for named special games.

    Parameters
    ----------
    G : Game
        The game to compute the representation of.

    Returns
    -------
    s : str
        The name of the game.
    """
    G = canonicalize(G)
    G_hash = hash(G)

    zero = Game()

    if not len(G._left | G._right):
        return '0'

    star = Game({zero}, {zero})

    if G_hash == hash(star):
        return _SYMBOLS['star'][bool(latex)]

    # nimbers
    if G.is_impartial:
        return _SYMBOLS['star'][bool(latex)] + f"{len(G._left)}"

    # numbers
    if G.is_number:
        # non-zero dyadic rational
        if G._left:
            lf = Fraction(next(iter(G._left)).value)
        if G._right:
            rf = Fraction(next(iter(G._right)).value)

        # specifically, integer
        if not G._right:
            return str(lf + 1)
        if not G._left:
            return str(rf - 1)

        # dyadic rational
        v = (lf + rf) / 2
        n, d = v.numerator, v.denominator
        return _SYMBOLS['frac'][bool(latex)](n, d)

    # n↑, n↑*, n↓, n↓*
    up = hash(Game({zero}, {star}))
    up_star = hash(Game({zero, star}, {zero}))
    down = hash(Game({star}, {zero}))
    down_star = hash(Game({zero}, {zero, star}))

    if G_hash == up:
        return _SYMBOLS['up'][bool(latex)]
    elif G_hash == up_star:
        return _SYMBOLS['up'][bool(latex)] + _SYMBOLS['star'][bool(latex)]
    elif G_hash == down:
        return _SYMBOLS['down'][bool(latex)]
    elif G_hash == down_star:
        return _SYMBOLS['down'][bool(latex)] + _SYMBOLS['star'][bool(latex)]

    g = copy(G)
    i = 1
    while True:
        if g._left == {zero} and len(g._right) == 1:
            i += 1
            g = next(iter(g._right))
            g_hash = hash(g)
            if g_hash == up:
                if i in [2, 3, 4]:
                    arrow = _SYMBOLS[f'{i}up'][bool(latex)]
                else:
                    arrow = f"{i}" + _SYMBOLS['cdot'][bool(latex)] + _SYMBOLS['up'][bool(latex)]
                arrow += _SYMBOLS['star'][bool(latex)] * ((i+1) % 2)
                return arrow
            elif g_hash == up_star:
                if i in [2, 3, 4]:
                    arrow = _SYMBOLS[f'{i}up'][bool(latex)]
                else:
                    arrow = f"{i}" + _SYMBOLS['cdot'][bool(latex)] + _SYMBOLS['up'][bool(latex)]
                arrow += _SYMBOLS['star'][bool(latex)] * (i % 2)
                return arrow
        else:
            break

    g = copy(G)
    i = 1
    while True:
        if g._right == {zero} and len(g._left) == 1:
            i += 1
            g = next(iter(g._left))
            g_hash = hash(g)
            if g_hash == down:
                if i in [2, 3, 4]:
                    arrow = _SYMBOLS[f'{i}down'][bool(latex)]
                else:
                    arrow = f"{i}" + _SYMBOLS['cdot'][bool(latex)] + _SYMBOLS['down'][bool(latex)]
                arrow += _SYMBOLS['star'][bool(latex)] * ((i+1) % 2)
                return arrow
            elif g_hash == down_star:
                if i in [2, 3, 4]:
                    arrow = _SYMBOLS[f'{i}down'][bool(latex)]
                else:
                    arrow = f"{i}" + _SYMBOLS['cdot'][bool(latex)] + _SYMBOLS['down'][bool(latex)]
                arrow += _SYMBOLS['star'][bool(latex)] * (i % 2)
                return arrow
        else:
            break

    if len(G._left) == len(G._right) == 1:
        G_L, G_R = next(iter(G._left)), next(iter(G._right))
        if G_L.is_number and G_R.is_number:
            # switches
            if G_L > G_R:
                lf = Fraction(G_L.value)
                rf = Fraction(G_R.value)
                mean = (lf + rf) / 2
                diff = (lf - rf) / 2
                return switch(mean, diff, latex)

            # tepid games
            else:  # G_L == G_R; G_L < G_R caught by numbers above.
                return f"{G_L.value}" + _SYMBOLS['star'][bool(latex)]

    if G._left == {zero} and len(G._right) == 1:
        G_R = next(iter(G._right))
        if G_R._left == {zero} and len(G_R._right) == 1:
            G_RR = next(iter(G_R._right))
            return _SYMBOLS['tiny'][bool(latex)](f"{(-G_RR).value}")

    if G._right == {zero} and len(G._left) == 1:
        G_L = next(iter(G._left))
        if G_L._right == {zero} and len(G_L._left) == 1:
            G_LL = next(iter(G_L._left))
            return _SYMBOLS['miny'][bool(latex)](f"{(G_LL).value}")

    #todo: sums

    return repr(G)
