Validation
==========

dmsAIR is validated against Master-Equation reference solutions from PLATO
for all production systems.

H\ :sub:`2`\  + H (3-body)
--------------------------

Three temperatures: 5 000, 10 000, 20 000 K; no-dissociation and
with-dissociation regimes.

- Internal-energy relaxation ⟨E\ :sub:`int`\ ⟩(t): within 3 % of ME at
  20 000 K, within 10 % at 10 000 K (slower convergence at lower
  Ttr/Tint mismatch).
- QSS dissociation rate ``k_DD``: matches ME within statistical noise
  once N\ :sub:`p` ≥ 10\ :sup:`5`\ .

Reference ME curves stored in ``postprocessing/Reference/<T>K/``.

CNO systems (3-body)
--------------------

Three subsystems × three PESs × six regimes × five temperatures = 270
production cases, compared against PLATO's
``MasterEquationAnalysis/<subsys>/<T>/`` reference set.

- ``Inelastic_4A`` ↔ DMS ``inelastic``
- ``Exchange1`` ↔ DMS ``exchange1`` (CN+O channel)
- ``Exchange2_4S`` ↔ DMS ``exchange2`` (CO+N channel)
- ``Exchange1_Dissociation`` ↔ DMS ``exchange1+dissociation``
- ``Exchange2_4S_Dissociation`` ↔ DMS ``exchange2+dissociation``
- ``DirectDissociation`` ↔ DMS ``directdissociation`` (DMS restricts
  the dissociation channel to direct trajectories — no transient CN
  or CO bound intermediate)
- ``TotalDissociation`` ↔ DMS ``totaldissociation`` (DMS keeps every
  dissociation trajectory, direct and exchange-mediated)

Post-processor: ``postprocessing/Postprocessing/postprocessing.py
--system CNO``.

H\ :sub:`2`\  + H\ :sub:`2`\  (4-body)
---------------------------------------

Inelastic and dissociation regimes at 10 000 and 20 000 K. Used to exercise
the 4-body code path (arrangement codes 0, -1, -2, 3..6); reference ME
not available for all channels, so primary validation is the regression
suite.

Regression test suite
---------------------

``make regression`` runs three golden-output checks:

1. ``intstudy_3body_H3`` — IntegratorStudy on H3 default grid.
2. ``scatmap_3body_CNO`` — ScatteringMap on CNO/NO+C.
3. ``scatmap_4body_H4`` — ScatteringMap on H4.

All three must pass before committing any change to the collision or
integration code path.
