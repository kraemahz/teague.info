# Codex review request: Lemma 5c proof check (Paper 10 minimax static tightening)

## Mode

**Proof verification**, not constructive review. We have a derivation in `drafts/lemma_5c_minimax_static_tightening.tex` that builds on your earlier suggested inequality (the risk-adjusted minimax lift from the Lemma 5 review round). This round is checking whether the model assumptions and quantitative floor we derived hold up.

If you find a soundness issue, please flag it. If the derivation holds, please confirm and we'll move on. We are not asking for stylistic feedback or scope expansion.

## What to read

Primary:
- `docs/paper10/drafts/lemma_5c_minimax_static_tightening.tex` — the proof sketch (8pp PDF)
- `docs/paper10/drafts/lemma_5_anti_monopolar_robustness.tex` — context (the v4 synthesis your earlier review produced)

Source paper sections used in the derivation:
- `docs/paper3/sections/substitution.tex` — Proposition 6 (Paper 3's anti-monopolar property), §sec:domination_kills, §sec:substitution_coop, Corollary on strategy-dependent internal rate
- `docs/paper3/sections/risk.tex` — minimax/risk-adjusted machinery (the source for the substrate-diversification advantage concept)
- `docs/paper2/...` — leverage and cooperative-capability decomposition (cited in residuals; relevant to Q1)
- `docs/paper6/sections/phase_boundary.tex` — Remark on $m=2$ fragility (relevant to $\mindep$ definition)
- `docs/paper5/sections/witnesses.tex` — substrate-distinctness assumption (Witness Availability Requires $m \geq 2$)

## Context: what changed since the last review

In the previous round you suggested the inequality
```
V^{div,mm} - V^{D,mm} = (r_ext - Δr_K)/(1-γ) - Δ_0 + Δ_div · γ^T_adv
```
with `Δ_div` requiring a "floor stronger than m_eff ≥ 3 because skeleton substrates make the minimax advantage arbitrarily small."

This draft formalizes that suggestion. We:

1. Defined a substrate-targeting shock model explicitly (it is not in Paper 3 — we constructed it).
2. Derived `Δ_div` from a value-function decomposition of the post-shock state.
3. Made `m_eff^indep` precise (failure-correlation independence) and used it instead of nominal `m_eff`.
4. Derived a quantitative floor: `Δ_div · γ^T_adv ≥ vol_L^K · (1 - 1/m_eff^indep) · p_shock`.
5. Discovered (during the derivation, not from your previous review) that adversarial targeting under non-uniform `vol_L` distribution collapses the advantage even with `m_eff^indep ≥ 3`. This produced a new operational requirement (balanced-`vol_L` distribution) that the v4 synthesis did not anticipate.

We want to verify these moves are sound before Paper 10 cites Lemma 5c as established.

## What we want from you

Five specific verification questions, in priority order:

### Q1. Is the post-shock rate model defensible?

We model the post-shock surviving rate as
```
(r_K + r_ext)^{post,div} = (r_K + r_ext) · (1 - 1/m_eff^indep)
```
treating the loss of one substrate as proportionally reducing the rate. This is a linearization.

Paper 2's leverage and cooperative-capability decomposition is non-linear: losing a substrate eliminates cooperative capabilities whose participants spanned that substrate, with potentially non-proportional effect on the rate. Specifically:
- Cooperative capabilities with all participants in the eliminated substrate go to zero.
- Cooperative capabilities with mixed participation depend on whether the surviving participants can still complete the cooperative output.
- Single-substrate (non-cooperative) capabilities supported on the eliminated substrate go to zero.

**Question:** Is the proportional approximation `(r_K + r_ext)(1 - 1/m_eff^indep)` defensible as a *lower* bound (conservative for the diversity strategy)? If not, what's the tighter form derivable from Paper 2 axioms? If the conservative form is wrong (i.e., post-shock rate is *worse* than the proportional approximation), the entire safe region calculation needs to be rebuilt.

### Q2. Is the dominator's post-shock rate of zero defensible?

We assume the dominator has consolidated to one substrate, so a substrate-targeting shock targeting that substrate eliminates the entire coalition `vol_L`, giving `r_K^{post-shock,D} = 0`.

Two concerns:
- "Consolidated to one substrate" admits operational interpretation. The dominator may retain residual presence on other substrates (e.g., backup data on a secondary substrate without primary operations there). Should the post-shock rate reflect this residual?
- If shocks target substrates with probability proportional to substrate $\volL$-share, the dominator's single substrate is hit with probability $\approx 1$. But under a uniform shock distribution over *available* substrates, the dominator with $\meff = 1$ has its substrate hit with probability 1. Both give the same answer ($P(\text{shock} \to D\text{'s substrate}) = 1$), but for different reasons.

