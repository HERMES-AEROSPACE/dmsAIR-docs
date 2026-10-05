Regression Tests
================

dmsAIR ships a golden-output regression suite that must stay green before
any change to the collision, integration, quantisation, or measurement
code paths is merged.

Two flavours of test live side-by-side:

* **App-level tests** — run a real binary (``dmsAIR_ScatteringMap``,
  ``dmsAIR_IntegratorStudy``, or ``dmsAIR_HeatBath``) on a small input
  with a fixed RNG seed and bit-compare a chosen output file.
* **Unit tests** — run a dedicated driver ``dmsAIR_UnitTests`` that
  exercises elemental Fortran helpers (RNG seeding, particle scatter,
  Maxwell-Boltzmann velocity sampling) with deterministic inputs and
  bit-compares the printed results.

Running
-------

.. code-block:: bash

   make regression

This compiles ``dmsAIR_ScatteringMap``, ``dmsAIR_IntegratorStudy``, and
``dmsAIR_UnitTests``, then iterates over every directory under
``tests/regression/cases/`` and diffs each case's output against the
checked-in ``golden.dat``.

A clean run prints, e.g.::

  -- running intstudy_3body_H3
  [ OK ]  intstudy_3body_H3   (2 lines match, text)
  -- running scatmap_3body_CNO
  [ OK ]  scatmap_3body_CNO   (8 rows × 24 cols match)
  -- running scatmap_4body_H4
  [ OK ]  scatmap_4body_H4    (6 rows × 24 cols match)
  -- running unittest_core
  [ OK ]  unittest_core       (15 lines match, text)

  === Regression summary: 4 passed, 0 failed ===

Test inventory
--------------

App-level cases
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - Name
     - What it exercises
   * - ``intstudy_3body_H3``
     - ``dmsAIR_IntegratorStudy`` on H3 with both VV and BS integrators.
       Catches drift in the energy-conservation columns
       (``mean_|dH|_Ha``, ``mean_|dH|/e_in``, ``mean_|dH|/e_out``).
       Wall-time column is stripped before comparison.
   * - ``scatmap_3body_CNO``
     - ``dmsAIR_ScatteringMap`` on CNO / NO+C — 3-body arrangement
       detection, per-channel χ(b, E) accumulation, RPI peak
       classification of dissociation as direct vs. indirect.
   * - ``scatmap_4body_H4``
     - ``dmsAIR_ScatteringMap`` on H4 — 4-body code path including
       double-dissociation event detection (``arr=-2``) and the
       homonuclear-product update branch.

All three app-level cases run with ``rng_seed = 42`` for bit-exact
reproducibility.

Unit tests (``unittest_core``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A single bundle that runs 15 elemental-function tests in a few
milliseconds and writes one output line per test. Bundle organised by
the module under test:

**RNG foundations** — every other test depends on the gfortran PRNG
behaving deterministically under fixed seeds. If any of these drift,
treat the suite as untrusted until investigated.

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - Test
     - Property
     - Tolerance
   * - ``rng_determinism``
     - Seed=42, 1000 draws → bit-exact ``(sum, min, max, first, last)``
     - bit-exact (canary)
   * - ``rng_repeatability``
     - Re-seeding with the same value gives an identical stream
     - exact zero diff
   * - ``rng_seed_isolation``
     - seed=A vs seed=B → different streams (``max_diff > 1e-6``)
     - sentinel

**``Particle_Class :: Elastic_Scatter``** — hard-sphere isotropic
scattering. Tests cover both the analytical conservation laws and the
short-circuit edge case.

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - Test
     - Property
     - Tolerance
   * - ``elastic_scatter``
     - Energy + linear momentum conserved
     - rel < 1e-12
   * - ``elastic_zero_g``
     - ``g_rel < 1e-30`` short-circuit leaves velocities frozen
     - exact zero

**``Particle_Class :: Inelastic_Scatter``** — energy budget for
internal-energy exchange:
``E_rel_new = E_rel_old + Δ_Eint`` with isotropic re-direction of the
relative-velocity vector.

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - Test
     - Property
     - Tolerance
   * - ``inelastic_scatter``
     - Total ΔKE = Δ_Eint, momentum conserved, ΔE_rel = Δ_Eint
     - rel < 1e-12
   * - ``inelastic_forbidden``
     - Energetically forbidden (Δ_Eint < −E_rel_old) returns unchanged
     - exact zero
   * - ``inelastic_release_grows``
     - Δ_Eint = +2·E_rel → E_rel grows by factor 3 exactly
     - rel < 1e-12
   * - ``inelastic_absorb_shrinks``
     - Δ_Eint = −0.5·E_rel → E_rel halves exactly
     - rel < 1e-12
   * - ``inelastic_zero_delta``
     - Δ_Eint = 0 redirects \|g\| isotropically without changing E_rel
     - rel < 1e-12

**``Particle_Class :: Resample_CoM_Velocity``** — Box-Muller-derived
Maxwell–Boltzmann sampler. Tests cover safety, accuracy, isotropy, and
equipartition scaling laws.

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - Test
     - Property
     - Tolerance
   * - ``resample_zero_mass``
     - Particle with ``Mass = 0`` zeros velocity (no NaN, no overflow)
     - exact zero
   * - ``resample_kT``
     - 50000 samples at T=20000K → ``<½mv²> = 1.5·k_B·T``
     - rel < 5%
   * - ``resample_isotropy``
     - ``<v_x²> = <v_y²> = <v_z²>`` at 50000 samples
     - rel < 5%
   * - ``resample_T_scaling``
     - Same RNG seed: KE(T₂) / KE(T₁) = T₂ / T₁ exactly
     - rel < 5%
   * - ``resample_mass_dep``
     - Equipartition: <KE> independent of mass; ⟨v²⟩ ∝ 1/m
     - rel < 5%

**Per-species partition functions ``Z(T)``** — pins the levels database
itself, not just the formulas operating on it. The test reads each
species' ``levels_<sp>.inp`` directly (same files the production apps
load at runtime) and computes
``Z(T) = Σᵢ (2 jᵢ + 1) · exp(-(Eᵢ - E_min) / k_B T)``.
Any change to the eint values, line count, or level set in a CoarseAIR
DB regen surfaces here BEFORE production output starts drifting.

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - Test
     - Property
     - Tolerance
   * - ``partition_NO_T1000``
     - NO at T=1000 K: prints ``nlev`` + ``Z(T)`` to 16 sig figs
     - bit-exact
   * - ``partition_NO_T20000``
     - NO at T=20000 K
     - bit-exact
   * - ``partition_H2_T1000``
     - H2 at T=1000 K
     - bit-exact
   * - ``partition_H2_T20000``
     - H2 at T=20000 K
     - bit-exact

