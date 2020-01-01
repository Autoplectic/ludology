# -*- coding: utf-8 -*-

"""
Tests for ludology.tools.
"""

import pytest

import sys

from hypothesis import given
from ludology.hypothesis import games, nimbers

from ludology import Game, Nimber
from ludology.closet import zero, pm_one, star
from ludology.sums import conjunctive
from ludology.tools import (canonicalize, left_stop, right_stop,
                            left_incentives, right_incentives, remoteness)


# double the recursion limit:
sys.setrecursionlimit(2 * sys.getrecursionlimit())


@pytest.mark.parametrize(('g', 'v'), [
    (zero, (0, '+')),
    (pm_one, (1, '-')),
    (star, (0, '-')),
])
def test_left_stop_1(g, v):
    """
    Test left stops with adornment.
    """
    stop = left_stop(g)
    assert stop == v


@pytest.mark.parametrize(('g', 'v'), [
    (zero, 0),
    (pm_one, 1),
    (star, 0),
])
def test_left_stop_2(g, v):
    """
    Test left stops without adornment.
    """
    stop = left_stop(g, adorn=False)
    assert stop == v


@pytest.mark.parametrize(('g', 'v'), [
    (zero, (0, '-')),
    (pm_one, (-1, '+')),
    (star, (0, '+')),
])
def test_right_stop_1(g, v):
    """
    Test right stops with adornment.
    """
    stop = right_stop(g)
    assert stop == v


@pytest.mark.parametrize(('g', 'v'), [
    (zero, 0),
    (pm_one, -1),
    (star, 0),
])
def test_right_stop_2(g, v):
    """
    Test right stops without adornment.
    """
    stop = right_stop(g, adorn=False)
    assert stop == v


def test_left_incentives():
    """
    Test for the incentives of a known example.
    """
    g = Game({0}, {Game({0}, {-2})})
    li = {Game({Game({2}, {0})}, {0})}
    assert left_incentives(g) == li


def test_right_incentives():
    """
    Test for the incentives of a known example.
    """
    g = Game({0}, {Game({0}, {-2})})
    ri = {Game({Game({2}, {0}), 2}, {0})}
    assert right_incentives(g) == ri


@given(G=games())
def test_canonicalize(G):
    """
    Test that canonicalizing doesn't effect the value of the game.
    """
    assert canonicalize(G) == G


@given(G=nimbers(max_value=5), H=nimbers(max_value=5))
def test_remoteness(G, H):
    """
    Tests for remoteness.
    """
    assert remoteness(Nimber(conjunctive(G, H))) == min([remoteness(G), remoteness(H)])
