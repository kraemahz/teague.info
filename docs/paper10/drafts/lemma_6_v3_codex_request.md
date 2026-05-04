# Codex review request: Lemma 6 v3 — re-review after Round B revisions

## Mode

**v3 confirmation review.** Round B returned "v3 needed" with one
significant problem ($T_{\mathrm{cascade}}$ used as upper bound when
the source result gives only a lower bound) plus two issues (Q1
discrete boundary not rigorous; Q2 clock comparability not in (C5)).

V3 fixes:

- **Significant problem fix.** Introduced
  $\Tbeta := (\log(1/\alpha) + \log(1/\beta)) / (\kappa \deltastar)$
  as the SPRT high-probability detection quantile (a legitimate
  *upper* bound on $T_{\mathrm{detect}}$ via Lemma 4's
  Wald–Hoeffding tail). Replaced $T_{\mathrm{cascade}}$ as the
  integration horizon for $\rhogap$. The lemma now has two parts:
  - (ii) supremum bound: $h_{\mathrm{detect}} \leq h_{\mathrm{static}}
    + \rhogap \cdot \Tbeta$ with prob $\geq 1-\beta$
  - (iii) lead-time-before-cascade: $\Tbeta \leq \tau_{\mathrm{meta}}
    \leq T_{\mathrm{cascade}}$ with prob $\geq 1-\beta'$
  This separates the two roles of cascade time previously conflated.
- **Q1 fix.** Adopted $t_0 := t_0^-$ convention (last safe SPRT
  step before crossing). Now $\epsgap(t_0) \leq h_{\mathrm{static}}$
  is rigorous without "absorbed buffer" handwaving.
- **Q2 fix.** Added (C11.CLK) named sub-clause: detection and
  cascade times expressed in SPRT exposure clock with calibrated
  high-probability lower bound on event count before cascade.
- **Q4 reinforcement.** Added explicit statement that $\rhogap$ is
  calibrated in $\epsgap$ metric and excludes $K_{\mathrm{Lip}}$.

Round B confirmed Q3 (union-class $\deltastar$) and Q5 (promote
(C11) to theorem-level) as Sound; carried forward unchanged.

## What to read

Primary:
- `docs/paper10/drafts/lemma_6_full_proof_v3.tex` — v3 (8pp PDF)

Reference:
- Round B findings: `b6jn9c92a.output` lines 2559-2615
- `docs/paper10/sections/main_theorem.tex` C1-C10 — where (C11) and
  (C11.CLK) get added
- `docs/paper10/appendices/proofs.tex` §A.4 (Lemma 4) — Wald–Hoeffding
  tail bound that defines $\kappa$
- `docs/paper10/sections/lemmas.tex` §4.10 (Lemma 5d) — needs
  union-class amendment at integration (option (c) per Round B)

## What we want from you

Five v3 verification questions:

### Q1. Is the $T_{\mathrm{cascade}} \to \Tbeta$ replacement rigorous?

V3's key fix. $\Tbeta = (\log(1/\alpha) + \log(1/\beta)) /
(\kappa \deltastar)$ comes from Lemma 4's Wald–Hoeffding tail
$\Pr[T_{\mathrm{detect}} > T] \leq \exp(-\kappa T \deltastar)$
solved at level $\beta$.

**Question:** Is the constant-tracking correct? Specifically:

- Is $\kappa$ (the sub-Gaussian/Hoeffding constant of the SPRT
  log-likelihood per step) truly a deployment-class constant, or
  could it depend on $|P|$ via channel-model multiplicity (e.g., if
  more capabilities $\Rightarrow$ more channels $\Rightarrow$
  higher per-step variance)?
- Is the intensivity argument for $\Tbeta$ in Step 7 sound, or do we
  need to surface a (C5) sub-clause that $\kappa$ is intensive?
- Does the form $\Tbeta = O(1/\deltastar)$ correctly capture the
  Wald–Hoeffding scaling, or is there a $\log$ factor missing?

### Q2. Is the discrete boundary convention ($t_0 := t_0^-$) sufficient?

