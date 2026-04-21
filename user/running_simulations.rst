Running Simulations
===================

Local (single workstation)
--------------------------

Every case directory in ``run/`` contains a symlink to ``src/scripts/dmsAIR.sh``
that launches the binary with the local MPI stack (OpenMPI by default):

.. code-block:: bash

   cd run/H3/NoDissociation/10000K
   ./dmsAIR.sh             # 16 MPI ranks (default)
   ./dmsAIR.sh 8           # 8 ranks
   NRANKS=32 ./dmsAIR.sh   # via env

On a login node that lacks the InfiniBand fabric the script falls back to
TCP+shared-memory automatically.

SLURM cluster
-------------

Each case also ships with ``sbatch_heatbath.slurm``; submit via:

.. code-block:: bash

   cd run/CNO/4A2/NO+C/exchange1/10000K
   sbatch sbatch_heatbath.slurm

The SLURM script loads the cluster toolchain, applies the required PMIx
bypass for login nodes without MUNGE, and uses ``mpirun --bind-to none`` to
avoid OpenMPI 5.x over-binding on partial allocations.

Adaptive parameter sweep (``launchDMS.py``)
-------------------------------------------

``src/scripts/launchDMS.py`` submits any chosen subset of
(subsystem × PES × regime × temperature) cases. Examples:

.. code-block:: bash

   # All NO+C cases on the 4A2 PES (default)
   ./launchDMS.py

   # Only the exchange1 + exchange1+dissociation regimes at 10 000 K:
   ./launchDMS.py --regime exchange1 exchange1+dissociation --T 10000

   # Compare 2A1x2 vs 2A1+2A2 at 5000, 10000, 20000 K:
   ./launchDMS.py --pes 2A1x2 2A1+2A2 --T 5000 10000 20000

   # CO+N on all 3 PESs, full sweep:
   ./launchDMS.py --subsys CO+N --pes all

   # Preview without submitting:
   ./launchDMS.py --pes all --dry-run

Output layout
-------------

.. code-block:: text

   <case_dir>/
   ├── dmsAIR.inp           # input
   ├── levels_*.inp         # rovibrational level tables
   ├── dmsAIR.sh            # local launcher (symlink)
   ├── sbatch_heatbath.slurm
   ├── log.out_<jobid>      # SLURM stdout
   ├── log.err_<jobid>      # SLURM stderr
   └── Output/
       ├── box.csv          # macroscopic history
       └── pop.csv          # population distributions
