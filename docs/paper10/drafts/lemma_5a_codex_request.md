# Codex review request: Lemma 5a (Substrate floor) — full proof draft

## Mode

**Proof verification.** Third item from `docs/paper10/TODO_proofs.md` Phase 2 work: promoting Lemma 5a from inline outline to formal proof for the appendix.

The current Paper 10 §4.7 has an inline outline asserting $\rext \geq r_*(m^*) \sim \rho_0 \binom{m^*}{2}$ under $I_6'$ + substrate-distinctness, without formalizing the coercivity assumption or proving the pairwise-additivity scaling.

Same review pattern as Lemmas 1, 2: write full proof → codex review → cycle until clean → integrate.

## What to read

Primary:
- `docs/paper10/drafts/lemma_5a_full_proof.tex` — full proof draft (6pp PDF)

Source paper sections referenced:
- `docs/paper3/sections/substitution.tex` — Horizon Aware's $\rext$ definition and anti-monopolar property; cross-substrate cooperative novelty
- `docs/paper6/sections/lyapunov.tex` C1, C2 — coercivity-style assumptions in Phase Redundancy (structural template for Lemma 5a's CN)

Reference:
- `docs/paper10/main.pdf` — current Paper 10 draft, §4.7 has the current inline outline
- `docs/paper10/sections/main_theorem.tex` — Theorem 1 conditions (C1)-(C9), where CN may need to surface as (C10)
- `docs/paper10/appendices/proofs.tex` — Lemmas 1, 2 appendix proofs (the pattern Lemma 5a follows)

## What we want from you

Five verification questions from the proof draft's §"Specific verification questions for codex review":

### Q1. Is Assumption CN correctly formalized?

CN: each pair of distinct substrates contributes rate $\rext^{(s_i, s_j)} \geq \rho_0 > 0$.

**Question:** Should CN admit per-pair heterogeneity by default, with $\rho_0 = \min_{i,j} \rho^{(s_i, s_j)}$ derived rather than asserted? The current uniform-$\rho_0$ form is simple but loses information about heterogeneous substrate pairs.

### Q2. Is Step 4 (rate additivity under joint independence) rigorous?

Step 4 argues that under joint failure-correlation independence (Definition: joint event-class), per-pair cooperative-novelty rates are statistically independent and therefore additive: $\rext \geq \sum_{i<j} \rext^{(s_i, s_j)}$.

**Question:** Is this argument watertight? In particular, does it require additional structural conditions (e.g., cooperative production from one pair does not consume capabilities that would otherwise contribute to another pair's cooperatives)?

### Q3. Is the higher-order cooperative caveat correctly handled?

The proof bounds $\rext$ using only pairwise channels (binom(m^*, 2)), with higher-order cooperatives contributing additionally to make the bound conservative.

**Question:** Is this the right structural treatment? Alternatively, the lemma could incorporate higher-order rates directly: $\rext \geq \sum_{k \geq 2} \rho_0^{(k)} \binom{m^*}{k}$. Which form is cleaner for the deployment claim's purposes?

### Q4. Is the $r_*(m^*) = \rho_0 \binom{m^*}{2}$ formula consistent with Horizon Aware?

The lemma's pairwise scaling assumes Paper 3's anti-monopolar framework, which establishes $\rext > 0$ but doesn't give a quantitative floor.

**Question:** Does Paper 3 give any quantitative bound on $\rext$ that Lemma 5a is in tension with, or is the lemma a strict refinement? In particular, are there cases where Paper 3's framework would predict $\rext$ scaling differently (e.g., not $\binom{m^*}{2}$ but $m^*$ or $m^{*\,3}$)?

### Q5. Should CN be promoted to a theorem-level condition?

Lemma 1 added (C6), (C7), (C8) to Theorem 1; Lemma 2 added (C9). Lemma 5a's coercivity assumption CN is structurally similar to PR's C1, C2.

**Question:** Should CN be promoted to a theorem-level condition (C10) of Theorem 1, analogous to the previous lemma-driven additions? Or can it remain a Lemma 5a deployment-class assumption without theorem-level surfacing? The trade-off: theorem-level visibility (operators see the assumption) vs. theorem-statement length (already up to C9).

## Output format

For each Q1-Q5:
- **Sound** — confirmation, ready for appendix integration with any minor refinements.
- **Issue identified** — name precisely; recommend whether v2 needed or addressable at integration.
- **Significant problem** — explain the obstruction.

If you find an issue we did not name (e.g., introduced by the proof's structure, or a Paper 3 source-mismatch), flag it.

## Goal

Settle whether Lemma 5a v1 is ready for appendix integration, or whether v2 is needed before integration.
