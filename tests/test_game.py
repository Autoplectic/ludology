"""
Tests for ludology.game.
"""

import pytest
from hypothesis import given
from hypothesis.strategies import integers

from ludology import Game
from ludology.canonical_form import canonical_form
from ludology.closet import half, miny, one, pm_one, star, star2, tiny, up, zero
from ludology.games import Outcome
from ludology.games.printing import unicode_fraction


@pytest.mark.parametrize(('g1', 'g2'), [
    (one, zero),
    (one, half),
    (one, -one),
    (zero, -one),
    (zero, -half),
    (up, zero),
    (half, up),
    (up + up, star),
    (zero, zero),
    (up, up),
])
def test_ge(g1, g2):
    """
    Test the ordering of several Games.
    """
    assert g1 >= g2


@pytest.mark.parametrize(('g1', 'g2'), [
    (one, zero),
    (one, half),
    (one, -one),
    (zero, -one),
    (zero, -half),
    (up, zero),
    (half, up),
    (up + up, star),
])
def test_gt(g1, g2):
    """
    Test the ordering of several Games.
    """
    assert g1 > g2


@pytest.mark.parametrize(('g1', 'g2'), [
    (zero, one),
    (half, one),
    (-one, one),
    (-one, zero),
    (-half, zero),
    (zero, up),
    (up, half),
    (star, up + up),
    (zero, zero),
    (up, up),
])
def test_le(g1, g2):
    """
    Test the ordering of several Games.
    """
    assert g1 <= g2


@pytest.mark.parametrize(('g1', 'g2'), [
    (zero, one),
    (half, one),
    (-one, one),
    (-one, zero),
    (-half, zero),
    (zero, up),
    (up, half),
    (star, up + up),
])
def test_lt(g1, g2):
    """
    Test the ordering of several Games.
    """
    assert g1 < g2


@pytest.mark.parametrize(('g1', 'g2'), [
    (star, zero),
    (star, up),
    (one, pm_one),
    (pm_one, -one),
    (pm_one, star),
    (pm_one, zero),
])
def test_fuzzy_1(g1, g2):
    """
    Test the ordering of several Games.
    """
    assert g1 | g2


def test_fuzzy_2():
    """
    Test the ordering of several Games.
    """
    assert star | 0
    assert 0 | star


def test_equiv_1():
    """
    Test the ordering of several Games.
    """
    g = Game({star})
    assert g == zero


def test_equiv_2():
    """
    Test the ordering of several Games.
    """
    g = Game(right={star})
    assert g == zero


@pytest.mark.parametrize('g', [
    zero,
    star,
    star2,
])
def test_impartial(g):
    """
    Test that these games are impartial.
    """
    assert g.is_impartial


@pytest.mark.parametrize('g', [
    one,
    half,
    up,
    up + star,
    pm_one,
])
def test_not_impartial(g):
    """
    Test that these games are not impartial.
    """
    assert not g.is_impartial


@pytest.mark.parametrize('g', [
    star,
    up,
    -up,
    Game({0}, {Game({0}, {-1})}),
])
def test_infinitesimal(g):
    """
    Test that these games are infinitesimal.
    """
    assert g.is_infinitesimal


@pytest.mark.parametrize('g', [
    half,
    one,
    zero,
    pm_one,
])
def test_not_infinitesimal(g):
    """
    Test that these games are not infinitesimal.
    """
    assert not g.is_infinitesimal


@pytest.mark.parametrize('g', [
    pm_one,
    Game({2}, {1}),
])
def test_switch(g):
    """
    Test that these games are switches.
    """
    assert g.is_switch


@pytest.mark.parametrize('g', [
    zero,
    one,
    up,
    star,
])
def test_not_switch(g):
    """
    Test that these games are not switches.
    """
    assert not g.is_switch


@pytest.mark.parametrize('g', [
    star,
    up,
    zero,
])
def test_dicotic(g):
    """
    Test that these games are dicotic.
    """
    assert g.is_dicotic


