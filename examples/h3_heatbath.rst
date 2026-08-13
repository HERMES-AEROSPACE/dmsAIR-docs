H\ :sub:`2`\  + H heat bath
===========================

The canonical 3-body validation case. PES: Boothroyd–Keogh–Martin–Peterson
(BKMP2) / Schwenke, linked through CoarseAIR's ``H3_BH`` system.

Case tree
---------

.. code-block:: text

   run/Hydrogen/H3/Inelastic/<T>K[_GB]/
   run/Hydrogen/H3/Inelastic_noExch/<T>K[_GB]/
   run/Hydrogen/H3/Dissociation/<T>K/

with ``T`` ∈ {2500, 5000, 7500, 10000, 15000, 20000, 25000}. The ``_GB``
siblings belong to the :doc:`Gaussian-binning </theory/gaussian_binning>`
campaign (bmax = 15 Bohr, Np = 20000).

Regime 1 — Inelastic (with exchange)
------------------------------------

.. code-block:: text

   Allow Dissociation   = no
   Allow Exchange Arr 1 = yes

   Species: H2 (X=0.5), H (X=0.5)
   Nb of Collision Pairs = 1        # H2 + H  (H3 system)

Enabled processes: rovibrational energy transfer H₂(v,J) + H →
H₂(v′,J′) + H **and homogeneous exchange** H₂ + H′ → H₂′ + H. The swap
returns the same chemical species, so the event is handled as an
inelastic-with-exchange transition on the same level table (ortho/para
``gnuc`` bookkeeping applies across the swap); particle identity is
preserved and the composition stays at 0.5/0.5. Exchange transfers whole
quanta, which is why this system is insensitive to the histogram-binning
representation and serves as the **null control** of the GB campaign.

Regime 2 — Inelastic-only (``Inelastic_noExch``)
------------------------------------------------

.. code-block:: text

   Allow Dissociation   = no
   Allow Exchange Arr 1 = no

Same deck with the exchange channel **discarded**: trajectories that end
in an atom swap are dropped, leaving only the non-reactive V–T/R–T
channel. This isolates the H₂+He-like part of a reactive system — the arm
that should show the binning artifact (and respond to Gaussian binning)
even though the full system does not.

Regime 3 — Dissociation
-----------------------

.. code-block:: text

   Allow Dissociation   = yes
   Allow Exchange Arr 1 = yes

Adds H₂ + H → H + H + H. QSS dissociation rates come out at
``k_DD ≈ 10^-17..10^-16`` m³/s depending on temperature.

Product kinetics
----------------

H₂ + H is the special case where product kinetics are **automatically
closed**: the dissociation product (atomic H) *is already the collision
partner*, so newly produced atoms immediately participate in H₂ + H
collisions through the same pair — no extra deck machinery needed. The
composition drift (X_H2 down, X_H up) feeds straight back into the NTC
collision frequencies.

What is *not* simulated in this deck: H₂ + H₂ collisions (declare the H4
pair for that — see the :doc:`hydrogen mixture </examples/h2mix_heatbath>`,
which runs all three hydrogen pairs at once) and recombination
(three-body, outside the binary-collision framework — see the general
discussion in :doc:`CO + N(4S) </examples/con4s_heatbath>`).

Running and comparison
----------------------

.. code-block:: bash

   cd run/Hydrogen/H3/Inelastic/10000K
   sbatch sbatch_heatbath.slurm      # or ./dmsAIR.sh 16 locally

Pair with the ME ``Inelastic_w_Exchange`` variant (the exchange channel
lives *inside* the ME's inelastic bookkeeping for H3);
``Inelastic_noExch`` pairs with the exchange-free ME variant. Compare in
energy space (mean internal energy), not via cross-code Tvib inversions.
