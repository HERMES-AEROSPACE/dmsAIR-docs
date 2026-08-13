CO + N(⁴S) heat bath
====================

Third CNO partner system: CO colliding with ground-state atomic nitrogen
(**⁴S**). The quartet manifold runs on the single UCI_4A2 surface
(degeneracy 1), making this the cleanest of the three partner systems —
no doublet weighting, no excited-state bookkeeping.

Case tree
---------

.. code-block:: text

   run/Verification/CO+N4S_<regime>/<T>/

with ``T`` ∈ {``5000K``, ``10000K``, ``20000K``} and ``regime`` ∈
{``Inelastic``, ``Exchange1_4S_Products``, ``Exchange2_4S_Products``,
``Exchange1_4S_Dissociation_Products``,
``Exchange2_4S_Dissociation_Products``, ``TotalDissociation``}.

ME counterparts follow the ``_4A`` naming (``Inelastic`` ↔ ME
``CO+N4S/<T>/Inelastic_4A``).

Channel selection
-----------------

Heterogeneous exchange, selected with the per-pair filters exactly as in
the :doc:`CN + O example </examples/cno_heatbath>`:

- ``Exchange1_4S_Products``: CO + N → CN + O
- ``Exchange2_4S_Products``: CO + N → NO + C

with the parasitic third channel blocked per pair. The ``_4S_`` tag pins
the atomic products to the quartet manifold, matching the ME reference.

Dissociation regimes add ``Allow Dissociation = yes`` on top of the same
exchange selections; ``TotalDissociation`` turns exchange off entirely so
the dissociation flux is a single lumped channel (the like-for-like setup
against the ME's total-dissociation variant).

Deck highlights (``CO+N4S_Inelastic/10000K``)
---------------------------------------------

.. code-block:: text

   Nb of Particles        = 272340
   Allow Dissociation     = no
   Allow Exchange Arr 1   = no
   Allow Kernel           = yes

   Collision Pair PES Model 1       = UCI_4A2
   Collision Pair PES Degeneracy 1  = 1.00000

The large particle count keeps the ME-consistent mixture composition
resolved (the CO fraction is diluted by the partner species in the
composition convention shared with the ME reference).

Running
-------

.. code-block:: bash

   cd run/Verification/CO+N4S_Inelastic/10000K
   sbatch sbatch_heatbath.slurm
