CO + N(²D) heat bath
====================

Second CNO partner system: the C–N–O complex entered from CO + N with the
nitrogen atom in its excited **²D** electronic state. On the doublet
manifold the relevant surface is UCI_2A1 (×2 doublet convention), so this
system is the doublet-side complement of
:doc:`CO + N(4S) </examples/con4s_heatbath>`.

Case tree
---------

.. code-block:: text

   run/Verification/CO+N2D_<regime>/<T>/

with ``T`` ∈ {``5000K``, ``10000K``, ``20000K``} and ``regime`` ∈
{``Inelastic``, ``Exchange1_2D_Products``, ``Exchange2_2D_Products``,
``Exchange1_2D_Dissociation_Products``,
``Exchange2_2D_Dissociation_Products``, ``TotalDissociation``}.

ME counterparts follow the ``_2A`` naming (e.g. ``Inelastic`` ↔ ME
``CO+N2D/<T>/Inelastic_2A``).

Channel selection
-----------------

Exchange here is **heterogeneous** (products CN + O or NO + C are different
species from CO); the mechanism and the per-pair
``Allow Exchange P<n> Arr <m>`` filters are exactly as described in the
:doc:`CN + O example </examples/cno_heatbath>` — only the arrangement
labels map to different products because the atom ordering differs:

- ``Exchange1_2D_Products``: CO + N → CN + O (the back-reaction of the
  CN + O system's Exchange 1)
- ``Exchange2_2D_Products``: CO + N → NO + C

The ``_2D_`` tag records that the *atomic product* is tracked in the ²D
state, keeping the electronic bookkeeping consistent with the ME reference
on the doublet surface.

Deck highlights (``CO+N2D_Inelastic/10000K``)
---------------------------------------------

.. code-block:: text

   Nb of Particles        = 63130
   Allow Dissociation     = no
   Allow Exchange Arr 1   = no
   Allow Kernel           = yes

   Collision Pair PES Model 1       = UCI_2A1
   Collision Pair PES Degeneracy 1  = 0.40020    # per-T, doublet x2 convention

The degeneracy is temperature-dependent (Boltzmann electronic weighting),
regenerated per deck by ``gen_partner_systems.py``.

Comparison caveats
------------------

Two standing caveats when comparing against the ME reference:

1. The ME *Global* variants apply an intersection filter across surfaces —
   pair single-surface DMS decks only with the matching single-surface ME
   variant (``_2A`` here).
2. Excited-state ME kinetics for CO + N(²D) include a rate-redirect
   (``k_pred``) convention for channels without direct QCT coverage; treat
   those lines as model input, not ground truth, when attributing
   discrepancies.

Running
-------

.. code-block:: bash

   cd run/Verification/CO+N2D_Inelastic/10000K
   sbatch sbatch_heatbath.slurm
