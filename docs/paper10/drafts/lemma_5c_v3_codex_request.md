# Codex review request: Lemma 5c v3 confirmation

## Mode

**Tight confirmation review.** This is a follow-up to your Round B review (`drafts/lemma_5c_v2_codex_request.md` ran against v2). You returned "citeable for single-shock, substrate-targeting safe-region correction" with one substantive remaining issue (Q3, multi-shock dimensional inconsistency) and three minor cleanups (Q1 counterfactual $\alpha_s$, Q4 mechanism scope, Q5 citation discipline).

V3 incorporates all four. The structural single-shock argument is unchanged — Round B already verified it. This round verifies the multi-shock fix, which is the only material change.

If the multi-shock derivation holds, Paper 10 cites Lemma 5c v3 as established. If a remaining issue surfaces, we revise to v4.

## What to read

Primary:
- `docs/paper10/drafts/lemma_5c_minimax_static_tightening.tex` — v3 draft (15pp PDF)
- See §"Summary of changes from v2 (codex Round B)" for the per-finding fix, and §"Multi-shock extension via discounted marginal loss increments" (the new derivation)

Source paper sections (unchanged from Round B):
- `docs/paper3/sections/substitution.tex` §domination_kills — Paper 3's volume-survival form
- `docs/paper3/sections/risk.tex` (~line 60) — $\mathbb{E}[\gamma^T]$ vs $\gamma^{\mathbb{E}[T]}$ warning

## What changed in v3

Per Round B verdicts:

- **Q1:** $\alpha_s$ now defined via counterfactual formula $\alpha_s = (\volL(G_K) - \volL(G_K^{-s})) / \volL(G_K)$. Additive attribution called out as estimator with overcounting bias (Remark following Definition).
- **Q3:** New formulation $\Ddiv^{\mathrm{multi}} = \mathbb{E}[\sum_i \gamma^{T_i} (\delta_i^D - \delta_i^{\mathrm{div}})]$ where $\delta_i$ is the marginal $\volL$-loss at shock $i$. Single-shock reduction explicitly verified. Substrate exhaustion corrected to additive $1 - k/m$, not multiplicative $(1 - \alpha_{\max})^k$. High-$\pshock$ behavior analyzed via $\kappa = \mathbb{E}[\gamma^{T_1}]$.
- **Q4:** Remark added clarifying "adversarial mechanism" = whole causal attack campaign, not atomic step.
- **Q5:** Citation discipline note added: Lemma 5c covers substrate-targeting only.

## What we want from you

Three verification questions, focused entirely on the multi-shock derivation (the only material change). The single-shock argument and the minor cleanups (Q1, Q4, Q5) are either already verified or routine; we don't need to re-litigate them unless v3 introduced a regression.

### Q1. Does the discounted marginal loss formulation reduce correctly to single-shock $\Ddiv$ in the limit?

V3 §"Single-shock reduction (sanity check)" claims:

In the single-shock limit (only $T_1 = \Tadv$ matters; $T_i = \infty$ for $i \geq 2$ with negligible probability):
$$\Ddiv^{\mathrm{multi}} \to \mathbb{E}[\gamma^{\Tadv}] \cdot (\delta_1^D - \delta_1^{\mathrm{div}})$$

With $\delta_1^D = \volL_K$ (full domination) and $\delta_1^{\mathrm{div}} = \lossdivmax \cdot \volL_K$ (balanced diversity), this gives
$\Ddiv^{\mathrm{multi}} \to \volL_K (\lossDmax - \lossdivmax) \mathbb{E}[\gamma^{\Tadv}]$
which matches the single-shock $\Ddiv$ from Definition 2 exactly.

**Question:** Is this reduction rigorous? Specifically:
- Is the assumption "$T_i = \infty$ for $i \geq 2$ with negligible probability" the correct formal characterization of the single-shock limit, or do we need a different limiting procedure (e.g., $\pshock \to 0$ with the planning horizon held fixed)?
- Are there edge cases (e.g., $\pshock$ moderate but planning horizon short) where the reduction is approximate rather than exact?

### Q2. Does the substrate-exhaustion accounting correctly handle non-equal substrate distribution?

V3 §"Substrate exhaustion under additive removal" assumes balanced substrates (each carrying $1/\mindep$ of $\volL_K$). The marginal loss for diversity at shock $i$ is then constant: $\delta_i^{\mathrm{div}} \approx \volL_K / \mindep$ for $i \leq \mindep$.

For non-equal substrate distribution, the worst-case adversarial targeting hits the highest-$\alpha$ substrate first. The marginal losses $\delta_i^{\mathrm{div}}$ would then vary with $i$ (decreasing as the highest-$\alpha$ substrates are removed first).

**Question:**
- Does the v3 derivation work for non-equal distributions, with the marginal losses replaced by the adversarial-targeting-ordered $\alpha_{(1)} \geq \alpha_{(2)} \geq \ldots$? Or does it require a different formulation?
- The balanced-$\volL$ invariant ($\max_s \alpha_s \leq 1/m^* + \epsilon$) bounds the variation; under that bound, can we argue the equal-substrate analysis is a tight upper bound on the actual derivation? Or is there a subtle interaction with the discount factor that breaks this?

### Q3. Does the high-$\pshock$ analysis produce a defensible bound when $\kappa$ is close to 1?

V3 derives:
$$\Ddiv^{\mathrm{multi}} = \volL_K \left[\kappa - \frac{1}{\mindep} \cdot \frac{\kappa - \kappa^{\mindep+1}}{1 - \kappa}\right]$$

with $\kappa = \pshock / (\pshock - \ln \gamma)$. As $\pshock \to \infty$ (or $\gamma \to 1$), $\kappa \to 1$ and the second term blows up. V3 argues the net advantage approaches a non-positive limit, indicating "the front-loaded advantage at $T_1$ dominates and the safe region remains non-trivial" only for finite $\pshock$.

**Question:**
- Is the $\kappa$ formulation correct for Poisson shock arrivals? Specifically, $\kappa = \pshock / (\pshock - \ln \gamma)$ comes from $\mathbb{E}[\gamma^{T_1}]$ for $T_1 \sim \text{Exp}(\pshock)$ — is this the right derivation?
- Does the bound's degradation as $\kappa \to 1$ have operational implications Paper 10 must surface? E.g., is there a deployment regime where the safe region is trivially small even with all invariants satisfied?
- Is "the advantage approaches non-positive in the limit" a problem for the lemma's claim, or is it correctly handled by the operational requirement that $\pshock$ is bounded away from $1$ (i.e., shocks are rare relative to the planning horizon)?

## Output we want

For each Q1–Q3:

- **Yes:** brief confirmation, no further action needed.
- **Caveat:** state the caveat. Whether it requires a v4 revision or can be added as a Remark in v3.
- **No:** explain the issue and what fix would resolve it.

Plus: if you find an issue we did not name (e.g., a soundness problem in the multi-shock derivation that wasn't covered by Q1–Q3, or a regression introduced by v3 in the single-shock or minor-cleanup sections), flag it.

The goal is to settle whether Lemma 5c v3 is citeable as established for Paper 10's main theorem composition.
