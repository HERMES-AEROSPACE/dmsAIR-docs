Direct Molecular Simulation
===========================

Motivation
----------

Hypersonic re-entry and high-enthalpy flows drive molecular gases far from
thermodynamic equilibrium. Translational, rotational, vibrational and
electronic modes relax on overlapping time-scales and reactive channels
(exchange, dissociation) open up. Classical rate-based chemistry — built on
a Boltzmann assumption for the internal-state distribution — breaks down
precisely in the regime that matters for vehicle design.

State-to-state (StS) master equations address this by integrating the full
set of rovibrational-level rate equations against *ab initio* rate
coefficients. They are accurate but expensive to build (requiring a
pre-computed rate-coefficient database of size :math:`\sim N_{\mathrm{lev}}^2`
per collision pair) and confined to 0-D or quasi-1-D reactor geometries.

A complementary approach — **direct molecular simulation (DMS)** — embeds
the trajectory calculation itself inside a stochastic particle framework.

Historical note
---------------

DMS was pioneered by Koura in the late 1990s [Koura1997]_. The method was
historically recognised under the terminology *classical-trajectory
calculation direct simulation Monte Carlo* (CTC-DSMC). The original
CTC-DSMC was primarily designed to address non-reactive gas flow and the
study of non-reactive nitrogen shock flows. The method was later extended
to reactive gas flows by Fujita [Fujita2002]_, who renamed it
*quasi-classical trajectory direct simulation Monte Carlo* (QCT-DSMC). The
method was further improved with the development of *ab initio* potential
energy surfaces (PES) and has since been deployed for the study of
energy-transfer and dissociation processes in a large number of
collisional systems [Valentini2016]_ [SchwartzentruberEtAl2017]_
[GroverSchwartzentruber2019]_ [Torres2024]_. In the remaining part of this
documentation, the authors adhere to the now-commonly-accepted terminology,
i.e. **DMS**.

Conceptual definition
---------------------

The DMS method is an *ab initio* variant of the standard direct simulation
Monte Carlo (DSMC) framework [Bird1994]_, in that it embeds
first-principles trajectory calculations within the DSMC algorithm. In
essence, DMS computes molecular trajectories *on-the-fly* as part of the
simulation of an evolving gas. Rather than resolving all possible energy
transitions, DMS selectively samples the most dominant transitions
occurring with non-negligible frequency under the conditions of interest.
Although computationally demanding, DMS has become the method of choice for
the study of four-body reactive systems and multi-component gas mixtures
where StS rate databases would be prohibitive to pre-compute. Recent
applications of DMS to full 3-D hypersonic flows [ValentiniDoubleCone]_
[ValentiniBluntWedge]_ and comparative benchmarks of DMS against empirical
DSMC chemistry models [Grover2025]_ further support its status as the
reference method for ab-initio-driven nonequilibrium chemistry.

The dmsAIR loop
---------------

At each time step dmsAIR performs the following operations:

1. **NTC pair sampling.** Candidate collision pairs are drawn stochastically
   via Bird's No-Time-Counter algorithm, with an acceptance probability
   :math:`P_{\mathrm{acc}} = \sigma v_{\mathrm{rel}} / (\sigma v_{\mathrm{rel}})_{\max}`.
   See :doc:`ntc`.
2. **QCT trajectory.** Each accepted pair is resolved by integrating
   Hamilton's equations on the PES using CoarseAIR's trajectory machinery.
   See :doc:`qct`.
3. **Arrangement classification.** At convergence, the surviving bond(s)
   identify the product arrangement — inelastic, exchange, single
   dissociation, or (for 4-body) double dissociation. See
   :doc:`reactive_channels`.
4. **Quantisation.** The surviving molecule's coordinates are passed to
   CoarseAIR's ``FindState`` routine, which performs a semiclassical action
   integral over the outcome's diatomic potential to recover the
   post-collision :math:`(v', j')`.
5. **Bath update.** The target particle's quantum numbers and phase-space
   state are updated (or, for heteronuclear exchange, preserved), and the
   translational CoM velocity is (re)sampled according to the bath type.
   See :doc:`bath_types`.
6. **Ensemble observables.** Translational temperature, internal
   temperature, pressure, mole fractions and rate coefficients emerge from
   the particle ensemble — no empirical models required.

Strategy (c) — persistent phase-space propagation
--------------------------------------------------

The dmsAIR implementation follows the *strategy (c)* of
[GroverSchwartzentruber2019]_: each molecular particle carries its full
atomic :math:`(x, v)` between collisions rather than being regenerated from
the quantum numbers :math:`(v, j)` before every event. Only an isotropic
random rotation is applied at the start of each collision to de-bias the
orientation. Strategy (c) avoids the "quantisation round-trip" error that
plagues strategies (a) and (b), where a coordinate → :math:`(v,j)` →
coordinate cycle introduces a small but systematic energy drift. The
ensemble therefore remains faithful to the microscopic dynamics over the
full duration of a heat-bath relaxation.

Macroscopic observables
-----------------------

Rate coefficients for each reactive channel are measured directly from the
event counts accumulated over the output interval:

.. math::

   k_{\mathrm{ch}} = \langle v_{\mathrm{rel}} \rangle \, \pi b_{\max}^2 \,
                     \frac{N_{\mathrm{ch}}}{N_{\mathrm{att}}}

where :math:`b_{\max}` is the cut-off impact parameter,
:math:`N_{\mathrm{ch}}` is the number of events of type *ch*
(inelastic / exchange / dissociation) and :math:`N_{\mathrm{att}}` is the
total number of NTC-accepted attempts in the same window.
