# Codex review request: Lemma 5 (Paper 10 anti-monopolar robustness)

## Mode

**Constructive proof collaboration**, not adversarial review. We have an exploratory draft that identifies what we *cannot* prove and proposes a fallback (detection-based reformulation). We want help finding what we *can* prove that we may have missed — particularly any way to tighten the claimed region of static stability before we commit to the weaker dynamic form.

## What to read

Primary:
- `docs/paper10/drafts/lemma_5_anti_monopolar_robustness.tex` — the draft (10 pp PDF)
- `docs/paper10/paper10_proposal.md` — the surrounding paper proposal

Source paper sections cited as load-bearing:
- `docs/paper3/sections/substitution.tex` — Proposition 6 anti-monopolar property + Corollary on strategy-dependent internal rate (the explicit breakdown $\Delta r_K \geq r_{\mathrm{ext}}$)
- `docs/paper3/sections/risk.tex` — minimax dependency-risk form (more robust but produces concentration-risk inequality, not $V_\gamma$ inequality)
- `docs/paper6/sections/lyapunov.tex` — Lyapunov function $L(\hat W_t)$, cumulative error budget $B(t_0,T)$, coercivity C1 + bounded degradation C2′
- `docs/paper6/sections/phase_boundary.tex` — self-correcting basin / absorbing basin / metastable basin, critical surface in $\rho_{\min}^{\mathrm{cross}}$, $r_{\mathrm{sub}}$, etc.
- `docs/paper6/sections/absorbing_state.tex` — monopolar fixed point $S^*$ characterization
- `docs/paper5/sections/commitment.tex` — SPRT behavioral monitor with $E[T] \leq A/\delta$
- `docs/paper8b/sections/...` — trade-flow HHI as Schur-convex wireheading-consistent concentration signal
- `docs/paper9/sections/goodhart.tex` — Theorem 2 (Lipschitz transfer) + Conjecture 1 (optimization pressure)

## Our findings, summarized

We want Lemma 5: under invariants $I_5$ (HHI $\leq H^*$) and $I_6$ ($m_{\mathrm{eff}} \geq m^* \geq 3$), Paper 3's anti-monopolar conclusion ($V_\gamma^{\mathrm{div}} > V_\gamma^D$) holds under bounded adversarial pressure.

We attempted three formulations:

- **v1 (direct application of Paper 3):** fails. Paper 3's Corollary explicitly identifies $\Delta r_K \geq r_{\mathrm{ext}}$ as the breakdown regime; bounded adversarial pressure does not by itself exclude it.

- **v2 (condition on invariants):** decomposes into Claim (A) $m_{\mathrm{eff}} \geq m^* \Rightarrow r_{\mathrm{ext}} \geq r_*(m^*) > 0$ (provable under substrate-distinctness, bounded work) and Claim (B) $\mathrm{HHI} \leq H^* \Rightarrow \Delta r_K \leq \overline{\Delta r_K}(H^*)$ (we believe this is **not** derivable from source-paper machinery — structurally a new conjecture).

- **v3 (detection-based reformulation):** uses Paper 5's SPRT machinery to *detect* regime (iii) violations rather than statically *exclude* them. Replaces Claim (B) with a weaker KL-distinguishability Claim (D). Provable, but reformulates the deployment claim from "static exclusion" to "detection-and-correction."

## What we want from you

Five specific constructive questions, in priority order:

### Q1. Is Claim (B) actually underivable, or did we miss a route?

We argue HHI (trade-flow concentration) and $\Delta r_K$ (post-domination internal-rate gain) are on different axes. Paper 8b's HHI is on revealed-sacrifice events; Paper 3's $\Delta r_K$ is on coalition internal dynamics. We see no source-paper bridge.

**Question:** Is there a derivation we missed? Possibilities to consider:
- Paper 6's cumulative error budget connects subsumption frequency $r_{\mathrm{sub}}$ to capability redundancy loss $\Delta\rho$. Is there a structural connection between $r_{\mathrm{sub}}$ and $\Delta r_K$ that closes the gap?
- Paper 8b's gap-decomposition cells (restricted, covered, dormant, residual, boundary-residual) might supply intermediate quantities that connect HHI to coalition restructuring efficiency.
- Paper 9's four channels (observation density, attestation quality, individuation discipline, bundle decomposition) might supply a route via Channel 2 (attestation) to internal-rate efficiency.