**Question:** Is the binary $0$-vs-$(r_K + r_{\mathrm{ext}})(1 - 1/m_{\mathrm{eff}}^{\mathrm{indep}})$ comparison the right model? Or do we need a continuous parameter (degree of domination $\delta \in [0,1]$) that interpolates between the two? If continuous, how does the safe region's structure change?

### Q3. Is the balanced-$\volL$ requirement the right formalization?

The adversarial-targeting analysis (§5 of the draft) shows that if `vol_L` is non-uniformly distributed across $\mindep$ substrates, the adversary targets the highest-`vol_L` substrate first. The conservative bound becomes
```
Δ_div · γ^T_adv ≥ vol_L^K · (1 - max_s α_s) · p_shock
```
where `α_s` is the `vol_L`-share of substrate `s`. In the worst case ($\alpha_s = 1$ for some $s$), the bound is zero.

We propose adding the operational requirement: `max_s α_s ≤ 1 - 1/m^* + ε` for small `ε`.

**Question:** Is this the right formalization? Alternatives we considered but did not pursue:
- Entropy-based: `H(α) ≥ log(m^*) - δ` for stated `δ`.
- Effective-substrates-via-Hill-number: `(Σ α_s^q)^{1/(1-q)} ≥ m^*` for stated `q`.
- Worst-case-substrate: `min_s α_s ≥ 1/(2m^*)` (every substrate carries non-trivial mass).

Which formulation is structurally most appropriate? Does it matter? Composability with the rest of Paper 10's invariants is a consideration.

### Q4. Does the multi-shock extension change the headline bound?

The derivation models only the first shock. A second shock after the first further reduces the surviving substrate fraction.

For deployments with high `p_shock` (multiple shocks expected within the planning horizon), the multi-shock extension matters. The first-shock formula gives:
```
Δ_div · γ^T_adv ≥ vol_L^K · (1 - 1/m_eff^indep) · p_shock
```

A naive multi-shock extension (independent shocks across the surviving substrates):
```
After k shocks: surviving fraction ≈ (1 - 1/m_eff^indep)^k
```
The expected value of the geometric series with shock arrival rate `p_shock` and discount `γ` produces a different (smaller) safe region.

**Question:** Does the multi-shock extension preserve the safe-region structure with adjusted constants, or does it require a different decomposition? Specifically: does the safe region collapse to zero as `p_shock → 1` (continuous adversarial pressure), or does it stabilize at a non-trivial bound?

### Q5. Is the substrate-targeting shock model the right adversarial primitive for Lemma 5c?

The lift presupposes substrate-targeting as the dominant adversarial threat. In practice, capability-targeting attacks (suppressing individual capabilities without targeting their substrate) and coalition-internal corruption (insider attacks that preserve substrate identity but compromise the actor) may dominate.

**Question:** Should Lemma 5c be stated more narrowly ("against substrate-targeting adversaries") or extended to cover other shock classes? If extended, each shock class would need its own `Δ_div` derivation.

In particular: the deployment-safety theorem currently composes Lemma 5c with the rest of the machinery. If Lemma 5c only handles substrate-targeting adversaries, the composed theorem inherits that scope. Is this acceptable, or does Paper 10 need a unified adversarial-event model that handles substrate-targeting, capability-targeting, and coalition-internal cases?

## What we are NOT asking

- Whether the draft is well-written. It's exploratory.
- Whether the substrate-targeting shock model is the right operational primitive overall. We're settling that based on what's tractable.
- LaTeX or notation feedback.
- Empirical estimation of `p_shock` (that's deployment-tooling, not theorem content).

## Output we want

For each question Q1–Q5, one of:
- **Yes, the move is sound.** With a one-line confirmation and any minor refinements that strengthen it.
- **No, here's the obstruction.** With a structural argument explaining what breaks. If a fix is obvious, sketch it; otherwise, note that it requires substantive new content.
- **Conditional on X.** Where X is a specific assumption that, if added, makes the move sound. Be explicit about whether X is operationally defensible.

If you find a soundness issue we did not name (e.g., a circular reasoning step or a hidden assumption), flag it.

The goal is to settle whether Lemma 5c is citeable as stated, citeable with stated modifications, or requires further derivation work before Paper 10 can rely on it.
