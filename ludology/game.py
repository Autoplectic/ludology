"""
"""

from copy import copy, deepcopy
from fractions import Fraction
from functools import lru_cache, wraps
from math import ceil, floor, inf, log

from .tools import canonicalize


__all__ = [
    'Game',
]


def gamify_inputs(f):
    @wraps(f)
    def inner(*args):
        args = tuple(Game(_) for _ in args)
        return f(*args)

    return inner


class Game(object):
    """
    """

    def __init__(G, left=None, right=None):
        """
        """
        # passed in a number
        if isinstance(left, (int, float, Fraction)):
            v = float(left)
            if v.is_integer():
                if v == 0:
                    G._left = set()
                    G._right = set()
                elif v > 0:
                    G._left = {Game(v-1)}
                    G._right = set()
                else:
                    G._left = set()
                    G._right = {Game(v+1)}
            else:
                _, d = v.as_integer_ratio()
                G._left = {Game(v - 1/d)}
                G._right = {Game(v + 1/d)}
        # passed in a game
        elif isinstance(left, Game):
            G._left = copy(left._left)
            G._right = copy(left._right)
        # passed in sets
        else:
            if left is not None:
                G._left = {Game(_) for _ in left}
            else:
                G._left = set()
            if right is not None:
                G._right = {Game(_) for _ in right}
            else:
                G._right = set()

    @gamify_inputs
    # @lru_cache(maxsize=None)
    def __ge__(G, H):
        """
        """
        a = all(not H >= G_R for G_R in G._right)
        b = all(not H_L >= G for H_L in H._left)
        return a and b

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __le__(G, H):
        """
        """
        return H >= G

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __gt__(G, H):
        """
        """
        return G >= H and not H >= G

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __lt__(G, H):
        """
        """
        return H > G

    @gamify_inputs
    # @lru_cache(maxsize=None)
    def __eq__(G, H):
        """
        """
        if hash(G) == hash(H):
            return True
        else:
            return G >= H and H >= G

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __or__(G, H):
        """
        """
        return not (G >= H or H >= G)

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __ror__(G, H):
        """
        """
        return G | H

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __neg__(G):
        """
        """
        return Game({-G_R for G_R in G._right}, {-G_L for G_L in G._left})

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __add__(G, H):
        """
        """
        if not G.is_number and H.is_number:
            lefts = {G_L + H for G_L in G._left}
            rights = {G_R + H for G_R in G._right}
            return Game(lefts, rights)
        elif G.is_number and not H.is_number:
            lefts = {H_L + G for H_L in H._left}
            rights = {H_R + G for H_R in H._right}
            return Game(lefts, rights)
        else:
            left_a = {H + G_L for G_L in G._left}
            left_b = {G + H_L for H_L in H._left}
            right_a = {H + G_R for G_R in G._right}
            right_b = {G + H_R for H_R in H._right}
            return Game(left_a | left_b, right_a | right_b)

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __radd__(G, H):
        """
        """
        return G + H

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __sub__(G, H):
        """
        """
        return G + (-H)

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __mul__(G, H):
        """
        """
        left_a = {G_L * H + G * H_L - G_L * H_L for G_L in G._left for H_L in H._left}
        left_b = {G_R * H + G * H_R - G_R * H_R for G_R in G._right for H_R in H._right}
        right_a = {G_L * H + G * H_R - G_L * H_R for G_L in G._left for H_R in H._right}
        right_b = {G_R * H + G * H_L - G_R * H_L for G_R in G._right for H_L in H._left}
        return Game(left_a | left_b, right_a | right_b)

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __rmul__(G, H):
        """
        """
        return G * H

    @gamify_inputs
    @lru_cache(maxsize=None)
    def _inverse(G):
        """
        """
        pass

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __div__(G, H):
        """
        """
        return G * H._inverse()

    def __hash__(G):
        """
        """
        return hash((frozenset(G._left), frozenset(G._right)))

    def __str__(G):
        """
        """
        return G.value

    def __repr__(G):
        """
        """
        lefts = ','.join(G_L.value for G_L in sorted(G._left))
        rights = ','.join(G_R.value for G_R in sorted(G._right))
        return '{{{}|{}}}'.format(lefts, rights)

    @property
    def is_impartial(G):
        """
        """
        a = G._left == G._right
        b = all(G_L.is_impartial for G_L in G._left)
        return a and b

    @property
    def is_number(G):
        """
        """
        a = all(g.is_number for g in G._left | G._right)
        b = all(G_L < G_R for G_L in G._left for G_R in G._right)
        return a and b

    @property
    def is_switch(G):
        """
        """
        if len(G._left) == len(G._right) == 1:
            G_L = next(iter(G._left))
            G_R = next(iter(G._right))
            if G_L.is_number and G_R.is_number and G_L > G_R:
                return True
        return False

    @property
    def birthday(G):
        """
        """
        if G._left == G._right == set():
            bday = 0
        else:
            bday = max(g.birthday for g in G._left | G._right) + 1

        return bday

    @property
    def outcome(G):
        """
        """
        zero = Game()
        if G == zero:
            return 'P'
        elif G > zero:
            return 'L'
        elif G < zero:
            return 'R'
        else:
            return 'N'

    @property
    def value(G):
        """
        """
        return _value_str(G)


