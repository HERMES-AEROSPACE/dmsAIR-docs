Input File Reference
====================

Every case is driven by a plain-text ``dmsAIR.inp`` file. Keywords are
case-sensitive; unknown keywords are silently ignored (dmsAIR prints a
warning to stdout but continues). Comment lines start with ``#``.

This page documents **every** keyword recognised by the input parser in
``src/DMS_Input_Class.F90``, grouped by logical block, together with its
type, default value, allowed range and a short description.

Thermodynamics
--------------

.. list-table::
   :header-rows: 1
   :widths: 28 10 14 48

   * - Keyword
     - Type
     - Default
     - Description
   * - ``Translational Temperature [K]``
     - real
     - —
     - Imposed translational temperature :math:`T_{\mathrm{tr}}` of the
       isothermal bath (also used to initialise Maxwellian velocities
       for the adiabatic bath).
   * - ``Internal Temperature [K]``
     - real
     - —
     - Initial internal (rovibrational) temperature
       :math:`T_{\mathrm{int}}` of the diatomic bath; sets the initial
       Boltzmann :math:`(v, j)` distribution.
   * - ``Pressure [Pa]``
     - real
     - —
     - Initial pressure; used with :math:`T_{\mathrm{int}}` to set the
       initial number density :math:`n = P / (k_B T_{\mathrm{int}})`.

Numerics
--------

.. list-table::
   :header-rows: 1
   :widths: 28 10 14 48

   * - Keyword
     - Type
     - Default
     - Description
   * - ``Nb of Particles``
     - integer
     - —
     - Total number of simulation particles in the bath (all species).
   * - ``Nb of Time Steps``
     - integer
     - —
     - Total macroscopic DMS time-steps to run.
   * - ``Impact Parameter [Bohr]``
     - real
     - —
     - Legacy global cut-off impact parameter. Production runs use the
       per-pair ``Collision Pair bmax`` keyword instead.
   * - ``Particle Weight``
     - real
     - 1.0
     - Statistical weight (number of real molecules per simulation
       particle).
   * - ``Output Interval``
     - integer
     - —
     - Number of DMS steps between ``box.csv`` writes.
   * - ``Population Output Interval``
     - integer
     - —
     - Number of DMS steps between ``pop.csv`` writes.
   * - ``Kernel Output Interval``
     - integer
     - —
     - Number of DMS steps between kernel-count dumps
       (requires ``Allow Kernel = yes``).
   * - ``Allow Kernel``
     - yes/no
     - no
     - Enable per-step :math:`(v, j) \to (v', j')` transition-kernel
       accumulation and output.
   * - ``DMS Timestep Fraction``
     - real
     - 0.1
     - DMS macro timestep as a fraction of the local mean collision
       time.
   * - ``RNG Seed``
     - integer
     - −1
     - Seed for the Fortran RNG. ``-1`` (default) ⇒ seed from
       ``system_clock`` (non-reproducible, production).
       ``≥0`` ⇒ deterministic, used by the regression test suite.

Physics options
---------------

.. list-table::
   :header-rows: 1
   :widths: 28 10 14 48

   * - Keyword
     - Type
     - Default
     - Description
   * - ``Bath Type``
     - string
     - isothermal
     - ``isothermal`` (imposed :math:`T_{\mathrm{tr}}`) or
       ``adiabatic`` (energy-conserving). See :doc:`/theory/bath_types`.
   * - ``Allow Dissociation``
     - yes/no
     - no
     - Master switch for dissociation events.
   * - ``Allow Double Dissociation``
     - yes/no
     - no
     - 4-body only. Enables the fully-dissociated channel
       (``arrangement = -2``). Disabled by default to keep DMS-vs-ME
       comparisons like-for-like.
   * - ``Allow Exchange``
     - yes/no
     - yes
     - Master switch for all exchange reactions.
   * - ``Allow Exchange Arr N``
     - yes/no
     - yes
     - Per-arrangement exchange filter for :math:`N \in \{2, 3, 4, 5,
       6\}`. Set to ``no`` to silence channel :math:`N` (e.g. ``Arr 3 =
       no`` keeps only CN + O in NO + C). See
       :doc:`/theory/reactive_channels`.
   * - ``Propagate Phase Space``
     - yes/no
     - yes
     - Strategy (c): persistent atomic :math:`(q, \dot q)` between
       collisions. Recommended.

Integrator
----------