@pytest.mark.parametrize('g', [
    miny(3),
    one,
    pm_one,
    tiny(one),
])
def test_not_dicotic(g):
    """
    Test that these games are not dicotic.
    """
    assert not g.is_dicotic


@pytest.mark.parametrize('g', [
    star,
    up,
    -up,
    one + star,
    -3 + up,
])
def test_numberish(g):
    """
    Test that these games are numberish.
    """
    assert g.is_numberish


@pytest.mark.parametrize('g', [
    pm_one,
    Game({5 / 2, Game({4}, {2})}, {Game({-1}, {-2}), Game({0}, {-4})}),
])
def test_not_numberish(g):
    """
    Test that these games are not numberish.
    """
    assert not g.is_numberish


@pytest.mark.parametrize(('g', 'bday'), [
    (zero, 0),
    (one, 1),
    (-one, 1),
    (star, 1),
    (up, 2),
    (canonical_form(up + star), 2),
    (half, 2),
])
def test_birthday(g, bday):
    """
    Test some birthdays.
    """
    assert g.birthday == bday


@pytest.mark.parametrize(('g', 'sp'), [
    (up, {up, zero, star, zero}),
])
def test_subpositions(g, sp):
    """
    Test that subpositions are yielded correctly.
    """
    assert set(g.subpositions()) == sp


@pytest.mark.parametrize(('a', 'b', 'c'), [
    (zero, zero, zero),
    (star, star, zero),
    (one, -one, zero),
    (one, zero, one),
    (zero, one, one),
    (one, 0, one),
    (0, one, one),
    (one, star, Game({one}, {one})),
    (star, one, Game({one}, {one})),
])
def test_add(a, b, c):
    """
    Test Game addition.
    """
    assert a + b == c


@pytest.mark.parametrize(('a', 'b', 'c'), [
    (zero, zero, zero),
    (star, star, star),
    (one, -one, -1),
    (one + 1, 1, 2),
    (2, one, one + one),
])
def test_mul(a, b, c):
    """
    Test Game multiplication.
    """
    assert a * b == c


@pytest.mark.parametrize(('g', 'o'), [
    (zero, Outcome.PREVIOUS),
    (star, Outcome.NEXT),
    (one, Outcome.LEFT),
    (up, Outcome.LEFT),
    (-up, Outcome.RIGHT),
])
def test_outcome(g, o):
    """
    Test the outcome class of several games.
    """
    assert g.outcome == o


@pytest.mark.parametrize(('g', 'v'), [
    (star, '∗'),
    (pm_one, '±1'),
    (Game({Game(3)}, {Game(1)}), '2±1'),
    (up, '↑'),
    (2 * up, '⇑'),
    (up + star, '↑∗'),
    (up + up + star, '⇑∗'),
    (-up, '↓'),
    (2 * -up, '⇓'),
    (-up + star, '↓∗'),
    (-up + -up + star, '⇓∗'),
    (Game({one}, {1}), '1∗'),
    (Game({0}, {Game({0}, {-2})}), '⧾_2'),
    (Game({Game({2}, {0})}, {0}), '⧿_2'),
    (star2, '∗2'),
    (Game({5 / 2, Game({4}, {2})}, {Game({-1}, {-2}), Game({0}, {-4})}), '{3±1, ⁵⁄₂｜-2±2, -³⁄₂±½}'),
    (Game({0}, {star2}), '{0｜∗2}'),
    (Game({star2}, {0}), '{∗2｜0}'),
])
def test_value(g, v):
    """
    Test that several games evaluate to the correct short-hand value.
    """
    assert g.value == v


@given(integers(min_value=-7, max_value=7), integers(min_value=0, max_value=3))
def test_value_dyadic_rational(m, j):
    """
    Test the construction of dyadic rationals.
    """
    frac = m / 2**j
    num, denom = frac.as_integer_ratio()
    string = unicode_fraction(num, denom)
    game = Game(frac)
    assert game.value == string


def test_game_fail():
    """
    Test that Game punts when constructing "deep" games.
    """
    with pytest.raises(ValueError):
        Game(1 / 3)
