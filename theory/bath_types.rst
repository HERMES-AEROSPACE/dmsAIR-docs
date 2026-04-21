Heat Bath Types
===============

dmsAIR supports two canonical 0-D bath configurations, selected via the
``Bath Type`` keyword. These mirror the two reactor flavours studied
throughout the DMS literature — the isothermal (imposed-temperature)
bath that maps onto Master-Equation (ME) reactors, and the adiabatic
post-shock bath used in e.g. [Valentini2016]_ and
[Torres2024Adiabatic]_.

Isothermal bath
---------------

``Bath Type = isothermal`` (default).

The translational temperature :math:`T_{\mathrm{tr}}` is **imposed**: at
every time step each particle's centre-of-mass velocity is resampled from
a Maxwell–Boltzmann distribution at :math:`T_{\mathrm{tr}}`. The internal
temperature :math:`T_{\mathrm{int}}`, in contrast, evolves freely via
collisional energy exchange from the initial value
(``Internal Temperature``) toward the equilibrium set by
:math:`T_{\mathrm{tr}}`.

This is the 0-D analogue of an infinite translational reservoir at
:math:`T_{\mathrm{tr}}` coupled to a fixed inventory of internal-state
population. It matches PLATO's ``Box_ODE`` reactor convention, so DMS-vs-ME
comparisons are apples-to-apples.

Adiabatic bath
--------------

``Bath Type = adiabatic``.

No velocity resampling — the total energy of the particle ensemble is
conserved to integrator accuracy. Both :math:`T_{\mathrm{tr}}` and
:math:`T_{\mathrm{int}}` evolve and asymptote to a common equilibrium
temperature determined by the initial conditions (energy conservation +
particle-number conservation). This is the relevant configuration for
post-shock relaxation studies where the bath temperature is not externally
maintained [Torres2024Adiabatic]_.

Density and pressure convention
-------------------------------

The initial ``Pressure`` sets the total number density via

.. math::

   n = \frac{P}{k_B \, T_{\mathrm{int}}} ,

i.e. using :math:`T_{\mathrm{int}}` (not :math:`T_{\mathrm{tr}}`). This is
a deliberate choice that matches PLATO's reactor-bath conventions and
preserves the initial internal-state distribution without perturbation.
After initialisation, :math:`n` is held fixed (isothermal) or evolves via
energy/particle conservation (adiabatic).

Isothermal velocity resampling
------------------------------

In the isothermal bath, the per-step Maxwellian resampling acts on the
*translational* degrees of freedom only. The internal state
:math:`(v, j)` and the bond phase of each molecule are **not** touched
between collisions — they evolve exclusively through the QCT collision
events. This decoupling is what preserves the non-Boltzmann structure of
the internal distribution during rapid relaxation, and is a direct
implementation of the DMS isothermal-bath prescription described in
[Torres2024]_ (Appendix A.6).