.. list-table::
   :header-rows: 1
   :widths: 28 10 14 48

   * - Keyword
     - Type
     - Default
     - Description
   * - ``Integrator``
     - string
     - BS
     - ``BS`` (adaptive Bulirsch–Stoer, default) or ``VV`` (fixed-step
       Velocity Verlet). See :doc:`/theory/integrators`.
   * - ``VV Timestep [a.u.]``
     - real
     - 2.0
     - Fixed macro timestep for the VV integrator, in atomic time units.

Output
------

.. list-table::
   :header-rows: 1
   :widths: 28 10 14 48

   * - Keyword
     - Type
     - Default
     - Description
   * - ``Output Path``
     - string
     - ``Output/``
     - Directory (relative to the case dir) into which ``box.csv``,
       ``pop.csv`` and ancillary diagnostics are written.

Species block
-------------

Per-species keywords are repeated once per species, terminated by the
next ``Species Name``. ``Nb of Species`` sets the total count.

.. list-table::
   :header-rows: 1
   :widths: 28 10 14 48

   * - Keyword
     - Type
     - Default
     - Description
   * - ``Nb of Species``
     - integer
     - 0
     - Number of species blocks that follow.
   * - ``Species Name``
     - string
     - —
     - Species label (e.g. ``NO``, ``C``).
   * - ``Species Np``
     - integer
     - auto
     - Optional. Explicit particle count for this species. Overrides the
       fraction implied by ``Species X`` if both are given.
   * - ``Species X``
     - real
     - —
     - Initial mole fraction (must sum to 1 across species).
   * - ``Species Tint [K]``
     - real
     - global
     - Per-species initial internal temperature; falls back to
       ``Internal Temperature`` if omitted.
   * - ``Species Levels File``
     - string
     - —
     - Rovibrational-level table for this species (mandatory for a
       molecular species).
   * - ``Species Is Molecule``
     - yes/no
     - —
     - Distinguishes molecular (``yes``) from atomic (``no``) species.
   * - ``Species NAtoms``
     - integer
     - —
     - Number of atoms in this species (1 for atom, 2 for diatomic).
   * - ``Species Atom Mass 1 [a.u.]``
     - real
     - —
     - Mass of atom 1 of this species (atomic units).
   * - ``Species Atom Mass 2 [a.u.]``
     - real
     - —
     - Mass of atom 2. Required only for diatomics.
   * - ``Species Atom Name 1``
     - string
     - —
     - Name tag for atom 1 (e.g. ``N``).
   * - ``Species Atom Name 2``
     - string
     - —
     - Name tag for atom 2.
   * - ``Species Diatomic Model``
     - string
     - —
     - Diatomic potential identifier (e.g. ``UCI``, ``UMN``,
       ``Schwenke``).
   * - ``Species gnuc Even J``
     - real
     - 1.0
     - Nuclear-spin degeneracy for even :math:`j` rotational levels
       (homonuclear diatomics only).
   * - ``Species gnuc Odd J``
     - real
     - 1.0
     - Nuclear-spin degeneracy for odd :math:`j`.

Collision-pair block
--------------------

Collision pairs define which species interact and which PES is used. A
single case may declare several pairs; per-pair keywords are repeated.

.. list-table::
   :header-rows: 1
   :widths: 28 10 14 48

   * - Keyword
     - Type
     - Default
     - Description
   * - ``Nb of Collision Pairs``
     - integer
     - 0
     - Number of collision-pair blocks that follow.
   * - ``Collision Pair Species 1``
     - integer
     - —
     - Index of the first species (1-based) in the species list.
   * - ``Collision Pair Species 2``
     - integer
     - —
     - Index of the second species.
   * - ``Collision Pair bmax [Bohr]``
     - real
     - —
     - Cut-off impact parameter for NTC pair selection. See
       :doc:`/theory/ntc` for the calibration metric.
   * - ``Collision Pair System``
     - string
     - —
     - CoarseAIR system identifier (e.g. ``CNO``, ``H3``, ``H4``).
   * - ``Collision Pair Database Path``
     - string
     - ``$COARSEAIR_DTB/``
     - Path to the CoarseAIR ``dtb`` directory. Supports env-var
       expansion.
   * - ``Collision Pair Dinit [Bohr]``
     - real
     - 30.0
     - Initial separation of the colliding partners at the start of each
       QCT trajectory.

PES declarations (per pair)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Up to five electronic states can be declared per collision pair. Only
``Nb of PESs`` entries are actually loaded.

