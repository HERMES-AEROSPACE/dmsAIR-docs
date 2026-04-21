Architecture Reference
======================

Source-tree layout
------------------

.. code-block:: text

   dmsAIR/
   ├── app/                         # Executables (one Fortran program per folder)
   │   ├── HeatBath/                #   dmsAIR_HeatBath — main production binary
   │   ├── ScatteringMap/           #   dmsAIR_ScatteringMap — χ(b, E) grid scans
   │   └── IntegratorStudy/         #   dmsAIR_IntegratorStudy — integrator bench
   ├── src/
   │   ├── DMS_Input_Class.F90      # Input parser, dmsAIR.inp keywords
   │   ├── DSMC/
   │   │   ├── DMS_Collision_Class.F90   # Collision-object driver (Execute_QN)
   │   │   ├── QCT_Collision_Module.F90  # QCT-specific logic
   │   │   └── Integrator_Class.F90      # BS / VV integrators
   │   ├── Measurement/
   │   │   └── Measurement_Class.F90     # box.csv writer, rate accumulators
   │   ├── Particles/
   │   │   ├── Particle_Class.F90        # Particle_Type
   │   │   └── Initialise_Class.F90      # Boltzmann / mixture initialisers
   │   ├── Collision_Pair/
   │   │   └── NTC_Class.F90             # No-Time-Counter pairing
   │   ├── LevelsDB_Module.F90           # Rovibrational levels DB I/O
   │   └── scripts/
   │       ├── dmsAIR.sh                 # Local launcher (symlinked into cases)
   │       ├── sbatch_heatbath.slurm     # SLURM template
   │       └── launchDMS.py              # Adaptive batch submitter
   ├── run/                         # Case tree (one case = one dmsAIR.inp folder)
   ├── postprocessing/              # Python analysis tools
   ├── docs/                        # Sphinx source (this site)
   ├── build/                       # Build artifacts (gitignored)
   └── Makefile

Collision pipeline
------------------

Each accepted NTC pair flows through:

.. code-block:: text

   HeatBath.F90
     └─ DMS_Colls(iCPair)%Execute_QN(...)
          └─ (DMS_Collision_Class.F90) Execute_QN_DMS_Collision
               ├─ SetInitialState  ← persistent phase-space coords
               ├─ Random rotation  ← isotropic orientation
               ├─ ComputeCoordinatesVelocities  (CoarseAIR) ← approach geometry
               ├─ ShiftCoordinates              (CoarseAIR)
               ├─ Integrator%Integrate → Traj%PaQ(:,1)
               ├─ Extract_Products_From_PaQ     ← arrangement detection
               └─ MolState%FindState            (CoarseAIR) ← quantise (v', j')

Post-return, HeatBath:

1. MPI_Allreduces the collision-result buffers across ranks.
2. Applies the nuclear-spin acceptance filter (homonuclear only).
3. Applies the per-channel filters (``Allow Exchange``, ``Allow Exchange
   Arr N``, ``Allow Dissociation``).
4. Updates particle (v, j, pos, vel) — guarded by the ``is_homonuclear_product``
   flag so heteronuclear exchange doesn't poison the bath with
   wrong-manifold quantum numbers.
5. Increments the per-pair counters (``pair_N_att``, ``pair_N_inel``,
   ``pair_N_exch``, ``pair_N_exch_by_arr``, ``pair_N_diss``, ...).

MPI model
---------

dmsAIR uses a **coll-buffer-replicated** MPI pattern: each rank computes
its share of accepted pairs, then ``MPI_Allreduce`` broadcasts the
collision results into a shared buffer that every rank walks through
synchronously. This keeps all ranks in lockstep on particle-state updates
without any hand-rolled reduction of per-particle arrays.

Per-rank cost scales with ``NPairs_accepted / NRanks``; NTC pair selection
is the only serial bottleneck (O(N_p) per step).
