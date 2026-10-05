1D Couette and Fourier flows
============================

Wall-bounded 1D flows with the ``dmsAIR_Flow1D`` solver: a planar channel
between two Maxwell walls, sharing the collision machinery, input format
and level databases with the 0D heat bath. Full solver documentation:
:doc:`/user/flow1d`.

Two ready-to-run H₂ + He cases are distributed:

.. code-block:: text

   run/Flow1D/Couette_H2He/     # opposed wall motion -> shear-driven flow
   run/Flow1D/Fourier_H2He/     # wall temperature difference -> heat conduction

Couette flow
------------

The two walls move in opposite tangential (*y*) directions at equal
temperature; the observables are the velocity profile
:math:`u_y(x)`, the velocity slip at the walls and the shear stress.

.. code-block:: text

   # run/Flow1D/Couette_H2He/dmsAIR.inp (key excerpts)
   Translational Temperature [K] = 300      # initial gas state
   Internal Temperature [K]      = 300

   Domain Length [m]           = 5.0e-5
   Nb of Cells                 = 30
   Wall Left Temperature [K]   = 300
   Wall Right Temperature [K]  = 300
   Wall Left Velocity Y [m/s]  = -500
   Wall Right Velocity Y [m/s] = 500
   Wall Accommodation          = 1.0        # fully diffuse walls
   Wall Internal Accommodation = 1.0

   Nb of Particles = 4000
   Bath Type       = adiabatic              # REQUIRED for Flow1D

   Collision Pair System = H2He             # same QCT machinery as 0D

Fourier flow
------------

Same channel, walls at rest with a temperature difference; the
observables are the temperature profile :math:`T(x)`, the temperature
jumps at the walls and the wall heat flux.

.. code-block:: text

   # run/Flow1D/Fourier_H2He/dmsAIR.inp (differences from Couette)
   Translational Temperature [K] = 650      # start near the mean
   Internal Temperature [K]      = 650
   Wall Left Temperature [K]   = 300
   Wall Right Temperature [K]  = 1000
   Wall Left Velocity Y [m/s]  = 0
   Wall Right Velocity Y [m/s] = 0

What the solver does with this
------------------------------

- ``Bath Type = adiabatic`` is mandatory: particle velocities persist
  between steps (no Maxwellian resampling), so gradients can develop.
  The x-direction is discretised into ``Nb of Cells`` uniform cells used
  for NTC pair selection and for sampling.
- Walls are Maxwell boundaries: with ``Wall Accommodation = 1.0`` every
  wall encounter re-emits the particle diffusely at the wall state;
  ``Wall Internal Accommodation`` controls whether the molecular (v, j)
  is also resampled at the wall temperature.
- Collisions run through the same QCT pipeline as the heat bath, so
  transport coefficients emerge from the *ab initio* PES with no
  viscosity or conductivity model.

Since only the H₂ + He pair is declared, the enabled processes are
rovibrational energy transfer (no exchange channel, dissociation off) —
the transport analogue of the
:doc:`H2+He heat bath </examples/h2he_heatbath>`.

Running
-------

.. code-block:: bash

   make flow1d                       # builds build/bin/dmsAIR_Flow1D
   cd run/Flow1D/Couette_H2He
   mpirun -np 4 ../../../build/bin/dmsAIR_Flow1D dmsAIR.inp

Output: ``profiles.csv`` (one row per cell per output interval —
:math:`u_y`, T components, density per cell) and ``walls.csv`` (slip /
jump, shear stress ``tau`` exerted by the gas on the wall, heat flux
``q`` from gas to wall). Discard the transient with
``Sampling Start Step`` and average the steady-state windows; see
:doc:`/user/flow1d` for the column conventions and the validation against
analytic slip/jump solutions.