.. list-table::
   :header-rows: 1
   :widths: 34 10 14 42

   * - Keyword
     - Type
     - Default
     - Description
   * - ``Collision Pair Nb of PESs``
     - integer
     - 1
     - Number of electronic PESs to load for this pair.
   * - ``Collision Pair PES Model K``
     - string
     - —
     - Name of the :math:`K`-th PES model (:math:`K = 1..5`), e.g.
       ``UCI_4A2``, ``H3_BH``, ``H4_BMKP``.
   * - ``Collision Pair PES Degeneracy K``
     - real
     - 1.0
     - Statistical weight of the :math:`K`-th PES (fraction of
       trajectories sampled on it).
   * - ``Collision Pair PES Parameters File``
     - string
     - —
     - Optional file of PES-specific parameter overrides.
   * - ``Collision Pair Distinguish PESs``
     - yes/no
     - no
     - When multiple PESs are declared, report rate coefficients per-PES
       instead of aggregated.

Product-molecule declarations (per pair)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For heteronuclear reactive systems the product molecules that can form
after an exchange must be enumerated so their diatomic potentials and
level tables are loaded.

.. list-table::
   :header-rows: 1
   :widths: 40 10 14 36

   * - Keyword
     - Type
     - Default
     - Description
   * - ``Collision Pair Nb of Molecule Types``
     - integer
     - 1
     - Number of distinct molecular products for this pair (e.g. 3 for
       NO + C: NO, CN, CO).
   * - ``Collision Pair Molecule K Name``
     - string
     - —
     - Label of the :math:`K`-th molecule (:math:`K = 1..4`).
   * - ``Collision Pair Molecule K Diatomic Model``
     - string
     - —
     - Diatomic-potential identifier for the :math:`K`-th molecule.
   * - ``Collision Pair Molecule K Levels File``
     - string
     - —
     - Rovibrational-level table for the :math:`K`-th molecule.
   * - ``Collision Pair Diatomic Model``
     - string
     - —
     - Global diatomic-model override (fallback when per-molecule models
       are not set).

ODE / trajectory parameters (per pair)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 32 10 14 44

   * - Keyword
     - Type
     - Default
     - Description
   * - ``Collision Pair ODE dt [a.u.]``
     - real
     - —
     - Initial/target integrator step size (atomic time units).
   * - ``Collision Pair ODE eps``
     - real
     - 1.0e-8
     - Relative error tolerance passed to the BS integrator.
   * - ``Collision Pair ODE NSteps``
     - integer
     - —
     - Maximum number of sub-steps in the BS modified-midpoint
       extrapolation.
   * - ``Collision Pair ODE Relax``
     - real
     - 0.5
     - Step-size relaxation factor for the BS solver after a rejected
       step.
   * - ``Collision Pair ODE ncall``
     - integer
     - 10
     - Number of convergence checks performed per macro call to the
       integrator.
   * - ``Collision Pair ODE Rmax [Bohr]``
     - real
     - 40.0
     - Convergence radius: when the largest atom-pair distance exceeds
       ``Rmax`` the trajectory is declared finished.
   * - ``Collision Pair ODE tmax [a.u.]``
     - real
     - —
     - Wall-time cap per trajectory. Long-lived complexes exceeding this
       are flagged non-converged and excluded from statistics.

Quantisation parameters (per pair)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These feed CoarseAIR's ``FindState`` routine (see
:doc:`/theory/qct`).

.. list-table::
   :header-rows: 1
   :widths: 30 10 14 46

   * - Keyword
     - Type
     - Default
     - Description
   * - ``Collision Pair nquad``
     - integer
     - 50
     - Number of Gauss–Legendre nodes in the radial action integral.
   * - ``Collision Pair rcent lower``
     - real
     - 1.0
     - Lower bracket (Bohr) for the inner-turning-point search.
   * - ``Collision Pair rcent upper``
     - real
     - 30.0
     - Upper bracket (Bohr) for the outer-turning-point search.
   * - ``Collision Pair rfact``
     - real
     - 0.0
     - Safety factor applied to the turning-point bracket; 0 disables.
   * - ``Collision Pair tthresau``
     - real
     - 1.0e-100
     - Vibrational-period threshold below which a state is treated as
       unbound.
   * - ``Collision Pair HamAbsTol``
     - real
     - 1.0e-5
     - Diagnostic threshold on :math:`|\Delta H|` per trajectory (not a
       rejection filter — all converged trajectories are accepted; see
       :doc:`/theory/qct`).
   * - ``Collision Pair CoarseAIR Config``
     - string
     - —
     - Optional path to a CoarseAIR-style configuration file for
       advanced tuning.

Example
-------

A production NO + C input on the UCI 4A\ :sub:`2` PES, configured for the
``exchange1 + dissociation`` regime (CN + O channel only, dissociation
enabled). The layout follows the same ordering used throughout the
``run/`` tree: Thermodynamics → Numerics → Physics options → Integrator →
Output → Species → Collision pair(s).

