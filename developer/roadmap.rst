Development Roadmap
===================

Near-term
---------

- **CNO sweep**: complete the 270-case production run (3 PES × 3 subsys × 6
  regimes × 5 T), validate against PLATO ME, and publish the rate
  coefficient tables.
- **Nuclear-spin statistics for exchange channels**: the current filter
  only fires for inelastic homonuclear collisions; extend to exchange
  outcomes once the heteronuclear arrangement is fully tracked.
- **Proper exchange bath bookkeeping**: for heteronuclear exchange, the NO
  reactant particle is currently left in its pre-collision state (good
  approximation for low exchange rates). A future "remove and replenish
  from the Ttr reservoir" pathway would match the ME first-order kinetics
  more precisely.

Mid-term
--------

- **4-body CNO systems** (N\ :sub:`2` + O, O\ :sub:`2` + N, etc.) via the
  existing 4-body code path — the arrangement-detection fix opens this up.
- **State-resolved rate-coefficient output**: save ``k(v, j → v', j')`` per
  channel, not just ensemble-averaged rates. The ``kernel_count`` array is
  already in place; needs a post-processor.
- **Adiabatic bath validation** against shock-tube data.

Long-term
---------

- **Coupling to flow solvers** (DSMC and CFD). DMS-derived state-resolved
  rates are the natural input to multi-temperature CFD models; automated
  export to PLATO's mixture files would close the loop.
- **GPU trajectory offload** for the QCT inner loop. CoarseAIR's PES
  evaluation is the dominant cost; an OpenMP-target or CUDA port of the
  PES calls could yield 5-10× speed-up per rank.
- **Machine-learned PESs** — plug in BNN/GP surrogates for trajectory
  bulk evaluations with uncertainty quantification.

Completed
---------

- Heteronuclear exchange quantisation (Rev 0.1)
- Per-arrangement exchange filter (``Allow Exchange Arr N``)
- 4-body support (H4, double-dissociation handling)
- Strategy (c) persistent phase-space propagation
- MPI-parallel NTC pair processing
- Sphinx documentation site (this site)