@lru_cache(maxsize=None)
def _value_str(G):
    """
    """
    G = canonicalize(G)
    G_hash = hash(G)

    zero = Game()

    if not len(G._left | G._right):
        return '0'

    star = Game({zero}, {zero})

    if G_hash == hash(star):
        return '∗'

    up = hash(Game({zero}, {star}))
    up_star = hash(Game({zero, star}, {zero}))
    down = hash(Game({star}, {zero}))
    down_star = hash(Game({zero}, {zero, star}))

    if G_hash == up:
        return '↑'
    elif G_hash == up_star:
        return '↑∗'
    elif G_hash == down:
        return '↓'
    elif G_hash == down_star:
        return '↓∗'

    g = copy(G)
    i = 1
    while True:
        if g._left == {zero} and len(g._right) == 1:
            i += 1
            g = next(iter(g._right))
            g_hash = hash(g)
            if g_hash == up:
                return f"{i}·↑" + "∗" * ((i+1) % 2)
            elif g_hash == up_star:
                return f"{i}·↑" + "∗" * (i % 2)
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
                return f"{i}·↓" + "∗" * ((i+1) % 2)
            elif g_hash == down_star:
                return f"{i}·↓" + "∗" * (i % 2)
        else:
            break

    # nimbers
    if G.is_impartial:
        return f"∗{len(G._left)}"

    if G.is_number:
        # non-zero integer
        if G._left:
            lf = Fraction(next(iter(G._left)).value)
        if G._right:
            rf = Fraction(next(iter(G._right)).value)

        if not G._right:
            return str(lf + 1)
        if not G._left:
            return str(rf - 1)

        # dyadic rational
        # "simplest number l < x < r...
        # d = 2**floor(log(rf - lf, 2))
        # if ceil(lf) > lf and ceil(lf) < rf:
        #     x = ceil(lf)
        # elif lf % d:
        #     x = ((lf // d) + 1) * d
        # else:
        #     x = (lf + rf) / 2

        # return str(x)
        return str((lf + rf) / 2)

    if len(G._left) == len(G._right) == 1:
        G_L, G_R = next(iter(G._left)), next(iter(G._right))
        if G_L.is_number and G_R.is_number:
            # switches
            if G_L > G_R:
                lf = Fraction(G_L.value)
                rf = Fraction(G_R.value)
                mean = (lf + rf) / 2
                diff = (lf - rf) / 2
                if mean:
                    return f"{mean}±{diff}"
                else:
                    return f"±{diff}"

            # tepid games
            else:  # G_L == G_R, G_L < G_R caught by numbers above.
                return f"{G_L.value}∗"

    if G._left == {zero} and len(G._right) == 1:
        G_R = next(iter(G._right))
        if G_R._left == {zero} and len(G_R._right) == 1:
            G_RR = next(iter(G_R._right))
            return f"➕_{(-G_RR).value}"

    if G._right == {zero} and len(G._left) == 1:
        G_L = next(iter(G._left))
        if G_L._right == {zero} and len(G_L._left) == 1:
            G_LL = next(iter(G_L._left))
            return f"➖_{(G_LL).value}"

    #todo: sums

    return repr(G)


def _value_latex(G):
    """
    """
    pass