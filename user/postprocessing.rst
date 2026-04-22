Post-processing
===============

dmsAIR ships a suite of Python post-processors under ``postprocessing/``.

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

Population inspection
---------------------

``pop.csv`` contains the rovibrational population ``n(v,j)/gnuc(j)`` at each
sampled step. Typical analysis: overlay against a Boltzmann distribution at
the inverted ``Tint(t)`` to visualise departure from equilibrium.
