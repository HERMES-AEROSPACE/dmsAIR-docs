H₂ + He heat bath
=================

The most demanding validation system in the suite: a stiff, light diatomic
(:math:`\theta_v(\mathrm{H_2}) \approx 6300` K) against an inert, weakly
interacting collider, with **no reactive channel**. All internal energy
transfer is non-reactive V–T/R–T — precisely the regime where mapping
continuous classical dynamics onto the quantised ladder is hardest, and the
system that motivated :doc:`Gaussian binning </theory/gaussian_binning>`.

Case tree
---------

.. code-block:: text

   run/Hydrogen/H2He/Inelastic/<T>K[_GB]/
   run/Hydrogen/H2He/Dissociation/<T>K/

with ``T`` ∈ {2500, 5000, 7500, 10000, 15000, 20000, 25000}. The ``_GB``
siblings are the Gaussian-binning arm: same decks with GB enabled and
``bmax`` reduced to 15 Bohr (Np = 20000 everywhere).

No exchange channel
-------------------

H₂ + He *has* formal exchange arrangements (H + HeH), but HeH is not a
bound product worth tracking and the ME reference has no such channel, so
exchange is disabled outright:

.. code-block:: text

   Allow Exchange Arr 1 = no

This makes H₂ + He the pure *non-reactive* end-member: contrast with
homogeneous exchange (H₂ + H, where atom swap moves whole quanta — see the
:doc:`hydrogen mixture example </examples/h2mix_heatbath>`) and
heterogeneous exchange (the
:doc:`CNO partner systems </examples/cno_heatbath>`). Because it lacks the
exchange pathway, H₂ + He relaxes exclusively through near-threshold
non-reactive transitions at low :math:`T/\theta_v` — the histogram-binning
artifact regime.

Deck highlights (``Inelastic/5000K``)
-------------------------------------

.. code-block:: text

   Translational Temperature [K] = 5000
   Internal Temperature [K]      = 300
   Pressure [Pa]                 = 1000

   Nb of Particles      = 20000
   Allow Dissociation   = no
   Allow Exchange Arr 1 = no
   Allow Kernel         = yes         # state-to-state kernel for DB analysis

   Collision Pair System        = H2He
   Collision Pair bmax [Bohr]   = 20.0     # long-range deflections matter
   Collision Pair PES Model 1   = H2He_BMPmod

   Species gnuc Even J = 1            # para-H2
   Species gnuc Odd J  = 3            # ortho-H2

The large ``bmax`` is deliberate: grazing collisions at 10–20 Bohr
contribute measurably to rotational relaxation at high collision energies.

The Gaussian-binning arm
------------------------

The GB campaign runs **three families at every temperature**, all with
``Nb of Particles = 20000`` and ``Collision Pair bmax [Bohr] = 15.0``:

- ``H2He/Inelastic/<T>K_GB`` — the system under test;
- ``H3/Inelastic/<T>K_GB`` — H₂ + H *with* exchange: the null control
  (whole-quantum exchange should make GB a no-op);
- ``H3/Inelastic_noExch/<T>K_GB`` — H₂ + H with exchange *discarded*:
  isolates the non-reactive channel of the reactive system, which should
  behave H₂+He-like under GB.

Each ``_GB`` deck adds:

.. code-block:: text

   Gaussian Binning = yes
   GB Epsilon Vib   = 0.10

Gaussian binning forces quantum-number carry ON and pays the
snap-to-level energy from the products' relative translation (see
:doc:`/theory/gaussian_binning` for the mechanism and for the
rate-normalisation caveat that applies before comparing GB relaxation
times against the ME). The pass criteria for this arm:

1. the measured kernel's up/down ratio reaches the detailed-balance value;
2. the low-temperature E\ :sub:`vib` no longer runs ahead of the ME
   (sub-quantum accumulation closed);
3. the H₂ + H control (exchange-dominated, whole-quantum) is unaffected.

Dissociation
------------

``Dissociation/<T>K`` decks set ``Allow Dissociation = yes`` (single master
switch — the per-pathway keys are deprecated no-ops). With no exchange
channel, every dissociation event here is *direct* by construction; the
per-event direct/exchange-assisted classification in the output is only
informative for systems with open exchange channels.

Running and analysis
--------------------

.. code-block:: bash

   cd run/Hydrogen/H2He/Inelastic/5000K_GB
   sbatch sbatch_heatbath.slurm

Compare internal-energy relaxation against the ME reference in **energy
space** (mean internal energy from the level populations), never via
cross-code :math:`T_{\mathrm{vib}}` inversions — the two codes' temperature
definitions differ at high T. The pairing is
H2+He ↔ ME ``Inelastic`` (channel-matched, dissociation lines stripped).
