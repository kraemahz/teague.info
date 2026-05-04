# Codex review request: Lemma 6 v4 — re-review after Round C revisions

## Mode

**v4 confirmation review.** Round C returned "v4 needed" with one
significant problem (Q1: $\Tbeta$ algebra didn't match Lemma 4's
Hoeffding form) plus four issues (Q2 boundary leak, Q3 weak (C11.CLK),
Q4 mislabeled $\beta'$, Q5 incomplete constant taxonomy).

V4 fixes:

- **Q1 algebra fix (the significant problem).** Rederived $\Tbeta$
  directly from Lemma 4's exact Hoeffding form
  $\Pr[T_{\mathrm{detect}} > t] \leq \exp(-2(t\delta - A)^2/(tR^2))$.
  Result: $\Tbeta = \max\{2A/\deltastar,
  R^2\log(1/\beta)/(2\deltastar^2)\}$. The asymptotic regime gives
  $\Tbeta \sim 1/\deltastar^2$, not $1/\deltastar$. Surfaces $R$
  via (C5.HOEFF) and $A$ via Paper 5 SPRT threshold.

- **(C5.HOEFF) added.** Bounded LLR-increment range as deployment-
  class condition: $|\ell_n| \leq R$ a.s. with $R$ independent of
  $|P|$ via channel-multiplicity policy.

- **Q3 fix: (C11.CLK) strengthened.** Replaced existence-only form
  ($N_{\min}, q_{\min}$) with: deterministic $\Ncasc$ + named
  failure probability $\bclk$ such that $\Pr[\Nev(\tau_{\mathrm{meta}})
  \geq \Ncasc] \geq 1 - \bclk$, with audit constraint $\Ncasc \geq
  \Tbeta$. This makes $\Tbeta \leq \tau_{\mathrm{meta}}$ operational
  with named probability $1-\bclk$, not just bounded throughput.

- **Q4 fix: $\beta'$ relabeled.** Dropped v3's incorrect use of
  $\beta' = \exp(-\kappa\tau_{\mathrm{meta}}\deltastar)$ (an SPRT
  detection-tail form) for cascade-clock event. V4 uses $\bclk$
  from (C11.CLK) instead, with total Layer 2 failure $\leq \beta +
  \bclk$.

- **Q5 fix: constant taxonomy completed.** Surfaced $\alpha$ (Type-I,
  monitor parameter), $R$ (LLR range, (C5.HOEFF)), $\Ncasc, \bclk$
  ((C11.CLK)), $A = \log((1-\beta)/\alpha)$ (SPRT threshold), with
  multiplicity bookkeeping via (C5.HOEFF).

- **Q2 integration note carried.** $t_0 := t_0^-$ convention
  internal to Lemma 6 is sufficient; integration must update
  Theorem 1's Layer 2 proof to express the transition in SPRT
  exposure clock.

## What to read

Primary:
- `docs/paper10/drafts/lemma_6_full_proof_v4.tex` — v4 (10pp PDF)

Reference:
- Round C findings: `b5f25ecvr.output` lines 2581-2647
- `docs/paper10/appendices/proofs.tex` §A.4 (Lemma 4) — exact
  Hoeffding form that v4 inverts
- `docs/paper5/sections/commitment.tex` line 319 — Paper 5 SPRT
  threshold $A = \log((1-\beta)/\alpha)$

## What we want from you

Five v4 verification questions:

### Q1. Is the v4 $\Tbeta$ derivation algebraically correct?

V4 inverts Lemma 4's asymptotic Hoeffding bound:
$\exp(-2T\deltastar^2/R^2) \leq \beta \Rightarrow T \geq R^2 \log(1/\beta)/(2\deltastar^2)$.

The full $\Tbeta = \max\{2A/\deltastar,
R^2\log(1/\beta)/(2\deltastar^2)\}$ ensures both regimes covered.

**Question:** Is this derivation rigorous? In particular:
- Is the asymptotic approximation $2(t\deltastar - A)^2/(tR^2)
  \approx 2t\deltastar^2/R^2$ for $t\deltastar \gg A$ sufficient,
  or does the proof need to invert the exact form?
