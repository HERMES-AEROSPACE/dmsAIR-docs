Installation
============

Prerequisites
-------------

+-------------------+------------------+------------------------------------------+
| Dependency        | Version          | Notes                                    |
+===================+==================+==========================================+
| Fortran compiler  | gfortran ≥ 9     | With MPI wrapper (``mpif90``)            |
+-------------------+------------------+------------------------------------------+
| MPI               | OpenMPI / MPICH  | For parallel execution                   |
+-------------------+------------------+------------------------------------------+
| BLAS/LAPACK       | Any              | OpenBLAS recommended                     |
+-------------------+------------------+------------------------------------------+
| CoarseAIR         | Required         | External install — see below             |
+-------------------+------------------+------------------------------------------+
| Python 3          | ≥ 3.8            | Post-processing: numpy / pandas / mpl    |
+-------------------+------------------+------------------------------------------+

CoarseAIR dependency
--------------------

dmsAIR links against an **externally-built** CoarseAIR static library; no
CoarseAIR source is vendored in this repo. You will need:

- A CoarseAIR source tree (upstream:
  `simoneventuri/CoarseAIR <https://github.com/simoneventuri/CoarseAIR>`_)
- The built static library ``lib/libcoarseair.a`` plus module files under
  ``mod/*.mod``
- The ``dtb/`` data directory (PES + level databases)

Two environment variables tell dmsAIR where to find them:

+--------------------+----------------------------------------------------------+
| Env var            | Purpose                                                  |
+====================+==========================================================+
| ``COARSEAIR_BUILD``| Build directory with ``lib/libcoarseair.a`` + ``mod/``   |
+--------------------+----------------------------------------------------------+
| ``COARSEAIR_DTB``  | Path to the CoarseAIR ``dtb/`` directory                 |
+--------------------+----------------------------------------------------------+

Required CoarseAIR patches
~~~~~~~~~~~~~~~~~~~~~~~~~~

dmsAIR calls four procedures that are ``private`` in upstream CoarseAIR.
Apply these patches to ``CoarseAIR/src/Collision/Collision_Class.F90``
(inside the ``type :: Collision_Type ... contains ... private`` block) and
rebuild:

.. code-block:: diff

   - procedure           ::    ComputeCoordinatesVelocities
   + procedure ,public   ::    ComputeCoordinatesVelocities
   - procedure           ::    ShiftCoordinates
   + procedure ,public   ::    ShiftCoordinates
   - procedure           ::    SetPaQ
   + procedure ,public   ::    SetPaQ
   - procedure           ::    ApplyTransformation
   + procedure ,public   ::    ApplyTransformation

Build
-----

.. code-block:: bash

   export COARSEAIR_BUILD=/path/to/CoarseAIR/build/coarseair-1.1-release-gnu-9.3.0
   export COARSEAIR_DTB=/path/to/CoarseAIR/coarseair/dtb
   cd /path/to/dmsAIR
   make -j8

The build produces three binaries under ``build/bin/``:

- ``dmsAIR_HeatBath`` — the main production binary (used by the ``run/`` tree)
- ``dmsAIR_ScatteringMap`` — deflection-angle scans for ``bmax`` selection
- ``dmsAIR_IntegratorStudy`` — integrator benchmarking tool

Build artefacts
---------------

.. code-block:: text

   build/
   ├── bin/     # executables
   ├── obj/     # compiled object files (.o)
   └── mod/     # Fortran module files (.mod)

``make clean`` removes the whole ``build/`` tree.
