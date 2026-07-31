Output File Reference
=====================

Every simulation writes two CSV files into ``Output/``:

- ``box.csv`` — bath-averaged macroscopic history (one row per sampled step)
- ``pop.csv`` — rovibrational population distribution at every sampled step
- ``kernel.csv`` — :math:`(v, j) \to (v', j')` transition counters
  (kernel diagnostic; only when ``Allow Kernel = yes``)

This page documents the exact column layout of ``box.csv``.

box.csv layout
--------------

The file starts with one header row listing every column name, followed
by one data row per ``Output Interval`` steps. The schema is
header-driven, so the postprocessing pipeline (``postprocessing.py``)
locates columns by name rather than by position. Column blocks are:

1. **Bath state** (5 columns)
2. **Per-species state** (9 columns per declared species)
3. **Per-pair rate coefficients + dissociation-energy coupling**
   (14 columns per collision pair)
4. **Trajectory diagnostic** (1 column)

For NO+C on 4A\ :sub:`2` (one collision pair, six declared species —
NO, C, CN, CO, N, O) the row width is therefore
:math:`5 + 9 \times 6 + 14 \times 1 + 1 = 74` columns.

Block 1 — Bath state
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 26 14 60

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
       \rangle / 3 k_B` with peculiar velocities). Pinned to the bath
       setpoint by isothermal velocity resampling each step.
   * - ``Tint [K]``
     - K
     - Mixture internal temperature — population-weighted mean of
       per-species ``Tint_<species>`` over molecular species. Falls
       back to ``Ttrans`` when no bound molecule is present.
   * - ``p [Pa]``
     - Pa
     - Pressure derived from the active-species count and
       :math:`T_{\mathrm{tr}}`.
   * - ``rho [kg/m^3]``
     - kg/m³
     - Mass density of the active ensemble.

Block 2 — Per-species state
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Nine columns per declared species, including atoms (atom species emit
zero for energy / temperature columns since they have no rovibrational
structure). For a NO+C / 4A\ :sub:`2` run with the six species
``NO, C, CN, CO, N, O`` the block is :math:`9 \times 6 = 54` columns.

.. list-table::
   :header-rows: 1
   :widths: 30 14 56

   * - Column
     - Unit
     - Description
   * - ``X_<species>``
     - —
     - Mole fraction of the named species. Defined as
       :math:`n_{\mathrm{sp}}/\sum_{\mathrm{sp}'} n_{\mathrm{sp}'}` over
       declared species, so :math:`\sum X = 1` exactly.
   * - ``n_<species> [1/m^3]``
     - 1/m³
     - Number density of the named species.
   * - ``E_int_qn_<species> [eV]``
     - eV
     - Mean internal (rovibrational) energy of the species, from the
       quantised level table — :math:`\langle E_i \rangle - E_g` where
       :math:`E_g` is the species' (v=0, J=0) eigenvalue.
   * - ``E_int_cont_<species> [eV]``
     - eV
     - Same mean internal energy, but reconstructed from the continuous
       strategy-(c) atomic coordinates (kinetic + diatomic potential −
       per-species V_min). The two should agree within
       vibrational-period sampling noise. **Each species uses its own
       diatomic potential** — heteronuclear exchange products (CN, CO)
       no longer reference the target's PES (Bug #1 fix, 2026-05-06).
   * - ``Tint_<species> [K]``
     - K
     - Internal temperature obtained by inverting the species'
       single-temperature Maxwell-Boltzmann partition function so that
       ``<E_int>(Tint) = E_int_qn``. Atoms emit 0.
   * - ``E_rot_<species> [eV]``
     - eV
     - Mean rotational excitation per molecule, defined per Panesi
       (2013) Eq. 25 as :math:`\langle E_i - E_{v_i,0} \rangle`
       (rotational portion at fixed v).
   * - ``E_vib_<species> [eV]``
     - eV
     - Mean vibrational excitation per molecule, defined per Panesi
       (2013) Eq. 26 as :math:`\langle E_{v_i, 0} - E_{0,0} \rangle`
       (vibrational portion at J=0).
   * - ``Trot_<species> [K]``
     - K
     - Rotational temperature obtained by inverting the coupled
       implicit equations
       :math:`\langle E_{\mathrm{rot}}\rangle(T_R, T_V) =
       \langle E_{\mathrm{rot}}\rangle_{\mathrm{obs}}` and
       :math:`\langle E_{\mathrm{vib}}\rangle(T_R, T_V) =
       \langle E_{\mathrm{vib}}\rangle_{\mathrm{obs}}` against the
       rovibrational Boltzmann partition (Panesi 2013, Eqs. 27–30) by
       alternating bisection. Atoms emit 0.
   * - ``Tvib_<species> [K]``
     - K
     - Vibrational temperature from the same coupled inversion as
       ``Trot``.

The decomposition is exact:
:math:`E_{\mathrm{int\_qn}} = E_{\mathrm{vib}} + E_{\mathrm{rot}}` to
machine precision. Particles whose ``vqn`` couldn't be classified
(out-of-table after FindState) are excluded from ``E_rot``/``E_vib``
accumulation but still contribute to ``E_int_qn`` and ``Tint`` via the
classical FindState eigenvalue.

Block 3 — Rate coefficients + dissociation-energy coupling (per pair)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fourteen columns per collision pair. Rate coefficients are window-
averaged: every reset of the per-window counters at ``Output Interval``
steps clears them, so each row reports the rate over the elapsed
interval, not since :math:`t = 0`. The velocity prefactor is the Maxwell
mean relative speed (the accepted-pair mean corrected by the exact moment
ratio :math:`8/3\pi`; see :doc:`/theory/reactive_channels`). Rate columns
written by binaries built before 2026-07-09 are a uniform ≈18 % high and
should be rescaled by :math:`8/3\pi \approx 0.8488`.

.. list-table::
   :header-rows: 1
   :widths: 38 14 48

   * - Column
     - Unit
     - Description
   * - ``k_I_P<N> [m3/s]``
     - m³/s
     - Total inelastic rate coefficient for collision pair :math:`N`.
   * - ``k_Ex_P<N> [m3/s]``
     - m³/s
     - Total exchange rate coefficient (sum over arrangements).
   * - ``k_DD_P<N> [m3/s]``
     - m³/s
     - Total dissociation rate coefficient — single channel
       (CoarseAIR ``arrangement = -1`` events). The proximity-threshold
       direct/indirect classifier and its associated columns
       (``k_DDdir``, ``k_ID_arr*``) were removed in 2026-05-06 (Bug #2
       cleanup). Per Grover, Torres & Schwartzentruber (2019), DMS
       reports a single total dissociation rate.
   * - ``k_Ex_P<N>_<target>_<product_K>_arrK [m3/s]``
     - m³/s
     - Per-arrangement exchange rate for arrangement :math:`K \in
       \{2 .. 6\}`. Five slots; labels are filled from the declared
       product-molecule table for arrangements
       :math:`\le` ``Collision Pair Nb of Molecule Types`` and padded
       as ``arr<K>`` otherwise.
   * - ``k_DDdbl_P<N> [m3/s]``
     - m³/s
     - Double-dissociation rate (4-body systems only — both diatoms
       break in a single trajectory; zero for 3-body pairs).
   * - ``k_DD_A_P<N> [m3/s]``
     - m³/s
     - Single-dissociation sub-channel: **target** diatom broke
       (``diss_kind`` P). For 3-body pairs all singles land here, so
       ``k_DD_A = k_DD``.
   * - ``k_DD_B_P<N> [m3/s]``
     - m³/s
     - Single-dissociation sub-channel: **projectile** diatom broke
       (``diss_kind`` Q; 4-body only). For homonuclear AB = CD systems,
       statistically identical to ``k_DD_A``.
   * - ``k_DD_ex_P<N> [m3/s]``
     - m³/s
     - Single-dissociation sub-channel: exchange-assisted (a new
       cross-pair bond formed while a diatom broke; 4-body only).
       ``k_DD_A + k_DD_B + k_DD_ex = k_DD`` to machine precision.
   * - ``C_DR_P<N>``
     - —
     - Macdonald (2020) Eq. 11 dissociation–rotation coupling:
       :math:`C_{DR} = \sum_p [E_{\mathrm{rot}}]_p / (N_{\mathrm{diss}}
       D_0)`, where the sum runs over molecules dissociating in this
       output window and :math:`D_0` is the bond dissociation energy
       of the target species. Dimensionless.
   * - ``C_DV_P<N>``
     - —
     - Macdonald (2020) Eq. 11 dissociation–vibration coupling:
       :math:`C_{DV} = \sum_p [E_{\mathrm{vib}}]_p / (N_{\mathrm{diss}}
       D_0)`. Dimensionless.

For NO+C on 4A\ :sub:`2` the block renders as:

.. code-block:: text

   k_I_P1, k_Ex_P1, k_DD_P1,
   k_Ex_P1_NO_CN_arr2, k_Ex_P1_NO_CO_arr3, k_Ex_P1_arr4,
   k_Ex_P1_arr5, k_Ex_P1_arr6,
   k_DDdbl_P1, k_DD_A_P1, k_DD_B_P1, k_DD_ex_P1, C_DR_P1, C_DV_P1

The ``arr4..arr6`` slots are zero for 3-body systems.

Block 4 — Trajectory diagnostic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A single integer column at the end of the row.

.. list-table::
   :header-rows: 1
   :widths: 20 14 66

   * - Column
     - Unit
     - Description
   * - ``N_traj_acc``
     - —
     - Number of QCT trajectories accepted by the NTC selector and
       successfully integrated to convergence in this output window.
       A diagnostic for collision-rate sanity checks.

pop.csv layout
--------------

``pop.csv`` has one column per rovibrational level of the target
diatom (``pop(v=V, j=J)``), written each ``Population Output Interval``
steps. Column values are the fraction of the target population in
that state. See :doc:`postprocessing` for how to reconstruct a
Boltzmann-equivalent internal temperature from this distribution.

References
----------

- Panesi, Magin, Munafò, Schwartzentruber, *J. Chem. Phys.* **138**,
  044312 (2013) — Tvib/Trot decomposition (Eqs. 19–30).
- Macdonald, Munafò, Johnston, Panesi, *J. Phys. Chem. A* **124**,
  6986 (2020) — dissociation-energy coupling :math:`C_{DR}`,
  :math:`C_{DV}` (Eq. 11).
- Grover, Torres, Schwartzentruber, *Phys. Fluids* **31**, 076107
  (2019) — single-channel dissociation methodology.
