NO + C heat bath
================

A heteronuclear 3-body system with **two distinct exchange channels** —
NO+C → CN+O and NO+C → CO+N. The first production test of the CO+N channel
after the heteronuclear-quantisation fix.

Case tree
---------

.. code-block:: text

   run/CNO/<PES>/NO+C/<regime>/<T>/

with

- ``PES`` ∈ {``2A1x2``, ``2A1+2A2``, ``4A2``}
- ``regime`` ∈ {``inelastic``, ``exchange1``, ``exchange2``,
  ``exchange1+dissociation``, ``exchange2+dissociation``,
  ``directdissociation``, ``totaldissociation``}
- ``T`` ∈ {``1500K``, ``2500K``, ``5000K``, ``10000K``, ``20000K``}

= 3 × 7 × 5 = 105 cases per subsystem (NO+C / CN+O / CO+N).

Regime mapping
--------------

.. list-table::
   :header-rows: 1
   :widths: 32 50

   * - Regime folder
     - Input flags
   * - ``inelastic``
     - Allow Exchange Arr 1 = no, Allow Diss = no
   * - ``exchange1``
     - Allow Exchange Arr 3 = no (CN+O only)
   * - ``exchange2``
     - Allow Exchange Arr 2 = no (CO+N only)
   * - ``exchange1+dissociation``
     - Ex1 only + Allow Dissociation = yes
   * - ``exchange2+dissociation``
     - Ex2 only + Allow Dissociation = yes
   * - ``totaldissociation``
     - Allow Exchange Arr 1 = no, Allow Diss = yes → single dissociation channel

.. note::

   The current ME-consistent generation of these cases (per-temperature
   electronic degeneracies, product-pair decks) lives under
   ``run/Verification/NO+C_<regime>/<T>/`` alongside the
   :doc:`partner systems </examples/cno_heatbath>`; the tree above is the
   original PES-resolved sweep.

Regime deck highlights and enabled processes
--------------------------------------------

**Inelastic** (single pair, no reactions):

.. code-block:: text

   Allow Dissociation   = no
   Allow Exchange Arr 1 = no
   Nb of Collision Pairs = 1        # NO + C

Only NO(v,J) + C → NO(v′,J′) + C energy transfer is enabled.

**Exchange with product kinetics** (``NO+C_Exchange1_Products``):

.. code-block:: text

   Allow Exchange Arr 1 = yes
   Allow Exchange P1 Arr 2 = yes   # NO+C -> CN+O   (desired forward)
   Allow Exchange P1 Arr 3 = no    # NO+C -> CO+N   (parasitic)
   Allow Exchange P2 Arr 2 = no    # CN+O -> CO+N   (parasitic — reverse)
   Allow Exchange P2 Arr 3 = yes   # CN+O -> NO+C   (desired back)

   Species: NO (X=0.5), C (X=0.5), CN, CO, N, O (all X=0)
   Nb of Collision Pairs = 2
   # P1: NO + C  (reactants)      # P2: CN + O  (products)

Enabled processes: NO relaxation + forward exchange on P1; CN relaxation
+ back-exchange on P2. **Note the arrangement flip**: the desired channel
is ``Arr 2`` on P1 but ``Arr 3`` on P2 — the arrangement index numbers
atom-pair slots *within* each pair, so the same index is a different
reaction in different pairs. This is exactly why the per-pair filter
form exists; a global ``Allow Exchange Arr N`` cannot express this
selection.

**Dissociation** variants add ``Allow Dissociation = yes`` on top of the
same pair structure (break-up opens on every declared pair);
``TotalDissociation`` reduces to one pair with exchange off, giving the
single lumped dissociation channel that matches the ME
total-dissociation variant. Direct vs exchange-assisted is classified
per event from the trajectory record (diagnostic only).

**Product kinetics:** exchange products relax and back-react only
because the deck declares the product pair (P2) — without it they are
composition-only spectators. Dissociation fragments (atoms) are always
spectators: dmsAIR has no recombination. The full recipe for enabling
product kinetics in a new deck is in the
:doc:`CO + N(4S) example </examples/con4s_heatbath>`.

Running a single case
---------------------

dmsAIR supports two execution modes, selected by which launcher you call
inside the case directory.

**Local machine** (laptop / workstation; runs MPI directly):

.. code-block:: bash

   cd run/CNO/4A2/NO+C/exchange1/10000K
   ./dmsAIR.sh 16     # 16 MPI ranks (omit the argument → default 16)

**Cluster with a SLURM scheduler** (submit a batch job):

.. code-block:: bash

   cd run/CNO/4A2/NO+C/exchange1/10000K
   sbatch sbatch_heatbath.slurm

The two launchers are designed to be drop-in equivalents:

- ``dmsAIR.sh`` wraps ``mpirun`` for the local architecture, with a
  TCP + shared-memory fallback when the host lacks an InfiniBand fabric.
  The rank count is an argument (``./dmsAIR.sh <N>``), an environment
  variable (``NRANKS=<N> ./dmsAIR.sh``), or defaults to 16.
- ``sbatch_heatbath.slurm`` is a SLURM template that sets
  ``--nodes``, ``--ntasks-per-node``, accounts and partitions, loads the
  cluster toolchain, and invokes the binary via ``mpirun --bind-to none``
  to bypass the SLURM PMIx stack on hosts where MUNGE is unavailable.

Only one of the two is active in a given environment — if
``$SLURM_JOB_ID`` is defined, ``dmsAIR.sh`` tightens its MPI fabric
settings to full-speed (UCX/IB) production; otherwise it falls back to
TCP. This way the **same** case directory can be run on either
architecture without edits.

Launching a full sweep
----------------------

.. code-block:: bash

   # All seven regimes × five temperatures on the 4A2 PES
   ./src/scripts/launchDMS.py --subsys NO+C --pes 4A2 --regime all --T all
   # = 35 SLURM submissions

Post-processing
---------------

.. code-block:: bash

   python3 postprocessing/Postprocessing/postprocessing.py \
       --system CNO --subsys NO+C --pes 4A2

Generates comparison plots against PLATO's ME reference at
``/home/ccivrais/WORKSPACE/PLATO/run/CNO/MasterEquationAnalysis/NO+C/``.
