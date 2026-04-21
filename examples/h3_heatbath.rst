H\ :sub:`2`\  + H heat bath
===========================

The canonical 3-body validation case. PES: Boothroyd–Keogh–Martin–Peterson
(BKMP2) / Schwenke, linked through CoarseAIR's ``H3_BH`` system.

Case directory
--------------

.. code-block:: text

   run/H3/NoDissociation/{5000K, 10000K, 20000K}/
   run/H3/Dissociation/{5000K, 10000K, 20000K}/

Inelastic + exchange relaxation
-------------------------------

.. code-block:: bash

   cd run/H3/NoDissociation/10000K
   ./dmsAIR.sh 16

Expected behaviour at 10 000 K:

- Inelastic events dominate; exchange is symmetry-equivalent (identical H atoms).
- Internal temperature relaxes from 300 K toward 10 000 K with
  τ\ :sub:`VT` ≈ 50 ns.
- X\ :sub:`H2` and X\ :sub:`H` stay at their initial 0.5 / 0.5 split (no reactions).

With dissociation
-----------------

.. code-block:: bash

   cd run/H3/Dissociation/10000K
   ./dmsAIR.sh 16

Additional physics: H\ :sub:`2` + H → H + H + H, with QSS dissociation rate
``k_DD ≈ 10^{-17}..10^{-16}`` m\ :sup:`3`\ /s depending on temperature.

Comparison with Master Equation
-------------------------------

.. code-block:: bash

   python3 postprocessing/Postprocessing/postprocessing.py --no-diss
   python3 postprocessing/Postprocessing/postprocessing.py --diss

Reference ME data from PLATO is stored under
``postprocessing/Reference/<T>K/``.
