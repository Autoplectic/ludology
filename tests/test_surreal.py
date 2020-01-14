"""
Tests for ludology.surreal.
"""

import pytest

from ludology import Game, Surreal
from ludology.closet import one, star, zero


@pytest.mark.parametrize('n', [
    Surreal.from_value(0),
    Surreal.from_value(1 / 2),
    Surreal.from_value(0.125),
    Surreal.from_value(-1),
    Surreal.from_value(2),
])
def test_is_number(n):
    """
    Test that all Surreals are numbers.
    """
    assert n.is_number


@pytest.mark.parametrize(('n', 'v'), [
    (Surreal.from_value(0), True),
    (Surreal.from_value(1 / 2), False),
    (Surreal.from_value(0.125), False),
    (Surreal.from_value(-1), False),
    (Surreal.from_value(2), False),
])
def test_is_impartial(n, v):
    """
    Test that all Surreals (other than 0) are not impartial.
    """
    assert n.is_impartial == v


@pytest.mark.parametrize(('n', 'v'), [
    (Surreal.from_value(0), True),
    (Surreal.from_value(1 / 2), False),
    (Surreal.from_value(0.125), False),
    (Surreal.from_value(-1), False),
    (Surreal.from_value(2), False),
])
def test_is_dicotic(n, v):
    """
    Test that all Surreals (other than 0) are not dicotic.
    """
    assert n.is_dicotic == v


@pytest.mark.parametrize('n', [
    Surreal.from_value(0),
    Surreal.from_value(1 / 2),
    Surreal.from_value(0.125),
    Surreal.from_value(-1),
    Surreal.from_value(2),
])
def test_is_infinitesimal(n):
    """
    Test that all Surreals are not infinitesimal.
    """
    assert not n.is_infinitesimal


@pytest.mark.parametrize('n', [
    Surreal.from_value(0),
    Surreal.from_value(1 / 2),
    Surreal.from_value(0.125),
    Surreal.from_value(-1),
    Surreal.from_value(2),
])
def test_is_numberish(n):
    """
    Test that all Surreals are numberish.
    """
    assert n.is_numberish


@pytest.mark.parametrize('n', [
    Surreal.from_value(0),
    Surreal.from_value(1 / 2),
    Surreal.from_value(0.125),
    Surreal.from_value(-1),
    Surreal.from_value(2),
])
def test_is_switch(n):
    """
    Test that no Surreals are switches.
    """
    assert not n.is_switch


@pytest.mark.parametrize(('a', 'b'), [
    (0, 0),
    (1, 0),
    (-1, 0),
    (-1, 1),
    (1 / 2, 1 / 2),
    (1 / 2, 1),
])
def test_order(a, b):
    """
    Test the addition of two Surreals.
    """
    assert (Surreal.from_value(a) >= Surreal.from_value(b)) == (a >= b)


@pytest.mark.parametrize(('a', 'b'), [
    (Surreal.from_value(0), zero),
    (Surreal.from_value(1 / 2), zero),
    (Surreal.from_value(3 / 4), star),
])
def test_order_game(a, b):
    """
    Test the addition of two Surreals.
    """
    assert a >= b


@pytest.mark.parametrize(('a', 'b'), [
    (0, 0),
    (1, 0),
    (-1, 0),
    (-1, 1),
    (1 / 2, 1 / 2),
    (1 / 2, 1),
])
def test_add(a, b):
    """
    Test the addition of two Surreals.
    """
    assert Surreal.from_value(a) + Surreal.from_value(b) == Surreal.from_value(a + b)


@pytest.mark.parametrize(('a', 'b', 'c'), [
    (Surreal.from_value(1), star, one + star),
    (Surreal.from_value(2), 3 * one, Surreal.from_value(5)),
])
def test_add_game(a, b, c):
    """
    Test the addition of a Surreal with a Game.
    """
    assert a + b == c


@pytest.mark.parametrize(('a', 'b'), [
    (0, 0),
    (1, 0),
    (-1, 0),
    (-1, 1),
    (1 / 2, 1 / 2),
    (1 / 2, 1),
])
def test_add_game_2(a, b):
    """
    Test the addition of two Surreals.
    """
    assert Surreal.from_value(a) + Surreal.from_value(b) == Game(a + b)


@pytest.mark.parametrize(('a', 'b'), [
    (0, 0),
    (1, 0),
    (-1, 0),
    (-1, 1),
    (1 / 2, 1 / 2),
    (1 / 2, 1),
])
def test_mul(a, b):
    """
    Test the multiplication of two Surreals.
    """
    assert Surreal.from_value(a) * Surreal.from_value(b) == Surreal.from_value(a * b)


@pytest.mark.parametrize(('a', 'b'), [
    (0, 0),
    (1, 0),
    (-1, 0),
    (-1, 1),
    (1 / 2, 1 / 2),
    (1 / 2, 1),
])
def test_mul_game(a, b):
    """
    Test the multiplication of two Surreals.
    """
    assert Surreal.from_value(a) * Game(b) == Surreal.from_value(a * b)


@pytest.mark.parametrize(('a', 'b'), [
    (0, 0),
    (1, 0),
    (-1, 0),
    (-1, 1),
    (1 / 2, 1 / 2),
    (1 / 2, 1),
])
def test_mul_game_2(a, b):
    """
    Test the multiplication of two Surreals.
    """
    assert Surreal.from_value(a) * Surreal.from_value(b) == Game(a * b)


@pytest.mark.parametrize(('a', 'b'), [
    (1, 1),
    (1, 1 / 2),
    (2, 1),
])
def test_div(a, b):
    """
    Test the division of two Surreals.
    """
    assert Surreal.from_value(a) / Surreal.from_value(b) == Surreal.from_value(a / b)


@pytest.mark.xfail
@pytest.mark.parametrize(('a', 'b'), [
    (1, 1),
    (1, 1 / 2),
    (2, 1),
])
def test_div_game(a, b):
    """
    Test the division of a Surreal by a Game.
    """
    assert Surreal.from_value(a) / Game(b) == Game(a / b)


@pytest.mark.parametrize('n', [
    1,
    2,
    8,
    1 / 2,
    1 / 4,
])
def test_invert(n):
    """
    Test the inversion of a Surreal.
    """
    assert Surreal.from_value(n)._invert() == Surreal.from_value(1 / n)


def test_surreal_fail():
    """
    Test that Surreal doesn't try to construct things like 1/3.
    """
    with pytest.raises(ValueError):
        Surreal.from_value(1 / 3)
