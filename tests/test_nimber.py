"""
"""

import pytest

from ludology import Game, Nimber


def test_add_nimbers():
    """
    """
    a = Nimber(5)
    b = Nimber(6)
    c = Nimber(3)
    assert a + b == c


def test_add_nimber_game():
    """
    """
    a = Nimber(3)
    b = Game(Nimber(2))
    c = Game(Nimber(1))
    assert a + b == c


def test_mul_nimbers():
    """
    """
    a = Nimber(2)
    b = Nimber(6)
    c = Nimber(11)
    assert a * b == c


def test_mul_nimber_game():
    """
    """
    a = Nimber(2)
    b = Game(Nimber(2))
    c = Game(Nimber(3))
    assert a * b == c


def test_neg_nimbers():
    """
    """
    a = Nimber(5)
    assert a == -a


def test_eq_nimber_game():
    """
    """
    a = Nimber(3)
    b = Game(3)
    assert not a == b


def test_fail():
    """
    """
    with pytest.raises(ValueError):
        Nimber(0.5)


@pytest.mark.parametrize(['n', 'v'], [
    (0, '0'),
    (1, '∗'),
    (6, '∗6'),
])
def test_nimber_value(n, v):
    """
    """
    assert Nimber(n).value == v


@pytest.mark.parametrize('n', [
    Nimber(0),
    Nimber(3),
    Nimber(7),
])
def test_nimber_is_number(n):
    """
    """
    assert not n.is_number


@pytest.mark.parametrize('n', [
    Nimber(0),
    Nimber(3),
    Nimber(7),
])
def test_nimber_is_impartial(n):
    """
    """
    assert n.is_impartial


@pytest.mark.parametrize('n', [
    0,
    3,
    7,
])
def test_nimber_birthday(n):
    """
    """
    assert Nimber(n).birthday == n
