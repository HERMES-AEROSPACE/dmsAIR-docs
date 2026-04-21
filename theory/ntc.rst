No-Time-Counter (NTC) Pair Selection
=====================================

Collision-pair selection in dmsAIR uses Bird's No-Time-Counter (NTC)
method [Bird1994]_, adapted for the QCT collision model. The NTC
algorithm provides an unbiased sampling of the exact collision rate
without requiring the enumeration of all :math:`O(N^2)` candidate pairs
per time step.

Sampling law
------------

For a homogeneous cell of volume :math:`V_c` containing :math:`N` particles
of a given collision-pair type, the expected number of NTC trials per
time-step :math:`\Delta t` is

.. math::

   N_{\mathrm{trial}} = \frac{N (N - 1)}{2}
                        \frac{(\sigma v_{\mathrm{rel}})_{\max}
                              \, \Delta t}{V_c} ,

where :math:`(\sigma v_{\mathrm{rel}})_{\max}` is a running upper bound on
the collision-rate product — updated adaptively each time a new maximum is
observed. A trial pair is accepted with probability

.. math::

   P_{\mathrm{acc}} = \frac{\sigma \, v_{\mathrm{rel}}}
                           {(\sigma v_{\mathrm{rel}})_{\max}} .

Because the acceptance probability is exact up to the adaptive maximum,
the overall procedure recovers the canonical DSMC collision rate without
requiring the actual value of :math:`(\sigma v_{\mathrm{rel}})_{\max}` to
be known *a priori*.

Cross-section convention
------------------------

dmsAIR uses a **geometric** reference cross-section
:math:`\sigma = \pi b_{\max}^2`, where :math:`b_{\max}` is the cut-off
impact parameter of the QCT trajectory. All physics enters through the
outcome of the trajectory itself (inelastic / exchange / dissociation); no
empirical model (TCE, VHS) is invoked. This is what sets DMS apart from
conventional DSMC and is why the same infrastructure can handle any
reactive system without tuning [SchwartzentruberEtAl2017]_.

Parallel implementation
-----------------------

Per time step, all accepted pairs are pre-selected, their QCT trajectories
are evaluated in parallel across MPI ranks, and the post-collision updates
are then applied in a synchronised second pass. This scales cleanly
because each rank processes a disjoint subset of the pair queue; the
collision-result buffer is ``MPI_Allreduce``-combined before being walked
by every rank identically.

Choosing ``bmax``
-----------------

The choice of :math:`b_{\max}` is a physics calibration, not a free
parameter. For every new collision system, dmsAIR ships a companion tool
``dmsAIR_ScatteringMap`` that scans the mean deflection angle
:math:`\langle |\chi| \rangle` over a :math:`(b, E)` grid and locates the
outer boundary of the reactive/inelastic region — typically the
:math:`\langle|\chi|\rangle = 1^\circ` iso-contour.

For neutral–neutral scattering this boundary follows Langevin-capture
scaling:

.. math::

   b_{\max}(E) \approx a \, E^{-1/n} ,

where :math:`n` is the power of the dominant long-range attractive term
(:math:`n = 6` for van der Waals). :math:`b_{\max}` is chosen as the
maximum of :math:`b_{\max}(E)` over the energy range of interest, rounded
up to the next 0.5 Bohr. See :doc:`/examples/scattering_map` for the
full calibration workflow.
