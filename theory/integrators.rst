Trajectory Integrators
======================

dmsAIR provides five trajectory integrators. All integrate Hamilton's
equations on the PES; they differ in order, cost per step, and how they
handle energy conservation during deep close encounters.

+-----+-----------------------------+--------------+---------------------------+
| Key | Name                        | Order        | Notes                     |
+=====+=============================+==============+===========================+
| BS  | Bulirsch–Stoer (adaptive)   | variable     | Default for production;   |
|     |                             |              | non-symplectic, can drift |
|     |                             |              | during close approaches   |
+-----+-----------------------------+--------------+---------------------------+
| VV  | Velocity Verlet             | 2            | Symplectic; fixed dt      |
+-----+-----------------------------+--------------+---------------------------+
| Y4  | Yoshida 4th-order           | 4            | Symplectic composition;   |
|     |                             |              | 3 force evals/step        |
+-----+-----------------------------+--------------+---------------------------+
| Y6  | Yoshida 6th-order           | 6            | Symplectic composition;   |
|     |                             |              | 7 force evals/step        |
+-----+-----------------------------+--------------+---------------------------+
| RK4 | Runge–Kutta 4th-order       | 4            | Non-symplectic; reference |
+-----+-----------------------------+--------------+---------------------------+

Benchmark
---------

See :doc:`/examples/integrator_study` for the ``dmsAIR_IntegratorStudy``
tool that compares energy drift and reaction probability across integrators
on the same trajectory ensemble.

Recommendation
--------------

- **H3 / simple 3-body**: VV at ``VV Timestep = 2.0`` a.u. is
  energy-conserving to ~10\ :sup:`-6`\  Hartree and 2× faster than BS.
- **4-body systems**: BS is usually necessary because VV's fixed dt is
  insufficient during close three-atom encounters.
- **Long trajectories (complex formation)**: Yoshida Y4 offers the best
  energy-drift / cost ratio when ``tmax`` is large.
