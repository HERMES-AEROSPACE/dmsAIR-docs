Output File Reference
=====================

Every simulation writes two CSV files into ``Output/``:

- ``box.csv`` — bath-averaged macroscopic history (one row per sampled step)
- ``pop.csv`` — rovibrational population distribution at every sampled step

This page documents the exact column layout of ``box.csv``.

box.csv layout
--------------

The file starts with one header row listing every column name, followed
by one data row per ``Output Interval`` steps. For a single collision
pair (the standard heat-bath case) the row has **33 columns**, arranged
in four blocks:

1. Bath state (4 columns)
2. Per-species state (4 columns per species — 8 columns for a two-species
   mixture, e.g. NO + C)
3. Rate-coefficient block (15 columns per pair)
4. Species inventory — **number densities** (6 columns per pair)

Block 1 — Bath state
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 24 14 62

   * - Column
     - Unit
     - Description
   * - ``t [s]``
     - s
     - Simulation time.
   * - ``Ttrans [K]``
     - K
     - Translational temperature measured from the current particle
       ensemble (:math:`T_{\mathrm{tr}} = 2 \langle E_{\mathrm{kin}}
       \rangle / 3 k_B` with peculiar velocities).
   * - ``p [Pa]``
     - Pa
     - Pressure derived from the active-species count and
       :math:`T_{\mathrm{tr}}`.
   * - ``rho [kg/m^3]``
     - kg/m³
     - Mass density of the active ensemble.

Block 2 — Per-species state (legacy mole-fraction block)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Four columns per declared species (e.g. NO and C → 8 columns total).

.. list-table::
   :header-rows: 1
   :widths: 28 14 58

   * - Column
     - Unit
     - Description
   * - ``X_<species>``
     - —
     - Mole fraction of the named species. Only reactant species are
       reported here; product species (CN, CO, N, O for NO + C) appear
       in block 4.
   * - ``n_<species> [1/m^3]``
     - 1/m³
     - Number density of the named species.
   * - ``E_int_qn_<species> [eV]``
     - eV
     - Mean internal (rovibrational) energy of the species, from the
       quantised level table.
   * - ``E_int_cont_<species> [eV]``
     - eV
     - Same mean internal energy, but from the continuous
       strategy-(c) atomic coordinates rather than from the quantum
       numbers. The two should agree within vibrational-period
       sampling noise.

Block 3 — Rate coefficient block (per collision pair)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fifteen columns per collision pair, all with unit m³/s. The labels
reflect the pair index ``PN`` and the labels of the target / product
molecules.

.. list-table::
   :header-rows: 1
   :widths: 36 64

   * - Column
     - Description
   * - ``k_I_P<N> [m3/s]``
     - Total inelastic rate coefficient for collision pair ``N``.
   * - ``k_Ex_P<N> [m3/s]``
     - Total exchange rate coefficient (sum over arrangements).
   * - ``k_DD_P<N> [m3/s]``
     - Total dissociation rate coefficient (direct + all indirect
       pathways).
   * - ``k_Ex_P<N>_<target>_<product_K>``
     - Per-arrangement exchange rate for arrangement :math:`K \in
       \{2..6\}`. Five slots; labels are filled from the declared
       product-molecule table for arrangements :math:`\le`
       ``Collision Pair Nb of Molecule Types`` and padded as ``arr<K>``
       otherwise.
   * - ``k_DDdbl_P<N>``
     - Double-dissociation rate (4-body systems only; zero for 3-body
       pairs).
   * - ``k_DDdir_P<N>_<target>``
     - Direct dissociation rate (no transient bound complex).
   * - ``k_ID_P<N>_<target>_<product_K>``
     - Indirect (exchange-assisted) dissociation rate through
       arrangement :math:`K`. Five slots, labelled like the exchange
       block.

For NO + C on 4A\ :sub:`2` the block renders as:

.. code-block:: text

   k_I_P1, k_Ex_P1, k_DD_P1,
   k_Ex_P1_NO_CN, k_Ex_P1_NO_CO, k_Ex_P1_arr4, k_Ex_P1_arr5, k_Ex_P1_arr6,
   k_DDdbl_P1, k_DDdir_P1_NO,
   k_ID_P1_NO_CN, k_ID_P1_NO_CO, k_ID_P1_arr4, k_ID_P1_arr5, k_ID_P1_arr6

The ``arr4..arr6`` slots are zero for 3-body systems.

Block 4 — Species inventory (number densities)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Six columns per collision pair, each in units of 1/m³. These are the
**native, unambiguous** species populations — all products are tracked,
and the numbers are unaffected by the normalisation-convention
differences that plague mole-fraction comparisons between DMS and a
Master-Equation reactor.

.. list-table::
   :header-rows: 1
   :widths: 36 64

   * - Column
     - Description
   * - ``n_<target> [1/m^3]``
     - Target species number density (NO in NO + C). Decreases as
       exchange and dissociation consume it.
   * - ``n_<partner> [1/m^3]``
     - Partner species number density (C in NO + C). Decreases on
       exchange only — unchanged by dissociation.
   * - ``n_<product2> [1/m^3]``
     - First exchange-product diatom (arrangement 2 — e.g. CN for
       NO + C → CN + O).
   * - ``n_<product3> [1/m^3]``
     - Second exchange-product diatom (arrangement 3 — e.g. CO for
       NO + C → CO + N).
   * - ``n_<atomA> [1/m^3]``
     - Free first-atom of the target, produced by exchange via
       arrangement 3 **and** by dissociation (e.g. N in NO + C).
   * - ``n_<atomB> [1/m^3]``
     - Free second-atom of the target, produced by exchange via
       arrangement 2 **and** by dissociation (e.g. O in NO + C).

For NO + C on 4A\ :sub:`2` the block renders as
``n_NO, n_C, n_CN, n_CO, n_N, n_O`` — i.e. every species that can form
in the reactor is tracked explicitly.

Because these are number densities in 1/m³, the total-mass check is
straightforward: the sum
:math:`n_{\rm NO} + n_{\rm C} + n_{\rm CN} + n_{\rm CO} + n_{\rm N} + n_{\rm O}`
grows from its initial value :math:`n_{\rm NO,0} + n_{\rm C,0}` by
exactly :math:`\Delta n = n_{\rm diss}` (every dissociation event adds
one net particle: NO → N + O).

pop.csv layout
--------------

``pop.csv`` has one column per rovibrational level of the target
diatom (``pop(v=V, j=J)``), written each ``Population Output Interval``
steps. Column values are the fraction of the target population in
that state. See :doc:`postprocessing` for how to reconstruct a
Boltzmann-equivalent internal temperature from this distribution.
