Architecture Reference
======================

This page documents the current state of the dmsAIR source tree: the module
layout, every module's responsibility and its public routines, the
collision pipeline call chain, and the MPI execution model. It reflects the
code as it actually exists (18 source files — 6 programs in ``app/`` and 12
modules in ``src/``).

Source-tree layout
------------------

.. code-block:: text

   dmsAIR/
   ├── app/                              # Executables (one Fortran program per folder)
   │   ├── HeatBath/HeatBath.F90         #   dmsAIR_HeatBath — main production binary
   │   ├── Flow1D/Flow1D.F90             #   1D wall-bounded DMS (Couette / Fourier)
   │   ├── ScatteringMap/ScatteringMap.F90       #   χ(b, E) grid scans
   │   ├── IntegratorStudy/IntegratorStudy.F90   #   integrator / step-size bench
   │   ├── StateCheck/StateCheck.F90     #   state-reconstruction contract test
   │   └── UnitTests/UnitTests.F90       #   function-level regression driver
   ├── src/
   │   ├── DMS_Input_Class.F90           # Input parser, dmsAIR.inp keywords
   │   ├── Checkpoint_Module.F90         # Restart serialise / restore
   │   ├── Signal_Handler.F90            # SIGUSR1/SIGTERM clean-exit handlers
   │   ├── Timer_Module.F90              # Named-section wall-clock profiler
   │   ├── PrintGuard.F90                # Rank-0 print gate
   │   ├── DSMC/
   │   │   ├── DMS_Collision_Class.F90   # Collision-object driver (Execute_QN)
   │   │   ├── QCT_Collision_Module.F90  # QCT trajectory mechanics, χ scattering
   │   │   ├── Integrator_Class.F90      # BS / VV integrator abstraction
   │   │   └── NTC_Class.F90             # No-Time-Counter pairing
   │   ├── Measurement/
   │   │   └── Measurement_Class.F90     # box.csv writer, Tint/Tvib/Trot, rates
   │   └── Particles/
   │       ├── Particle_Class.F90        # Particle_Type + scatter helpers
   │       ├── Initialise_Class.F90      # Boltzmann / mixture initialisers
   │       └── LevelsDB_Module.F90       # Rovibrational levels DB I/O
   ├── run/                              # Case tree (one case = one dmsAIR.inp folder)
   ├── postprocessing/                   # Python analysis tools
   ├── docs/                             # Sphinx source (this site)
   ├── build/                            # Build artifacts (gitignored)
   └── Makefile

Module reference
----------------

Top-level ``src/``
~~~~~~~~~~~~~~~~~~~

**DMS_Input_Class.F90** — parses ``dmsAIR.inp``, holds the species and
collision-pair configuration, and populates the CoarseAIR input record.

- ``Read_DMS_Input`` (bound ``%Read``) — parse the keyword file into a
  ``DMS_Input_Type``.
- ``Populate_CAInput`` — fill a CoarseAIR ``Input_Type`` from a chosen
  collision pair (system, DB path, ODE/quantization params, PESs).
- ``Find_Collision_Pair`` — collision-pair index for an ordered species pair
  (order-independent; 0 if none).
- ``Expand_Env_Vars`` / ``Set_Environment_Variable`` — path ``$VAR`` expansion
  and process env-var setting.
- Types: ``Species_Def_Type``, ``CollisionPair_Def_Type``, ``DMS_Input_Type``.

**Checkpoint_Module.F90** — serialise/restore the full HeatBath state so a
wall-time-killed run can resume.

- ``Write_Checkpoint`` / ``Read_Checkpoint`` — pack/unpack particles, step,
  time, RNG and all counters (rank-0 gather, MPI broadcast on restore).
- ``Checkpoint_Exists`` — test for a restart file.

**Signal_Handler.F90** — install SIGUSR1/SIGTERM handlers so the scheduler can
request a clean checkpoint-and-exit.

- ``Install_Signal_Handlers`` — register the C-bound handler.
- ``g_terminate_now`` / ``g_term_signum`` — flags polled by the main loop.

**Timer_Module.F90** — lightweight named-section wall-clock profiler.

- ``Timer_Start`` / ``Timer_Stop`` — accumulate elapsed time + call count per
  named section.
- ``Timer_Report`` — MPI-reduce and write per-section CSV on root.
- ``Timer_Reset_All`` — clear the section table.

**PrintGuard.F90** — global ``print_enabled`` flag so only MPI rank 0 emits
setup-time banners.

``src/DSMC/``
~~~~~~~~~~~~~

**DMS_Collision_Class.F90** — collision-object driver with a pluggable
integrator; runs one trajectory per accepted pair and quantises the products.
All converged trajectories are accepted (textbook DMS; an energy-conservation
filter is opt-in via ``apply_energy_filter``).

- ``Execute_QN`` (``Execute_QN_DMS_Collision``) — **primary collision entry
  point**: runs a trajectory from quantum (v,j) initial states; returns product
  (v',j'), Eint, arrangement, and post-collision coordinates/velocities;
  handles 3- and 4-body.
