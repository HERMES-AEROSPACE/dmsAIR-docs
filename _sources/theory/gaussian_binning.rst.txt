Gaussian binning
================

*Added 2026-08-13.*

Why
---

DMS propagates **continuous classical** trajectories, but state-resolved
comparisons (and the master-equation references) live on the **quantised
rovibrational ladder**. The mapping between the two is a binning step: the
semiclassical actions returned by the trajectory,

.. math::

   v_{\mathrm{cl}} = \texttt{viba} - \tfrac{1}{2}, \qquad
   j_{\mathrm{cl}} = \texttt{AngMom} - \tfrac{1}{2},

are rounded to the nearest integers (*histogram binning*). Far above
threshold this is harmless. Near threshold — a stiff diatomic colliding with
a weak partner at :math:`T \lesssim \theta_v`, e.g. H\ :sub:`2` + He — it is
not:

1. **Sub-quantum transfer.** The classical oscillator absorbs fractions of a
   quantum per collision; carried between collisions this accumulates into a
   vibrational channel that quantum mechanics forbids (excitation requires a
   full quantum in one collision).
2. **Detailed-balance breakage.** Rounding treats near-threshold upward and
   downward transitions asymmetrically. The binned kernel's up/down rate
   ratio falls below the detailed-balance value; because the net relaxation
   flux is the small difference :math:`F_\uparrow - F_\downarrow`, a
   per-line deficit of a few percent is amplified several-fold in the
   relaxation time.

The master equation never has this problem: its kernels are completed by
detailed balance line-by-line, by construction.

What
----

Gaussian binning (GB; Bonnet & Rayez) replaces the hard rounding with a
quantisation *filter*: a trajectory outcome is weighted by how close its
final action lands to an integer. dmsAIR implements the accept/reject form —
after the product level :math:`(v', j')` is assigned, the collision outcome
is **accepted** with probability

.. math::

   p \;=\; \exp\!\left[-\left(
       \frac{v_{\mathrm{cl}} - v'}{\varepsilon_v}\right)^2\right]
   \;\times\;
   \underbrace{\exp\!\left[-\left(
       \frac{j_{\mathrm{cl}} - j'}{\varepsilon_j}\right)^2\right]}_{
       \text{only if } \varepsilon_j > 0}

(one draw per trajectory; for diatom–diatom collisions both molecules'
factors multiply). A rejected outcome is a **no-collision**: both particles
keep their pre-collision state.

Trajectories that land *on* a quantum state pass untouched; classically
allowed but quantum-mechanically half-forbidden mid-ladder outcomes are
discounted. Exchange reactions, which deposit whole quanta, are essentially
unaffected — which makes an exchange-dominated system (H\ :sub:`2` + H) the
natural null control.

Representation and energy conservation
--------------------------------------

``Gaussian Binning = yes`` **forces quantum-number carry ON**
(``Propagate Phase Space`` is overridden): continuous phase-space carry
between collisions *is* the sub-quantum channel GB exists to remove, so GB
on top of it would be inconsistent. Unlike the bare QN-carry diagnostic
mode, GB conserves energy per collision: the difference between the
continuous internal energy and the tabulated level energy (the "snap") is
paid from the products' relative translational energy, by rescaling both
product centre-of-mass velocities in the collision frame with a common
factor (momentum-preserving). If the products cannot pay, the outcome is
rejected and counted separately.

Normalisation caveat
--------------------

Bonnet's GB weight carries a :math:`1/(\varepsilon\sqrt{\pi})` prefactor
(unit mean over a uniformly distributed action). An accept/reject scheme
cannot represent weights above one, so committed rates equal the true GB
rates times a factor that is :math:`\approx \varepsilon\sqrt{\pi}`
(:math:`\approx 0.18` at :math:`\varepsilon = 0.1`) for lines whose
classical final-action distribution is smooth across the bin — but
:math:`\approx 1` for lines fed by classically complete jumps (exchange).
Detailed-balance *ratios* and kernel *shape* are unaffected where the
up/down lines share the same character; absolute relaxation times must be
interpreted through the measured kernel, not read off the raw clock.

Diagnostics
-----------

The end-of-run log reports::

   [GB] outcomes accepted: N   rejected (Gaussian draw): N   rejected (snap dE unpayable): N
   [GB] acceptance fraction: f

At production settings (:math:`\varepsilon_v = 0.1`, large ``bmax``) the
acceptance fraction is close to 1 — the trajectory ensemble is dominated by
grazing, near-elastic encounters that land on-quantum. The filter's effect
concentrates on the rare near-threshold inelastic outcomes, which is where
the histogram artifact lives.

Input keys
----------

.. code-block:: text

   Gaussian Binning = yes
   GB Epsilon Vib   = 0.10     # width in vibrational action [quanta]
   GB Epsilon Rot   = 0.0      # 0 = rotation stays histogram-binned

See the :doc:`/examples/h2he_heatbath` example for a production GB case.
