# Codex review request: C7 closed-form derivation

## Context

Paper 10 ("Goal-Frontier Maximization: A Provably Safe Regime for Capability-Unbounded Deployment") proves a conditional deployment-safety theorem with three non-derived premises: the Concentration-Gap Conjecture, Assumption SA1 (HHI surrogate adequacy), and Assumption (C7) bounded co-evolution.

Of these, (C7) is the most brittle: it asserts that a per-channel coupling magnitude $\bar{M}$ is bounded by a $|P|$-independent constant, but this is currently a free-floating assumption with only an empirical-audit measurement procedure (Audit 4). If $\bar{M}$ scales with $|P|$, the deployment claim's intensivity property collapses with no graceful-degradation pathway in the current framework.

The draft `c7_closed_form.tex` is an attempt to derive $\bar{M}$ in closed form from already-named primitive operational parameters: (C5.HOEFF) clip radius $B_{\mathrm{clip}}$, (C5.MULT) channel partition structure, and a verification-protocol-derived "shared-action probability bound" $Q^*$. If the derivation holds, (C7) graduates from assumption to corollary of (C5.HOEFF), (C5.MULT), and the structural property $Q^*$.

The closed form derived is:
$$\bar{M}(\mathcal{D}) \leq 2 Q^*(\mathcal{D}) \cdot B_{\mathrm{clip}}$$

with $Q^*(\mathcal{D}) \in [0, 1]$ defined as the maximum probability mass any admissible adversary places on actions that simultaneously affect more than one channel.

## Review focus

Please read `c7_closed_form.tex` and review for **mathematical correctness** of the proof. The structure is: 5-step derivation (decompose drift, split actions into shared/non-shared, bound cross-channel contribution by Hoeffding clipping, argue $j'$-only contributions don't couple, conclude with intensivity).

Specific questions I want answered:

1. **Is the operational definition of $M_{j \to j'}$ in Definition 1 consistent with what Audit 4 measures?** The audit says "unit perturbation in channel $j$ propagates to channel $j'$ within $\tau_{\mathrm{meta}}$." I interpreted this as: cross-channel sensitivity of expected per-step drift under any admissible adversary deviation from baseline. Is this faithful to the audit's intent, or does the cumulative-over-window interpretation (which the discussion section addresses) match better?

2. **Is Step 4's argument that "$j'$-only contributions don't couple $j$ to $j'$" valid under all admissible adversarial classes?** I argued that if two adversaries $q$ and $q'$ agree on $A \setminus A_{j, j'}$, then $\mu_{j'}(q) - \mu_{j'}(q')$ measures cross-channel coupling exactly. But this requires that $\mu_j$ is determined by the action distribution restricted to $A_j$ — could a hidden-common-cause adversarial class violate this?

3. **Is the intensivity claim for $Q^*$ in Step 6 correct?** I argued that under (C5.MULT)'s fixed channel partition, $Q^*$ depends on the partition's overlap structure (intensive) and the adversarial class (intensive by Lemma 5b/5e). But the open question section flags a stability concern: the *distribution* over actions under an admissible adversary may concentrate more mass on shared actions as $|P|$ grows. Is this concern well-founded, and if so, does (C5.MULT) need an additional sub-clause?

4. **Is the closed form $\bar{M} \leq 2 Q^* B_{\mathrm{clip}}$ tight enough to be useful?** A trivial bound $\bar{M} \leq 2 B_{\mathrm{clip}}$ already follows from (C5.HOEFF) clipping alone (every drift difference is at most $2 B_{\mathrm{clip}}$). The closed form is tighter only if $Q^* < 1$, which is the structural design target. Is the gain over the trivial bound worth the complexity introduced?

5. **Does the proof miss any cases?** The decomposition in Step 2 splits actions into "$A_{j,j'}$ shared," "$A_{j'} \setminus A_{j,j'}$ affecting only $j'$," and "neither." What about actions affecting only $j$? I omitted them from the cross-channel coupling because they don't shift $\mu_{j'}$, but they do shift $\mu_j$ — does Step 4's "agree on $A \setminus A_{j,j'}$" condition capture this correctly?

6. **Is the per-step vs. cumulative ambiguity resolvable?** The discussion section flags that Microfoundation's $K_{\mathrm{coev}}$ structural constant could aggregate per-step or be itself per-step. If you can read the structure of the closed form and tell whether it matches the per-step or cumulative semantics that Microfoundation actually requires, please do.

## Format

For each finding:
- [P0] Critical: proof is wrong / closed form doesn't deliver C7
- [P1] Substantive: proof has gaps or the definition of $Q^*$ has issues
- [P2] Polish: presentation could be clearer

For each: line reference into `c7_closed_form.tex`, problem description, suggested fix. Be specific. Aim for 5-10 findings. Do not pad.

Output the findings list directly with no preamble.