The levels files are pulled into the test scratch dir via symlinks
in ``tests/regression/cases/unittest_core/`` pointing at the canonical
copies under ``scatmap_3body_CNO/`` (NO) and ``scatmap_4body_H4/`` (H2).
The runner's ``cp -rL`` dereferences the symlinks at copy time, so the
test reads real file content. To add another species (e.g. CN, CO, N2,
O2): drop a symlink ``levels_<sp>.inp`` into ``unittest_core/`` and add
two ``call test_partition_function('<sp>', 'levels_<sp>.inp', T)``
calls (one cold, one hot) in ``app/UnitTests/UnitTests.F90``, then
``make bless-regression``.

Re-blessing
-----------

If you've intentionally changed physics and need to update the baselines:

.. code-block:: bash

   make bless-regression

This re-runs every case and overwrites every ``golden.dat`` with the
current output. **Inspect the diff carefully before committing** — this
is how silent regressions creep in.

Adding a new app-level test
---------------------------

1. Create ``tests/regression/cases/<tag>/`` with your inputs:

   * ``scatmap_*`` cases need ``dmsAIR.inp`` + ``scatmap.inp`` + level
     files.
   * ``intstudy_*`` cases need ``dmsAIR.inp`` + ``integrator_study.inp``
     + level files.
   * ``heatbath_*`` cases need ``dmsAIR.inp`` + level files; the runner
     compares ``Output/pop.csv`` (deterministic when ``RNG Seed`` is
     set).

2. Run ``make bless-regression`` — the runner picks up the new case
   automatically and writes ``golden.dat``.

3. Run ``make regression`` and confirm the new case is green.

Adding a new unit test
----------------------

Edit ``app/UnitTests/UnitTests.F90``. The boilerplate is::

   call test_my_function()    ! add to the body
   ...
   Subroutine test_my_function()
     ! ... do work, fix RNG seed first if you draw randomness
     write(u_out,'(A,1X,ES14.7,1X,A)') 'my_function ', residual, &
       pass_str(residual < tolerance)
   End Subroutine

then ``make bless-regression``. Each line emitted to ``u_out``
becomes one test in the bundle's ``golden.dat``.

Tests deliberately not yet in the suite
---------------------------------------

The following helpers are tested only indirectly via the app-level
cases because they live in unit-test-unfriendly scope (program
``contains`` block, or private to a module). Promote them to
``public ::`` of a small utility module if a focused test becomes
useful:

* ``Find_Species_ID_By_Name`` (in ``HeatBath.F90`` ``contains``)
* ``Find_CA_State`` (in ``HeatBath.F90`` ``contains``)
* ``Tint_From_Eint`` / ``Mean_Eint_At_T`` (private in ``Measurement_Class``)
* ``Pair_to_Atoms_DMS`` / ``Random_Rotation_Matrix`` (private in
  ``DMS_Collision_Class``)
