Hydrogen mixture heat bath
==========================

A full multi-pair mixture: H₂ with atomic H and He at a Saturn-like
composition (96.3 % H₂, 3.7 % He), running **three collision pairs
simultaneously** — H₂+H (H3 surface), H₂+H₂ (H4), H₂+He (H2He) — with a
shared Schwenke H₂ diatomic potential. This is the example that exercises
every reactive-channel switch in one deck.

Case tree
---------

.. code-block:: text

   run/Hydrogen/H2mix/Inelastic/<T>K/
   run/Hydrogen/H2mix/Dissociation/<T>K/

with ``T`` ∈ {2500, 5000, 7500, 10000, 15000, 20000, 25000}.

Mixture definition
------------------

.. code-block:: text

   Nb of Species = 3
   Species Name = H2      Species X = 0.963
   Species Name = H       Species X = 0.0      # produced by dissociation
   Species Name = He      Species X = 0.037

   Nb of Collision Pairs = 3
   Collision Pair Species 1/2 = 1, 2     Collision Pair System = H3
   Collision Pair Species 1/2 = 1, 1     Collision Pair System = H4
   Collision Pair Species 1/2 = 1, 3     Collision Pair System = H2He

The NTC machinery selects pairs per species combination; each pair carries
its own ``bmax`` (14.14 Bohr for H3, 10.0 for H4 and H2He in this deck).

Homogeneous exchange
--------------------

The H3 and H4 pairs undergo **homogeneous exchange**: the atom swap
H₂ + H′ → H₂′ + H (and the 4-body analogue) returns the *same chemical
species*. dmsAIR recognises this through the product-pair mass test and
handles the event as an inelastic-with-exchange transition — the particle
identity survives, the product state is projected onto the same H₂ level
table, and the nuclear-spin (ortho/para, ``gnuc``) bookkeeping applies
across the swap. No particles are created or destroyed.

.. code-block:: text

   Allow Exchange Arr 1 = yes    # exchange ON for the reactive pairs

The H₂+He pair contributes no exchange (see the
:doc:`H2+He example </examples/h2he_heatbath>`); dmsAIR simply finds no
bound heteronuclear product for that pair. For *heterogeneous* exchange —
where the swap creates a different species and per-channel selection
matters — see the :doc:`CNO partner systems </examples/cno_heatbath>`.

Dissociation: direct, exchange-assisted, and double
---------------------------------------------------

The ``Dissociation`` regime enables the full channel set:

.. code-block:: text

   Allow Dissociation        = yes
   Allow Double Dissociation = yes     # 4-body (H4 pair) only

**Direct vs exchange-assisted (diagnostic, not a switch).** A single master
switch gates all dissociation. Each event is then *classified* from the
per-pair trajectory record: if only the reactant atom-pair ever approached
a bound configuration the dissociation was direct; if a cross pair
transiently bound, it was exchange-assisted. The classification is written
to the output tallies. (The historical ``Allow Dissociation Direct`` /
``Allow Dissociation Indirect Arr N`` input keys — still present in older
decks — are accepted and ignored.)

**Double dissociation** is a 4-body channel (H₂ + H₂ → 4 H,
``arrangement = -2``): both molecules break in a single trajectory, and the
projectile molecule is split into two atomic particles alongside the
target's fragments. It is **off by default** because the master-equation
framework cannot represent the channel — enabling it makes the DMS more
complete but no longer like-for-like against an ME reference. In this
mixture deck it is enabled in the ``Dissociation`` regime and monitored as
a separate tally (``pair_N_diss_double``).

Note the composition consequence: dissociation grows the atomic-H
population from ``X = 0``, which switches on H₂+H (H3) collisions
dynamically as the mixture evolves — the reason the H species must be
declared even at zero initial fraction.

Running
-------

.. code-block:: bash

   cd run/Hydrogen/H2mix/Dissociation/10000K
   sbatch sbatch_heatbath.slurm

Per-pair rates (attempts, inelastic, exchange, dissociation, double
dissociation) are reported pair-resolved in ``box.csv``, so the three
sub-systems can be compared against their single-pair reference cases
directly.