- ``Execute`` — variant that starts from raw atomic phase-space coordinates
  (strategy-c persistent state).
- ``Execute_Fixed_b`` — as ``Execute`` but at a caller-specified impact
  parameter (no random *b* draw).
- ``Initialize`` — build the embedded integrator from the integrator-name
  selector.
- ``Reset_DMS_Collision_Counters`` — zero the module-level trajectory
  diagnostics (``N_traj_converged``, ``sum_dH_*``, ``DMS_Sel_iPES``, …).
- Type: ``DMS_Collision_Type``.

**QCT_Collision_Module.F90** — QCT trajectory mechanics: Hamiltonian ODE
right-hand side, initial-state construction, integration, arrangement
detection, product extraction, and scattering-angle evaluation. Used directly
by ScatteringMap/IntegratorStudy and (for initial-state setup) by
DMS_Collision_Class.

- ``QCT_Collision_Execute`` — full trajectory from raw target coords + relative
  speed.
- ``QCT_Collision_FromQN`` — trajectory starting from a quantum (v,j) state.
- ``QCT_Collision_Chi`` — CoM-frame scattering angle \|χ\| for any arrangement
  (drives ScatteringMap).
- ``QCT_FindState`` — quantise a product diatomic to (v,j) from Cartesian
  coordinates.
- ``QCT_SetInitialState`` / ``QCT_SetInitialState_Projectile`` — build
  target/projectile atomic coordinates from a quantum state on a given PES.
- ``QCT_Initialize`` — configure the thread-local ODE solver.

**Integrator_Class.F90** — ODE integrator abstraction for a CoarseAIR
trajectory.

- ``Integrate`` (``Integrate_Trajectory``) — dispatch to Bulirsch–Stoer or
  Velocity-Verlet, then record per-pair peak Rpi.
- ``Initialize`` — select BS/VV from a name string and configure the solver.
- Type: ``DMS_Integrator_Type``.

**NTC_Class.F90** — Bird No-Time-Counter collision-pair selection for the 0D
heat bath, with gnuc nuclear-spin importance boosting.

- ``NTC_SelectPairs`` — draw candidate pairs, accept with P = (σg)/(σg)\
  :sub:`max`, apply per-species gnuc importance weighting; return accepted pair
  indices + relative-velocity vectors.
- ``particle_boost`` — a particle's gnuc importance weight,
  gnuc\ :sub:`max`\ /gnuc(J).

``src/Measurement/``
~~~~~~~~~~~~~~~~~~~~~

**Measurement_Class.F90** — per-particle internal energy / (v,j),
Tint/Tvib/Trot reconstruction (Panesi 2013 decomposition), and the
``box.csv`` / population-row writers.

- ``WriteProperties`` (``Write_Properties``) — compute bulk properties
  (densities, Tint/Tvib/Trot, mole fractions) and append a ``box.csv`` row.
- ``Write_Pop_Row`` — write one population-distribution snapshot for a species.
- ``Compute_Eint_Cont`` / ``Compute_vj`` — continuous (classical) internal
  energy and the quantised (v,j) + eigen-Eint of a molecule.
- ``Calibrate_Cont_Zero`` — calibrate the per-species classical-energy zero
  (well minimum).
- ``BindSpeciesPotentials`` — map each species to its matching CoarseAIR
  diatomic potential (needed for heteronuclear exchange products).
- ``InitSpeciesLevels`` / ``SetSpeciesGnuc`` — load per-species level DBs and
  nuclear-spin weights.
- Type: ``Measurement_Type``.

``src/Particles/``
~~~~~~~~~~~~~~~~~~~

**Particle_Class.F90** — the single DMS particle (atom or molecule) carrying
CoM velocity, persistent atomic phase-space coordinates (strategy-c), and a
cached quantum state.

- ``ResampleVelocity`` — redraw CoM velocity from Maxwell–Boltzmann at *T*.
- ``Elastic_Scatter`` / ``Inelastic_Scatter`` — isotropic relative-velocity
  reorientation, optionally removing an internal-energy increment from the
  relative KE.
- Type: ``Particle_Type``.

**Initialise_Class.F90** — populate the particle array with Boltzmann-sampled
internal states and Maxwellian velocities.

- ``Initialise_Particles_Boltzmann`` — single-species initialisation at
  (Tint, Ttr).
- ``Initialise_Particles_Mixture`` — multi-species mixture (per-species counts
  and Tint).

**LevelsDB_Module.F90** — load and index a rovibrational levels database for
one species; (v,j) ↔ index ↔ energy lookups.

- ``Read`` — read the levels file, build the (v,j) table and per-v J=0 anchors
  for the Tvib/Trot decomposition.
- ``FindLevel`` / ``GetEnergy`` / ``GetVJ`` — level lookups by (v,j) or index.
- Types: ``Level_Type``, ``LevelsDB_Type``.

Programs (``app/``)
~~~~~~~~~~~~~~~~~~~~

