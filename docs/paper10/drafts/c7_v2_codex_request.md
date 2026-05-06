# Codex review request: C7 closed-form derivation v2

## Context

This is v2 of the C7 closed-form derivation in
`drafts/c7_closed_form_v2.tex`. The goal is to prove (C7) bounded
co-evolution as a corollary of (C5.HOEFF), (C5.MULT), a new
structural sub-clause (C5.OVL), and (C11)'s action rate cap, rather
than asserting it as a free-floating deployment-class assumption.

v1 (in `c7_closed_form.tex`) had two P0 issues:

1. Definition inconsistency: $M_{j \to j'}$ defined as total drift
   from baseline, but Step 4 excluded $j'$-only drift as
   "not coupling." Counterexample available.
2. Per-step vs cumulative semantic mismatch: v1 proved per-step
   bound but Audit 4 / Microfoundation $K_{\mathrm{coev}}$ are
   cumulative.

Plus 5 P1 issues (Step 4 false equality, LLR support vs.
incidence, $q_0$ shared mass, $Q^*$ intensivity not from
(C5.MULT) alone, single $q_0$ compatibility).

## v2 changes

1. **L1-normalized Lipschitz definition** of
   $M_{j \to j'}^{\mathrm{step}}$
   (Definition 3 / equation eq:M-def-v2): maximum $j'$-drift
   response per unit-$\ell_1$ $j$-perturbation, restricted to
   $j$-supported signed measures. This is a Lipschitz formulation
   that avoids the denominator-vanishing problem of naive
   Lipschitz definitions.

2. **Cumulative bound directly** (Lemma 2): aggregates per-step
   bound over $\Nev(\taumeta) \leq \lammax \cdot \taumeta$ events.
   This matches Audit 4's "within $\taumeta$" phrasing.

3. **Structural channel-incidence map** $I_j: A \to \{0, 1\}$
   separate from LLR support. Convention: $\ell^{(j)}(a) = 0$ for
   $a \notin A_j$ by structural extension.

4. **Baseline compatibility** assumption (Assumption 1): $q_0$'s
   conditional distributions on each $A_j$ equal $p_0^{(j)}$.

5. **New structural sub-clause (C5.OVL)** (Assumption 2):
   $\sup_{|P|} \sup_q \sum_{a \in A_{j,j'}} |q(a)| \leq Q_{\max} <
   1$. This makes the $Q^*$ intensivity claim explicit rather than
   implicit.

6. **Cumulative coupling bound** (equation
   eq:cumulative-bound):
   $$\bar{M}^{\mathrm{cum}}(\mathcal{D}) \leq \Bclip \cdot
   Q^*(\mathcal{D}) \cdot \lammax \cdot \taumeta$$
   where each factor is deployment-class intensive.

## Review focus

Please read `c7_closed_form_v2.tex` and check whether:

1. **Is the L1-normalized Lipschitz definition the right
   operational reading of Audit 4?** v1's reviewer noted Audit 4 is
   windowed; v2 splits per-step (Definition 3) and cumulative
   (Lemma 2). Is the L1-normalized per-step version a reasonable
   intermediate, or should the proof go directly to cumulative?

2. **Does the per-step bound (Lemma 1) actually go through?** I
   used $|\Delta\mu_{j'}[\Delta]| \leq \Bclip \cdot \|\Delta\|_1 \leq
   \Bclip$ (then tighter via $Q^*$). Are there any admissible
   $\Delta$ that violate this?

3. **Does the cumulative aggregation (Lemma 2) match what
   $K_{\mathrm{coev}}$ requires?** I assumed sum-over-events
   aggregation. Microfoundation's $K_{\mathrm{coev}}$ might use a
   different aggregation (supremum, integral, etc.); if so, the
   cumulative bound's aggregation step needs revising.

4. **Is the structural incidence map convention valid?** I require
   $\ell^{(j)}(a) = 0$ for $a \notin A_j$, treating channel
   classification as a structural property. Does this hold for the
   four-channel structure of Lemma 5b? (Poisson cooperative-rate,
   Bernoulli attestation, two multinomial concentrations.)

5. **Is (C5.OVL) a reasonable addition?** The new sub-clause makes
   the load-bearing structural condition explicit. Alternatives:
   (a) leave $\bar{M}$ free-floating (v1 / current paper posture);
   (b) derive (C5.OVL) from a deeper condition. Which posture
   serves the deployment-claim's epistemic transparency best?

6. **Does the pairwise-only bound suffice for the
   cooperative-overlap regime?** Lemma 5c involves multi-substrate
   dynamics with simultaneous channel co-evolution. Does the
   cumulative bound's pairwise structure capture what
   Microfoundation's composition correction term actually requires,
   or is a higher-order overlap bound needed?

7. **Are the v1 P0/P1 fixes adequately addressed?** v2 explicitly
   addresses the v1 P0-1 (definition inconsistency), P0-2 (per-step
   vs cumulative), P1-3 (Step 4 false equality), P1-4 (LLR vs
   incidence), P1-5 ($Q_\Delta^*$ formulation), P1-6 ($Q^*$
   intensivity), P1-7 ($q_0$ compatibility), P2-8 (pairwise
   terminology). Is each addressed adequately?

## Format

For each finding:
- [P0] Critical: proof is wrong / closed form doesn't deliver C7
- [P1] Substantive: proof has gaps, definitions have issues, or
  v1 issues not adequately addressed
- [P2] Polish: presentation could be clearer

For each: line reference into `c7_closed_form_v2.tex`, problem
description, suggested fix. Be specific. Aim for 5-10 findings.
Skip findings that are pre-existing v1 issues already addressed in
v2 unless v2's fix is incorrect.

Output the findings list directly with no preamble.
