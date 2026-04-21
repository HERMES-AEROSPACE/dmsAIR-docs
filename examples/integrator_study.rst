Integrator Study
================

``dmsAIR_IntegratorStudy`` benchmarks energy conservation and reaction
probability across the available trajectory integrators (BS, VV, Y4, Y6,
RK4). Primary use: pick the most efficient integrator for a new system
before committing to a production sweep.

Running
-------

.. code-block:: bash

   cd run/IntegratorStudy/H3_default
   ./run.sh

The input ``intstudy.inp`` specifies a list of integrators plus shared
trajectory parameters (``(b, E, v, j)``, ``N_traj``, ``dt``, ``eps``).

Output
------

``IntegratorStudy.dat`` has one row per integrator with:

- Total time
- Mean \|dH\| (energy drift per trajectory)
- Fraction converged
- Reaction-channel counts

Reading the output
------------------

On the H3 default grid at 10 000 K:

.. list-table::
   :header-rows: 1
   :widths: 10 15 20 15 20

   * -
     - cost/ev
     - ⟨\|dH\|⟩
     - P_react
     - notes
   * - BS
     - 1.0×
     - 10\ :sup:`-6`
     - ~0.12
     - reference
   * - VV
     - 0.4×
     - 10\ :sup:`-5`
     - ~0.12
     - good
   * - Y4
     - 1.2×
     - 10\ :sup:`-7`
     - ~0.12
     - best ratio
   * - Y6
     - 2.8×
     - 10\ :sup:`-9`
     - ~0.12
     - tight
   * - RK4
     - 1.1×
     - 10\ :sup:`-4`
     - drifts
     - avoid

Post-processing
---------------

.. code-block:: bash

   python3 postprocessing/IntegratorStudy/plot_integrator_comparison.py

Plots ⟨\|dH\|⟩ vs cost and reaction probability convergence.
