Changelog
=========

Rev 0.1 (2026-04)
-----------------

**Heteronuclear exchange quantisation (breaking fix)**

- Fixed ``MolState%iPair = 1`` hard-coding in ``src/DSMC/DMS_Collision_Class.F90``:
  exchange products are now quantised against the correct product diatomic
  potential (CN for arr=2, CO for arr=3), not the target's.
- Consequence: **any heteronuclear 3-body system** (NO+C, N2+O, O2+N, etc.)
  previously silently discarded one of its two exchange channels. The fix
  restores full per-channel rate-coefficient tracking.

**Per-channel exchange filter**

- New input keyword family: ``Allow Exchange Arr N = yes/no`` for
  N ∈ {2..6}. Lets the user isolate a single reaction channel for physics
  studies (``exchange1`` = CN+O only, ``exchange2`` = CO+N only).

**Measurement bounds fix**

- Declared ``pair_N_exch_by_arr`` and ``pair_N_diss_ID`` as ``dimension(:, 2:)``
  in ``src/Measurement/Measurement_Class.F90`` so the subroutine-local lower
  bound matches the caller's allocation ``(1:NCP, 2:6)``. Without this fix
  one slot was out of bounds and ``k_Ex_arr(6)`` returned garbage.

**CNO run tree restructured**

- ``exchange`` and ``exchange+dissociation`` folders replaced by
  ``exchange1`` / ``exchange2`` / ``exchange1+dissociation`` /
  ``exchange2+dissociation``. 270 case directories across 3 PESs, 3
  subsystems, 6 regimes, 5 temperatures.

**Documentation site**

- New Sphinx + sphinx_rtd_theme documentation, matching the PLATO docs
  layout. Source in ``docs/``, deployed to ``gh-pages``.

Earlier history
---------------

Pre-0.1 development notes are kept in ``docs/Reports/Development_Log.md``
(not part of the published documentation). Major milestones:

- Core Fortran port of Torres-Schwartzentruber DMS to the CoarseAIR stack.
- Strategy (c) persistent phase-space propagation implemented.
- MPI-parallel NTC pair processing.
- 4-body support (H4, extendable to N4/O4).
- ScatteringMap and IntegratorStudy companion binaries.
