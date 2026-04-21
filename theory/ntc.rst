No-Time-Counter (NTC) Pair Selection
=====================================

Collision-pair selection in dmsAIR uses Bird's No-Time-Counter method,
adapted for the QCT collision model.

Batch vs. sequential
--------------------

dmsAIR implements two NTC schemes selectable via the ``NTC Scheme`` keyword:

- ``batch`` (default, recommended): pre-select all accepted pairs for the
  current time step, evaluate their QCT trajectories via MPI, then apply the
  post-collision updates in a synchronised second pass. Scales cleanly across
  ranks because each rank processes a disjoint subset of the pair queue.
- ``sparta``: SPARTA-style sequential attempt loop. Useful for debugging
  small cases; not recommended for production.

Acceptance criterion
--------------------

A trial pair is accepted with probability

.. math::

   P_{\mathrm{acc}} = \frac{\sigma \, v_{\mathrm{rel}}}{(\sigma \, v_{\mathrm{rel}})_{\max}}

where :math:`\sigma = \pi b_{\max}^2` is the fixed reference cross-section.
The running maximum :math:`(\sigma v_{\mathrm{rel}})_{\max}` is updated
adaptively per collision pair type.

Choosing ``bmax``
-----------------

The ``Collision Pair bmax`` keyword sets the cut-off impact parameter. For
every new collision system, dmsAIR ships a companion tool
``build/bin/dmsAIR_ScatteringMap`` that scans ⟨\|χ\|⟩ over the ``(b, E)``
grid and locates the outer boundary of the reactive/inelastic region. A
Langevin-capture fit ``bmax(E) = a·E^b`` is typically used as the guiding
rule — see :doc:`/examples/scattering_map`.
