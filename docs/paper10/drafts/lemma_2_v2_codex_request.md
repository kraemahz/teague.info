# Codex review request: Lemma 2 v2 — re-review after Round A revisions

## Mode

**v2 confirmation review.** Round A returned "v2 needed before appendix integration" with five issues plus one main blocker (relative-vs-absolute sup-norm mismatch with Paper 9's actual definition).

V2 fixes:

- **Main fix (relative sup-norm).** Paper 9's $\epsnonres = \sup_c |P(c)-T(c)|/T(c)$ (relative). Added Assumption TF (truth floor $T(c) \geq T_{\min} > 0$); factor $1/T_{\min}$ enters $f(\epsilon_{\mathrm{safe}})$.
- **Q1:** Keep $L_{c,k}$ explicit per (capability, dimension) pair; $L_{\max}$ is closed-form bound.
- **Q2:** Restrict WB to safety-relevant subspace $S \subseteq \{1, \ldots, K\}$, with $\dim(c) \subseteq S$ for active $c$.
- **Q3, Q4:** Use weighted-dual-norm Cauchy-Schwarz: $\sum L_{c,k}|\epsilon_k| \leq \sqrt{\sum L_{c,k}^2/w_k} \cdot \sqrt{\Lyap}$.
- **Q5:** Layer 1 trace corrected per actual `main_theorem.tex` proof flow.

## What to read

Primary:
- `docs/paper10/drafts/lemma_2_full_proof_v2.tex` — v2 (7pp PDF)

Reference:
- Round A findings: `b7zya41oa.output`
- `docs/paper9/sections/goodhart.tex` line 184 — Paper 9's actual $\epsnonres$ definition
- `docs/paper6/sections/lyapunov.tex` — Phase Redundancy Lyapunov setup
- `docs/paper10/sections/main_theorem.tex` Layer 1 proof — the corrected trace

## What we want from you

Five v2 verification questions:

### Q1. Is the relative-sup-norm fix correctly handled?

V2 adds TF ($T(c) \geq T_{\min}$) and bounds $|P(c)-T(c)|/T(c) \leq |P(c)-T(c)|/T_{\min}$, then takes sup over absolute, then divides.

**Question:** Does the derivation $\sup_c |P(c)-T(c)|/T(c) \leq (1/T_{\min}) \cdot \sup_c |P(c)-T(c)|$ give the right relative-sup-norm bound, or does the sup-of-ratio require a different argument (e.g., bounding ratio directly per-capability before sup)?

The two approaches:
- **A** (v2's): bound absolute pointwise → sup absolute → divide by $T_{\min}$
- **B**: bound ratio pointwise → sup ratio

Are these equivalent under TF? In particular: does (A) give a strictly weaker bound than (B), and if so by how much?

### Q2. Is the explicit-$L_{c,k}$ form correct?

V2 keeps $L_{c,k}$ per (capability, dimension) pair, with $L_{\max} = \sup_{c,k} L_{c,k}$ for the closed-form bound. The proof gives both:
- Tighter weighted-dual-norm: $\sup_c \sqrt{\sum L_{c,k}^2/w_k} \sqrt{\Lyap}$
- Closed form: $L_{\max} \sqrt{N_{\max}/w_{\min}} \sqrt{\Lyap}$

**Question:** Is the explicit $L_{c,k}$ form correct, and is the $L_{\max}$ closed-form upper bound accurately derived from it? The derivation in Step 3 relies on $\sum L_{c,k}^2/w_k \leq L_{\max}^2 N_{\max}/w_{\min}$ — is this correct?

### Q3. Is the safety-relevant subspace $S$ formulation aligned with Phase Redundancy?

V2's WB restricts to $S \subseteq \{1, \ldots, K\}$ with $\dim(c) \subseteq S$ and $w_k \geq w_{\min}$ on $S$. Dimensions outside $S$ may have $w_k = 0$.

**Question:** Does Phase Redundancy's actual Lyapunov function operate on a fixed safety-relevant subspace, or does it sum over all dimensions $k = 1, \ldots, K$? If the latter, does $w_k = 0$ for some $k$ cause issues with PR's contraction analysis (e.g., dimensions with no Lyapunov contribution can drift unbounded)?

In particular, we want to verify that the bridge holds when $w_k = 0$ outside $S$ does not appear in $\Lyap$, so the bound $\sum_k w_k \epsilon_k^2 = \Lyap$ extends to "$\sum_{k \in S} w_k \epsilon_k^2 = \Lyap$" naturally.

### Q4. Is the Layer 1 trace correct now?

V2's §"Connection to Theorem 1 Layer 1 (corrected)" gives a six-step trace:
1. Steps 2-3 of Layer 1: $\Lyap < \epsilon_{\mathrm{safe}}$ via PR
2. Step 3 of Layer 1: Lemma 2 → $\epsnonres < f(\epsilon_{\mathrm{safe}})$
3. Step 4: gap decomposition $\epsgap \leq \epsnonres + \lambda \epsfloor$
4. Step 5: Goodhart bound $|g(T) - g(P)| \leq \mathrm{Lip}(g) \cdot \epsgap$
5. Step 5 also: $h_{\mathrm{static}}(\theta) := f(\epsilon_{\mathrm{safe}}) + \lambda \epsfloor$
6. Step 6: Lemma 1 packages

**Question:** Does this trace match `main_theorem.tex`'s actual Layer 1 proof? In particular, is the step-numbering aligned with the current proof flow?

### Q5. Is the constant taxonomy appropriate?

V2 distinguishes:
- **Source-derived**: $\epsilon_{\mathrm{safe}}$, $w_{\min}$ (PR's Lyapunov weights)
- **Deployment-policy-derived**: $N_{\max}$, $L_{\max}$, $L_{c,k}$, $T_{\min}$

**Question:** Is $T_{\min}$ correctly classified as deployment-policy-derived? It depends on the operational active-subspace selection ($P^{\mathrm{act}}$) — is that a deployment policy choice, or is there a structural argument for what $T_{\min}$ should be?

## Output format

For each Q1-Q5:
- **Sound** — confirmation, ready for appendix integration.
- **Issue identified** — name precisely; recommend whether v3 needed or addressable at integration.
- **Significant problem** — explain the obstruction.

If you find an issue we did not name (e.g., introduced by v2's restructuring or other Paper 9/Paper 6 mismatches), flag it.

## Goal

Settle whether Lemma 2 v2 is ready for appendix integration. If yes, proceed to next TODO item (Lemma 5a substrate floor). If v3 needed, revise.
