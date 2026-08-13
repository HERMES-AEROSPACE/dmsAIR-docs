H\ :sub:`2`\  + H\ :sub:`2`\  heat bath
========================================

The canonical 4-body (diatom + diatom) benchmark. PES: BMKP H4 via
CoarseAIR. The 4-body code path exercises QCT integration with the full
4-atom Hamiltonian, arrangement detection over pair indices 1..6, and the
double-dissociation channel.

Case tree
---------

.. code-block:: text

   run/Hydrogen/H4/Inelastic/<T>K/
   run/Hydrogen/H4/Dissociation/<T>K/
   run/Hydrogen/H4/DoubleDissociation/<T>K/

with ``T`` ∈ {2500, 5000, 7500, 10000, 15000, 20000, 25000}.

Regime 1 — Inelastic
--------------------

.. code-block:: text

   Allow Dissociation   = no
   Allow Exchange Arr 1 = yes

   Species: H2 (X=1.0), H (X=0.0)
   Nb of Collision Pairs = 1        # H2 + H2  (H4 system)

Enabled processes: rovibrational transfer in *both* colliding molecules
(target and projectile each carry persistent internal states) and
**homogeneous 4-body exchange** — atom swaps between the two H₂ (pair
indices 2–6), which return two H₂ molecules and are handled as
inelastic-with-exchange on the same level table, ``gnuc`` bookkeeping
included. Both molecules' post-collision states are committed, so V–V
transfer between the diatoms is captured naturally.

Regime 2 — Dissociation (single)
--------------------------------

.. code-block:: text

   Allow Dissociation        = yes
   Allow Double Dissociation = no

Adds H₂ + H₂ → H₂ + 2H: one of the two molecules breaks, the survivor's
(v′,J′) is kept. Each event is classified direct vs exchange-assisted
from the per-pair trajectory record (a diagnostic — the historical
``Allow Dissociation Direct`` / ``Indirect Arr N`` keys are ignored).
Double-dissociation trajectories are discarded in this regime so rates
stay apples-to-apples with the ME reference, which cannot represent the
channel.

Regime 3 — Double dissociation
------------------------------

.. code-block:: text

   Allow Dissociation        = yes
   Allow Double Dissociation = yes

Additionally enables H₂ + H₂ → 4H (``arrangement = -2``): both molecules
break in a single trajectory and the projectile molecule is split into
two atomic particles alongside the target's fragments. Monitored as its
own tally (``pair_N_diss_double`` in ``box.csv``), so the single- and
double-channel fluxes stay separable.

Product kinetics
----------------

The H atoms produced by (single or double) dissociation are declared in
the species list (``X = 0.0``) and tracked in the composition — but this
deck declares **only the H₂ + H₂ pair**, so free atoms are **spectators**:
they shift densities but never collide. To enable their kinetics, add the
H₂ + H pair (H3 system) to the deck — exactly the construction of the
:doc:`hydrogen mixture example </examples/h2mix_heatbath>`, which runs
H₂+H₂, H₂+H and H₂+He simultaneously so dissociation products feed
straight back into the collision dynamics. Recombination (3-body) is not
available in any deck — see :doc:`CO + N(4S) </examples/con4s_heatbath>`
for the general product-kinetics recipe and limits.

Running
-------

.. code-block:: bash

   cd run/Hydrogen/H4/Inelastic/10000K
   sbatch sbatch_heatbath.slurm      # or ./dmsAIR.sh 16 locally
