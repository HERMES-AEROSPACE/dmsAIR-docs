Direct Molecular Simulation
===========================

dmsAIR implements the Direct Molecular Simulation (DMS) approach of Koura
(1997), extended by Grover & Schwartzentruber (2019) and Torres &
Schwartzentruber (2024).

Core loop
---------

At each time step the algorithm:

1. **Samples collision pairs** stochastically via the No-Time-Counter (NTC)
   method — see :doc:`ntc`.
2. **Resolves each collision** by running a full QCT trajectory on an
   *ab initio* PES — see :doc:`qct`.
3. **Classifies the post-collision arrangement** (inelastic, exchange,
   single/double dissociation) — see :doc:`reactive_channels`.
4. **Quantises the surviving molecule(s)** back to rovibrational states
   via CoarseAIR's semiclassical action integrals.
5. **Applies the isothermal or adiabatic bath update** (Torres Appendix A)
   — see :doc:`bath_types`.

Strategy (c) — persistent atomic phase space
--------------------------------------------

Instead of regenerating atomic coordinates from the quantised ``(v, j)``
before every collision, dmsAIR stores the full atomic ``(x, v)`` between
collisions and re-samples only the orientation isotropically. This is
Grover & Schwartzentruber's strategy (c) — it avoids the "quantisation
round-trip" energy drift that plagues strategies (a) and (b).

Macroscopic observables
-----------------------

Temperature, pressure, composition, and rate coefficients emerge from the
ensemble — no empirical models required. Rate coefficients are measured as

.. math::

   k_{\mathrm{ch}} = \langle v_{\mathrm{rel}} \rangle \cdot \sigma \cdot
                     \frac{N_{\mathrm{ch}}}{N_{\mathrm{att}}}

where :math:`\sigma = \pi b_{\max}^2`, :math:`N_{\mathrm{ch}}` is the count
of events in channel *ch*, and :math:`N_{\mathrm{att}}` is the total number
of NTC-accepted attempts in the measurement window.
