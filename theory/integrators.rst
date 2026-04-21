Trajectory Integrators
======================

dmsAIR provides two trajectory integrators. Both integrate Hamilton's
equations on the PES; they differ in order, cost per step, and how they
handle energy conservation during deep close encounters.

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
     - Default for production; adaptive step size; non-symplectic.
   * - VV
     - Velocity Verlet
     - 2
     - Symplectic; fixed timestep set via ``VV Timestep [a.u.]``.

Benchmark
---------

See :doc:`/examples/integrator_study` for the ``dmsAIR_IntegratorStudy``
tool that compares energy drift and reaction probability between
integrators on the same trajectory ensemble. The comparative analysis
framework follows the GPU-accelerated QCT-benchmark methodology described
in [NormanGPU]_.
