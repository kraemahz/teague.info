# Codex review request: C7 closed-form derivation v5

## Context

This is v5 of the C7 closed-form derivation in
`drafts/c7_closed_form_v5.tex`. v4 was 0 P0 + 2 P1 + 1 P2 = 3
findings; codex declined to declare convergence. v5 closes those
three findings.

Progression:
- v1: 8 findings (2 P0)
- v2: 8 findings (1 P0)
- v3: 4 findings (0 P0) — converging
- v4: 3 findings (0 P0) — not yet ready
- v5 (this draft): targeting 0 P0 + 0/1 P1 — ready to integrate

## v5 fixes

1. **P1-1 ($H_j$ scoping carried to Lemma 1):** v4 defined
   $M_{j \to j'}^{\mathrm{step}}$ as a sup over $H_j$ but Lemma 1's
   proof was for $\Delta \in \mathcal{D}_j$. v5 proves Lemma 1 for
   $\Delta \in H_j$ directly (the inequality is purely algebraic;
   positivity of $q_0 + \Delta$ is not used). v5 also downgrades
   v4's equality-of-suprema claim (which required $q_0$ to have
   strictly positive mass on every $a \in A_j$ — not assumed) to
   the upper-bound direction.

2. **P1-2 (conditional baseline normalization):** v4 defined
   $p_0^{(j)} := \bar{p}_0^{(j)}|_{V_j}$ which is a sub-probability
   measure of mass $1 - \epsilon_j^{(0)}$, then called it "a
   probability measure on $V_j$" — inconsistent. v5 normalizes:
   $p_0^{(j)}(v) := \bar{p}_0^{(j)}(v) / (1 - \epsilon_j^{(0)})$,
   defined when $\epsilon_j^{(0)} < 1$. Assumption 1's projective
   consistency uses $\mathrm{Law}(\pi_j(a) \mid a \in A_j) =
   p_0^{(j)}$.

3. **P2 (aggregate suprema membership):** v4's Lemma 2(b1)/(b2)
   suprema listed only the budget condition. v5 adds explicit
   $\Delta_n^{(j)} \in H_j$ membership to the displayed suprema.

## Review focus

Please read `c7_closed_form_v5.tex` and check whether the three
v4 findings are now resolved:

1. **P1-1 fix verification:** Confirm Lemma 1 (line ~366) is now
   stated for $\Delta \in H_j$ and proves the bound algebraically
   without using $q_0 + \Delta \geq 0$. Confirm the surrounding
   prose (around line 286) downgrades the suprema-equality claim
   to upper-bound.

2. **P1-2 fix verification:** Confirm the normalization
   $p_0^{(j)}(v) := \bar{p}_0^{(j)}(v) / (1 - \epsilon_j^{(0)})$
   appears at line ~178, that this is consistent throughout
   subsequent uses, and that Assumption 1's projective consistency
   uses the normalized conditional law.

3. **P2 fix verification:** Confirm the Lemma 2(b1)/(b2) suprema
   include $\Delta_n^{(j)} \in H_j$ membership.

Also check whether the fixes introduce any new gaps. Specifically:
- Does the H_j-scoped Lemma 1 imply the deployment claim cleanly?
  (Hint: the operator norm on $H_j$ upper-bounds the
  admissible-restricted supremum, so the deployment-relevant bound
  follows.)
- Are extended baselines $\bar{p}_0^{(j)}$ and conditional
  baselines $p_0^{(j)}$ used consistently throughout?

## Convergence verdict

If 0 P0 and 0-1 P1 findings, please say "v5 is ready for
integration into Paper 10." This indicates the derivation is
finalized.

## Format

For each finding:
- [P0] Critical
- [P1] Substantive
- [P2] Polish

For each: line reference, problem description, suggested fix. Be
specific. Aim for 0-2 findings if v5 is ready.

Output the findings list directly with no preamble.
