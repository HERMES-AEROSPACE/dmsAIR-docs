Getting Started
===============

This page walks through a first dmsAIR simulation end-to-end: the H\ :sub:`2`\ +H
heat bath at 10 000 K, a canonical benchmark with published Master-Equation
(ME) references.

Prerequisites
-------------

Before installing dmsAIR you need a working CoarseAIR installation — see
:doc:`installation` for the full dependency list and the required CoarseAIR
visibility patches.

Build
-----

.. code-block:: bash

   export COARSEAIR_BUILD=$HOME/WORKSPACE/CoarseAIR/build/coarseair-1.1-release-gnu-9.3.0
   export COARSEAIR_DTB=$HOME/WORKSPACE/CoarseAIR/coarseair/dtb
   cd $HOME/WORKSPACE/dmsAIR
   make                # -> build/bin/dmsAIR_HeatBath

Other binaries are built by their own targets: ``make flow1d`` (1D
Couette/Fourier solver), ``make scatteringmap``, ``make integratorstudy``
and ``make unittests``.

Run the H3 example
------------------

.. code-block:: bash

   cd run/H3/NoDissociation/10000K
   ./dmsAIR.sh 4       # 4 MPI ranks

Output appears under ``Output/``:

- ``box.csv`` — bulk macroscopic history (Ttr, Tint, p, rho, mole fractions,
  rate coefficients per channel)
- ``pop.csv`` — rovibrational population distribution at every sampled step

Plot
----

.. code-block:: bash

   python3 postprocessing/Postprocessing/postprocessing.py --no-diss

Open ``postprocessing/Postprocessing/Figures/H3/NoDissociation/Energy.pdf`` to
see DMS (red dots) overlaid on the ME reference (black lines).

Where to go next
----------------

- :doc:`running_simulations` — local vs. SLURM launchers, parameter sweeps.
- :doc:`flow1d` — 1D wall-bounded flows (Couette / Fourier) with
  ``dmsAIR_Flow1D``.
- :doc:`/theory/bath_types` — isothermal vs. adiabatic 0D baths.
- :doc:`/reference/validation` — what has been verified against
  Master-Equation references, and to what accuracy.
