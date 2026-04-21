NO + C heat bath
================

A heteronuclear 3-body system with **two distinct exchange channels** —
NO+C → CN+O and NO+C → CO+N. The first production test of the CO+N channel
after the heteronuclear-quantisation fix.

Case tree
---------

.. code-block:: text

   run/CNO/<PES>/NO+C/<regime>/<T>/

with

- ``PES`` ∈ {``2A1x2``, ``2A1+2A2``, ``4A2``}
- ``regime`` ∈ {``inelastic``, ``exchange1``, ``exchange2``,
  ``exchange1+dissociation``, ``exchange2+dissociation``, ``dissociation``}
- ``T`` ∈ {``1500K``, ``2500K``, ``5000K``, ``10000K``, ``20000K``}

= 3 × 6 × 5 = 90 cases per subsystem (NO+C / CN+O / CO+N).

Regime mapping
--------------

+--------------------------------+------------------------------------------+
| Regime folder                  | Input flags                              |
+================================+==========================================+
| ``inelastic``                  | Allow Exchange = no, Allow Diss = no     |
+--------------------------------+------------------------------------------+
| ``exchange1``                  | Allow Exchange Arr 3 = no (CN+O only)    |
+--------------------------------+------------------------------------------+
| ``exchange2``                  | Allow Exchange Arr 2 = no (CO+N only)    |
+--------------------------------+------------------------------------------+
| ``exchange1+dissociation``     | Ex1 only + Allow Dissociation = yes      |
+--------------------------------+------------------------------------------+
| ``exchange2+dissociation``     | Ex2 only + Allow Dissociation = yes      |
+--------------------------------+------------------------------------------+
| ``dissociation``               | Allow Exchange = no, Allow Diss = yes    |
+--------------------------------+------------------------------------------+

Running a single case
---------------------

.. code-block:: bash

   cd run/CNO/4A2/NO+C/exchange1/10000K
   sbatch sbatch_heatbath.slurm            # cluster
   # or ./dmsAIR.sh 16                     # local

Launching a full sweep
----------------------

.. code-block:: bash

   # All six regimes × five temperatures on the 4A2 PES
   ./src/scripts/launchDMS.py --subsys NO+C --pes 4A2 --regime all --T all
   # = 30 SLURM submissions

Post-processing
---------------

.. code-block:: bash

   python3 postprocessing/Postprocessing/postprocessing.py \
       --system CNO --subsys NO+C --pes 4A2

Generates comparison plots against PLATO's ME reference at
``/home/ccivrais/WORKSPACE/PLATO/run/CNO/MasterEquationAnalysis/NO+C/``.

Expected physics
----------------

- Both exchange channels are exothermic: ΔE(Ex1) ≈ −1.2 eV, ΔE(Ex2) ≈ −4.6 eV.
- Ex2 (CO+N) is typically ~2× more frequent than Ex1 (CN+O) on the 4A2 PES
  because CO is more deeply bound.
- At 10 000 K the dissociation rate is ``k_DD ~ 10^{-16}`` m\ :sup:`3`\ /s.
