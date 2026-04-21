H\ :sub:`2`\  + H\ :sub:`2`\  heat bath
========================================

The canonical 4-body (diatom + diatom) benchmark. PES: BMKP H4 via CoarseAIR.

Case tree
---------

.. code-block:: text

   run/H4/NoDissociation/<T>/
   run/H4/Dissociation/<T>/

The 4-body code path exercises:

- QCT integration with the full 4-atom Hamiltonian
- Arrangement detection with pair indices 1..6
- **Double-dissociation** handling (``arr = -2``) — four free atoms in one
  trajectory; this channel is disabled by default (``Allow Double
  Dissociation = no``) so DMS rates remain apples-to-apples with ME.

Running
-------

.. code-block:: bash

   cd run/H4/NoDissociation/10000K
   ./dmsAIR.sh 16

Expected output: inelastic and exchange events, no dissociation. Both pair 1
and pair 6 (the two initial diatoms) remain intact for the inelastic bulk
of events.

.. note::

   The H4 system uses ``Collision Pair NAtoms = 4`` and
   ``Nb of Species = 1`` (both diatomics are H\ :sub:`2`). The ``QCT_Detect_Arrangement``
   routine treats the ``n_short == 1`` case as single-dissociation and the
   ``n_short == 0`` case as double-dissociation.
