"""
Tests for ludology.nimber.
"""

import pytest

from ludology import FarStar, Game, Nimber
from ludology.closet import one


def test_add_nimbers():
    """
    Test that Nimbers add correctly.
    """
    a = Nimber.from_integer(5)
    b = Nimber.from_integer(6)
    c = Nimber.from_integer(3)
    assert a + b == c


def test_add_nimber_game():
    """
    Test that Nimbers add with Games correctly.
    """
    a = Nimber.from_integer(3)
    b = Game(Nimber.from_integer(2))
    c = Game(Nimber.from_integer(1))
    assert a + b == c


def test_mul_nimbers():
    """
    Test that Nimbers multiply correctly.
    """
    a = Nimber.from_integer(2)
    b = Nimber.from_integer(6)
    c = Nimber.from_integer(11)
    assert a * b == c


def test_mul_nimber_game():
    """
    Test that Nimbers multiply with Games correctly.
    """
    a = Nimber.from_integer(2)
    b = Game(Nimber.from_integer(2))
    c = Game(Nimber.from_integer(3))
    assert a * b == c


def test_neg_nimbers():
    """
    Test that a Nimber is its own negative.
    """
    a = Nimber.from_integer(5)
    assert a == -a


def test_eq_nimber_game():
    """
    Test that Nimbers and Games equate properly.
    """
    a = Nimber.from_integer(3)
    b = 3 * one
    assert not a == b


def test_fail():
    """
    Test that Nimbers must have integral values.
    """
    with pytest.raises(ValueError):
        Nimber.from_integer(0.5)


@pytest.mark.parametrize(('n', 'v'), [
    (0, '0'),
    (1, '∗'),
    (6, '∗6'),
])
def test_nimber_value(n, v):
    """
    Test that the value of a Nimber is represented correctly.
    """
    assert Nimber.from_integer(n).value == v


@pytest.mark.parametrize('n', [
    Nimber.from_integer(3),
    Nimber.from_integer(4),
    Nimber.from_integer(7),
])
def test_nimber_is_number(n):
    """
    Test that Nimbers (other than 0) are not numbers.
    """
    assert not n.is_number


def test_nimber_is_number_2():
    """
    Test that the Nimber 0 is a number.
    """
    assert Nimber.from_integer(0).is_number


@pytest.mark.parametrize('n', [
    Nimber.from_integer(3),
    Nimber.from_integer(4),
    Nimber.from_integer(7),
])
def test_nimber_is_infinitesimal(n):
    """
    Test that Nimbers (other than 0) are infinitesimal.
    """
    assert n.is_infinitesimal


def test_nimber_is_infinitesimal_2():
    """
    Test that the Nimber 0 is not infinitesimal.
    """
    assert not Nimber.from_integer(0).is_infinitesimal


@pytest.mark.parametrize('n', [
    Nimber.from_integer(0),
    Nimber.from_integer(3),
    Nimber.from_integer(7),
])
def test_nimber_is_impartial(n):
    """
    Test that all Nimbers are impartial.
    """
    assert n.is_impartial


@pytest.mark.parametrize('n', [
    Nimber.from_integer(0),
    Nimber.from_integer(3),
    Nimber.from_integer(7),
])
def test_nimber_is_numberish(n):
    """
    Test that all Nimbers are numberish.
    """
    assert n.is_numberish


@pytest.mark.parametrize('n', [
    Nimber.from_integer(0),
    Nimber.from_integer(3),
    Nimber.from_integer(7),
])
def test_nimber_is_dicotic(n):
    """
    Test that all Nimbers are dicotic.
    """
    assert n.is_dicotic


@pytest.mark.parametrize('n', [
    0,
    3,
    7,
])
def test_nimber_birthday(n):
    """
    Test that Nimbers have the right birthdays.
    """
    assert Nimber.from_integer(n).birthday == n


@pytest.mark.parametrize('n', [
    Nimber.from_integer(0),
    Nimber.from_integer(1),
    Nimber.from_integer(2),
])
def test_far_star_sum(n):
    """
    Test that far-star sums to far-star.
    """
    fs = FarStar()
    assert fs + n == fs


def test_far_star_value():
    """
    Test that far star has the right value.
    """
    assert FarStar().value == "☆"


@pytest.mark.parametrize('n', [
    Nimber.from_integer(0),
    Nimber.from_integer(2),
    Nimber.from_integer(7),
])
def test_far_star_left(n):
    """
    Test that far star's left set contains an arbitrary Nimber.
    """
    assert n in FarStar().left


@pytest.mark.parametrize('n', [
    Nimber.from_integer(0),
    Nimber.from_integer(2),
    Nimber.from_integer(7),
])
def test_far_star_right(n):
    """
    Test that far star's right set contains an arbitrary Nimber.
    """
    assert n in FarStar().right
