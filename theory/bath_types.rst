Heat Bath Types
===============

dmsAIR supports two bath configurations, chosen via the ``Bath Type``
keyword.

Isothermal bath
---------------

``Bath Type = isothermal`` (default).

- The translational temperature :math:`T_{\mathrm{tr}}` is **imposed**: at
  every time step each particle's CoM velocity is resampled from a
  Maxwell–Boltzmann distribution at the prescribed :math:`T_{\mathrm{tr}}`.
- The internal temperature :math:`T_{\mathrm{int}}` evolves freely via
  collisional energy exchange from an initial value (``Internal Temperature``)
  toward the equilibrium set by :math:`T_{\mathrm{tr}}`.
- Matches the standard Master-Equation (ME) bath used by PLATO, making
  DMS-vs-ME comparisons apples-to-apples.

Adiabatic bath
--------------

``Bath Type = adiabatic``.

- No velocity resampling — the total energy is conserved (to integrator
  accuracy).
- :math:`T_{\mathrm{tr}}` and :math:`T_{\mathrm{int}}` both evolve and
  asymptote to a common equilibrium temperature determined by the initial
  conditions.
- Useful for pure relaxation studies where the imposed-temperature bath is
  an artefact.

.. note::

   Initial ``Pressure`` sets the total number density via
   :math:`n = P / (k_B T_{\mathrm{int}})`. This uses :math:`T_{\mathrm{int}}`,
   **not** :math:`T_{\mathrm{tr}}` — a deliberate choice that matches
   PLATO's reactor-bath conventions and preserves the initial internal-state
   distribution without perturbation.
