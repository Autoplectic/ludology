"""
Tests for ludology.surreal.
"""

import pytest

from ludology import Surreal


@pytest.mark.paramtrize('n', [
    Surreal(0),
    Surreal(1/2),
    Surreal(0.125),
    Surreal(-1),
    Surreal(2),
])
def test_is_number(n):
    """
    """
    assert n.is_number


@pytest.mark.paramtrize(['n', 'v'], [
    (Surreal(0), True),
    (Surreal(1/2), False),
    (Surreal(0.125), False),
    (Surreal(-1), False),
    (Surreal(2), False),
])
def test_is_impartial(n, v):
    """
    """
    assert n.is_impartial == v


@pytest.mark.paramtrize('n', [
    Surreal(0),
    Surreal(1/2),
    Surreal(0.125),
    Surreal(-1),
    Surreal(2),
])
def test_is_switch(n):
    """
    """
    assert not n.is_switch
