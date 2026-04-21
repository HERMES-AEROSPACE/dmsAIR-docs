Integrator Study
================

``dmsAIR_IntegratorStudy`` benchmarks energy conservation and reaction
probability across the available trajectory integrators (BS and VV).
Primary use: pick the most efficient integrator for a new system before
committing to a production sweep.

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

Post-processing
---------------

.. code-block:: bash

   python3 postprocessing/IntegratorStudy/plot_integrator_comparison.py

Plots ⟨\|dH\|⟩ vs cost and reaction probability convergence.
