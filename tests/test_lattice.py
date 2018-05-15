"""
"""

import pytest

from ludology import Game
from ludology.lattice import all_games_gen, build_poset_lattice


def test_all_games_gen_1():
    """
    """
    gen1a = {Game(), Game(1), Game(-1), Game({0}, {0})}
    gen1b = all_games_gen(1)
    assert gen1a == gen1b


def test_all_games_gen_2():
    """
    """
    gen2 = all_games_gen(2)
    assert len(gen2) == 22


def test_build_poset_lattice():
    """
    """
    lattice = build_poset_lattice(all_games_gen(2))
    assert len(lattice.edges()) == 36