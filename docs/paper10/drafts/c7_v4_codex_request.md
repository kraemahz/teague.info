# Codex review request: C7 closed-form derivation v4

## Context

This is v4 of the C7 closed-form derivation in
`drafts/c7_closed_form_v4.tex`. v3 was declared "converging" by
codex (0 P0 + 3 P1 + 1 P2 = 4 findings). v4 closes those four
findings.

Progression:
- v1 (`c7_closed_form.tex`): 2 P0 + 5 P1 + 1 P2 = 8 findings
- v2 (`c7_closed_form_v2.tex`): 1 P0 + 6 P1 + 1 P2 = 8 findings
- v3 (`c7_closed_form_v3.tex`): 0 P0 + 3 P1 + 1 P2 = 4 findings (converging)
- v4 (this draft): targeting 0 P0 + 0/1 P1 = ready to integrate

## v4 fixes

1. **P1-1 (operator norm scoping):** v3 called the supremum over
   admissible perturbations a "proper operator norm," but
   $\mathcal{D}_j$ isn't a vector space because admissibility
   includes $q_0 + \Delta \geq 0$. v4 introduces the linear space
   $H_j$ of $j$-supported zero-sum signed measures (no positivity
   constraint), defines the operator norm on $H_j$, and notes that
   the operator-norm bound on $H_j$ upper-bounds the
   admissible-restricted supremum.

2. **P1-2 (projective consistency type mismatch):** v3 had
   $(\pi_j)_* q_0 = p_0^{(j)}$ but pushforward is on $V_j \cup
   \{*_j\}$ while $p_0^{(j)}$ was on $V_j$. v4 introduces extended
   baselines $\bar{p}_0^{(j)}$ on $V_j \cup \{*_j\}$, with
   $p_0^{(j)} := \bar{p}_0^{(j)}|_{V_j}$ as the conditional
   baseline given engagement and $\epsilon_j^{(0)} :=
   \bar{p}_0^{(j)}(\{*_j\})$ as the baseline null-mass.

3. **P1-3 (Lemma 2(b) budget convention split):** v3 mixed total
   per-step budget ($\sum_j \|\Delta_n^{(j)}\|_1 \leq 1$) with
   per-source budget ($\sup_j \|\Delta_n^{(j)}\|_1 \leq 1$). v4
   splits Lemma 2 into:
   - Lemma 2(a): pairwise per-step budget, factor $C = 1$
   - Lemma 2(b1): aggregate-incoming under TOTAL per-step budget,
     factor $C = 1$
   - Lemma 2(b2): aggregate-incoming under PER-SOURCE per-step
     budget, factor $C = \Kch - 1$

4. **P2 (idle-bucket exposure binning):** v3's idle bucket worked
   but exposure binning was implicit. v4 adds explicit
   deterministic binning of $[0, \taumeta]$ into $\Nev(\taumeta)$
   bins, with $a_0$ identified as "count zero in this bin" and
   $A^{\mathrm{ev}}$ including positive-count buckets.

## Review focus

Please read `c7_closed_form_v4.tex` and check:

1. **Are all four v3 findings (P1-1, P1-2, P1-3, P2) adequately
   resolved in v4?** Verify each:
   - P1-1: $H_j$ defined as linear space (line ~243 of v4); operator
     norm now scopes to $H_j$ (line ~278); Remark 1 (line ~296)
     explains the relationship between $H_j$ supremum and
     admissible-restricted supremum.
   - P1-2: $\bar{p}_0^{(j)}$ extended baselines (line ~150);
     projective consistency (Assumption 1) now uses the extended
     form on $V_j \cup \{*_j\}$ (line ~217).
   - P1-3: Lemma 2 now has three clauses (a, b1, b2) with the
     correct factors $C \in \{1, 1, \Kch-1\}$ (line ~430).
   - P2: Exposure-binning paragraph (line ~135) makes the
     continuous-time → discrete-bin model explicit.

2. **Did the fixes introduce any new gaps?** Specifically:
   - Does the $H_j$-vs-$\mathcal{D}_j$ scoping argument hold? The
     claim is that $\mathcal{D}_j \subseteq H_j$ contains a
     neighborhood of 0, so the operator-norm bound on $H_j$
     covers the admissible-restricted supremum.
   - Are the extended baselines $\bar{p}_0^{(j)}$ used consistently
     throughout the rest of the draft?
   - Are the three Lemma 2 clauses' proofs correct?
   - Does the exposure-binning paragraph fit naturally with the
     idle-bucket convention?

3. **Is v4 ready to integrate into Paper 10?** If you find 0 P0
   and 0-1 P1 findings, please say so explicitly: this indicates
   the derivation is finalized and we should plan integration.

## Format

For each finding:
- [P0] Critical: must-fix before integration
- [P1] Substantive: gaps in proof or definitions
- [P2] Polish: presentation could be clearer

For each: line reference, problem description, suggested fix. Be
specific. Aim for 0-3 findings if v4 is ready; more only if
something substantive is missing.

If 0 P0 and 0-1 P1, declare convergence and say "v4 is ready for
integration into Paper 10."

Output the findings list directly with no preamble.
