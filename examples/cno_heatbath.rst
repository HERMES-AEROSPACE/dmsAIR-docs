CN + O heat bath
================

The first CNO *partner system*: the same C–N–O collision complex as
:doc:`NO + C </examples/noc_heatbath>`, entered from the CN + O arrangement.
Together with :doc:`CO + N(2D) </examples/con2d_heatbath>` and
:doc:`CO + N(4S) </examples/con4s_heatbath>` it closes the kinetic triangle

.. code-block:: text

   NO + C  ⇌  CN + O  ⇌  CO + N  ⇌  NO + C

so every exchange channel measured in one system has its back-reaction
measured in another. All partner-system decks are generated
ME-consistently by ``gen_partner_systems.py`` (per-temperature electronic
degeneracies, doublet ×2 convention).

Case tree
---------

.. code-block:: text

   run/Verification/CN+O_<regime>/<T>/

with ``T`` ∈ {``5000K``, ``10000K``, ``20000K``} and ``regime`` ∈

.. list-table::
   :header-rows: 1
   :widths: 34 46

   * - Regime
     - Meaning / ME counterpart
   * - ``Inelastic``
     - UCI_4A2 surface, exchange off → ME ``Inelastic_4A``
   * - ``Inelastic_2A1``
     - UCI_2A1 (×2 doublet) surface → ME ``Inelastic_2A``
   * - ``Exchange1_2D_Products`` / ``Exchange1_4S_Products``
     - CN + O → CO + N, resolved by the product-atom electronic state
   * - ``Exchange2_Products``
     - CN + O → NO + C
   * - ``*_Dissociation_Products``
     - same channel selections with ``Allow Dissociation = yes``
   * - ``TotalDissociation``
     - exchange off, dissociation on → single lumped dissociation channel

.. warning::

   **Surface pairing.** ``CN+O_Inelastic`` is the *single-surface* UCI_4A2
   deck and pairs with the ME ``Inelastic_4A`` variant;
   ``CN+O_Inelastic_2A1`` pairs with ``Inelastic_2A``. Pairing a
   single-surface DMS run against a *Global* (multi-surface) ME variant
   fabricates a large spurious discrepancy.

Heterogeneous exchange and how channels are selected
----------------------------------------------------

CN + O exchange is **heterogeneous**: the product diatom (CO or NO) is a
*different chemical species* from the reactant CN. dmsAIR detects this by a
product-pair mass test; a heterogeneous product is never force-labelled on
the reactant's level table — the event consumes both reactants and creates
the product molecule and atom as new particles.

The arrangement index numbers atom-pair slots *within* a collision pair
(target atoms 1,2 + projectile atom 3 → ``Arr 2`` is the (1,3) pair,
``Arr 3`` the (2,3) pair). The same index is therefore a *different
reaction* in different pairs, which is why channel selection uses the
**per-pair** filter:

.. code-block:: text

   Allow Exchange Arr 1    = yes           # master switch
   Allow Exchange P1 Arr 2 = yes   # CN+X -> CO+atom   (desired)
   Allow Exchange P1 Arr 3 = no    # CN+X -> NO+atom   (parasitic)
   Allow Exchange P2 Arr 2 = yes   # CO+N -> CN+atom   (desired back)
   Allow Exchange P2 Arr 3 = no    # CO+N -> NO+atom   (parasitic)

This deck (``Exchange1_*_Products``) isolates the CN + O ⇌ CO + N pair of
reactions while blocking the NO-producing channel on *both* collision
pairs — something the global ``Allow Exchange Arr N`` form cannot express,
because it sets every pair identically.

Contrast this with **homogeneous exchange** (H\ :sub:`2` + H,
H\ :sub:`2` + H\ :sub:`2`): there the atom swap returns the *same* chemical
species, the particle identity is preserved, and the event is handled as an
inelastic-with-exchange transition on the same level table (with
nuclear-spin bookkeeping). See the
:doc:`hydrogen mixture example </examples/h2mix_heatbath>`.

Dissociation
------------

``Allow Dissociation = yes`` is the only dissociation gate (the historical
``Allow Dissociation Direct`` / ``Indirect Arr N`` keys are accepted but
ignored). Whether a dissociation event was *direct* or *exchange-assisted*
is classified per event from the per-pair trajectory record (which
atom-pairs transiently approached a bound configuration) and reported in
the output — it is a diagnostic, not an input switch.

Deck highlights (``CN+O_Inelastic/10000K``)
-------------------------------------------

.. code-block:: text

   Nb of Particles        = 72930          # ME-consistent mixture size
   Allow Dissociation     = no
   Allow Exchange Arr 1   = no
   Allow Kernel           = yes            # state-to-state kernel.csv
   Propagate Phase Space  = yes

   Collision Pair PES Model 1       = UCI_4A2
   Collision Pair PES Degeneracy 1  = 1.00000

The 2A1 variants carry a *per-temperature* degeneracy (e.g. ``0.40020`` at
10000 K) so that the electronic-surface weighting matches the ME reference
at each bath temperature.

Running
-------

.. code-block:: bash

   cd run/Verification/CN+O_Inelastic/10000K
   sbatch sbatch_heatbath.slurm       # or ./dmsAIR.sh <ranks> locally
