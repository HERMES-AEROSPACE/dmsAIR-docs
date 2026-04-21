Direct Molecular Simulation
===========================

Motivation
----------

Hypersonic vehicles typically enter a planetary atmosphere at near-orbital
or super-orbital velocities. As a vehicle descends into the atmosphere, it
is subject to a severe aerothermodynamic loading and the total energy per
unit mass of the gas crossing the bow shock becomes sufficient to promote
chemical reactions [SchwartzentruberEtAl2017]_. Modelling the chemical
activity at such extreme conditions is essential, as the state of the flow
surrounding the vehicle may strongly alter its aerodynamic performance and
significantly modify the heat transfer to the surface.

Downstream of the shock wave, the translational degree of freedom
equilibrates almost instantaneously, whilst the internal modes
(rotational, vibrational, electronic) relax on comparable time-scales and
dissociative channels become accessible. Under these conditions, the
internal-state distribution departs substantially from a Boltzmann
equilibrium — precisely the regime in which classical multi-temperature
and empirical rate-based models break down [GroverSchwartzentruber2019]_
[Grover2025]_.

State-to-state (StS) master-equation methods address this difficulty by
solving a rate equation for each rovibrational level of the colliding
molecular partners [Macdonald2018]_. Although accurate, the construction
of a full StS kinetic database is extremely demanding. For a typical
diatomic it involves the calculation of :math:`\mathcal{O}(N_{\mathrm{lev}}^2)`
excitation and dissociation rate coefficients from *ab initio*
quasi-classical trajectories, carried out once and for all before the
master equation can even be integrated. Such databases are today tractable
only for a limited set of three-body systems, and become prohibitive for
multi-component mixtures or four-body reactive systems of practical
interest.

A complementary approach for modelling detailed nonequilibrium chemistry
in dilute gases is the **direct molecular simulation (DMS)**.

Historical context
------------------

DMS was pioneered by Koura in the late nineties [Koura1997]_ [Koura2002]_.
The method was historically recognised under the terminology
*classical-trajectory-calculation direct simulation Monte Carlo*
(CTC-DSMC). The original CTC-DSMC was primarily designed to address the
nonreactive rotational relaxation of nitrogen in shock waves and low-density
expansions, using semi-empirical intermolecular potentials
[Koura2002]_. A parallel line of development by Tokumasu and Matsumoto
[TokumasuMatsumoto1999]_ proposed a related *dynamic molecular collision*
(DMC) model in which the collision outcome was sampled from a pre-computed
molecular-dynamics database, rather than obtained on-the-fly — an
intermediate step between empirical DSMC chemistry and fully first-
principles DMS. The CTC-DSMC approach was later extended to vibrating
rotors and reactive gas flows by Fujita [Fujita2002]_, who renamed the
method *quasi-classical-trajectory direct simulation Monte Carlo*
(QCT-DSMC), introducing quantisation of the diatomic vibrational levels
and a proper treatment of exchange and dissociation.

The method was further refined through the development of high-fidelity
*ab initio* potential energy surfaces (PES) and has since been widely
deployed for the study of energy transfer and dissociation in nitrogen
[Valentini2016]_ [Macdonald2018]_, oxygen [GroverSchwartzentruber2019]_
[ManinderO2]_, and multi-component air and astrophysical mixtures
[ValentiniDoubleCone]_ [ValentiniBluntWedge]_ [Torres2024]_
[Torres2024Adiabatic]_. In what follows, the authors adhere to the now
commonly accepted terminology, i.e. **DMS**.

Conceptual definition
---------------------

The DMS method is an *ab initio* variant of the standard direct
simulation Monte Carlo (DSMC) framework [Bird1994]_, in that it embeds
first-principles trajectory calculations within the DSMC algorithm. In
essence, DMS computes molecular trajectories on-the-fly as part of the
simulation of an evolving gas. Rather than resolving all possible energy
transitions, DMS selectively samples the most dominant transitions
occurring with non-negligible frequency under the conditions of interest.
Although computationally demanding, DMS has become the method of choice
for the study of four-body reactive systems and multi-component gas
mixtures where StS rate databases would be prohibitive to pre-compute.

A useful way to contrast DMS with the alternatives is through the nature
of their input data:

- **Multi-temperature / empirical DSMC chemistry.** Input = a small set
  of fitted Arrhenius or phenomenological parameters. Cheap, but confined
  to the regime in which those parameters were calibrated.
- **State-to-state master equation.** Input = a pre-computed kinetic
  database of :math:`k_{i \to j}^{\mathrm{E}}(T)` and
  :math:`k_{i}^{\mathrm{D}}(T)` for every rovibrational transition. Very
  accurate, but restricted to 0-D or quasi-1-D reactor geometries.
