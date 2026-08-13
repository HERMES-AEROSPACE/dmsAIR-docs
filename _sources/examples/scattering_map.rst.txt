Scattering Map — selecting ``bmax``
====================================

The ``dmsAIR_ScatteringMap`` binary runs a dense grid of fixed-``(b, E)``
QCT trajectories and reports the mean deflection angle ⟨\|χ\|⟩ per channel.
This is how every new collision system's ``bmax`` is calibrated before
production runs.

Running
-------

.. code-block:: bash

   cd run/ScatteringMap/H2_H_v0j0
   ./run.sh

Each case dir contains:

- ``dmsAIR.inp`` — copied from the matching heat-bath case
- ``scatmap.inp`` — (b, E) grid parameters: ``Nb``, ``b_min``, ``b_max``,
  ``NE``, ``E_min_K``, ``E_max_K``, ``iState``, ``N_traj``
- ``levels_*.inp`` — rovibrational level tables
- ``ScatteringMap.dat`` — 24-column output per (b, E) row (channel-resolved)

Output columns
--------------

Per (b, E) row:

- 0-5:   b, E_eV, E_K, n_tot, ⟨\|χ\|⟩_tot, σ_tot
- 6-7:   n_I, ⟨\|χ\|⟩_I        (inelastic)
- 8-9:   n_Ex, ⟨\|χ\|⟩_Ex      (exchange)
- 10-11: n_DDs, ⟨\|χ\|⟩_DDs    (single diss)
- 12-13: n_DDd, ⟨\|χ\|⟩_DDd    (double diss, 4-body only)
- 14-23: arr2..arr6 per-arrangement (n, ⟨\|χ\|⟩) pairs

Plotting
--------

.. code-block:: bash

   python3 postprocessing/ScatteringMap/plot_chi_contour_v2.py
   python3 postprocessing/ScatteringMap/plot_chi_surface3d.py --family hydrogen_v0j0

Produces 2D jet-colormap contours with the ⟨\|χ\|⟩ = 1° iso-contour
overlaid. The rightmost b where ⟨\|χ\|⟩ ≥ 1° defines the practical
``bmax`` for that energy. A power-law fit ``bmax = a·E^b`` is produced by:

.. code-block:: bash

   python3 postprocessing/ScatteringMap/plot_bmax_powerlaw.py

For Langevin-capture neutral-neutral scattering the exponent is close to
:math:`-1/6` (V ∝ r\ :sup:`−6` van der Waals tail). Steeper exponents flag
a potential-barrier system; flatter flag hard-wall saturation.

bmax convergence study (2026-07)
--------------------------------

A dedicated b × E sweep (``run/BmaxSweep/``) verified the production
``bmax`` cut-offs for H3 (H2+H), H4 (H2+H2) and H2He against a
momentum-transfer criterion: the cut-off must sit beyond the impact
parameter where ⟨\|χ\|⟩ falls below 1° at the lowest thermally relevant
collision energy. All three production values were confirmed
**conservative**; H4 is the tightest margin (at 300 K). The
``chi(b, E)`` colormaps with the 1° isoline, the power-law fit and the
selected-``bmax`` cut-off line are produced by the plotters above and
stored under ``postprocessing/ScatteringMap/Figures/``.

Convergence clipping
--------------------

The plotters accept ``--conv-thr 0.5`` and ``--conv-smooth 1.0`` to mask
``(b, E)`` cells where too few trajectories converged within ``tmax``
(long-lived-complex territory). A Gaussian smoothing of the
convergence-fraction map cleans up single-cell speckle before thresholding.
