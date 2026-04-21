Quasi-Classical Trajectories
============================

Each collision in dmsAIR is resolved by a full QCT integration on the
selected PES. The trajectory machinery is inherited from CoarseAIR; dmsAIR
adds the driver layer that initialises the approach geometry, invokes the
integrator, and extracts the post-collision arrangement.

Approach geometry
-----------------

For a 3-body collision A + BC with specific relative energy :math:`E_{\rm rel}`
and impact parameter :math:`b`:

1. The diatom's bond-frame coordinates are drawn from its current ``(v, j)``
   (or from persistent phase space under strategy (c)) and rotated isotropically.
2. CoarseAIR's ``ComputeCoordinatesVelocities`` places the target at the
   origin and the projectile at a separation ``Dinit`` along the approach
   axis with the prescribed :math:`b` offset.
3. The initial Hamiltonian is evaluated to establish the reference energy
   used by the ``HamAbsTol`` filter at convergence.

Integration
-----------

Five integrators are available via the ``Integrator`` keyword. See
:doc:`integrators` for comparative benchmarks.

Termination
-----------

The trajectory is declared converged when either:

- any atom-pair separation exceeds :math:`R_{\max}` (products well separated);
- the trajectory time exceeds :math:`t_{\max}`.

Arrangement classification
--------------------------

At convergence the arrangement is inferred from the final atom-pair distances.
For a 3-body system (``NAtoms = 3``):

- ``arr = 0`` — original bond (pair 1) still shortest → **inelastic**
- ``arr = 2`` — pair (atom 1, atom 3) shortest → **exchange product 1**
- ``arr = 3`` — pair (atom 2, atom 3) shortest → **exchange product 2**
- ``arr = -1`` — all pairs separated → **dissociation**

For 4-body systems arrangements 3..6 cover the four cross pairs; ``arr = -2``
is reserved for double dissociation.

.. seealso::

   :doc:`reactive_channels` for how heteronuclear exchange products (CN vs
   CO in NO+C) are quantised against their own diatomic potentials — a fix
   added in Rev 0.1 that was required for any non-homonuclear system.
