"""
The basic Game class.
"""

from copy import copy
from enum import Enum
from fractions import Fraction
from functools import lru_cache, wraps


__all__ = [
    'Game',
    'Outcome',
]


def gamify_inputs(f):
    """
    Construct a decorator to cast all arguments to a function into Games.

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
    The outcome classes for Partizan Games under normal play conditions.

    Each Game belongs to one of four outcome classes:
      - P: The Game is a win for the previous player.
      - N: The Game is a win for the next player.
      - L: The Game is a win for the left player.
      - R: The Game is a win for the right player.
    """

    PREVIOUS = 'P'
    NEXT = 'N'
    LEFT = 'L'
    RIGHT = 'R'


class Game(object):
    """
    Partizan Games.

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
                    G._left = {Game(v - 1)}
                    G._right = set()
                else:
                    G._left = set()
                    G._right = {Game(v + 1)}
            else:
                _, d = v.as_integer_ratio()
                if d > 1024:
                    msg = f"{v} would result in a very deep game tree."
                    raise ValueError(msg)
                G._left = {Game(v - 1 / d)}
                G._right = {Game(v + 1 / d)}
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

    @property
    def left(G):
        """
        The left set.

        Returns
        -------
        G_L : set
            The left set.
        """
        return copy(G._left)

    @property
    def right(G):
        """
        The right set.

        Returns
        -------
        G_R : set
            The right set.
        """
        return copy(G._right)

    @gamify_inputs
    # @lru_cache(maxsize=None)
    def __ge__(G, H):
        """
        Determine if G is greater than H.

        A Game G is greater than or equal to a Game H so long as there are no
        G_R such that H >= G_R and there are no H_L such that H_L >= G.

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
        Determine if G is less than or equal to H.

        A Game G is less than or equal to H if H is greather than or equal to G:
        .. math::
           G <= H <=> H >= G.

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
        Determine if G is strictly greather than H.

        G is strictly greather than H if:
        .. math::
           G > H <=> G >= H and not H >= G.

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
        Determine if G is strictly less than H.

        G is strictly less than H if H is strictly greather than G:
        .. math::
           G < H <=> H > G

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
        Determine if G and H are equal.

        G and H are equal if G is greater than or equal to H, and H is greater
        than or equal to G:
        .. math::
           G == H <=> G >= H and G <= H.

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
        Determine if G is confused with H.

        G | H ('fuzzy' or 'confused with') if neither G >= H nor G <= H:
        .. math::
           G | H <=> not G >= H and not H >= G

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
        Determine if G is confused with H.

        G | H ('fuzzy' or 'confused with') if neither G >= H nor G <= H:
        .. math::
           G | H <=> not G >= H and not H >= G

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
        Compute the negation of G.

        -{G_L | G_R} is defined recursively as {-G_R | -G_L}.

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
        Compute the disjoint sum of G and H.

        The disjoint sum is defined as the result of playing on exactly one of G
        or H. Therefore, the left options of G + H are of the form G + H_L and
        H + G_L:
        .. math::
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
        Compute the disjoint sum of G and H.

        The disjoint sum is defined as the result of playing on exactly one of G
        or H. Therefore, the left options of G + H are of the form G + H_L and
        H + G_L:
        .. math::
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
        Compute the disjoint difference of G and H.

        The difference is defined as the sum of G and -H:
        .. math::
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
        Compute the Norton product of G and H.

        The product is defined by the property:
        .. math::
           a' < a, b' < b => (a - a') * (b - b') > 0
                          => a' * b + a * b' - a' * b' < a * b

        implying that quantities like the sum on the left should be in the left
        set of a * b.

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
        Compute the Norton product of G and H.

        The product is defined by the property:
        .. math::
           a' < a, b' < b => (a - a') * (b - b') > 0
                          => a' * b + a * b' - a' * b' < a * b

        implying that quantities like the sum on the left should be in the left
        set of a * b.

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
        Compute the inverse the Game G.

        The inverse is defined as:

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
        Compute the Norton quotient of G by H.

        The Norton quotient is defined as:
        .. math::
           G / H = G * (1 / H)

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
        Construct the hash of a Game.

        We define the hash as the hash of the left and right options. Python
        does the "right thing" and sets with equal members have the same hash.

        Returns
        -------
        hash : int
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
        Construct the repr for G.

        G is represented with the canonical Conway notation: {G_L | G_R}, where
        the options are their shorthand values if possible.

        Returns
        -------
        repr : str
            A representation of G.
        """
        lefts = ', '.join(G_L.value for G_L in sorted(G._left, key=str))
        rights = ', '.join(G_R.value for G_R in sorted(G._right, key=str))
        return f'{{{lefts}｜{rights}}}'

    def subpositions(G):
        """
        Construct an iterator over all subpositions of G.

        A subposition is G, or any Game reachable through any sequence of left
        or right options.

        Yields
        ------
        g : Game
            A subposition of G.
        """
        yield G
        for g in G._left | G._right:
            yield g
            yield from g.subpositions()

    @property
    def is_impartial(G):
        """
        Determine if G is impartial.

        A game is impartial if its left options equal its right options, and
        each of its options are impartial.

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
        Determine if G is dicotic.

        A dicotic, or all-small, Game is one where either both or neither player
        have options at every subposition. These are necessarily infinitesimal.

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
        Determine if G is infinitesimal.

        A Game is infinitesimal if it is non-zero and smaller than any positive
        real number and greater than any negative real number. Equivalently,
        it's left and right stops are both zero. Note, this does not imply that
        an infinitesimal can not be positive (> 0) or negative (< 0).

        Returns
        -------
        infinitesimal : bool
            Whether the game is infinitesimal or not.
        """
        from ..tools import left_stop, right_stop
        a = left_stop(G, adorn=False) == right_stop(G, adorn=False) == 0
        b = G != 0
        return a and b

    @property
    def is_number(G):
        """
        Determine if G is a number.

        A game is a (surreal) number if each of it left options is less than
        each of its right options, and all its options are also numbers.

        Returns
        -------
        number : bool
            Whether G is a number or not.

        Note
        ----
        The definition implies that, in canonical form, the number has at most
        one left option and one right option, because one must dominate. Also,
        if either of the two sets of options is empty, the number is an integer.
        """
        a = all(g.is_number for g in G._left | G._right)
        b = all(G_L < G_R for G_L in G._left for G_R in G._right)
        return a and b

    @property
    def is_numberish(G):
        """
        Determine if G is numberish.

        A Game is numberish if it is infinitesimally close to a number.

        Returns
        -------
        numberish : bool
            Whether G is numberish or not.
        """
        from ..tools import left_stop, right_stop
        return left_stop(G, adorn=False) == right_stop(G, adorn=False)

    @property
    def is_switch(G):
        """
        Determine if G is a switch.

        A game is a switch if it's left and right options are single numbers
        such that G_L > G_R.

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
        The birthday of G.

        The birthday of a game G is defined as the one more than the maximum
        birthday of its options. The birthday of the Game 0 is 0. It is the
        number of iterations one must apply, starting from the Game 0, to
        construct G under the normal Conway construction of a Game.

        Returns
        -------
        bday : int
            G's birthday.
        """
        if not G._left | G._right:
            return 0

        return max(g.birthday for g in G._left | G._right) + 1

    @property
    def outcome(G):
        """
        The outcome class of G.

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
        The value of the Game.

        The value of the game, potentially using the standard short-hand names
        for many important types of Games.

        Returns
        -------
        v : str
            The value of the Game as a string.
        """
        from .printing import value_str

        return value_str(G)