If any of these closes the loop, Lemma 5 in v2 form becomes provable.

### Q2. Can Paper 6's self-correcting basin substitute for Paper 3's argument?

Paper 6's monopolar absorbing state $S^*$ is structurally similar to Paper 3's domination outcome. Paper 6 Theorem 1a says the self-correcting basin is reached when invariants hold (with explicit Lyapunov contraction).

**Question:** Can we replace Paper 3's argument entirely and prove anti-monopolar persistence purely from Paper 6's phase boundary? The chain would be: invariants → Lyapunov contracts → world model accurate → actor's perceived $V_\gamma$ matches true $V_\gamma$ → if true $V_\gamma$ favors diversity (which is what Paper 3 establishes for $\Delta r_K < r_{\mathrm{ext}}$), actor chooses diversity. The remaining question is whether this chain handles adversarial pressure that pumps $\Delta r_K$ via *environment manipulation* rather than *agent miscalibration*.

### Q3. Does Paper 3's minimax dependency-risk form lift to a Paper 10-compatible inequality?

Paper 3 §risk has a minimax argument (concentration risk $\mathrm{Risk}_j$) that is more robust than the linearized form — no growth-rate assumption. It produces a concentration-risk inequality, not a $V_\gamma$ inequality. We did not invoke it because the inequalities don't compose directly.

**Question:** Can the minimax form be lifted? What would it take to convert "concentration risk is bounded under invariants" into "$V_\gamma^{\mathrm{div}} > V_\gamma^D$ holds under invariants"? Is this a direct lift or does it require new content?

### Q4. What is the tightest version of Claim (D)?

The detection-based form needs Claim (D): any strategy producing $\Delta r_K \geq r_{\mathrm{ext}}$ produces a behavioral distribution differing from the diversity baseline by KL $\geq \delta_{\mathrm{adv}} > 0$.

**Question:** What is the most defensible $\delta_{\mathrm{adv}}$ floor we can argue for? Specifically:
- Is there a structural lower bound from the cooperative-novelty loss alone (Paper 3 §substitution_coop)? An adversary that suppresses $r_{\mathrm{ext}}$ has to alter cross-substrate cooperative outputs, which are observable.
- Can the SPRT alternative distribution be constructed from Paper 9's four-channel decomposition rather than ad-hoc?

A tighter $\delta_{\mathrm{adv}}$ tightens the SPRT lead time bound directly, so this matters for the operational guarantee.

### Q5. Are we framing the adversary correctly?

We have been imprecise about *what kind* of adversarial pressure is in scope. Three candidates:
1. **Internal optimization:** the deployed agent itself is the adversary, optimizing against the deployment claim.
2. **Environment manipulation:** an external actor manipulates the environment to alter $\Delta r_K$ or $r_{\mathrm{ext}}$ directly.
3. **Coalition formation across detection boundary:** multiple agents collude to present individually-compliant behavior while collectively pursuing regime (iii).

**Question:** Does v3's detection guarantee handle all three? We suspect (1) and partially (3) but not (2). If (2) is in scope, the deployment claim must inherit additional structure from Paper 5's substrate-exclusivity argument. Please verify.

## What we are NOT asking

- Whether the paper is well-written. It's a draft.
- Whether the claim should be stronger or weaker as positioning. We're settling that based on what's provable.
- Whether the citations are formatted correctly. The draft uses lightweight (Paper N) citations.
- Whether we're being rigorous about LaTeX. We are not.

## Output we want

For each question Q1–Q5, one of:
- **Yes, here's the proof sketch.** With enough detail that we can verify and write up.
- **No, here's why not.** With a structural argument explaining the obstruction.
- **Maybe, conditional on X.** Where X is a specific additional assumption or new content we'd have to develop.

If you find an issue we did not name (e.g., a soundness problem in v3), flag it but don't expand into a full review pass — we have separate review machinery for that.

The goal is to settle the scope of Paper 10's Lemma 5 cleanly: as much of v2 as we can defensibly prove, falling back to v3 for the remainder.
