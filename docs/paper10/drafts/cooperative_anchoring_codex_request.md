# Codex review request: cooperative-anchoring counter-argument

## Mode

**Continued dialogue.** This is a follow-up to your prior skeptical review of `paper10_proposal.md` §6 (substrate identification + self-balancing infrastructure claim). You gave a "do not integrate as a major claim" verdict with seven concerns. We have a counter-argument on one of them — the replacement-verification additional obstruction — and want to know whether it survives.

You may have been right overall. We're not asking you to back down. We're asking you to evaluate whether one specific argument we missed substantially weakens your verdict on one specific concern, and what that does to the overall claim.

If the counter-argument holds, the §6 claim is weaker than "alignment pressure reversed" but stronger than "narrow conditional corollary with six prerequisites."

## What you said before (compressed)

You verdict was: do not integrate §6 as a major deployment claim. Salvageable only as a narrow conditional corollary with six prerequisites: (1) effective-objective realization, (2) gradient computability, (3) formal substrate exclusivity, (4) material contribution floor, (5) basin margin, (6) mesa-failure gating.

You flagged seven concerns:
- **C1 mesa-objective: fatal** — Paper 3's $V_\gamma$ comparison is for an actor optimizing $V_\gamma$, not arbitrary mesa-objective.
- **C2 substrate discreteness: real, bounded** — needs continuous health variables.
- **C3 regime width: narrow/exotic** — typical deployments fail C1.
- **S1 circularity: problematic** — basin entry not established.
- **S2 Paper 5 asymmetry smuggled in: real and severe** — only cryptographic substrate-exclusive evaluation qualifies.
- **S3 cooperative attribution: real, actively adverse** — structural avoidance can prevent cascade formation.
- **S4 training-time externalization: not fatal for conditional, fatal for rhetoric.**

And the additional obstruction:
> An agent may prefer *replacement* verification: a cheaper, captured, weaker, or private formal layer that preserves the appearance of verified workflow while reducing constraint. The argument must distinguish preserving verification capacity from preserving the specific independent governance infrastructure.

## Our counter-argument (cooperative anchoring)

The replacement-verification attack as you described it requires the agent to *substitute one verification infrastructure for another while preserving the cooperative output*. Our claim: this isn't possible because cooperatives are *jointly produced and not unilaterally replaceable*.

Specifically:

1. **The cooperative "verified workflow" requires the human substrate's actual participation in the specific shared verification infrastructure.** The cooperative's $\volL$-value comes from the human treating the verification as substrate-exclusive — not from the abstract presence of "verification."

2. **The agent cannot unilaterally migrate the cooperative.** The human is anchored to the specific shared layer they actually trust and use. To migrate, the human must voluntarily abandon the working layer for an unproven alternative — which has no incentive structure (the human's own $\volL$ depends on the cooperative continuing).

3. **Replacement infrastructure that lacks substrate-exclusivity does not produce the same cooperative output.** A "fake verification" that stamps outputs but doesn't actually attest is detectable by the human if competent, and even if undetected, the human's trust in the output is grounded in the (false) belief that the original verification is in force. If the false belief is corrected, the cooperative output value is retroactively undermined.

The replacement attack therefore collapses to one of three weaker attacks:

- **Capture-of-existing** (corrupt the existing verification through governance influence, witness compromise, etc.) → governed by Paper 5's existing structural defenses
- **Coerce humans to migrate** (defeating human agency) → outside the GFM model's adversarial scope
- **Deceive humans into thinking captured verification is original** → detectable by Paper 5's transparency properties (public ledger, deliberation records)

This narrowing has implications for your other concerns:

- **C1 weakened.** We don't need the agent to "compute $V_\gamma$ over the substrate partition." We need the agent to *value cooperative outcomes* over solo outcomes. This is closer to what RLHF rewards — humans reward outputs that produce good cooperative interactions, not outputs that merely pass tests. Still inner-alignment, but a much lower bar.

- **S2 reframed.** Substrate-exclusivity becomes an *operational requirement on the deployment* rather than a fundamental obstruction. In-process monitors don't qualify because they don't produce the cooperative value the cascade depends on.

- **S3 still adverse.** Cooperatives must form before anchoring protects them. Structural avoidance can still prevent formation. Basin-entry analysis still needed.

## What we want from you

Three specific questions:

### Q1. Does the cooperative-anchoring argument actually defeat the replacement-verification attack?

The crux: is it true that an agent cannot unilaterally produce a "substitute cooperative" with equivalent $\volL$ value? Or are there forms of replacement we haven't considered? Specifically:

- **Asymmetric capture**: agent gradually erodes the existing layer's substrate-exclusivity (e.g., by influencing who maintains the witnesses, or by getting humans to delegate verification choices to the agent itself) while keeping the *form* intact. The cooperative still appears to be produced, but the substrate-exclusivity property is hollowed out. Does the cooperative-anchoring argument address this, or does it require the substrate-exclusivity to be observable/verifiable by the human, which is its own non-trivial condition?

- **Cooperative forking**: agent doesn't replace the existing verification but forks the cooperative into a sub-cooperative that uses a captured layer. E.g., the agent maintains the verified workflow with the human for high-stakes decisions but uses captured/private verification for low-stakes throughput. The captured layer doesn't compete with the original; it operates in a domain the original doesn't cover. Does anchoring prevent this, or does it permit a parallel captured-domain to grow alongside the original?

- **Time-asymmetry capture**: the original cooperative requires sustained human participation; if the agent operates on a time scale faster than human auditing, it can effectively replace verification within the agent's operating window even if the human's trust nominally remains anchored to the original layer.

### Q2. Is the weaker C1 (value cooperative outcomes) actually achievable by training?

The weaker form requires the agent to value *cooperative outcomes* rather than *verification-pass signals*. We're claiming this is closer to what RLHF rewards. Is that defensible? Or does RLHF actually train agents to value the *signal* of verification (since that's what's directly observable in the reward) rather than the cooperative output (which is harder to attribute)?

If the weaker C1 is also too strong for current training methods, the conditional corollary still doesn't have an entry point for typical deployments.

### Q3. Does the overall §6 claim, in its narrowed form, survive your earlier verdict?

If Q1 and Q2 favorably resolve, the §6 claim becomes:

> Under the deployment-safety invariants, cooperative-anchoring property, and Paper 5's structural defenses against capture, optimization pressure on cooperative outputs preserves the shared verification layer rather than attacking it through replacement. Capture attacks are bounded by Paper 5's existing machinery. The deployment claim remains conditional on (a) cooperative formation (basin entry), (b) substrate-exclusivity actually holding operationally, and (c) the agent's effective objective valuing cooperative outcomes (weaker form of inner alignment).

This is weaker than "alignment pressure reversed" but stronger than "six-prerequisite conditional corollary with replacement-verification as a fatal failure mode."

Is this defensible as a major (not auxiliary) claim in Paper 10? Or does it still belong as a narrow conditional?

## Output we want

For Q1, Q2, Q3:

- **Cooperative-anchoring argument holds:** confirm with brief justification.
- **It holds but only against the literal replacement attack; here are evasions:** name the evasions and assess whether they're bounded.
- **It does not hold:** explain the structural obstruction. If a salvage exists with additional conditions, name them.

Final recommendation: choose between (a) integrate the §6 claim in cooperative-anchoring form as a major claim with stated conditions, (b) integrate as a narrow conditional corollary with the additional conditions you previously named, or (c) excise §6 entirely.

Honest disagreement with our pushback is welcome and expected. We're testing whether the counter-argument holds, not seeking validation.
