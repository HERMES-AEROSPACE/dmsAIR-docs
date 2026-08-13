CO + N(⁴S) heat bath
====================

Third CNO partner system: CO colliding with ground-state atomic nitrogen
(**⁴S**). The quartet manifold runs on the single UCI_4A2 surface
(degeneracy 1), making this the cleanest of the three partner systems —
no doublet weighting, no excited-state bookkeeping. This page also walks
through **which processes each regime enables**, and how **product
kinetics** are switched on.

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

Regime 1 — Inelastic
--------------------

One collision pair, no reactive channel: the only enabled process is
rovibrational energy transfer CO(v,J) + N → CO(v′,J′) + N.

.. code-block:: text

   Nb of Particles        = 272340
   Allow Dissociation     = no
   Allow Exchange Arr 1   = no
   Allow Kernel           = yes

   Nb of Collision Pairs  = 1
   Collision Pair Species 1/2       = 1, 2        # CO + N
   Collision Pair PES Model 1       = UCI_4A2
   Collision Pair PES Degeneracy 1  = 1.00000

Regime 2 — Exchange (``Exchange1_4S_Products``)
-----------------------------------------------

Heterogeneous exchange CO + N → CN + O, **with the product kinetics
simulated**. The deck declares six species (products at zero initial
fraction) and **two collision pairs** — the reactant pair *and* the
product pair:

.. code-block:: text

   Allow Dissociation     = no
   Allow Exchange Arr 1   = yes
   # Per-pair channel selection (arr=2 pairs target atom 1 with the
   # projectile, arr=3 atom 2):
   Allow Exchange P1 Arr 2 = yes   # CO+N -> CN+O    (desired)
   Allow Exchange P1 Arr 3 = no    # CO+N -> NO+C    (parasitic)
   Allow Exchange P2 Arr 2 = yes   # CN+O -> CO+N    (desired back)
   Allow Exchange P2 Arr 3 = no    # CN+O -> NO+C    (parasitic)

   Species: CO (X=0.5), N (X=0.5), NO (X=0), CN (X=0), C (X=0), O (X=0)

   Nb of Collision Pairs  = 2
   # P1: reactants
   Collision Pair Species 1/2 = 1, 2      # CO + N   (CNO system, UCI_4A2)
   # P2: products
   Collision Pair Species 1/2 = 4, 6      # CN + O   (CNO system, UCI_4A2)

Enabled processes:

- **P1 (CO + N):** CO rovibrational relaxation *and* the forward exchange
  CO + N → CN + O. The parasitic NO-producing arrangement is blocked.
- **P2 (CN + O):** as CN and O accumulate, they collide too — CN
  rovibrational relaxation *and* the back-exchange CN + O → CO + N. This
  closes the forward/backward reaction loop so the composition can
  approach chemical balance instead of draining monotonically.

``Exchange2_4S_Products`` is the same construction for the NO channel
(CO + N → NO + C desired, CN blocked, product pair NO + C).

Regime 3 — Exchange + dissociation
----------------------------------

``Exchange1_4S_Dissociation_Products`` keeps the two pairs and the same
per-pair exchange filters, and adds the single master switch:

.. code-block:: text

   Allow Dissociation = yes

Dissociation applies to **every declared pair**, so two break-up channels
open: CO + N → C + O + N (on P1) and CN + O → C + N + O (on P2). Each
event is classified direct vs exchange-assisted from the per-pair
trajectory record (diagnostic output — there is no input switch for the
pathway; the historical ``Allow Dissociation Direct`` / ``Indirect``
keys are ignored).

``TotalDissociation`` is the opposite reduction: **one** pair, exchange
off, dissociation on — the dissociation flux becomes a single lumped
channel, the like-for-like setup against the ME total-dissociation
variant:

.. code-block:: text

   Allow Dissociation   = no  ->  yes
   Allow Exchange Arr 1 = no
   Nb of Collision Pairs = 1          # CO + N only

Product kinetics: what is and is not simulated
----------------------------------------------

**A product species only collides if a collision pair is declared for
it.** That is the entire mechanism — and the reason the regime names
carry the ``_Products`` suffix:

- *With* the product pair (P2 above): exchange products are created as
  live particles, thermalise through their own inelastic collisions, and
  feed the back-reaction. Their rates appear pair-resolved in ``box.csv``
  (``pair_N_att``, ``pair_N_inel``, ``pair_N_exch``, … per pair).
- *Without* it (e.g. ``TotalDissociation``, or an exchange deck with only
  P1): products are still created and tracked in the composition — they
  shift densities and collision frequencies — but they are **spectators**:
  no internal relaxation, no back-reaction.

To enable product kinetics in your own deck:

1. **Declare the product species** with ``Species X = 0.0`` (they must
   exist in the species list even at zero initial fraction, with their
   own levels file if molecular).
2. **Add a collision pair** for the product combination — same
   ``Collision Pair System`` (CNO) and PES, its own ``bmax`` and ODE
   block.
3. **Set the per-pair exchange filters** on the new pair: enable the
   back-reaction arrangement, block the parasitic one (the ``P2 Arr``
   lines above). Without these, the product pair would open *all* its
   exchange channels by default.

Current limits, stated explicitly: dmsAIR has **no recombination** —
atoms produced by dissociation never re-form molecules (three-body
recombination is outside the binary-collision QCT framework), so C and O
from the dissociation regimes are always spectators. Likewise
product–product pairs (CN + CN, …) and any combination you do not declare
are not simulated; at trace product fractions their collision frequency
is negligible, which is why the ``_Products`` decks declare only the two
pairs that matter.

Running
-------

.. code-block:: bash

   cd run/Verification/CO+N4S_Exchange1_4S_Products/10000K
   sbatch sbatch_heatbath.slurm
