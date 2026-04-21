Regression Tests
================

dmsAIR ships a small golden-output regression suite that must pass before
any change to the collision, integration, or quantisation code paths.

Running
-------

.. code-block:: bash

   make regression

This compiles the binaries then runs three cases and diffs the outputs
against baseline files under ``regression/bless/``.

Test cases
----------

+---------------------------+---------------------------------------------------+
| Name                      | What it exercises                                 |
+===========================+===================================================+
| ``intstudy_3body_H3``     | IntegratorStudy on H3 default grid — integrator   |
|                           | energy drift + reaction probability               |
+---------------------------+---------------------------------------------------+
| ``scatmap_3body_CNO``     | ScatteringMap on CNO / NO+C — 3-body arrangement  |
|                           | detection, per-channel chi accumulation           |
+---------------------------+---------------------------------------------------+
| ``scatmap_4body_H4``      | ScatteringMap on H4 — 4-body code path,           |
|                           | double-dissociation classification                |
+---------------------------+---------------------------------------------------+

All three use ``rng_seed = 42`` for bit-exact reproducibility.

Re-blessing
-----------

If you've intentionally changed physics and need to update the baselines:

.. code-block:: bash

   make bless-regression

Inspect the diff carefully before committing the new baseline — this is how
silent regressions creep in.

Adding a new test
-----------------

1. Put the input files under ``regression/cases/<test_name>/``.
2. Add the expected output to ``regression/bless/<test_name>/``.
3. Append the case name to the ``TESTS`` list in ``Makefile``.
