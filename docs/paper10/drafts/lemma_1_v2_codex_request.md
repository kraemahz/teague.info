# Codex review request: Lemma 1 v2 — re-review after Round A revisions

## Mode

**v2 confirmation review.** Round A returned "not ready for appendix; needs v2" with five concerns. v2 incorporates the corrections. We want confirmation the corrections work before integrating into the appendix.

## What changed in v2

Per Round A findings (in `b8d4vg0sn.output`):

- **Q1 fix:** Definition 1 tightened to quantify over a fixed deployment class $\mathcal{D}$ with stated operational parameters. Removed the over-strong "extensive" equivalence.
- **Q2 (A1) fix:** Added per-capability admissibility as an explicit hypothesis (Assumption~\ref{ass:admis}), citing Microfoundation's Assumption 1 from `goodhart.tex`. A1 now reads "Under Assumption~\ref{ass:admis}, ..." 
- **Q2 (A2) refinement:** Direct ratio argument $\epsfloor = \volR(\ResS)/\volR(P) \leq 1$ replaces the weaker per-capability-rate justification.
- **Q2 (A4) main blocker fix:** A4 reformulated as a *new Paper 10 assumption*, not a Paper 9 derived consequence. The honest scope: Microfoundation's Composition Proposition (in `lineage.tex`, not `goodhart.tex` as v1 incorrectly cited) leaves co-evolution correction terms open. A4 is asserted explicitly as a deployment-class condition, with empirical testability noted.
- **Q3 fix:** A4 explicitly bounds $M(\text{deployment}) \leq \bar{M}$ uniformly. Step 3 absorbs $K_{\mathrm{coev}} \cdot \bar{M}$ without hidden $|P|$-dependence.
- **Q5 fix:** §"Connection to the deployment claim" rewritten. Lemma 1's role: showing $h_{\mathrm{static}}(\theta) := \epsnonresComposed + \lambda \cdot \epsfloor$ is intensive. Does **not** divide by $\mathrm{Lip}(g)$. Layer 1 binding now correctly uses Lemma 1 to bound the composed slack term, with $\mathrm{Lip}(g)$ multiplication as a separate composition step.
- **Q4 expansion:** New §"Discussion of constants" distinguishes source-derived ($K_c$, $K_{\mathrm{floor}}$, $K_{\mathrm{Lip}}$) from newly-assumed ($K_{\mathrm{coev}}$, $\bar{M}$) constants. The newly-assumed constants get explicit calibration-hook obligations.

## What to read

Primary:
- `docs/paper10/drafts/lemma_1_full_proof_v2.tex` — v2 draft (7pp PDF)

Reference:
- Round A findings: `/private/tmp/.../b8d4vg0sn.output` (your previous review)
- `docs/paper9/sections/goodhart.tex` — Microfoundation Assumption 1 (per-capability admissibility), the residual-class definition (Q2 A2 ratio argument)
- `docs/paper9/sections/lineage.tex` — Microfoundation Composition Proposition (the actual one, in lineage section, not goodhart). Codex Round A pointed out v1 mis-cited this.
- `docs/paper10/sections/main_theorem.tex` — Theorem 1's Layer 1 statement and proof (the connection Q5 is about)

## What we want from you

Five v2 verification questions:

### Q1. Is Definition 1's deployment-class formulation correct?

The reformulation: a bound is intensive in $|P|$ over $\mathcal{D}$ if there exists $C \geq 0$ depending on $\mathcal{D}$'s operational parameters but independent of $|P|$, such that $B \leq C$ for all valid states in $\mathcal{D}$.

**Question:** Does this address the v1 ambiguity? Is the deployment-class quantification operationally meaningful, or is it too loose (any inconvenient bound can be hidden in "operational parameters")?

### Q2. Is per-capability admissibility correctly imported as Assumption~\ref{ass:admis}?

Microfoundation's Assumption 1 is per-capability admissibility. The v2 draft asserts that under this admissibility, the per-channel sup-norms $\epsnonresChannel{c}$ are bounded by per-capability admissibility ceilings $\kappa_c$.

**Question:** Does Microfoundation's Assumption 1 actually deliver per-channel bounds, or only a per-capability bound? If only per-capability, is the path from per-capability bounds to per-channel sub-shares (Microfoundation calls these "channel sub-shares") rigorous, or does it require an additional step?

### Q3. Is A4's reformulation as a Paper 10 assumption (rather than Paper 9 derived) acceptable?

V2 explicitly states: A4 is a *new assumption* of Paper 10, not a Paper 9 derived consequence. The justification: Microfoundation's Composition Proposition leaves co-evolution open; Paper 10 takes the bounded-co-evolution claim as an explicit deployment-class assumption with empirical testability.

**Question:** Is this honest scope acceptable? Or does the deployment claim need a stronger foundation than an asserted-but-not-derived bound on $M$? In particular: does adding A4 as an assumption alongside SA1 (HHI surrogate adequacy) and (C4) (causally-grounded inner alignment) overload the conditional structure beyond what's defensible?

### Q4. Is the Layer 1 connection (\S"Connection to the deployment claim") now correct?

V2 rewrote this section to remove the v1 error of dividing by $\mathrm{Lip}(g)$. The new framing: Lemma 1 establishes $h_{\mathrm{static}}(\theta) \leq K_{\mathrm{slack}}$ (the composed slack term is intensive); $\mathrm{Lip}(g)$ multiplication is a separate step preserving intensivity.

**Question:** Is this connection now correctly stated? Does it match how Theorem 1's Layer 1 proof in `main_theorem.tex` actually invokes Lemma 1?

### Q5. Are the constant distinctions (source-derived vs. newly-assumed) appropriate?

V2 distinguishes:
- **Source-derived**: $K_{\mathrm{Lip}}$ (A3, deployment policy), $K_c$ (Microfoundation's Assumption 1), $K_{\mathrm{floor}}$ (Microfoundation's gap decomposition)
- **Newly-assumed**: $K_{\mathrm{coev}}$, $\bar{M}$ (both from A4)

**Question:** Is this distinction operationally useful? Does Paper 10's deployment-tooling specification need to add explicit calibration hooks for $K_{\mathrm{coev}}$ and $\bar{M}$ (the newly-assumed constants)?

## Output format

For each Q1-Q5:
- **Sound** — confirmation, ready for appendix integration.
- **Issue identified** — name the issue precisely; recommend whether v3 is needed or whether the issue can be addressed via remarks/clarifications during integration.
- **Significant problem** — explain the structural obstruction.

If you find a soundness issue not in Q1-Q5 (e.g., introduced by v2's revisions), flag it.

## Goal

Settle whether Lemma 1 v2 is ready for appendix integration into Paper 10. If yes, we proceed to Lemma 2 (Lyapunov-Goodhart bridge) following the same write→review→cycle pattern. If v3 is needed, we revise.
