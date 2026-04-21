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
  ``exchange1+dissociation``, ``exchange2+dissociation``, ``dissociation``}
- ``T`` ∈ {``1500K``, ``2500K``, ``5000K``, ``10000K``, ``20000K``}

= 3 × 6 × 5 = 90 cases per subsystem (NO+C / CN+O / CO+N).

Regime mapping
--------------

+--------------------------------+------------------------------------------+
| Regime folder                  | Input flags                              |
+================================+==========================================+
| ``inelastic``                  | Allow Exchange = no, Allow Diss = no     |
+--------------------------------+------------------------------------------+
| ``exchange1``                  | Allow Exchange Arr 3 = no (CN+O only)    |
+--------------------------------+------------------------------------------+
| ``exchange2``                  | Allow Exchange Arr 2 = no (CO+N only)    |
+--------------------------------+------------------------------------------+
| ``exchange1+dissociation``     | Ex1 only + Allow Dissociation = yes      |
+--------------------------------+------------------------------------------+
| ``exchange2+dissociation``     | Ex2 only + Allow Dissociation = yes      |
+--------------------------------+------------------------------------------+
| ``dissociation``               | Allow Exchange = no, Allow Diss = yes    |
+--------------------------------+------------------------------------------+

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

   # All six regimes × five temperatures on the 4A2 PES
   ./src/scripts/launchDMS.py --subsys NO+C --pes 4A2 --regime all --T all
   # = 30 SLURM submissions

Post-processing
---------------

.. code-block:: bash

   python3 postprocessing/Postprocessing/postprocessing.py \
       --system CNO --subsys NO+C --pes 4A2

Generates comparison plots against PLATO's ME reference at
``/home/ccivrais/WORKSPACE/PLATO/run/CNO/MasterEquationAnalysis/NO+C/``.
