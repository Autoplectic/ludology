# -*- coding: utf-8 -*-

"""
Tests for ludology.closet.
"""

from hypothesis import given

from ludology.closet import tiny, up
from ludology.hypothesis import games


@given(G=games())
def test_tiny_fixedpoint(G):
    """
    Test the tiny fixed point: tiny(tiny(tiny(G))) = up.
    """
    assert tiny(tiny(tiny(G))) == up
