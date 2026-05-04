# Codex review request: Lemma 2 (Lyapunov-Goodhart bridge) — full proof draft

## Mode

**Proof verification.** Second item from `docs/paper10/TODO_proofs.md` Phase 2 work: promoting Lemma 2 from inline proof outline to a self-contained formal proof for the appendix.

The current Paper 10 §4.3 has an inline outline with $N_{\max}$ and $w_{\min}$ as informal assumptions. This draft formalizes three deployment-class conditions (BD, CL, WB), walks through the Cauchy-Schwarz step-by-step, and explicitly connects to Theorem 1's Layer 1 proof.

Same review pattern as Lemma 1: write full proof → codex review → cycle until clean → integrate.

## What to read

Primary:
- `docs/paper10/drafts/lemma_2_full_proof.tex` — full proof draft (6pp PDF)

Source paper sections referenced:
- `docs/paper9/sections/goodhart.tex` — Microfoundation Goodhart bound, sup-norm $\epsnonres$
- `docs/paper6/sections/lyapunov.tex` — Phase Redundancy Lyapunov function $\Lyap = \sum_k w_k \epsilon_k^2$
- `docs/paper6/sections/phase_boundary.tex` — Phase Redundancy Theorem 1a (self-correcting basin)

Reference:
- `docs/paper10/main.pdf` — current Paper 10 draft, §4.3 has the current inline outline
- `docs/paper10/sections/main_theorem.tex` Steps 2-5 of Layer 1 proof — where Lemma 2 plugs in
- `docs/paper10/appendices/proofs.tex` — Lemma 1's appendix proof, integrated last round

## What we want from you

Five verification questions from the proof draft's §"Specific verification questions for codex review":

### Q1. Is Assumption CL (coordinate-Lipschitz parameterization) correctly stated?

CL says: for every capability $c$, $|T(c) - P(c)| \leq \sum_{k \in \mathrm{dim}(c)} |\epsilon_k|$ — i.e., the parameterization is coordinate-Lipschitz with constant $\leq 1$ in each dimension.

The proof sets $L_k = 1$ by absorbing into the $w_k$ weighting. **Question:** is this absorption argument rigorous, or should the lemma admit explicit per-dimension Lipschitz constants $L_k$ with corresponding modifications to $f(\epsilon_{\mathrm{safe}})$?

### Q2. Is Assumption WB (bounded weight floor) defensible?

WB requires $w_k \geq w_{\min} > 0$ for all dimensions. **Question:** does Phase Redundancy's Lyapunov machinery require strictly positive lower bound on weights, or can it accommodate $w_k = 0$ for some dimensions with corresponding restrictions on which dimensions enter the Lyapunov sum?

In particular, Phase Redundancy seems to allow safety-relevance weighting with some weights set to zero (effectively: dimensions outside the safety-relevant subset). Should WB be stated as $w_k > 0$ for $k$ in the safety-relevant subspace only, with $w_{\min}$ the minimum over that subspace?

### Q3. Is the Cauchy-Schwarz step (Step 2) rigorous?

Step 2 uses indicator weights $a_k = \mathbb{1}[k \in \mathrm{dim}(c)]$ and gets $\sqrt{|\mathrm{dim}(c)|} \leq \sqrt{N_{\max}}$.

**Question:** Is the indicator-function approach the right way to bound the per-capability sum, or is there a tighter bound using the actual coordinate sensitivities (which CL absorbed into $w_k$)? In particular, would using the per-dimension Lipschitz constants $L_k$ explicitly give $\sqrt{\sum_{k \in \mathrm{dim}(c)} L_k^2 / w_k} \cdot \sqrt{\Lyap}$, which could be sharper than the indicator bound?

### Q4. Is Step 3 (sum-of-squares to Lyapunov) rigorous?

Step 3: $\sum_k \epsilon_k^2 \leq \Lyap/w_{\min}$ via $w_k \geq w_{\min}$.

**Question:** Does this preserve all the structure we need, or does it lose information that a tighter bound (e.g., using $w_k$ directly in a weighted-Cauchy-Schwarz) would retain?

A potentially tighter alternative: use generalized Hölder/Cauchy-Schwarz with weights $w_k$ directly, getting $\sum_{k \in \mathrm{dim}(c)} |\epsilon_k| \leq \sqrt{\sum_{k \in \mathrm{dim}(c)} 1/w_k} \cdot \sqrt{\Lyap}$, which depends on $\sum 1/w_k$ over $\mathrm{dim}(c)$ rather than $|\mathrm{dim}(c)|/w_{\min}$. Is this materially tighter, or does the simpler form suffice?

### Q5. Is the Layer 1 connection (proof draft §6) correct?

The draft asserts the sequence:
- Steps 2-3 of Layer 1: $\Lyap < \epsilon_{\mathrm{safe}}$ via Phase Redundancy contraction
- Step 3 invokes Lemma 2: $\epsnonres < f(\epsilon_{\mathrm{safe}})$
- Step 5: $|g(T) - g(P)| \leq \mathrm{Lip}(g) \cdot \epsnonres < \mathrm{Lip}(g) \cdot f(\epsilon_{\mathrm{safe}})$
- Step 6 (Lemma 1's generic-X form with $X = f(\epsilon_{\mathrm{safe}})$): packages with residual floor and Lipschitz multiplication

**Question:** Is this trace correct against `docs/paper10/sections/main_theorem.tex`'s actual Layer 1 proof? Does Lemma 2 plug in exactly where Step 3 of that proof is currently stated?

## Output format

For each Q1-Q5:
- **Sound** — confirmation, ready for appendix integration with any minor refinements.
- **Issue identified** — name precisely; recommend whether v2 needed or addressable at integration.
- **Significant problem** — explain the obstruction.

If you find an issue we did not name (e.g., introduced by the proof's restructuring), flag it.

## Goal

Settle whether Lemma 2 v1 is ready for appendix integration, or whether v2 is needed before integration.
