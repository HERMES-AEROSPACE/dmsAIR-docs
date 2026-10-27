Adding a New Collision System
==============================

This page walks through the steps to bring a new collision system online.
Canonical example: adding N + N\ :sub:`2` (3-body).

1. Verify CoarseAIR support
---------------------------

The PES must be available in CoarseAIR's ``dtb/Systems/<system>/``. Check:

.. code-block:: bash

   ls $COARSEAIR_DTB/Systems/N3/

If present, the ``System = N3`` keyword in ``dmsAIR.inp`` will load it
automatically. If not, the PES has to be added to CoarseAIR first (out of
scope here).

2. Locate the levels files
--------------------------

Each atom pair that could form a bound molecule needs a rovibrational level
table. For N + N\ :sub:`2` the only diatomic is N\ :sub:`2`, so you need one
``levels_N2.inp`` file. Copy from CoarseAIR's ``dtb/Molecules/N2/<model>/``.

For heteronuclear systems with multiple possible products (e.g. NO+C),
bring in a ``levels_<product>.inp`` for each product type that the PES
supports.

3. Write the case ``dmsAIR.inp``
---------------------------------

The cleanest approach is to copy an existing heat-bath input (e.g.
``run/H3/NoDissociation/10000K/dmsAIR.inp``) and adjust:

- Species masses and names
- Levels files
- ``Collision Pair System``, ``Collision Pair PES Model``
- ``bmax`` (from a scattering-map study — see :doc:`/examples/scattering_map`)
- ``tmax`` and ``Nb of Time Steps`` consistent with the relaxation
  timescale at the target temperature

4. Calibrate ``bmax``
----------------------

Run ``dmsAIR_ScatteringMap`` to generate a ⟨\|χ\|⟩ map. Take the rightmost
``b`` where ⟨\|χ\|⟩ ≥ 1° as your ``bmax``, rounded up to the next 0.5 Bohr.
This is the standard DMS bmax-selection rule.

5. Smoke-test a short run
-------------------------

.. code-block:: bash

   cd run/<new_system>/Dissociation/10000K
   # truncate: Nb of Particles = 10000, Nb of Time Steps = 1000
   ./dmsAIR.sh 4

Verify:

- ``box.csv`` has 27 columns per row (12 non-rate + 15 rate)
- The expected reactive channels fire (check ``k_Ex_arr2``, ``k_Ex_arr3``,
  ``k_DD`` are non-zero where physics says they should be)
- Energy is conserved to your integrator's nominal precision

6. Generate the case tree
-------------------------

Use ``src/scripts/launchDMS.py`` as a template for the directory layout
(PES × subsystem × regime × temperature).

7. Heteronuclear-specific: verify both exchange channels
---------------------------------------------------------

For systems with two distinct exchange products (e.g. N + O\ :sub:`2` →
NO + O or O + NO), run a short ``exchange`` regime case and verify that
**both** ``k_Ex_arr2`` and ``k_Ex_arr3`` contain non-zero values. If one
is always zero the heteronuclear-quantisation path (see
:doc:`/theory/reactive_channels`) may not be wired correctly.

8. Validate against ME (optional but recommended)
--------------------------------------------------

If a PLATO Master-Equation solution is available for the same system and
PES, run the DMS-vs-ME comparator:

.. code-block:: bash

   python3 postprocessing/Postprocessing/postprocessing.py \
       --system <new_system> --subsys <pair> --pes <pes_name>
