Running Simulations
===================

dmsAIR supports two execution architectures through a pair of drop-in
launcher scripts shipped inside every case directory. The scripts share a
common input (``dmsAIR.inp`` + level tables + the binary under
``build/bin/``); only the launcher and the MPI-fabric settings differ.

Local machine (workstation / laptop)
------------------------------------

The wrapper ``src/scripts/dmsAIR.sh`` is symlinked into every case folder
and invokes ``mpirun`` directly:

.. code-block:: bash

   cd run/H3/NoDissociation/10000K
   ./dmsAIR.sh             # 16 MPI ranks (default)
   ./dmsAIR.sh 8           # 8 ranks
   NRANKS=32 ./dmsAIR.sh   # rank count from environment

On a local host without an InfiniBand fabric, the script automatically
falls back to TCP + shared-memory so the run completes on the loopback
interface. On a compute node inside a SLURM allocation, the fabric
settings are restored to UCX/IB for full-speed production.

Cluster with a SLURM scheduler
------------------------------

Each case also ships with ``sbatch_heatbath.slurm``, a template SLURM
batch script. Submit the job directly:

.. code-block:: bash

   cd run/CNO/4A2/NO+C/exchange1/10000K
   sbatch sbatch_heatbath.slurm

The SLURM script sets ``--nodes``, ``--ntasks-per-node``, the account /
partition, loads the cluster toolchain (GCC, OpenMPI), applies the PMIx
``native`` bypass required on hosts where MUNGE is not installed, and
invokes the binary via ``mpirun --bind-to none`` to avoid the OpenMPI 5.x
over-binding seen on partial allocations. Tune ``--time``, ``--nodes``
and ``--ntasks-per-node`` in the header at the top of the file to match
your cluster's queue policy.

Choosing between the two modes
------------------------------

+-----------------------------+-----------------------------+--------------------------------------------+
| Launcher                    | When to use                 | Typical size                               |
+=============================+=============================+============================================+
| ``./dmsAIR.sh [N]``         | Local interactive runs,     | :math:`\lesssim 32` MPI ranks              |
|                             | debugging, smoke tests      |                                            |
+-----------------------------+-----------------------------+--------------------------------------------+
| ``sbatch sbatch_heatbath``  | Production batch on a       | 1 node, 16–128 ranks; the script can be    |
|                             | SLURM-scheduled cluster     | edited to request multiple nodes           |
+-----------------------------+-----------------------------+--------------------------------------------+

The two launchers read **the same** ``dmsAIR.inp`` and produce identical
output files under ``Output/``. Switching between them requires no edits
to the case directory.

Adaptive parameter sweep (``launchDMS.py``)
-------------------------------------------

``src/scripts/launchDMS.py`` submits any chosen subset of
(subsystem × PES × regime × temperature) cases to a SLURM queue. Examples:

.. code-block:: bash

   # All NO+C cases on the 4A2 PES (default)
   ./launchDMS.py

   # Only exchange1 + exchange1+dissociation at 10 000 K:
   ./launchDMS.py --regime exchange1 exchange1+dissociation --T 10000

   # Compare 2A1x2 vs 2A1+2A2 at 5000, 10000, 20000 K:
   ./launchDMS.py --pes 2A1x2 2A1+2A2 --T 5000 10000 20000

   # CO+N on all three PESs, full sweep:
   ./launchDMS.py --subsys CO+N --pes all

   # Preview without submitting:
   ./launchDMS.py --pes all --dry-run

The sweeper always calls ``sbatch``; it is the intended driver for
cluster production runs. For local multi-case sweeps, a simple
``for`` loop over ``dmsAIR.sh`` invocations is sufficient.

Output layout
-------------

.. code-block:: text

   <case_dir>/
   ├── dmsAIR.inp           # input
   ├── levels_*.inp         # rovibrational level tables
   ├── dmsAIR.sh            # local launcher (symlink to src/scripts/dmsAIR.sh)
   ├── sbatch_heatbath.slurm
   ├── log.out_<jobid>      # SLURM stdout (cluster runs only)
   ├── log.err_<jobid>      # SLURM stderr (cluster runs only)
   └── Output/
       ├── box.csv          # macroscopic history
       └── pop.csv          # population distributions