.. code-block:: text

   ###############################################################################
   #  NO + C  Heat Bath  —  UCI_4A2  —  T_tr = 10 000 K
   #  regime: inelastic + exchange1 + dissociation (arr=2 only, CN + O)
   #  Np = 683 800;  bmax = 12.0 Bohr
   ###############################################################################

   # ==============================================================
   #  Thermodynamics
   # ==============================================================
      Translational Temperature [K]  = 10000
      Internal Temperature [K]       = 300
      Pressure [Pa]                  = 1000

   # ==============================================================
   #  Numerics
   # ==============================================================
      Nb of Particles             = 683800
      Nb of Time Steps            = 10000000
      Particle Weight             = 1
      Output Interval             = 100
      Population Output Interval  = 1000
      DMS Timestep Fraction       = 0.01

   # ==============================================================
   #  Physics options
   # ==============================================================
      Bath Type              = isothermal
      Allow Dissociation     = yes
      Allow Exchange         = yes
      Allow Exchange Arr 3   = no          # keep only CN + O (Exchange 1)
      Propagate Phase Space  = yes

   # ==============================================================
   #  Integrator (QCT trajectory)
   # ==============================================================
      Integrator          = VV
      VV Timestep [a.u.]  = 4.0

   # ==============================================================
   #  Output
   # ==============================================================
      Output Path  = Output/

   # ==============================================================
   #  Species
   # ==============================================================
      Nb of Species  = 2

      # --- Species 1: NO ---
      Species Name                = NO
      Species X                   = 0.5
      Species Tint [K]            = 300
      Species Levels File         = levels_NO.inp
      Species Is Molecule         = yes
      Species NAtoms              = 2
      Species Atom Name 1         = N
      Species Atom Mass 1 [a.u.]  = 25526.04298
      Species Atom Name 2         = O
      Species Atom Mass 2 [a.u.]  = 29148.94559
      Species Diatomic Model      = UCI
      Species gnuc Even J         = 1
      Species gnuc Odd J          = 1

      # --- Species 2: C ---
      Species Name                = C
      Species X                   = 0.5
      Species Is Molecule         = no
      Species NAtoms              = 1
      Species Atom Name 1         = C
      Species Atom Mass 1 [a.u.]  = 21868.661757

   # ==============================================================
   #  Collision pair(s)
   # ==============================================================
      Nb of Collision Pairs  = 1

      # --- Pair setup ---
      Collision Pair Species 1      = 1
      Collision Pair Species 2      = 2
      Collision Pair System         = CNO
      Collision Pair Database Path  = $COARSEAIR_DTB/

      # --- Geometry ---
      Collision Pair bmax [Bohr]   = 12.0
      Collision Pair Dinit [Bohr]  = 30.0

      # --- ODE parameters (QCT trajectory) ---
      Collision Pair ODE dt [a.u.]    = 5.0
      Collision Pair ODE eps          = 1.0e-8
      Collision Pair ODE NSteps       = 3
      Collision Pair ODE Relax        = 0.5
      Collision Pair ODE ncall        = 10
      Collision Pair ODE Rmax [Bohr]  = 40.0
      Collision Pair ODE tmax [a.u.]  = 1035000.0

      # --- Quantisation / find-state ---
      Collision Pair nquad        = 50
      Collision Pair rcent lower  = 1.0
      Collision Pair rcent upper  = 30.0
      Collision Pair rfact        = 0
      Collision Pair tthresau     = 1.0e-100
      Collision Pair HamAbsTol    = 1.0e-5

      # --- Potential Energy Surface(s) ---
      Collision Pair Nb of PESs        = 1
      Collision Pair PES Model 1       = UCI_4A2
      Collision Pair PES Degeneracy 1  = 0.11112
      Collision Pair Distinguish PESs  = no

      # --- Product molecule types ---
      Collision Pair Nb of Molecule Types       = 3
      Collision Pair Molecule 1 Name            = NO
      Collision Pair Molecule 1 Diatomic Model  = UCI
      Collision Pair Molecule 1 Levels File     = NO_UCI.inp
      Collision Pair Molecule 2 Name            = CN
      Collision Pair Molecule 2 Diatomic Model  = UCI
      Collision Pair Molecule 2 Levels File     = CN_UCI.inp
      Collision Pair Molecule 3 Name            = CO
      Collision Pair Molecule 3 Diatomic Model  = UCI
      Collision Pair Molecule 3 Levels File     = CO_UCI.inp
