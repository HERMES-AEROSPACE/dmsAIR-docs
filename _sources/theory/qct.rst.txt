Quasi-Classical Trajectories
============================

Each collision in dmsAIR is resolved by a full quasi-classical trajectory
(QCT) integration on the selected potential energy surface. The
trajectory machinery is inherited from CoarseAIR; dmsAIR adds the driver
layer that sets up the approach geometry, invokes the integrator, and
extracts the post-collision arrangement.

Hamiltonian formulation
-----------------------

For an :math:`N`-atom collision system, the dynamical state is the set of
atomic positions and momenta :math:`\{q_i, p_i\}_{i=1..N}`. The
non-relativistic Hamiltonian is

.. math::

   H = \sum_{i=1}^{N} \frac{p_i^2}{2 m_i} + V(q_1, \ldots, q_N) ,

where :math:`V` is the *ab initio* PES. The numerical integration of this
Hamiltonian follows the standard molecular-dynamics machinery reviewed in
[Frenkel]_. CoarseAIR works internally in Jacobi coordinates for the
three-body case and in atom-centred Cartesian coordinates for four-body.
The PES is evaluated per step by CoarseAIR's ``potcl`` routine, which
returns both :math:`V` and the atomic forces
:math:`F_i = -\partial V / \partial q_i`. dmsAIR itself does not touch the
PES — it treats it as an opaque oracle.

Initial-state sampling
----------------------

For a three-body event A + BC, the diatom's rovibrational state
:math:`(v, j)` is drawn from the bath's current population. Two strategies
coexist in the literature [GroverSchwartzentruber2019]_ and dmsAIR
implements the most accurate one: *strategy (c)*, in which the molecule
carries a persistent :math:`(q, \dot q)` between collisions and only the
orientation is re-randomised before each new event. This choice avoids
the rapid energy drift introduced by re-quantising coordinates at every
collision.

The projectile atom is placed at a separation :math:`D_{\mathrm{init}}`
along an axis offset by the impact parameter :math:`b` from the diatom's
centre of mass. The relative-velocity magnitude is fixed by the NTC-drawn
translational energy,

.. math::

   g_{\mathrm{rel}} = \sqrt{2 E_{\mathrm{rel}} / \mu} ,

where :math:`\mu` is the reduced mass of the colliding partners. For
four-body collisions (AB + CD) the projectile diatom is generated from
its own :math:`(v_2, j_2)` and placed symmetrically with respect to the
target.

Integration and termination
---------------------------

Hamilton's equations

.. math::

   \dot q_i = \frac{\partial H}{\partial p_i} , \qquad
   \dot p_i = -\frac{\partial H}{\partial q_i} ,

are integrated from :math:`t = 0` until convergence. A trajectory is
declared converged when **any** atom-pair separation exceeds
:math:`R_{\max}` (meaning at least one product has escaped) or the
wall-time exceeds :math:`t_{\max}`. Trajectories reaching
:math:`t_{\max}` without separating correspond to long-lived complexes;
they are flagged as non-converged and excluded from the rate-coefficient
statistics.

See :doc:`integrators` for the available Bulirsch–Stoer and
Velocity-Verlet integrators.

Arrangement classification
--------------------------

At convergence, dmsAIR inspects the final inter-atomic distances and
identifies the pair with the smallest :math:`r` (or the set of such pairs
for four-body). This yields the arrangement code used downstream; see
:doc:`reactive_channels`.

Semiclassical quantisation
--------------------------

At convergence, the surviving diatomic product is characterised by its
relative position :math:`\mathbf{r}` and conjugate momentum
:math:`\mathbf{p}`. Its internal (vibrational + rotational) energy is

.. math::

   E = \frac{p_r^2}{2 \mu} + \frac{L^2}{2 \mu r^2} + V(r) ,

where :math:`p_r` is the radial momentum, :math:`L = |\mathbf{r} \times
\mathbf{p}|` is the magnitude of the rotational angular momentum, and
:math:`V(r)` is the diatomic potential associated with the surviving
pair.

The product's coordinates are passed to CoarseAIR's ``FindState`` routine,
which recovers the semiclassical quantum numbers :math:`(v', j')` by
inverting the Bohr–Sommerfeld quantisation conditions:

**Rotational quantum number.** The conserved classical angular momentum
is mapped onto an integer :math:`j'` via

.. math::

   j' + \tfrac{1}{2} = \frac{L}{\hbar} ,

so that :math:`j'(j'+1) \hbar^2 \to L^2` in the correspondence limit.
Equivalently, :math:`j' = \lfloor L/\hbar - \tfrac{1}{2} \rfloor` rounded
to the nearest non-negative integer. Because :math:`L` is constant along
the asymptotic product trajectory, evaluating it at the end of the
integration is unambiguous.

**Vibrational quantum number.** Once :math:`j'` is fixed, :math:`v'` is
obtained from the radial action integral

.. math::

   v' + \tfrac{1}{2} =
       \frac{1}{\pi \hbar}
       \oint p_r \, dr
       = \frac{1}{\pi \hbar}
       \oint \sqrt{ 2 \mu \bigl( E - V_{\mathrm{eff}}(r) \bigr) } \; dr ,

evaluated between the inner and outer classical turning points of the
effective radial potential

.. math::

   V_{\mathrm{eff}}(r) = V(r) + \frac{\hbar^2 j'(j'+1)}{2 \mu r^2} .

The turning points are located numerically by CoarseAIR's ``TurningPoint``
routine, and the action integral is evaluated by Gauss-Legendre quadrature
with ``nquad`` nodes (a run-time input). The final
:math:`(v', j')` is then rounded to the nearest valid bound state and
matched against the levels database to recover the quantised internal
energy :math:`\varepsilon_{v' j'}`.

For heteronuclear exchange in a polyatomic system (e.g. NO + C → CN + O on
the 4A\ :sub:`2` surface), the product molecule must be quantised against
**its own** diatomic potential — the quantum numbers are obtained from
the CN (or CO) potential, not the original NO potential. dmsAIR selects
the correct pair's potential (``MolState%iPair = max(arrangement, 1)``)
before calling ``FindState``.

Energy-conservation diagnostic
------------------------------

The drift :math:`|\Delta H| = |H(t_{\mathrm{end}}) - H(0)|` is recorded
for every converged trajectory. Following the SPARTA-QCT convention
adopted in [Torres2024]_, all converged trajectories are accepted in the
statistics regardless of :math:`|\Delta H|`; the drift is reported as a
diagnostic only.