V3 defines $t_0$ as the last safe SPRT step before crossing,
making $\epsgap(t_0) \leq h_{\mathrm{static}}$ exact. The first
crossing event occurs at $s_1$, with single-step jump bounded by
$\rhogap$ via (C11).

**Question:** Does this leak into Theorem 1's Layer 1$\to$Layer 2
transition statement? Currently Theorem 1's Layer 1 proof talks
about the safe region in continuous-time language; does Lemma 6's
discrete boundary convention require the theorem-level proof to
adopt the same convention, or is the convention purely
internal to Lemma 6?

### Q3. Is (C11.CLK) the right framing for clock comparability?

V3 treats (C11.CLK) as a sub-clause of (C11), bundling
gap-growth-rate-per-step with event-count-floor.

**Question:** Are these two assertions:
- (C11) per-step gap-growth bound
- (C11.CLK) event-count floor before cascade

tight enough conceptually to bundle into one condition (C11) with
sub-clauses, or are they orthogonal deployment properties that
deserve separate top-level conditions (C11) and (C12)? The pattern
from (C9) [BD/CL/WB/TF] and (C10) [CN/SU] supports sub-clause
bundling when conditions share the same calibration audit; (C11)
and (C11.CLK) would share Audit 7. Does that justify bundling?

### Q4. Is the union bound composition $\beta + \beta'$ in the Layer 2 operational form correct?

V3 has Lemma 6(ii) at confidence $1-\beta$ and Lemma 6(iii) at
confidence $1-\beta'$. The Layer 2 operational form composes these
via union bound: total failure probability $\leq \beta + \beta'$.

**Question:** Is this the right composition? The two events:
- $E_1 = \{T_{\mathrm{detect}} \leq \Tbeta\}$ (prob $\geq 1-\beta$)
- $E_2 = \{\Tbeta \leq \tau_{\mathrm{meta}}\}$ (prob $\geq 1-\beta'$)

For Layer 2 to deliver "detection completes before cascade with
bounded gap", we need $E_1 \cap E_2$. Union bound gives
$\Pr[E_1^c \cup E_2^c] \leq \beta + \beta'$. But are $E_1$ and
$E_2$ independent or correlated through the channel-model
structure? If correlated (e.g., both driven by the same noise),
the bound could be tighter; if anti-correlated, the union bound
might be loose but still valid.

### Q5. Is the constant taxonomy now complete?

The Discussion section enumerates $h_{\mathrm{static}}$, $\rhogap$,
$\Tbeta$, $\tau_{\mathrm{meta}}, T_{\mathrm{cascade}}$, $\beta$,
$\beta'$.

**Question:** Are there any remaining hidden $|P|$-dependent
constants in $\Tbeta$, $\rhogap$, or the SPRT parameters that we
haven't surfaced? In particular:

- Does $\alpha$ (Type I error) need to be surfaced as a
  deployment-class parameter or is it purely a monitor design
  choice?
- Does the conversion from SPRT exposure clock to wall-clock time
  introduce any $|P|$-dependent constants beyond (C11.CLK)?
- The constant $\kappa$ in Wald–Hoeffding: should we name a
  (C5.HOEFF) sub-clause asserting $\kappa$ is intensive over
  $\mathcal{D}$?

## Output format

For each Q1-Q5:
- **Sound** — confirmation, ready for appendix integration with any
  minor refinements.
- **Issue identified** — name precisely; recommend whether v4 needed
  or addressable at integration.
- **Significant problem** — explain the obstruction.

If you find an issue we did not name, flag it.

## Goal

Settle whether Lemma 6 v3 is ready for appendix integration. If yes,
proceed to the integration step (which will: add §A.7 with v3 proof,
add (C11) with sub-clauses to Theorem 1, amend Lemma 5d to union-
class option (c), update Theorem 1's Layer 2 proof to use $\Tbeta$
and remove the v1 source-citation overstatement, add Audit 7 to §8
deployment tooling). If v4 needed, revise.
