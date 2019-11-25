"""
The basic Game class.
"""

from collections import namedtuple
from copy import copy
from enum import Enum
from fractions import Fraction
from functools import lru_cache, wraps

from .tools import canonicalize


__all__ = [
    'Game',
]


def gamify_inputs(f):
    """
    A decorator to cast all arguments to a function into Games.

    Parameters
    ----------
    f : func
        The function to decorate.

    Returns
    -------
    inner : func
        The decorated function.
    """
    @wraps(f)
    def inner(*args):
        args = tuple(Game(_) for _ in args)
        return f(*args)

    return inner


class Outcome(Enum):
    """
    Representing the outcome classes of Games.
    """
    PREVIOUS = 'P'
    NEXT     = 'N'
    LEFT     = 'L'
    RIGHT    = 'R'


class Game(object):
    """
    A game consists of a *left set* and a *right set*, and is often written:

        { G_L | G_R }

    where G_L is the left set of Games, and G_R is the right set of Games. The trivial game, {|},
    is known as 0 and is said to have been born on day 0. Recursively, we can define games born
    on day `n` as all possible games whose left set and right set consist of Games having birthdays
    no later than day `n-1`.
    """

    def __init__(G, left=None, right=None):
        """
        Construct a Game.

        Parameters
        ----------
        left : iterable, number, Game, None
            If an iterable, it is the left set of the game. If a number, construct the game
            corresponding to that number. If a Game, use its left set, and if None, treat the left
            set as empty.
        right : iterable, None
            The right set of the game. If None, treat the right set as empty.
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
                if d > 1024:
                    msg = f"{v} would result in a very deep game tree."
                    raise ValueError(msg)
                G._left = {Game(v - 1/d)}
                G._right = {Game(v + 1/d)}
        # passed in a game
        elif isinstance(left, Game):
            G._left = {Game(_) for _ in left._left}
            G._right = {Game(_) for _ in left._right}
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
        A Game G is greater than or equal to a Game H so long as there are no G_R such that
        H >= G_R and there are no H_L such that H_L >= G.

        Parameters
        ----------
        H : Game
            The second game.

        Returns
        -------
        ge : bool
            G >= H.
        """
        a = all(not H >= G_R for G_R in G._right)
        b = all(not H_L >= G for H_L in H._left)
        return a and b

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __le__(G, H):
        """
        G <= H if H >= G.

        Parameters
        ----------
        H : Game
            The second game.

        Returns
        -------
        le : bool
            G <= H.
        """
        return H >= G

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __gt__(G, H):
        """
        G > H if G >= H and not G == H.

        Parameters
        ----------
        H : Game
            The second game.

        Returns
        -------
        gt : bool
            G > H.
        """
        return G >= H and not H >= G

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __lt__(G, H):
        """
        G < H if G <= H and not G == H.

        Parameters
        ----------
        H : Game
            The second game.

        Returns
        -------
        lt : bool
            G < H.
        """
        return H > G

    @gamify_inputs
    # @lru_cache(maxsize=None)
    def __eq__(G, H):
        """
        G == H if G >= H and G <= H.

        Parameters
        ----------
        H : Game
            The second game.

        Returns
        -------
        eq : bool
            G == H.
        """
        if hash(G) == hash(H):
            return True
        else:
            return G >= H and H >= G

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __or__(G, H):
        """
        G | H ('fuzzy' or 'confused with') if neither G >= H nor G <= H.

        Parameters
        ----------
        H : Game
            The second game.

        Returns
        -------
        fuzzy : bool
            G | H.
        """
        return not (G >= H or H >= G)

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __ror__(G, H):
        """
        G | H ('fuzzy' or 'confused with') if neither G >= H nor G <= H.

        Parameters
        ----------
        H : Game
            The second game.

        Returns
        -------
        fuzzy : bool
            G | H.
        """
        return not (G >= H or H >= G)

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __neg__(G):
        """
        -{G_L | G_R} is recursively defined as {-G_R | -G_L}.

        Returns
        -------
        ng : Game
            -G.
        """
        return Game({-G_R for G_R in G._right}, {-G_L for G_L in G._left})

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __add__(G, H):
        """
        The disjoint sum of two games:
            G + H = {G + H_L, H + G_L | G + H_R, H + G_R}

        Parameters
        ----------
        H : Game
            The second Game.

        Returns
        -------
        GplusH : Game
            The sum of G and H.
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
        The disjoint sum of two games:
            G + H = {G + H_L, H + G_L | G + H_R, H + G_R}

        Parameters
        ----------
        H : Game
            The second Game.

        Returns
        -------
        GplusH : Game
            The sum of G and H.
        """
        return G + H

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __sub__(G, H):
        """
        The disjoint difference of two games:
            G - H = G + (-H)

        Parameters
        ----------
        H : Game
            The second Game.

        Returns
        -------
        GminusH : Game
            The difference of G and H.
        """
        return G + (-H)

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __mul__(G, H):
        """
        The Norton product of G and H.

        Parameters
        ----------
        H : Game
            The second Game.

        Returns
        -------
        GtimesH : Game
            The product of G and H.
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
        The Norton product of G and H.

        Parameters
        ----------
        H : Game
            The second Game.

        Returns
        -------
        GtimesH : Game
            The product of G and H.
        """
        return G * H

    @gamify_inputs
    @lru_cache(maxsize=None)
    def _inverse(G):
        """
        Invert the Game G.

        Returns
        -------
        Ginv : Game
            The inverse of G.
        """
        # TODO: implement this.
        raise NotImplementedError

    @gamify_inputs
    @lru_cache(maxsize=None)
    def __truediv__(G, H):
        """
        The Norton quotient of G by H:

            G / H = G * (1/H)

        Parameters
        ----------
        H : Game
            The second Game.

        Returns
        -------
        GdivH : Game
            The quotient of G by H.
        """
        return G * H._inverse()

    def __hash__(G):
        """
        Define the hash of a game as the hash of the left and right options.

        Returns
        -------
        hash : str
            The hash of G.
        """
        return hash((frozenset(G._left), frozenset(G._right)))

    def __str__(G):
        """
        The value of G as a string.

        Returns
        -------
        s : str
            The value of G as a string.
        """
        return G.value

    def __repr__(G):
        """
        Construct a representation of G. It is of the form {G_L|G_R}, where the options are
        their shorthand values if possible.

        Returns
        -------
        r : str
            A representation of G.
        """
        lefts = ','.join(G_L.value for G_L in sorted(G._left, key=str))
        rights = ','.join(G_R.value for G_R in sorted(G._right, key=str))
        return '{{{}|{}}}'.format(lefts, rights)

    def subpositions(G):
        """
        Return an iterator over all subpositions of G.

        Yields
        ------
        g : Game
            A subposition of G.
        """
        for g in G._left | G._right:
            yield g
            yield from g.subpositions()

    @property
    def is_impartial(G):
        """
        A game is impartial if its left options equal its right options, and each of its options
        are impartial.

        Returns
        -------
        impartial : bool
            Whether G is impartial or not.
        """
        if G._left == G._right:
            if all(G_L.is_impartial for G_L in G._left):
                return True
        return False

    @property
    def is_dicotic(G):
        """
        A dicotic, or all-small, Game is one where either both or neither player have options
        at every subposition.

        Returns
        -------
        dicotic : bool
            Whether the Game is dicotic or not.
        """
        if not (bool(G._left) ^ bool(G._right)):
            if all(g.is_dicotic for g in G._left | G._right):
                return True
        return False

    @property
    def is_infinitesimal(G):
        """
        A game is infinitesimal if it is non-zero and smaller than any positive number and greater
        than any negative number. Equivalently, it's left and right stops are both zero. Note, this
        does not imply that an infinitesimal can not be positive (> 0) or negative (< 0).

        Returns
        -------
        infinitesimal : bool
            Whether the game is infinitesimal or not.
        """
        from .tools import left_stop, right_stop
        a = left_stop(G, adorn=False) == right_stop(G, adorn=False) == 0
        b = G != 0
        return a and b

    @property
    def is_number(G):
        """
        A game is a (surreal) number if each of it left options is less than each of its right
        options, and all its options are also numbers.

        Returns
        -------
        number : bool
            Whether G is a number or not.

        Note
        ----
        The definition implies that, in canonical form, the number has at most one left option and
        one right option, because one must dominate. Also, if either of the two sets of options is
        empty, the number is an integer.
        """
        a = all(g.is_number for g in G._left | G._right)
        b = all(G_L < G_R for G_L in G._left for G_R in G._right)
        return a and b

    @property
    def is_numberish(G):
        """
        A Game is numberish if it is infinitesimally close to a number.

        Returns
        -------
        numberish : bool
            Whether G is numberish or not.
        """
        from .tools import left_stop, right_stop
        return left_stop(G, adorn=False) == right_stop(G, adorn=False)

    @property
    def is_switch(G):
        """
        A game is a switch if it's left and right options are numbers, and G_L > G_R.

        Returns
        -------
        number : bool
            Whether G is a switch or not.
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
        The birthday of a game G is defined as the one more than the maximum birthday of its
        options.

        Returns
        -------
        bday : int
            G's birthday.
        """
        if G._left == G._right == set():
            bday = 0
        else:
            bday = max(g.birthday for g in G._left | G._right) + 1

        return bday

    @property
    def outcome(G):
        """
        The outcome of a Game belongs to one of four equivalence classes:

            P : A win for the second player.
            N : A win for the first player.
            L : A win for the left player, regardless of play order.
            R : A win for the right player, regardless of play order.

        Returns
        -------
        o : Outcome
            The outcome class of game G.
        """
        zero = Game()
        if G == zero:
            return Outcome.PREVIOUS
        elif G > zero:
            return Outcome.LEFT
        elif G < zero:
            return Outcome.RIGHT
        else:
            return Outcome.NEXT

    @property
    def value(G):
        """
        The value of the game in short-hand.

        Returns
        -------
        v : str
            The value of the Game as a string.
        """
        return _value_str(G)


