Reactive Channels
=================

A QCT trajectory launched from A + BC (3-body) can terminate in any of
four arrangement classes. dmsAIR counts and propagates each class separately.

3-body system
-------------

Atoms are numbered 1, 2 (target diatom) and 3 (projectile atom). Pair
indices follow CoarseAIR's convention:

.. code-block:: text

   pair 1 = (1, 2)   ← original target bond
   pair 2 = (1, 3)   ← exchange candidate 1
   pair 3 = (2, 3)   ← exchange candidate 2

Arrangement codes:

+----------+-------------------------------------+------------------------+
| code     | meaning                             | NO+C example           |
+==========+=====================================+========================+
| ``0``    | inelastic (pair 1 survived)         | NO* + C → NO' + C      |
+----------+-------------------------------------+------------------------+
| ``2``    | exchange pair 2 is the new product  | NO + C → CN + O (Ex1)  |
+----------+-------------------------------------+------------------------+
| ``3``    | exchange pair 3 is the new product  | NO + C → CO + N (Ex2)  |
+----------+-------------------------------------+------------------------+
| ``-1``   | dissociation (no bond survives)     | NO + C → N + O + C     |
+----------+-------------------------------------+------------------------+

Both exchange channels are counted in separate per-arrangement bins
(``k_Ex_arr2``, ``k_Ex_arr3``) so rate coefficients for Ex1 and Ex2 are
reported independently.

4-body system
-------------

For diatom + diatom collisions (``NAtoms = 4``) the pair ordering is

.. code-block:: text

   pair 1 = (1, 2)   ← target diatom
   pair 2 = (1, 3)
   pair 3 = (1, 4)
   pair 4 = (2, 3)
   pair 5 = (2, 4)
   pair 6 = (3, 4)   ← projectile diatom

Arrangement ``0`` is inelastic (pairs 1 and 6 intact), arrangements
``3..6`` are the four cross-pair exchanges, ``-1`` is single dissociation,
``-2`` is double dissociation.

Per-channel filters
-------------------

Any individual exchange channel can be disabled via
``Allow Exchange Arr N = no`` (for N ∈ {2..6}). Rejected events are not
counted in ``pair_N_att`` or ``pair_N_exch``, keeping rate coefficients for
the enabled channels statistically clean. This is the mechanism behind
the ``exchange1`` / ``exchange2`` regime folders in the CNO run tree.

.. note::

   Fix history — the heteronuclear exchange pathways were silently
   discarded in versions prior to Rev 0.1 because ``MolState%iPair = 1``
   was hard-coded when quantising the product molecule. A CN or CO product
   was being quantised against the NO potential and systematically
   rejected. This is now fixed via ``MolState%iPair = max(arrangement, 1)``.
