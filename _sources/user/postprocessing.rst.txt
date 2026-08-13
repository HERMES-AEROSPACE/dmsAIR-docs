Post-processing
===============

dmsAIR ships a suite of Python post-processors under ``postprocessing/``.

.. note::

   The repository tracks **scripts and input decks only**. Simulation
   outputs (``box.csv``, ``pop.csv``, ``kernel.csv``, checkpoints) and the
   multi-GB Master-Equation reference solutions/databases
   (``postprocessing/Reference/``, ``postprocessing/Reference_Clement/``,
   ``postprocessing/Postprocessing/DerivedData/``) live only on the local
   machine / cluster and are excluded via ``.gitignore``. Obtain reference
   data from the group storage before running the comparison scripts.

H3 DMS-vs-ME comparison
-----------------------

.. code-block:: bash

   python3 postprocessing/Postprocessing/postprocessing.py --no-diss
   python3 postprocessing/Postprocessing/postprocessing.py --diss

Generates ``Energy.pdf``, ``Concentration.pdf``, ``Pressure.pdf`` with DMS
results overlaid on the Master-Equation reference from PLATO.

CNO DMS-vs-ME comparison
------------------------

.. code-block:: bash

   python3 postprocessing/Postprocessing/postprocessing.py \
       --system CNO --subsys NO+C --pes 4A2 --T 5000K 10000K 20000K

Produces per-species mole fractions, internal temperature trace, pressure,
and a QSS-rate summary. The default regime → ME mapping is:

+------------------------------+---------------------------------+
| DMS regime                   | PLATO ME reference              |
+==============================+=================================+
| ``inelastic``                | ``Inelastic_4A``                |
+------------------------------+---------------------------------+
| ``exchange1``                | ``Exchange1``                   |
+------------------------------+---------------------------------+
| ``exchange2``                | ``Exchange2_4S``                |
+------------------------------+---------------------------------+
| ``exchange1+dissociation``   | ``Exchange1_Dissociation``      |
+------------------------------+---------------------------------+
| ``exchange2+dissociation``   | ``Exchange2_4S_Dissociation``   |
+------------------------------+---------------------------------+
| ``directdissociation``       | ``DirectDissociation``          |
+------------------------------+---------------------------------+
| ``totaldissociation``        | ``TotalDissociation``           |
+------------------------------+---------------------------------+

Override with ``--me-map "regime=folder"`` tokens.

Scattering maps
---------------

.. code-block:: bash

   python3 postprocessing/ScatteringMap/plot_chi_contour_v2.py
   python3 postprocessing/ScatteringMap/plot_chi_surface3d.py
   python3 postprocessing/ScatteringMap/plot_bmax_powerlaw.py

- ``plot_chi_contour_v2.py``: 2D ⟨\|χ\|⟩(b, E) contour maps per channel (total,
  inelastic, exchange, dissociation).
- ``plot_chi_surface3d.py``: 3D surface view.
- ``plot_bmax_powerlaw.py``: Langevin-capture fit ``bmax = a·E^b`` at the 1°
  iso-contour.

Verification suite (DMS vs ME)
------------------------------

Beyond the main ``postprocessing.py`` pipeline, dedicated verification
scripts under ``postprocessing/Postprocessing/`` compare DMS runs
one-to-one against Master-Equation references:

- ``verify_H2_strategy3_vs_ME.py`` / ``verify_H2_dissociation_vs_ME.py`` —
  H2+H and H2+He relaxation and dissociation against the rebuilt PLATO
  box databases.
- ``verify_CNO_inelastic_vs_ME.py`` / ``verify_CNO_all_vs_ME.py`` — CNO
  subsystems per PES and regime.
- ``compare_H2_ME_DMS.py`` / ``compare_H4_DMS_vs_ME.py`` /
  ``compare_coupled_NOCN.py`` — multi-source overlays (DMS vs independent
  ME datasets; coupled NO+C ↔ CN+O).
- ``extract_H2_qss_quantities.py`` / ``extract_NOC_qss_quantities.py`` /
  ``extract_verification_tau.py`` — QSS rates and e-folding relaxation
  times from ``box.csv`` histories.
- ``me_pop_reader.py`` — shared reader for PLATO ``pop_<species>.dat``
  population files (Trot/Tvib reconstruction via the Panesi
  decomposition); ``me_db_closure_test.py`` — ME database sanity checks.

Population inspection
---------------------

``pop.csv`` contains the rovibrational population ``n(v,j)/gnuc(j)`` at each
sampled step. Typical analysis: overlay against a Boltzmann distribution at
the inverted ``Tint(t)`` to visualise departure from equilibrium.
