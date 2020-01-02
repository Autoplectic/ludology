# -*- coding: utf-8 -*-

"""
Tests for ludology.sums.
"""

import pytest

from ludology import Game, canonicalize
from ludology.closet import one, pm_one, star, up, zero
from ludology.sums import (conjunctive, continued_conjunctive,
                           diminished_disjunctive, disjunctive, ordinal,
                           selective, sequential, shortened_selective, side)


G = Game({0}, {pm_one})


@pytest.mark.parametrize(('G', 'H', 'J'), [
    (G, up, Game({1}, {Game({1}, {1})})),
    (G, zero, G),
    (zero, G, G),
])
def test_disjunctive(G, H, J):
    """
    Test that the disjunctive sum matches known results.
    """
    assert canonicalize(disjunctive(G, H)) == J


@pytest.mark.parametrize(('G', 'H', 'J'), [
    (G, up, Game({1}, {Game({1}, {1})})),
    (G, zero, G),
    (zero, G, G),
])
def test_disjunctive_2(G, H, J):
    """
    Test that the disjunctive sum matches known results, without canonizing.
    """
    assert canonicalize(disjunctive(G, H, canon=False)) == J


@pytest.mark.parametrize(('G', 'H', 'J'), [
    (G, up, up),
    (G, zero, zero),
    (zero, G, zero),
])
def test_conjunctive(G, H, J):
    """
    Test that the conjunctive sum matches known results.
    """
    assert canonicalize(conjunctive(G, H)) == J


@pytest.mark.parametrize(('G', 'H', 'J'), [
    (G, up, Game({1}, {Game({1, one + star}, {-1, -one + star}), Game({1}, {1, pm_one})})),
    (G, zero, G),
    (zero, G, G),
])
def test_selective(G, H, J):
    """
    Test that the selective sum matches known results.
    """
    assert canonicalize(selective(G, H)) == J


@pytest.mark.parametrize(('G', 'H', 'J'), [
    (G, up, up),
    (G, zero, zero),
    (zero, G, zero),
])
def test_diminished_disjunctive(G, H, J):
    """
    Test that the diminished disjunctive sum matches known results.
    """
    assert canonicalize(diminished_disjunctive(G, H)) == J


@pytest.mark.parametrize(('G', 'H', 'J'), [
    (G, up, one),
    (G, zero, G),
    (zero, G, G),
])
def test_continued_conjunctive(G, H, J):
    """
    Test that the continued conjunctive sum matches known results.
    """
    assert canonicalize(continued_conjunctive(G, H)) == J


@pytest.mark.parametrize(('G', 'H', 'J'), [
    (G, up, Game({0}, {star, Game({0, star}, {0, star})})),
    (G, zero, zero),
    (zero, G, zero),
])
def test_shortened_selective(G, H, J):
    """
    Test that the shortened selective sum matches known results.
    """
    assert canonicalize(shortened_selective(G, H)) == J


@pytest.mark.parametrize(('G', 'H', 'J'), [
    (G, up, Game({1}, {Game({1}, {1, pm_one}), pm_one})),
    (G, zero, G),
    (zero, G, G),
])
def test_ordinal(G, H, J):
    """
    Test that the ordinal sum matches known results.
    """
    assert canonicalize(ordinal(G, H)) == J


@pytest.mark.parametrize(('G', 'H', 'J'), [
    (G, up, Game({0}, {1 / 2})),
    (G, zero, G),
    (zero, G, G),
])
def test_side(G, H, J):
    """
    Test that the side sum matches known results.
    """
    assert canonicalize(side(G, H)) == J


@pytest.mark.parametrize(('G', 'H', 'J'), [
    (G, up, one),
    (G, zero, G),
    (zero, G, G),
])
def test_sequential(G, H, J):
    """
    Test that the sequential sum matches known results.
    """
    assert canonicalize(sequential(G, H)) == J
