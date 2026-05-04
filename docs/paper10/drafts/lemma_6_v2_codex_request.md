# Codex review request: Lemma 6 v2 — re-review after Round A revisions

## Mode

**v2 confirmation review.** Round A returned "v2 needed" with Q2
($h_{\mathrm{detect}}$ definition) flagged as significant problem,
plus structural notes on Q1 (monitoring clock), Q3
($\rho_g$ vs. $K_{\mathrm{Lip}}$ double-counting), Q4 (union-class
KL floor), and Q5 (theorem-level surfacing).

V2 fixes:

- **Q1 fix.** (C11) reformulated in monitoring-clock form — discrete
  per-SPRT-step $(\Delta\epsgap)_n \leq \rhogap$ with explicit
  continuous variant $d\epsgap/ds \leq \rhogap$. SPRT exposure clock
  $s$ named as canonical clock; conversion to wall time is via
  event-rate normalization.
- **Q2 fix (the big one).** $h_{\mathrm{detect}}$ redefined as
  supremum gap, not integrated increment:
  $h_{\mathrm{detect}}(\theta) := \sup_{t} \epsgap(t) \leq
  \epsgap(t_0) + \rhogap \cdot T_{\mathrm{detect}}$, with boundary
  condition $\epsgap(t_0) \leq h_{\mathrm{static}}$ at the
  Layer 1$\to$2 crossing, giving final form
  $h_{\mathrm{detect}} \leq h_{\mathrm{static}} + \rhogap \cdot
  T_{\mathrm{cascade}}$ (with prob $\geq 1-\beta'$).
- **Q3 fix.** Renamed $\rho_g \to \rhogap$ to make explicit that
  (C11) bounds gap-growth rate (not alignment-property-error rate),
  eliminating double-counting concerns with $K_{\mathrm{Lip}}$.
- **Q4 fix.** Union-class KL floor $\deltastar = \min(\deltaadv,
  \delta_{\mathrm{adv}}^{\mathrm{env}})$ now used throughout; v1's
  $\deltaadv$-only formulation undercounted Layer 2's full detection
  class $\Aadv \cup \Aadv^{\mathrm{env}}$.
- **Q5 fix.** (C11) Bounded gap-growth rate explicitly framed for
  promotion to theorem-level condition, with operational
  interpretation and audit hook noted.
- **Source-citation correction.** Removed v1's overstatement that
  Paper 9's "$T$ failure modes" remark establishes the per-step
  gap-growth bound. (C11) is now framed as a new Paper 10
  operational assumption (analogous to (C7) bounded co-evolution and
  SA1 HHI surrogate adequacy), not a derived consequence.

## What to read

Primary:
- `docs/paper10/drafts/lemma_6_full_proof_v2.tex` — v2 (6pp PDF)

Reference:
- Round A findings: `lemma_6_full_proof.tex` v1 codex review output
- `docs/paper10/sections/main_theorem.tex` C1-C10 — where (C11) gets
  added
- `docs/paper10/appendices/proofs.tex` §A.4 (Lemma 4) — SPRT tail
  bound
- `docs/paper10/sections/lemmas.tex` §4.10 (Lemma 5d) — tail
  composition that v2 wants amended to use $\deltastar$
- `docs/paper10/sections/lemmas.tex` §4.11 (Lemma 5e) — environment-
  side KL floor source for $\delta_{\mathrm{adv}}^{\mathrm{env}}$

## What we want from you

Five v2 verification questions:

### Q1. Is the supremum-form $h_{\mathrm{detect}}$ definition correct, and does the boundary condition hold rigorously?

V2 redefines:
$h_{\mathrm{detect}}(\theta) := \sup_{t \in [t_0,t_0+T_{\mathrm{detect}}]} \epsgap(t)$
and bounds it by $\epsgap(t_0) + \rhogap \cdot T_{\mathrm{detect}}$,
with $\epsgap(t_0) \leq h_{\mathrm{static}}(\theta)$ via Layer 1.

**Question:** Is the boundary-condition argument
($\epsgap(t_0) \leq h_{\mathrm{static}}$ at the Layer 1$\to$2
crossing) watertight? Step 4 invokes "continuity (or single-step
boundedness under (C11))" to handle the moment of crossing. Does
this handle:

- (a) Continuous-time deployments where $\epsgap$ is a continuous
  function of $t$ — boundary equality $\epsgap(t_0) = h_{\mathrm{static}}$
  by continuity?
