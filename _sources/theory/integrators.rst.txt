Trajectory Integrators
======================

dmsAIR provides two trajectory integrators. Both integrate Hamilton's
equations on the PES; they differ in order of accuracy, cost per step, and
in how they handle the energy conservation during deep close encounters.

.. list-table::
   :header-rows: 1
   :widths: 10 35 15 40

   * - Key
     - Name
     - Order
     - Notes
   * - BS
     - Bulirsch–Stoer (adaptive)
     - variable
     - Default for production; modified-midpoint with Richardson
       extrapolation and an adaptive step size; non-symplectic.
   * - VV
     - Velocity Verlet
     - 2
     - Symplectic; fixed timestep set via ``VV Timestep [a.u.]``.

Benchmark
---------

See :doc:`/examples/integrator_study` for the ``dmsAIR_IntegratorStudy``
tool that compares energy drift and reaction probability between the two
integrators on the same trajectory ensemble. The comparative methodology
follows the GPU-accelerated QCT-benchmark approach described in
[NormanGPU]_.
