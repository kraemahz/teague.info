# Codex review request: Lemma 5c v2 confirmation

## Mode

**Confirmation review.** This is a follow-up to your Round A review of `lemma_5c_minimax_static_tightening.tex`. You returned "not citeable as stated" with five soundness errors and constructive replacements. The v2 draft incorporates every correction. We want confirmation that the corrections are technically sound before Paper 10 cites Lemma 5c as established.

This is a tighter scope than Round A — we're verifying specific fixes, not exploring open questions. If the corrections hold, Lemma 5c becomes a citeable building block. If any still have soundness issues, name them precisely.

## What to read

Primary:
- `docs/paper10/drafts/lemma_5c_minimax_static_tightening.tex` — the v2 draft (11pp PDF, revised)
- §"Summary of changes from v1" near the end enumerates every codex Round A point and the corresponding fix in v2

Source paper sections (for verification):
- `docs/paper3/sections/substitution.tex` §sec:domination_kills (around line 1381) — Paper 3's volume-survival form $\Ddiv = \min_s \volL(G^{-s})$ that v2 cites as the correct source
- `docs/paper3/sections/risk.tex` (around line 60) — Paper 3's $\mathbb{E}[\gamma^T]$ vs $\gamma^{\mathbb{E}[T]}$ warning that v2 now respects
- `docs/paper2/sections/axioms.tex` and `docs/paper2/sections/leverage.tex` — Paper 2 axioms that v2's $\alpha_s$ shock-loss attribution should respect

Cross-reference:
- `docs/paper10/paper10_proposal.md` §6 — the cooperative-anchoring property that v2 §4.1 (tripartite identification) should align with

## Your Round A findings being confirmed

For each codex Round A finding, the v2 fix:

- **Q1 (proportional rate model not derivable):** v2 replaces with Paper 3's volume-survival penalty, normalized as $\Ddiv = \volL_K (\lossDmax - \lossdivmax) \mathbb{E}[\gamma^{\Tadv}]$.
- **Q2 (binary 0-vs-rate):** v2 uses continuous loss-fraction parameter; full failure-correlated single-substrate domination → $\lossDmax \approx 1$, partial domination → smaller.
- **Q3 (threshold flip):** v2 corrected to $\max_s \alpha_s \leq 1/m^* + \epsilon$. $\alpha_s$ is the full shock-loss fraction including cooperative-loss attribution.
- **Q4 (multi-shock):** v2 adds Remark with $A_{\mathrm{multi}} = \mathbb{E}\sum_t \gamma^t (\volL_{\mathrm{div}}^{\mathrm{surv}}(t) - \volL_D^{\mathrm{surv}}(t))$.
- **Q5 (scope):** v2 explicitly narrows to substrate-targeting adversaries; capability-targeting / coalition-internal / environment-manipulation shock classes named and excluded.
- **$\mathbb{E}[\gamma^T]$ vs $\gamma^{\mathbb{E}[T]}$:** v2 uses the expectation-of-discount form throughout.
- **Pairwise vs joint independence:** v2 strengthens to joint / event-class independence formalized in Definition.
- **Inconsistent $\Ddiv$ form:** v2 fixes a single form per Definition.
- **New: tripartite canonical identification:** v2 §4.1 aligns with Paper 10 §6.

## What we want from you

Five verification questions, one per substantive correction:

### Q1. Is the equivalence between Paper 3's $\Ddiv = \min_s \volL(G^{-s})$ form and the normalized loss-fraction form $\volL_K (\lossDmax - \lossdivmax)$ rigorous?

The transformation: Paper 3's absolute-volume contraction penalty is $\min_s \volL(G^{-s})$. v2 rewrites this as $\volL_K (1 - \lossdivmax)$ where $\lossdivmax = \max_s \alpha_s$ and $\alpha_s = \volL_K|_s / \volL_K$ is the substrate's full $\volL$-share.

For the diversity strategy, $\min_s \volL(G^{-s}) = \volL_K (1 - \max_s \alpha_s) = \volL_K (1 - \lossdivmax)$.

For the dominator strategy under full failure-correlated single-substrate domination, $\min_s \volL(G^{-s}) = 0$ (the worst shock removes everything), so $\volL_K (1 - \lossDmax) = 0$ and $\lossDmax = 1$.

The advantage is then $\Ddiv = \volL_K (1 - \lossdivmax) - \volL_K (1 - \lossDmax) = \volL_K (\lossDmax - \lossdivmax)$.

