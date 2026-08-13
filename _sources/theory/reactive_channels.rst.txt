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

Outcome classification is by **bond counting**: ``n_short`` is the number
of atom pairs whose final separation is below the 10-Bohr cut-off. For a
4-body trajectory, ``n_short = 0`` is a double dissociation (``-2``),
``n_short = 1`` a single dissociation (``-1``, the surviving pair
identifying which diatom broke), and ``n_short ≥ 2`` is inelastic (both
original bonds survive) or exchange (labelled by the shortest new pair).
Single dissociations additionally carry a ``diss_kind`` sub-channel —
target diatom broke (**P**), projectile diatom broke (**Q**), or
exchange-assisted — reported as separate rate columns ``k_DD_A`` /
``k_DD_B`` / ``k_DD_ex`` in ``box.csv`` (for homonuclear AB = CD systems,
P and Q are statistically identical, which serves as a built-in
consistency check).

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
\rangle` the **Maxwell mean** relative speed :math:`\langle g
\rangle_{\mathrm{MB}}`. Note that the NTC-*accepted* pairs are
flux-weighted (acceptance :math:`\propto g`), so their sample-mean speed
is :math:`\langle g^2 \rangle / \langle g \rangle = (3\pi/8)\,\langle g
\rangle_{\mathrm{MB}}`; the flux enhancement is already carried by the
*number* of accepted collisions, so the prefactor must be converted back
by the exact moment ratio :math:`8/3\pi` (using the accepted-pair mean
directly overestimates every :math:`k` by ≈18 %, temperature- and
mass-independently — fixed 2026-07-09; ``box.csv`` rate columns written
before then should be rescaled by :math:`8/3\pi \approx 0.8488`).
Because the sampled :math:`(b, E_{\mathrm{rel}})` distribution is the
correct thermal distribution set by the NTC acceptance law, this yields
the state-specific *thermal* rate coefficient
:math:`k_{\mathrm{ch}}(T_{\mathrm{tr}}, T_{\mathrm{int}})` without
further assumption. Cross-verification against master-equation references
at matched bath conditions is used as the primary validation criterion
[Macdonald2018]_ [GroverSchwartzentruber2019]_ [ManinderO2]_, alongside
dedicated QCT rate-coefficient studies on nitrogen [FujitaN2]_ and on
CO + O [FujitaCO]_.

Electronic manifolds and multi-PES sampling
-------------------------------------------

A heavy-particle collision correlates to several Born–Oppenheimer potential
energy surfaces — the electronic manifolds of the reactant asymptote. For
example :math:`\mathrm{C}(^3P) + \mathrm{NO}(^2\Pi)` spans 36 electronic states
that split into doublet and quartet surfaces such as :math:`2A_1`, :math:`2A_2`
and :math:`4A_2`. Each PES carries a statistical weight :math:`g_K`, the
fraction of the reactant electronic manifold correlating to it — a
(temperature-dependent) ratio of electronic partition functions.

dmsAIR can integrate several PESs in one run. Per collision a single PES is
drawn with probability proportional to its weight, and the pair is rejected
with probability :math:`1 - \sum_K g_K` (the remaining manifold is not
simulated); see :ref:`the multi-PES sampling rule <multi-pes-sampling>` for the
exact cumulative draw. Two consequences follow:

- the **relaxation rate** carries the factor :math:`\sum_K g_K` — only that
  fraction of NTC-selected collisions produces dynamics. A single-PES run thus
  reproduces that PES's *contribution* to the global relaxation, whereas
  running all correlated PESs reproduces the **global**,
  electronically-mixed dynamics directly (rather than summing separate runs);
- the **rate coefficient** :math:`k_{\mathrm{ch}}` above is *unaffected* —
  both :math:`N_{\mathrm{ch}}` and :math:`N_{\mathrm{att}}` are counted after
  the PES draw, so the weight cancels and :math:`k_{\mathrm{ch}}` is the
  full-manifold (per-collision) value; the electronic degeneracy is then
  applied to the tabulated rate, as in the master-equation pipeline.

