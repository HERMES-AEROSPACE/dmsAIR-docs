Input File Reference
====================

Every case is driven by a plain-text ``dmsAIR.inp`` file. Keywords are
case-sensitive; unknown keywords are ignored with a warning.

Thermodynamics
--------------

.. code-block:: text

   Translational Temperature [K]  = 10000     # imposed Ttr (isothermal bath)
   Internal Temperature [K]       = 300       # initial Tint for the diatomic bath
   Pressure [Pa]                  = 1000      # initial pressure

Numerics
--------

.. code-block:: text

   Nb of Particles             = 683800
   Nb of Time Steps            = 10000000
   Particle Weight             = 1
   Output Interval             = 100          # box.csv cadence (steps)
   Population Output Interval  = 1000         # pop.csv cadence (steps)
   DMS Timestep Fraction       = 0.01         # dt_DMS / t_collision

Physics options
---------------

.. code-block:: text

   Bath Type              = isothermal        # or 'adiabatic'
   Allow Dissociation     = yes
   Allow Exchange         = yes               # master switch for all exchange channels
   Allow Exchange Arr 2   = yes               # per-channel switch (arr=2 = first exchange pair)
   Allow Exchange Arr 3   = yes               # per-channel switch (arr=3 = second exchange pair)
   Propagate Phase Space  = yes               # strategy (c): persistent atomic coords

Per-arrangement exchange flags
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For a 3-body system (A+BC) two exchange arrangements are defined:

- ``arr=2`` → product pair (atom 1, atom 3).  For NO+C: **CN+O** (Exchange 1).
- ``arr=3`` → product pair (atom 2, atom 3).  For NO+C: **CO+N** (Exchange 2).

For a 4-body system (AB+CD) arrangements 3..6 cover the four cross pairs.

Individual channels can be disabled to isolate a single reaction pathway.
Typical recipes for NO+C:

+--------------+------------------------+---------------------+
| Regime       | Allow Exchange         | Allow Arrangement   |
+==============+========================+=====================+
| exchange1    | ``yes``                | ``Arr 3 = no``      |
+--------------+------------------------+---------------------+
| exchange2    | ``yes``                | ``Arr 2 = no``      |
+--------------+------------------------+---------------------+
| exchange     | ``yes``                | (both on)           |
+--------------+------------------------+---------------------+

Integrator
----------

.. code-block:: text

   Integrator          = VV             # BS | VV
   VV Timestep [a.u.]  = 4.0

Species & pairs
---------------

Each species block defines one particle type (atom or diatomic molecule).
Example — NO + C with the UCI 4A2 PES:

.. code-block:: text

   Nb of Species = 2

   Species Name                = NO
   Species X                   = 0.5
   Species Tint [K]            = 300
   Species Levels File         = levels_NO.inp
   Species Is Molecule         = yes
   Species NAtoms              = 2
   Species Atom Name 1         = N
   Species Atom Mass 1 [a.u.]  = 25526.04298
   Species Atom Name 2         = O
   Species Atom Mass 2 [a.u.]  = 29148.94559
   Species Diatomic Model      = UCI
   Species gnuc Even J         = 1
   Species gnuc Odd J          = 1

   Species Name                = C
   Species X                   = 0.5
   Species Is Molecule         = no
   Species NAtoms              = 1
   Species Atom Name 1         = C
   Species Atom Mass 1 [a.u.]  = 21868.661757

   Nb of Collision Pairs = 1
   Collision Pair Species 1      = 1
   Collision Pair Species 2      = 2
   Collision Pair System         = CNO
   Collision Pair bmax [Bohr]    = 12.0
   Collision Pair PES Model 1    = UCI_4A2
   Collision Pair PES Degeneracy 1 = 0.11112
