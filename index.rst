dmsAIR — Direct Molecular Simulation for Atmospheric Interactions and Reactions
=================================================================================

**dmsAIR** is a massively parallel Fortran code for simulating nonequilibrium
gas dynamics at the molecular level. It resolves individual collisions between
atoms and molecules by running quasi-classical trajectory (QCT) calculations
on *ab initio* potential energy surfaces (PES), within the Direct Simulation
Monte Carlo (DSMC) statistical framework.

The code targets **hypersonic re-entry** and **high-enthalpy flow**
applications where the internal energy distribution of molecular species
departs from thermodynamic equilibrium — conditions where conventional rate
models break down and state-resolved physics is required.

.. note::

   dmsAIR is developed at the University of California, Irvine, in the
   `HERMES Aerospace research group <https://hermes-aerospace.github.io/>`_
   led by Prof. Marco Panesi. It is released under the
   `MIT License <https://github.com/ClementCivrais/dmsAIR/blob/main/LICENSE>`_.

.. toctree::
   :maxdepth: 2
   :caption: User Documentation

   user/getting_started
   user/installation
   user/running_simulations
   user/input_reference
   user/postprocessing

.. toctree::
   :maxdepth: 2
   :caption: Theory Guide

   theory/dms
   theory/qct
   theory/ntc
   theory/integrators
   theory/bath_types
   theory/reactive_channels

.. toctree::
   :maxdepth: 2
   :caption: Examples Guide

   examples/h3_heatbath
   examples/noc_heatbath
   examples/h4_heatbath
   examples/scattering_map
   examples/integrator_study

.. toctree::
   :maxdepth: 2
   :caption: Reference

   reference/about
   reference/validation
   reference/changelog
   reference/bibliography

.. toctree::
   :maxdepth: 2
   :caption: Developer Documentation

   developer/architecture
   developer/adding_a_system
   developer/regression_tests
   developer/roadmap

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