- (b) Discrete event-clock deployments where $\epsgap$ may jump by
  up to $\rhogap$ per SPRT step — boundary inequality
  $\epsgap(t_0) \leq h_{\mathrm{static}} + \rhogap$ via single-step
  boundedness?

The proof says "absorbing this into the bound" — should the final
bound include an explicit single-step buffer term, or is the
absorption justified by re-defining $T_{\mathrm{detect}}$ to start
from $t_0^-$?

### Q2. Is the SPRT-step monitoring-clock formulation of (C11) correctly stated?

V2 states (C11) primarily in discrete form $(\Delta\epsgap)_n \leq
\rhogap$ with continuous variant $d\epsgap/ds \leq \rhogap$, and
notes "the discrete and continuous forms agree under fixed step
duration or bounded event-rate normalization."

**Question:** Is fixed-step normalization a separate assumption that
should be named (e.g., (C11.FS) Fixed event-rate normalization), or
is it implicit in (C5) continuous SPRT monitoring? What about
deployments with bursty event rates where step duration varies — does
(C11)'s per-step bound translate cleanly to a wall-clock rate, or is
there a gap?

### Q3. Is the union-class KL floor $\deltastar$ the right composition for Layer 2?

V2 defines $\deltastar = \min(\deltaadv, \delta_{\mathrm{adv}}^{\mathrm{env}})$
to cover Layer 2's $\Aadv \cup \Aadv^{\mathrm{env}}$. The proof
remarks Lemma 5d as currently stated covers $\Aadv$ only, and
flags this as "a small amendment that should be made at integration."

**Question:** Is this the right composition?

- Option (a): Re-state Lemma 5d with $\deltastar$ throughout (the
  v2 plan). This requires editing §4.10.
- Option (b): Lemma 6 invokes Lemma 5b and Lemma 5e separately,
  then takes the minimum at the end. This keeps Lemma 5d narrow but
  makes Lemma 6's tail-bound chain longer.
- Option (c): Define $\deltastar$ as the deployment-class KL floor
  for the union class as a primary object, and let Lemma 5d be a
  union-class statement from the start.

Which framing is cleanest for the proof, and which integrates best
with the existing §4.10 / §4.11 / appendix §A.4 structure?

### Q4. Is the renaming $\rho_g \to \rhogap$ sufficient to clarify gap-growth vs. alignment-property-error?

V1 conflated $\rho_g$ (per-step alignment-property-error rate) with
$\rho_{\mathrm{gap}}$ (per-step proxy-truth gap-growth rate),
creating a double-counting risk with $K_{\mathrm{Lip}}$ in the Layer
2 operational form. V2 renames to $\rhogap$ and frames (C11) as
purely a gap-growth bound; Lipschitz multiplication by $K_{\mathrm{Lip}}$
is then a separate (C6) factor.

**Question:** Is the renaming sufficient, or does the proof require
additional changes (e.g., explicit decomposition of the gap into
channel-deviation magnitude vs. alignment-property mapping)? In
particular, does the gap-growth bound implicitly assume a smooth
$g$, or is it really independent of $g$'s smoothness?

### Q5. Should (C11) be a theorem-level condition or absorbed into (C5)?

V2 frames (C11) as ready for promotion to (C11) of Theorem 1, in
the (C6)-(C10) sequence. The trade-off:

- **Promotion (current draft).** Separate condition makes the
  assumption visible; audit hook (Audit 7) can target the gap-growth
  rate calibration directly.
- **Absorption into (C5).** Sub-clause of continuous SPRT monitoring
  keeps the condition list shorter; framing is "monitoring with
  bounded gap-growth rate."

**Question:** Which is the right design choice for Theorem 1's
condition surface? Pattern from Lemmas 1, 2, 5a was to add separate
conditions (C6), (C9), (C10) — does the same logic apply here, or is
(C11) sufficiently a property of the monitor (rather than a property
of the deployment substrate) to justify absorbing into (C5)?

## Output format

For each Q1-Q5:
- **Sound** — confirmation, ready for appendix integration with any
  minor refinements.
- **Issue identified** — name precisely; recommend whether v3 needed
  or addressable at integration.
- **Significant problem** — explain the obstruction.

If you find an issue we did not name, flag it.

## Goal

Settle whether Lemma 6 v2 is ready for appendix integration. If yes,
proceed to next TODO item (Lemma 5e environment-side KL floor
appendix promotion). If v3 needed, revise.