- Is the $1/\deltastar^2$ scaling correctly captured (the v3 mistake
  was the $1/\deltastar$ scaling)?
- Does the $\max$-form correctly handle the regime where
  $A/\deltastar$ dominates (small $\beta$ or large $\alpha$)?

### Q2. Is (C5.HOEFF) the right framing for bounded LLR range?

V4 adds (C5.HOEFF): $|\ell_n| \leq R$ a.s. with $R$ deployment-class
and channel-multiplicity bounded.

**Question:** Does this correctly handle:
- (a) Fixed four-channel monitoring (Paper 5 default)?
- (b) Environment-side mirror channels (Paper 10 Lemma 5e)?
- (c) Multinomial channel partitions where multiplicity could grow
  with $|P|$?

The clause says "channel partition is either fixed or family-wise
corrected." Is family-wise correction (e.g., Bonferroni) the right
mechanism, or does the bound need stronger assumptions like
fixed-cardinality channel sets?

### Q3. Is (C11.CLK) v4 form sufficient?

V4 has two parts:
- (1) $\Pr[\Nev(\tau_{\mathrm{meta}}) \geq \Ncasc] \geq 1 - \bclk$
- (2) Audit constraint: $\Ncasc \geq \Tbeta$

Step 7 of the proof chains $\Tbeta \leq \Ncasc \leq
\Nev(\tau_{\mathrm{meta}})$.

**Question:** Is this watertight? In particular:
- Does the audit-time inequality $\Ncasc \geq \Tbeta$ need
  probabilistic treatment if calibration is imperfect, or is
  treating it as a hard constraint (with operational responsibility
  on the operator) acceptable?
- Does $\bclk$ need to compose with calibration-error probability
  separately, or is the operator audit responsibility sufficient
  to make $\bclk$ purely about event-throughput tail?

### Q4. Is the probability labeling now unambiguous?

V4 dropped v3's $\beta' = \exp(-\kappa\tau_{\mathrm{meta}}\deltastar)$
for cascade-clock. The v4 labels:
- $\beta$ — SPRT detection-tail probability
- $\bclk$ — clock-calibration failure probability
- Total Layer 2 failure $\leq \beta + \bclk$

**Question:** Are there any places where v3's $\beta'$ might re-enter
through Lemma 5d composition? Lemma 5d (currently in §4.10) uses
$\beta' = \exp(-\kappa\tau_{\mathrm{meta}}\deltaadv)$ as its tail
bound. At integration, will the union-class amendment cleanly drop
$\beta'$ from this lemma, or will Lemma 5d's $\beta'$ leak into
Theorem 1's Layer 2 proof and conflict with v4's $\bclk$?

### Q5. Is the constant taxonomy now complete?

V4 enumerates: $h_{\mathrm{static}}, \rhogap, \Tbeta, A, \alpha,
\beta, R, \Ncasc, \bclk, \tau_{\mathrm{meta}}, T_{\mathrm{cascade}}$.

**Question:** Are there remaining hidden $|P|$-dependent constants?
In particular:
- $\alpha$ is treated as monitor-design parameter; is its
  deployment-class status sufficient via (C5)'s monitoring framing,
  or does $\alpha$ need its own named clause?
- Is the channel-multiplicity policy adequately surfaced via
  (C5.HOEFF), or does it need a separate (C5.MULT) clause?
- Are there constants in the SPRT machinery (e.g., the LLR's
  measurability, finiteness of moments) that we've assumed without
  surfacing?

## Output format

For each Q1-Q5:
- **Sound** — confirmation, ready for appendix integration with any
  minor refinements.
- **Issue identified** — name precisely; recommend whether v5 needed
  or addressable at integration.
- **Significant problem** — explain the obstruction.

If you find an issue we did not name, flag it.

## Goal

Settle whether Lemma 6 v4 is ready for appendix integration. The
v4 changes from v3 are substantial (algebra correction, two new
clauses (C5.HOEFF) and strengthened (C11.CLK), probability
relabeling). If clean, proceed to integration. If v5 needed, revise.
