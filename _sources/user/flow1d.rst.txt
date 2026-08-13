1D simulations — Flow1D (Couette / Fourier)
===========================================

``dmsAIR_Flow1D`` is the 1D wall-bounded DMS solver: a planar channel with
the wall-normal direction *x*, walls at :math:`x = 0` (left) and
:math:`x = L` (right), and a flow homogeneous in *y* and *z*. It resolves
the two canonical wall-bounded configurations:

- **Couette flow** — equal wall temperatures, opposite wall *y*-velocities;
  yields the velocity profile u\ :sub:`y`\ (x), velocity slip, and the shear
  stress τ\ :sub:`xy`.
- **Fourier flow** — unequal wall temperatures, zero wall velocities;
  yields the temperature profile T(x), temperature jumps, and the heat flux
  q\ :sub:`x`.

Unlike the 0D heat bath, the gas phase is inherently **adiabatic** (no
thermostat): centre-of-mass velocities persist between steps and evolve only
through QCT collisions, elastic scattering and wall interactions. Total
energy is conserved up to the net energy exchanged with the walls (checked
by the built-in monitor). Because velocities persist, Flow1D always applies
the collision-frame alignment rotation (see
:doc:`/developer/architecture`) — without it the fixed CoarseAIR approach
axis anisotropises the temperature components and pumps a spurious species
drift.

Collisions reuse the 0D HeatBath machinery unchanged: **per-cell NTC
selection** (``NTC_SelectPairs_Cell``) + CoarseAIR QCT trajectories with
degeneracy-weighted multi-PES sampling, the gnuc nuclear-spin scheme, and
strategy-(c) persistent atomic coordinates.

Wall model
----------

Each wall is a Maxwell boundary. With probability ``Wall Accommodation``
the particle is re-emitted diffusely from a half-Maxwellian at the wall
temperature (tangential drift = the wall's *y*-velocity); otherwise it
reflects specularly. On each diffuse reflection, a molecule's internal
(v, j) state is additionally re-sampled from a Boltzmann distribution at
the wall temperature with probability ``Wall Internal Accommodation``.

.. note::

   When comparing against other codes at partial accommodation, note that
   PICLas's ``TransACC`` is a per-bounce *energy* accommodation, not the
   Maxwell diffuse-probability convention used here (and by SPARTA /
   dsmcFoam). The models coincide only at full accommodation (α = 1).

Building and running
--------------------

.. code-block:: bash

   make flow1d                      # builds build/bin/dmsAIR_Flow1D
   cd run/Flow1D/Couette_H2He
   mpirun -np 4 <path>/dmsAIR_Flow1D

MPI parallelisation is replicated-data, as in HeatBath: movement, wall
interaction and NTC selection run on all ranks with a step-seeded common
RNG stream (bit-identical, no broadcast), while QCT trajectories are
distributed round-robin over ranks and combined with ``MPI_Allreduce``.

Input keywords
--------------

In addition to the standard 0D keywords (see :doc:`input_reference`),
Flow1D reads:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Keyword
     - Meaning
   * - ``Domain Length [m]``
     - Channel width *L* (wall-normal direction *x*).
   * - ``Nb of Cells``
     - Number of uniform sampling/NTC cells across the channel.
   * - ``Wall Left Temperature [K]`` / ``Wall Right Temperature [K]``
     - Maxwell wall temperatures.
   * - ``Wall Left Velocity Y [m/s]`` / ``Wall Right Velocity Y [m/s]``
     - Tangential wall velocities (Couette drive).
   * - ``Wall Accommodation``
     - Diffuse-reflection probability α ∈ [0, 1] (1 = fully diffuse,
       0 = specular).
   * - ``Wall Internal Accommodation``
     - Probability of re-sampling the internal (v, j) state on a diffuse
       bounce.
   * - ``Sampling Start Step``
     - First step included in the time-averaged profiles (discard the
       transient).
   * - ``Profile Output Interval``
     - Steps between rows of ``profiles.csv`` / ``walls.csv``.
   * - ``Bath Type = adiabatic``
     - Required — Flow1D has no thermostat.
   * - ``Geometry File = <path>``
     - Optional: moves the domain and boundary definition to a separate
       file with per-face diffuse/specular/periodic boundaries
       (``Domain Length X/Y/Z [m]``, ``Nb of Cells X``, per-face
       temperature/velocity/accommodation). The particle weight is then
       derived from (P, T\ :sub:`int`, V, N\ :sub:`p`).

Output files
------------

``profiles.csv`` — one row per cell per output interval; the measurement
set mirrors the dsmcFoam+ (MNF) volume fields:

.. code-block:: text

   t [s], cell, x [m], n [1/m^3], X_<species>...,
   rho [kg/m^3], ux [m/s], uy [m/s],
   Ttr_x [K], Ttr_y [K], Ttr_z [K], Ttr [K], Trot [K], Tvib [K], Tov [K],
   p [Pa], E_int [eV], E_rot [eV], E_vib [eV], tau_xy [Pa], q_x [W/m^2]

``walls.csv`` — per-wall surface tallies
(``hits, tau [Pa], q [W/m^2], p [Pa]`` for left and right). Sign
conventions: ``tau`` is the shear stress exerted *by the gas on the wall*
(positive = gas drags the wall toward +y); ``q`` is the heat flux *from
the wall into the gas* (positive = wall heats the gas); ``p`` is the
normal pressure (always positive). Together τ and p are the tangential and
normal components of dsmcFoam's ``fD`` surface field.

``pop.csv`` — rovibrational population snapshots of species 1, as in the
0D solver.

Consistency checks worth making on every run: interior τ\ :sub:`xy` (or
q\ :sub:`x`) uniform across cells and equal to both wall tallies;
q\ :sub:`L` ≈ −q\ :sub:`R` (Fourier); n·T ≈ const across the channel.

Example decks and verification
------------------------------

Ready-to-run verification decks live under ``run/Flow1D/``:

- ``Fourier_H2He`` — H2/He 50:50, 1 kPa, L = 50 µm (Kn ≈ 0.2), walls
  300 / 1000 K. Verified: isotropic T components collapsing onto one smooth
  T\ :sub:`tr`\ (x) with wall temperature jumps, uniform q\ :sub:`x`
  balanced with both wall tallies to ~1 %, and the H2-specific
  rotational/vibrational split (E\ :sub:`vib` frozen while E\ :sub:`rot`
  tracks T(x)) that this solver exists to resolve.
- ``Couette_H2He`` — same gas, 300 K walls at ∓500 m/s: near-linear
  u\ :sub:`y`\ (x) with ~135 m/s slip per wall at Kn ≈ 0.2, uniform
  τ\ :sub:`xy` equal to the wall tallies, and a small viscous-heating bump.
- ``Compare_H2`` / ``ASML_H2`` / ``Exp_P100`` — cross-code (SPARTA, PICLas)
  and experiment-comparison campaigns for H2 heat flux across the
  transition regime.

The solver has additionally been anchored at the free-molecular limit
(matching the analytic two-stream values to 1–2.5 %, including the quantum
rotational effusion contribution) and cross-validated against DSMC at
Kn = 10, with the DMS-vs-DSMC heat-flux gap at lower Kn traced to the
rotational conduction channel (ab-initio cross-sections and realistic
rotational collision numbers vs. the VHS/constant-Z\ :sub:`rot` kernel).

v1 limitations
--------------

- No checkpoint/restart and no transition-kernel output.
- Double-dissociation events are discarded (the energy-consistent 4-atom
  velocity split is not yet wired through the buffers).
