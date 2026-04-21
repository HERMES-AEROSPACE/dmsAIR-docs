Reactive Channels
=================

At the end of a QCT trajectory, every surviving atom pair whose separation
remains below a bond cut-off (:math:`r_{\max} = 10` Bohr) is classified as
a "bound product". The pattern of bound and broken pairs uniquely
identifies the outcome class — inelastic, exchange (with multiple
branches for heteronuclear systems), or dissociation. dmsAIR counts and
propagates each class separately so that state-resolved rate coefficients
emerge naturally from the collision statistics.

For a three-body system A + BC, three physical outcomes are relevant:

- **Inelastic** (pair 1 survives): the target diatom re-emerges with a
  possibly different :math:`(v', j')`. Dominant at low translational
  energies; encodes VT, RT and VV energy transfer.
- **Exchange**: a new bond forms between atoms that were not originally
  bonded. For heteronuclear systems with distinct product manifolds this
  yields multiple distinguishable branches (e.g. NO + C → CN + O *vs.*
  NO + C → CO + N on the 4A\ :sub:`2` PES).
- **Dissociation**: no bond survives; the diatom is fragmented into two
  free atoms.

For four-body systems AB + CD the analogous outcomes include *double
dissociation* — all four atoms escaping in a single event. The double-
dissociation channel cannot be represented in a standard pair-based
master equation, and is therefore disabled by default in dmsAIR so that
DMS-vs-ME comparisons remain strictly like-for-like
(``Allow Double Dissociation = no``).

Arrangement codes
-----------------

Three-body system
~~~~~~~~~~~~~~~~~

Atoms are numbered 1, 2 (target diatom) and 3 (projectile atom). Pair
indices follow CoarseAIR's convention:

.. code-block:: text

   pair 1 = (1, 2)   ← original target bond
   pair 2 = (1, 3)   ← exchange candidate 1
   pair 3 = (2, 3)   ← exchange candidate 2

Arrangement codes:

+----------+-------------------------------------+------------------------+
| code     | meaning                             | NO + C example         |
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
(``k_Ex_arr2``, ``k_Ex_arr3``) so that rate coefficients for Ex1 and
Ex2 are reported independently.

Four-body system
~~~~~~~~~~~~~~~~

For diatom + diatom collisions (``NAtoms = 4``) the pair ordering is

.. code-block:: text

   pair 1 = (1, 2)   ← target diatom
   pair 2 = (1, 3)
   pair 3 = (1, 4)
   pair 4 = (2, 3)
   pair 5 = (2, 4)
   pair 6 = (3, 4)   ← projectile diatom

Arrangement ``0`` is inelastic (pairs 1 and 6 intact), arrangements
``3..6`` are the four cross-pair exchanges, ``-1`` denotes single
dissociation and ``-2`` double dissociation.

Per-channel filters
-------------------

Any individual exchange channel can be disabled via
``Allow Exchange Arr N = no`` (for :math:`N \in \{2..6\}`). Rejected
events are not counted in ``pair_N_att`` or ``pair_N_exch``, keeping the
rate coefficients of the enabled channels statistically clean. This is
the mechanism behind the ``exchange1`` / ``exchange2`` regime folders in
the CNO run tree.

Rate coefficient measurement
----------------------------

Rate coefficients for every channel are measured directly from the event
counts per NTC-output window:

.. math::

   k_{\mathrm{ch}} = \langle v_{\mathrm{rel}} \rangle \; \pi b_{\max}^2 \;
                     \frac{N_{\mathrm{ch}}}{N_{\mathrm{att}}} ,

with :math:`b_{\max}` the cut-off impact parameter (cross-section
convention: geometric, not empirical) and :math:`\langle v_{\mathrm{rel}}
\rangle` the ensemble-averaged relative velocity of the accepted pairs.
Because the sampled :math:`(b, E_{\mathrm{rel}})` distribution is the
correct thermal distribution set by the NTC acceptance law, this yields
the state-specific *thermal* rate coefficient
:math:`k_{\mathrm{ch}}(T_{\mathrm{tr}}, T_{\mathrm{int}})` without
further assumption. Cross-verification against master-equation references
at matched bath conditions is used as the primary validation criterion
[Macdonald2018]_ [GroverSchwartzentruber2019]_ [ManinderO2]_, alongside
dedicated QCT rate-coefficient studies on nitrogen [FujitaN2]_ and on
CO + O [FujitaCO]_.

.. note::

   Fix history — the heteronuclear exchange pathways were silently
   discarded in versions prior to Rev 0.1 because ``MolState%iPair = 1``
   was hard-coded when quantising the product molecule. A CN or CO
   product was being quantised against the NO potential and systematically
   rejected. This is now fixed via
   ``MolState%iPair = max(arrangement, 1)``.