- **HeatBath.F90** — main production binary: 0D isothermal heat-bath DMS
  driver (mixture init → NTC selection → MPI-strided trajectory execution →
  reduce → filter → particle update → output → checkpoint). Main loop at
  ``HeatBath.F90:1011``. Also hosts the adiabatic (energy-conserving) bath;
  see :doc:`/theory/bath_types`.
- **Flow1D.F90** — 1D wall-bounded DMS solver for planar Couette and Fourier
  flows: cell-based NTC over a 1D mesh, diffuse/specular walls with
  momentum/heat tallies, and per-cell profiles (T components, u\ :sub:`y`,
  composition, E\ :sub:`rot`/E\ :sub:`vib`). Uses the collision-frame
  alignment rotation (see below) since particle velocities persist between
  collisions.
- **ScatteringMap.F90** — arrangement-resolved \|χ\|(b, E\ :sub:`trans`\ ) grid
  scan for one collision pair, averaged over random orientations/phases.
- **IntegratorStudy.F90** — integrator / step-size sensitivity bench (VV, Y4,
  Y6, RK4, BS), recording \|dH\| drift, convergence and wallclock per
  trajectory.
- **StateCheck.F90** — end-to-end contract test for strategy-3 state
  reconstruction: builds phase space for every level of a species via
  ``QCT_SetInitialState``, hands it to CoarseAIR's ``FindState``, and checks
  that ``viba``/``AngMom``/``Eint``/boundedness invert back to the level the
  phase space came from (quantifies label ambiguity near dissociation).
  Diagnostic tool — no Makefile target yet; compile it against the same
  objects as the other apps when needed.
- **UnitTests.F90** — function-level regression driver: exercises pure helper
  routines with deterministic inputs for golden-file comparison in
  ``tests/regression/``.

Collision-frame alignment (persistent-velocity gases)
-----------------------------------------------------

CoarseAIR trajectories keep the approach axis fixed in the trajectory frame
(molecular orientation is randomised instead), so product CoM velocities come
back oriented to that fixed axis rather than to the pair's actual approach
direction. The isothermal 0D bath never sees this (velocities are resampled
every step), but any configuration with **persistent** velocities — the
adiabatic bath and Flow1D — would anisotropise the temperature components and
pump a spurious species drift. ``Execute_QN`` therefore returns the
trajectory-frame initial relative-velocity direction, and
``Build_Alignment_Rotation`` (``DMS_Collision_Class``) provides the orthogonal
map onto the pair's actual approach direction (random azimuth about it);
Flow1D always applies it, HeatBath applies it in adiabatic mode only. The
isothermal path draws no extra random numbers and remains bit-identical.

Collision pipeline
------------------

Each accepted NTC pair flows through the following call chain (file:line for the
current source):

.. code-block:: text

   HeatBath.F90:1011   do iStep = 1, NSteps                       (main loop)
     :1039   call NTC_SelectPairs(...)                  → NTC_Class.F90:50
     :1111   do iPair = rank+1, NPairs_accepted, nprocs (per-rank stride)
     :1211   call DMS_Colls(iCPair)%Execute_QN(...)     → DMS_Collision_Class.F90:340
                ├─ QCT_SetInitialState_Projectile (4-body)  QCT_Collision_Module.F90:905
                ├─ ComputeCoordinatesVelocities / ShiftCoordinates  (CoarseAIR)
                ├─ Integrator%Integrate → Traj%PaQ          Integrator_Class.F90:106
                ├─ Extract_Products_From_PaQ (arrangement)  DMS_Collision_Class.F90:1042
                └─ MolState%FindState (quantise v',j')      DMS_Collision_Class.F90:649

Post-return, in HeatBath:

1. ``MPI_Allreduce`` the collision-result buffers across ranks
   (``HeatBath.F90:1425``).
2. Apply the nuclear-spin acceptance filter (homonuclear molecules only).
3. Apply the per-channel filters: the ``Allow Exchange`` master switch, the
   per-pair/arrangement gate ``allow_exch_arr(iCPair, arr)``, and
   ``Allow Dissociation``.
4. Update particle (v, j, pos, vel) — guarded by ``is_homonuclear_product`` so
   heteronuclear exchange products are consumed and re-tagged rather than
   poisoning the bath with wrong-manifold quantum numbers.
5. Increment the per-pair counters (``pair_N_att``, ``pair_N_inel``,
   ``pair_N_exch``, ``pair_N_exch_by_arr``, ``pair_N_diss``, …).

MPI model
---------

dmsAIR uses a **coll-buffer-replicated** MPI pattern: each rank computes its
share of accepted pairs, then ``MPI_Allreduce`` broadcasts the collision
results into a shared buffer that every rank walks through synchronously. This
keeps all ranks in lockstep on particle-state updates without any hand-rolled
reduction of per-particle arrays.

Per-rank cost scales with ``NPairs_accepted / NRanks``; NTC pair selection is
the only serial bottleneck (O(N\ :sub:`p`) per step, on rank 0).
