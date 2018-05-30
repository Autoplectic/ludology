.. games.rst
.. include:: definitions.rst

Games
=====

A Game :math:`G` is defined as two sets of Games, a left set and a right set, and is typically denoted:

.. math::

   G = \Game{\leftoption}{\rightoption}

where :math:`\leftoption` denotes a typical member of the left set and :math:`\rightoption` denotes a typical member of the right set.

This recursive definition requires a base case, which in this case in given by both sets being empty, and we define this game to be ":math:`0`":

.. math::

   0 \equiv \Game{}{}

From here three new Games can be constructed:

.. math::

   1  &\equiv \Game{0}{} = \Game{\Game{}{}}{}

   -1 &\equiv \Game{}{0} = \Game{}{\Game{}{}}

   *  &\equiv \Game{0}{0} = \Game{\Game{}{}}{\Game{}{}}
