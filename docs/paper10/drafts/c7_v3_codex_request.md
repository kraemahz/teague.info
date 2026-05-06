# Codex review request: C7 closed-form derivation v3

## Context

This is v3 of the C7 closed-form derivation in
`drafts/c7_closed_form_v3.tex`. The goal is to derive (C7) bounded
co-evolution as a corollary rather than an assumption, so the
loose thread (C7) represents in Paper 10's deployment claim
disappears.

Progression:
- v1 (`c7_closed_form.tex`): 2 P0 + 5 P1 + 1 P2 = 8 findings
- v2 (`c7_closed_form_v2.tex`): 1 P0 + 6 P1 + 1 P2 = 8 findings
- v3 (this draft): aiming for convergence

v3 addresses all 8 v2 findings explicitly:

1. **P0-1 (rate cap):** v2 used (C11.CLK) as upper rate cap, but
   it's actually a lower throughput floor. v3 introduces (C7.RATE)
   as a separate upper exposure-rate cap.

2. **P1-2 (Lipschitz normalization):** v2 used $\sup_{\|\Delta\|_1
   \leq 1}$. v3 uses $\sup_{\Delta \neq 0} |\Delta\mu_{j'}|/
   \|\Delta\|_1$, the proper operator norm.

3. **P1-3 (Poisson rate shifts):** v2's zero-sum $\Delta$ couldn't
   represent rate changes. v3 introduces an idle action $a_0$ so
   rate shifts are representable as redistributions including the
   idle bucket.

4. **P1-4 (pairwise vs aggregate):** v2 used pairwise max only. v3
   states both pairwise (factor $C = 1$) and aggregate-incoming
   (factor $C = \Kch - 1$) bounds.

5. **P1-5 ((C5.OVL) optional):** v2 added (C5.OVL) as a load-bearing
   structural condition. Codex's positive finding showed it isn't
   needed for intensivity ($Q^*$ is auto in $[0,1]$). v3 drops
   (C5.OVL) from the main proof and demotes it to optional
   strict-smallness refinement.

6. **P1-6 (multi-label incidence):** v2's binary $I_j$ couldn't
   handle multi-label ledger entries. v3 uses per-channel
   projection maps $\pi_j: A \to V_j \cup \{*_j\}$.

7. **P1-7 (pathwise window budget):** v2 had ambiguous "unit
   perturbation maintained throughout window." v3 specifies
   pathwise perturbation classes $\{\Delta_n\}_n$ with explicit
   per-step or total budget conventions.

8. **P2-8 (baseline compatibility):** v2 underspecified overlapping
   channel consistency. v3 adds projective consistency:
   $(\pi_j)_* q_0 = p_0^{(j)}$ for all $j$.

## v3 main result

Under (C5.HOEFF), (C7.RATE), (C5.MULT) channel projection
structure, and projective baseline consistency:

$$\bar{M}^{\mathrm{cum}}(\mathcal{D}) \leq C \cdot \Bclip \cdot \lammax \cdot \tau_{\mathrm{meta}}$$

with $C \in \{1, \Kch - 1\}$ depending on budget convention. Each
factor is deployment-class intensive in $|P|$, so $\bar{M}^{\mathrm{cum}}$
is bounded by a $|P|$-independent constant.

Optional refinement: under (C5.OVL) ceiling $Q_{\max} < 1$:

$$\bar{M}^{\mathrm{cum}}(\mathcal{D}) \leq C \cdot Q_{\max} \cdot \Bclip \cdot \lammax \cdot \tau_{\mathrm{meta}}$$

## Review focus

Please read `c7_closed_form_v3.tex` and check:

1. **Are all v2 findings (P0-1 through P2-8) adequately addressed
   in v3?** Each one should have a corresponding fix; verify each.

2. **Does the operator-norm Lipschitz definition (Definition 2)
   work mathematically?** It's $\sup_{\Delta \neq 0}
   |\Delta\mu_{j'}|/\|\Delta\|_1$, scale-invariant under
   $\Delta \to t\Delta$.

3. **Does the per-step bound proof (Lemma 1) go through?** The
   proof: $|\Delta\mu_{j'}| \leq \Bclip \cdot \|\Delta\|_1$, divide
   by $\|\Delta\|_1$, take sup. Are there admissible $\Delta$ that
   violate this?

4. **Does the cumulative bound proof (Lemma 2) go through?** Sums
   per-step bounds over $\Nev(\tau_\mathrm{meta}) \leq \lammax
   \cdot \tau_\mathrm{meta}$ steps.

5. **Is (C7.RATE) cleanly distinct from (C11.CLK)?** (C7.RATE) is a
   deterministic upper bound on $\Nev$; (C11.CLK) is a probabilistic
   lower bound. They can both hold simultaneously.

6. **Does the projection-map structure (Section 2.2) handle the
   four-channel structure of Lemma 5b?** Poisson, Bernoulli,
   multinomial channels — does the projection convention work
   uniformly?

7. **Does the idle-bucket convention (Section 2.5,
   Remark 1) correctly handle Poisson rate shifts?** A
   cooperative-output rate change is represented as mass
   redistribution between $a_0$ and event actions; verify this
   captures rate shifts faithfully.

8. **Is the pairwise vs aggregate-incoming distinction
   (Lemma 2(a) vs (b)) usefully stated, or does it confuse
   things?** The two budget conventions (per-step vs total,
   per-source vs sum) generate four cases; v3 states the natural
   ones.

9. **Does the projective consistency in
   Assumption 1 actually constrain real verification protocols
   reasonably?** The condition $(\pi_j)_* q_0 = p_0^{(j)}$ for all
   $j$ requires per-channel baselines to be simultaneously
   realizable.

## Format

For each finding:
- [P0] Critical: proof is wrong / closed form doesn't deliver C7
- [P1] Substantive: gaps in proof or definitions
- [P2] Polish: presentation could be clearer

For each: line reference into `c7_closed_form_v3.tex`, problem
description, suggested fix. Be specific. Aim for 3-7 findings if
v3 is converging; more if it's not. Skip findings that are
pre-existing / already addressed unless v3's fix is incorrect.

If v3 has 0 P0 and ≤3 P1 findings, please say so explicitly: this
indicates the derivation is converging and we should integrate it
into Paper 10.

Output the findings list directly with no preamble.