- **Direct molecular simulation.** Input = a set of PESs suitable for
  describing the interactions between colliding molecules and atoms, and
  nothing else [Macdonald2018]_. Rate coefficients are measured directly
  from the particle ensemble; no pre-computed kinetic data is required.

Ingredients required by DMS
---------------------------

Because DMS resolves individual collisions through on-the-fly trajectory
calculations, its sole microscopic input is a set of *ab initio*
**potential energy surfaces** describing the interactions between the
atoms that constitute the chemical system of interest. No cross sections,
no rate coefficients and no internal-energy transition tables need to be
pre-computed.

Concretely, the DMS user must provide:

1. A PES for each reactive three- (or four-) body system of interest,
   given either in tabulated form or as an analytical fit. dmsAIR delegates
   all PES evaluations to CoarseAIR, which natively supports a range of
   NASA-Ames, University-of-Minnesota and University-of-California-Irvine
   surfaces.
2. A set of rovibrational level tables :math:`\{v, j, \varepsilon_{vj}\}`
   for each diatomic that may appear as a reactant or as a product of an
   exchange event. These are derived semiclassically from the diatomic
   potential associated with each pair of atoms.
3. A specification of the collisional system (chemical identities, atomic
   masses, nuclear-spin degeneracies, and initial thermodynamic state of
   the bath).

All other quantities — relaxation times, rate coefficients, product
distributions, non-Boltzmann signatures — emerge from the simulation
itself, without any adjustable parameters.

The dmsAIR loop
---------------

At each time step, dmsAIR performs the following operations:

1. **NTC pair sampling.** Candidate collision pairs are drawn stochastically
   via Bird's No-Time-Counter algorithm, with an acceptance probability
   :math:`P_{\mathrm{acc}} = \sigma v_{\mathrm{rel}} / (\sigma v_{\mathrm{rel}})_{\max}`.
   See :doc:`ntc`.
2. **QCT trajectory.** Each accepted pair is resolved by integrating
   Hamilton's equations on the PES. See :doc:`qct`.
3. **Arrangement classification.** At convergence, the surviving bond(s)
   identify the product arrangement — inelastic, exchange, single
   dissociation, or (for four-body systems) double dissociation. See
   :doc:`reactive_channels`.
4. **Quantisation.** The surviving molecule's coordinates are passed to
   CoarseAIR's ``FindState`` routine, which performs a semiclassical
   action integral over the outcome's diatomic potential to recover the
   post-collision :math:`(v', j')`.
5. **Bath update.** The target particle's quantum numbers and phase-space
   state are updated (or, for heteronuclear exchange, preserved), and the
   translational centre-of-mass velocity is (re)sampled according to the
   bath type. See :doc:`bath_types`.
6. **Ensemble observables.** Translational temperature, internal
   temperature, pressure, mole fractions and rate coefficients are
   measured directly from the particle ensemble — no empirical models
   involved.

Strategy (c) — persistent phase-space propagation
--------------------------------------------------

dmsAIR follows the *strategy (c)* formulation of
[GroverSchwartzentruber2019]_: each molecular particle carries its full
atomic :math:`(q, \dot q)` between consecutive collisions rather than
being regenerated from the quantum numbers :math:`(v, j)` at the start of
every event. Only an isotropic random rotation is applied to de-bias the
orientation. This choice avoids the systematic "quantisation round-trip"
energy drift that affects strategies (a) and (b), in which the repeated
coordinate → :math:`(v, j)` → coordinate cycle biases the ensemble over
long relaxation times. Strategy (c) preserves the microscopic dynamics
over the whole duration of a heat-bath relaxation and is the
recommended configuration for every production case distributed with
dmsAIR.

Macroscopic observables
-----------------------

Rate coefficients for every reactive channel are measured directly from
the event counts accumulated over the output interval:

.. math::

   k_{\mathrm{ch}} = \langle v_{\mathrm{rel}} \rangle \, \pi b_{\max}^2 \,
                     \frac{N_{\mathrm{ch}}}{N_{\mathrm{att}}} ,

where :math:`b_{\max}` is the cut-off impact parameter,
:math:`N_{\mathrm{ch}}` is the number of events of type *ch*
(inelastic / exchange / dissociation) and :math:`N_{\mathrm{att}}` is the
total number of NTC-accepted attempts in the same window. Because the
sampled :math:`(b, E_{\mathrm{rel}})` distribution is the correct thermal
distribution set by the NTC acceptance law, this yields the state-specific
*thermal* rate coefficient
:math:`k_{\mathrm{ch}}(T_{\mathrm{tr}}, T_{\mathrm{int}})` without any
further assumption. Close cross-validation against StS master-equation
references at matched bath conditions is used as the primary criterion of
physical consistency [Macdonald2018]_ [GroverSchwartzentruber2019]_.