**Question:** Is this transformation rigorous? Specifically:
- Are there partial-domination cases where the $\lossDmax$ formulation breaks down (e.g., where the worst-case shock for the dominator isn't unique, or where residual operations on multiple substrates create a different worst case)?
- Does the cooperative-loss attribution to $\alpha_s$ (cooperatives whose participants required substrate $s$) preserve Paper 2's axiomatic structure for $\volL$, or does it require new axioms?
- Is there a case where $\alpha_s$ as defined exceeds 1 due to multi-substrate cooperative attribution (e.g., a three-way cooperative attributed in full to each of three substrates)? If so, how does v2 handle it?

### Q2. Does the corrected balance threshold $\max_s \alpha_s \leq 1/m^* + \epsilon$ capture the operational requirement?

The v1 error was using $\leq 1 - 1/m^* + \epsilon$, which allowed monopoly. v2 uses $\leq 1/m^* + \epsilon$, requiring near-uniform.

**Question:**
- Is $\epsilon$ a free deployment-engineering parameter, or determined by some quantity in the safe-region calculation?
- Does the threshold compose correctly with the safe-region inequality (Equation \ref{eq:safe_region_concrete})? Specifically, what value of $\lossdivmax$ does the threshold imply, and does that value give a non-trivial safe region for typical $\rext$, $\Delta_0$, $\gamma$?
- Should the threshold be tighter ($\max \alpha_s \leq 1/m^*$ exactly) or is the $\epsilon$ slack required for operational tractability (substrates can't be perfectly balanced in practice)?

### Q3. Is the multi-shock formulation algebraically consistent with the single-shock case?

v2 Remark provides $A_{\mathrm{multi}} = \mathbb{E}\sum_t \gamma^t (\volL_{\mathrm{div}}^{\mathrm{surv}}(t) - \volL_D^{\mathrm{surv}}(t))$ to replace $\Ddiv$ in the safe-region inequality for high-$\pshock$ regimes.

**Question:**
- Does $A_{\mathrm{multi}}$ reduce to $\Ddiv$ as $\pshock \to 0$ (single-shock limit)?
- Is the diversity strategy's surviving fraction $(1 - \alpha_{\max})^k$ after $k$ shocks correct under independent shocks, or does it require additional assumptions (e.g., that each shock targets a still-operational substrate, not one already removed)?
- How does $A_{\mathrm{multi}}$ behave under recovery dynamics (substrate replacement after removal)? v2 flags this as deferred but the deferral may matter operationally.

### Q4. Does joint / event-class independence (Definition \ref{def:indep}) match the operational requirement?

v2 strengthens from pairwise correlation factorization to: "no single adversarial mechanism in scope produces shocks to more than one substrate."

**Question:**
- Is this formalization aligned with what an attacker can actually do? An attacker may use multi-step mechanisms where each step targets one substrate but the mechanism in aggregate hits multiple. Does the definition cover this?
- Operationally, the threat model $\mathcal{T}$ contains the adversarial mechanism classes; this list is human-curated and may miss novel mechanisms. Is the v2 definition robust to threat-model incompleteness, or does an unknown mechanism violate the assumption retroactively?
- Are there alternative formalizations (e.g., based on conditional independence given the attacker's information, or based on causal-graph factorization) that would compose better with Paper 10's other invariants?

### Q5. Does the tripartite canonical identification (§4.1) align correctly with §6?

v2 §4.1 introduces the Human / AI / Formal-Operational identification as the canonical $\mindep = 3$ configuration, citing Paper 10 §6.

**Question:**
- Does Lemma 5c's substrate-targeting shock model apply to the Formal-Operational layer in the way §6 implies? Specifically: when an adversary "targets the formal layer" what does that mean operationally, and does the resulting $\alpha$ for the formal layer make sense?
- §6's cooperative-anchoring claim depends on the human substrate's participation anchoring the cooperative. Does Lemma 5c's substrate-targeting analysis preserve this property, or does it implicitly assume the cooperative continues to function under partial substrate removal in a way §6 does not?
- Are there inconsistencies between Lemma 5c's threat model (substrate-targeting only) and §6's broader claim (which spans capture-of-existing, asymmetric capture, etc.)? The narrowed scope of Lemma 5c should not undermine §6's claim, but the composition needs verification.

## Output we want

For each Q1–Q5:

- **Yes, the correction is sound:** brief confirmation with any minor refinements.
- **Mostly yes, but here's a caveat:** state the caveat and whether it requires a v3 revision or can be handled with a remark.
- **No, the correction has a remaining issue:** explain the issue and what would fix it.

If you find a soundness issue we did not name, flag it.

The goal is to settle whether Lemma 5c v2 is citeable as established for Paper 10's main theorem composition.
