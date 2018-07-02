.. games.rst
.. py:module:: ludology.game
.. include:: definitions.rst

Games
=====

A Game :math:`G` is defined as two sets of Games, a left set and a right set, and is typically denoted:

.. math::

   G = \Game{\leftoption}{\rightoption}

where :math:`\leftoption` denotes a typical member of the left set and :math:`\rightoption` denotes a typical member of the right set. A Game represents the current state of a game, where the left set consists of the possible game states the Left player can transition the game to, while the right set consists of the possible game states the Right player can transition the game to.

This recursive definition requires a base case, which in this case in given by both sets being empty, and we define this game to be ":math:`0`":

.. math::

   0 \equiv \Game{}{}

From here three new Games can be constructed:

.. math::

   1  &\equiv \Game{0}{} = \Game{\Game{}{}}{}

   -1 &\equiv \Game{}{0} = \Game{}{\Game{}{}}

   *  &\equiv \Game{0}{0} = \Game{\Game{}{}}{\Game{}{}}

Operations
----------

The negation of a Game is equivalent to swapping players:

.. math::

   -G = \Game{-\rightoption}{-\leftoption}

The (disjoint) sum of two Games is defined by:

.. math::

   G + H = \Game{G + \leftoption[H], \leftoption + H}{G + \rightoption[H], \rightoption + H}

and subtraction is defined as :math:`G - H = G + (-H)`.
