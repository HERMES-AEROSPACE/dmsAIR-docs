No-Time-Counter (NTC) Pair Selection
=====================================

Collision-pair selection in dmsAIR uses Bird's No-Time-Counter (NTC)
scheme [Bird1994]_, adapted to the DMS collision model. The NTC algorithm
provides an unbiased sampling of the exact collision rate without
requiring the enumeration of all :math:`\mathcal{O}(N^2)` candidate pairs
per time step.

Sampling law
------------

For a homogeneous cell of volume :math:`V_c` containing :math:`N`
particles of a given collision-pair type, the expected number of NTC
trials per time step :math:`\Delta t` is

.. math::

   N_{\mathrm{trial}} = \frac{N (N - 1)}{2}
                        \frac{(\sigma v_{\mathrm{rel}})_{\max}
                              \, \Delta t}{V_c} ,

where :math:`(\sigma v_{\mathrm{rel}})_{\max}` is a running upper bound
on the collision-rate product — updated adaptively each time a new
maximum is observed during the simulation. A trial pair is accepted with
probability

.. math::

   P_{\mathrm{acc}} = \frac{\sigma \, v_{\mathrm{rel}}}
                           {(\sigma v_{\mathrm{rel}})_{\max}} .

Because the acceptance probability is exact up to the adaptive upper
bound, the overall procedure recovers the canonical DSMC collision rate
without requiring the actual value of
:math:`(\sigma v_{\mathrm{rel}})_{\max}` to be known *a priori*.

Cross-section convention
------------------------

dmsAIR adopts a purely **geometric** reference cross section
:math:`\sigma = \pi b_{\max}^2`, where :math:`b_{\max}` is the cut-off
impact parameter of the QCT trajectory. All physics enters through the
outcome of the trajectory itself (inelastic / exchange / dissociation); no
empirical model (TCE, VHS, Arrhenius) is invoked. This is what
distinguishes DMS from conventional DSMC and is why a single infrastructure
can treat any reactive system without retuning [SchwartzentruberEtAl2017]_.

Parallel implementation
-----------------------

Per time step, all accepted pairs are pre-selected, their QCT trajectories
are evaluated in parallel across MPI ranks, and the post-collision updates
are applied in a synchronised second pass. The scheme scales cleanly
because each rank processes a disjoint subset of the pair queue; the
collision-result buffer is ``MPI_Allreduce``-combined before being walked
by every rank identically, ensuring consistent particle states across
processes.

Selecting the cut-off impact parameter
--------------------------------------

The choice of :math:`b_{\max}` is one of the very few physical
calibrations required by DMS, but it is **not** a free parameter. An
under-resolved :math:`b_{\max}` truncates the reactive tail; an
over-resolved value wastes an enormous number of trajectories on
trivially unreactive (large-:math:`b`) encounters and eventually
over-resolves the flow field.

dmsAIR ships a companion binary, ``dmsAIR_ScatteringMap``, that implements
the calibration metric proposed by the HERMES Aerospace group. The idea
is to sweep the full :math:`(b, E_{\mathrm{rel}})` plane and measure the
ensemble-averaged magnitude of the centre-of-mass deflection angle
:math:`\langle |\chi| \rangle_{\mathrm{tot}}`, summed over every possible
reactive and non-reactive outcome. The outer boundary of the interacting
region is then located by the iso-line
:math:`\langle |\chi| \rangle_{\mathrm{tot}} = 1^\circ`, beyond which a
collision can be considered dynamically inert to within machine precision.

Two operational criteria follow from this map:

1. **Power-law envelope (thermal bath).** For a given collisional system,
   the :math:`\chi = 1^\circ` contour can typically be fitted by a
   power law

   .. math::

      b_{\max}(E_{\mathrm{rel}}) \approx a \, E_{\mathrm{rel}}^{\, b} ,

   reflecting the Langevin-capture scaling of a long-range attractive
   tail. Choosing :math:`b_{\max}` as the upper envelope of this fit over
   the relevant range of collision energies provides the most
   energy-efficient sampling.

2. **Zero-energy limit (post-shock / expansion flows).** For highly
   non-equilibrium conditions where a significant fraction of the
   translational distribution sits close to :math:`E_{\mathrm{rel}} \to 0`,
   the power-law envelope diverges. In that regime, the more conservative
   criterion is to choose :math:`b_{\max}` such that the
   :math:`\chi = 1^\circ` iso-contour intersects the
   :math:`E_{\mathrm{rel}} = 0` axis — i.e. no reactive or inelastic
   events are truncated at vanishing relative energy.

The two criteria converge at high :math:`E_{\mathrm{rel}}`; at low
:math:`E_{\mathrm{rel}}` the second is the safer choice and is the
default recipe adopted for all production cases distributed with dmsAIR.

See :doc:`/examples/scattering_map` for the full calibration workflow and
the post-processing scripts that generate the power-law fits.