Symbol = namedtuple('Symbol', ['unicode', 'latex'])


_SYMBOLS = {
    'star': Symbol('*', r'\ensuremath{\ast}'),
    'up': Symbol('↑', r'\ensuremath{\uparrow}'),
    'down': Symbol('↓', r'\ensuremath{\downarrow}'),
    '2up': Symbol('↑↑', r'\ensuremath{\Uparrow}'),
    '2down': Symbol('↓↓', r'\ensuremath{\Downarrow}'),
    'cdot': Symbol('·', r'\ensuremath{\cdot}'),
    'pm': Symbol('±', r'\ensuremath{\pm}'),
    'frac': Symbol((lambda n, d: f"{n}/{d}"), (lambda n, d: f'\\ensuremath{{\\nicefrac{{{n}}}{{{d}}}}}')),
    'miny': Symbol((lambda g: '⧿_' + g), (lambda g: r'\ensuremath{\tminus}_{' + g + '}')),
    'tiny': Symbol((lambda g: '⧾_' + g), (lambda g: r'\ensuremath{\tplus}_{' + g + '}')),
}


@lru_cache(maxsize=None)
def _value_str(G, latex=False):
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
                return f"{i}" + _SYMBOLS['cdot'][bool(latex)] + \
                                _SYMBOLS['up'][bool(latex)] + \
                                _SYMBOLS['star'][bool(latex)] * ((i+1) % 2)
            elif g_hash == up_star:
                return f"{i}" + _SYMBOLS['cdot'][bool(latex)] + \
                                _SYMBOLS['up'][bool(latex)] + \
                                _SYMBOLS['star'][bool(latex)] * (i % 2)
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
                return f"{i}" + _SYMBOLS['cdot'][bool(latex)] + \
                                _SYMBOLS['down'][bool(latex)] + \
                                _SYMBOLS['star'][bool(latex)] * ((i+1) % 2)
            elif g_hash == down_star:
                return f"{i}" + _SYMBOLS['cdot'][bool(latex)] + \
                                _SYMBOLS['down'][bool(latex)] + \
                                _SYMBOLS['star'][bool(latex)] * (i % 2)
        else:
            break

    # nimbers
    if G.is_impartial:
        return _SYMBOLS['star'][bool(latex)] + f"{len(G._left)}"

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

        v = (lf + rf) / 2
        n, d = v.numerator, v.denominator
        return _SYMBOLS['frac'][bool(latex)](n, d)

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
                    return f"{mean}" + _SYMBOLS['pm'][bool(latex)] + f"{diff}"
                else:
                    return _SYMBOLS['pm'][bool(latex)] + f"{diff}"

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
