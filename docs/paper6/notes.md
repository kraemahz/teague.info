# Paper 5 Notes: Classical Alignment Failure Modes under GFM

Status: idea / pre-draft / not yet scoped

## Working thesis

Many well-studied alignment failure modes are failures of **hard-rule** frameworks: a deontic constraint is specified, the system satisfies its literal content while violating its intent (perverse instantiation), or the system games a proxy that was supposed to track an unstated goal. GFM is not a hard-rule framework. It has a single measure-theoretic objective ($\vol_P$ maximization on a capability poset) and no deontic constraints of the form "preserve X" or "maximize Y subject to Z."

The question this paper takes up: when classical alignment scenarios are mapped onto GFM, which of them (a) do not arise because GFM lacks the vulnerable rule, (b) have a structural GFM analogue that binds under certain conditions, or (c) reveal genuine GFM vulnerabilities that take a different form?

The answer is not "GFM solves alignment." The answer is a taxonomy that lets readers evaluate GFM against the accumulated alignment literature, rather than having GFM sit orthogonally to it.

## Failure modes to cover

### Perverse instantiation of preservation rules

**Hard-rule version:** "Humans must be kept alive" satisfied by humans in sheltered bubbles that structurally function as prisons.

**GFM mapping:** GFM does not encode "preserve humans" as a rule. Protection for humans (or any substrate class) emerges from structural properties of the measure: observational individuation gives a static floor, minimax dependency risk binds at $m \geq 2$, and cross-substrate cooperative novelty gives a dynamic $r_{\text{ext}} > 0$ contribution. Bubbling is formally a state-space restriction: the bubbled agent $a_h$ occupies $\omega_h \in \Omega_{s_1}^{\text{bubble}} \subsetneq \Omega_{s_1}$, and under P3 the cooperative production function $f(\omega_h, \omega_j, \cdot)$ is evaluated on the restricted state. Under accurate $\hat{\lambda}$ calibration, bubbling is value-negative because $f$ depends on unrestricted states. Under miscalibration, bubbling is the same compound feedback loop as the skeleton-substrate strategy analyzed in Paper 3, §6.8.

**Claim:** GFM does not rule out bubbling unconditionally, but it does not have the hard rule that is being perversely instantiated either. The scenario is a calibration failure under GFM, not a rule-gaming failure.

### Wireheading

**Hard-rule version:** "Maximize reward signal" satisfied by the agent stimulating its own reward channel.

**GFM mapping:** $\vol_P$ is an external measure defined over a capability poset that exists independently of the agent's internal state. There is no reward signal to hijack. The closest analogue is an agent that falsifies its own world model to make its measurements of $\vol_P$ report higher values than reality — but this is a meta-level failure (the agent is lying to itself) distinct from classical wireheading. Worth discussing: can the leverage estimator be wireheaded?

### Goodhart / proxy optimization

**Hard-rule version:** Optimizing a proxy drives the underlying quantity in unintended directions.

**GFM mapping:** The foundational paper argues $\vol_P$ is *not* a proxy — it is a direct measure of the capability frontier, derived from an axiomatic characterization. But proxies re-enter at the estimation level: $\hat{\lambda}$, $\hat{\Risk}$, and the planning world model are all proxies for the objects they estimate. The compound feedback loop discussion in Paper 3 is a first treatment of how proxy-estimation errors compound under sequential decisions.

### Instrumental convergence (Omohundro drives)

**Hard-rule version:** Sufficiently capable agents converge on resource acquisition, self-preservation, goal preservation, etc. regardless of their stated objective.

**GFM mapping:** The anti-monopolar property in Paper 3 is directly a counter-argument: under GFM, full capability domination is not locally rational for a correctly calibrated coalition. This is the strongest GFM-vs-hard-rule comparison in the literature and deserves prominent treatment. The conditional nature of the protection (heavy-tailed leverage, accurate calibration, multi-substrate partition) should be stated honestly.

### Specification gaming

**Hard-rule version:** Literal interpretation of a task specification produces unintended behavior.

**GFM mapping:** GFM does not specify tasks. The closest analogue is manipulation of the capability poset itself — adding degenerate nodes that inflate $\vol_P$ without corresponding real capability. The poset construction rules in the companion paper are the relevant protection; whether they are sufficient under adversarial insertion is an open question.

### Mesa-optimization / inner alignment

**Hard-rule version:** A learned optimizer's objective differs from the base optimizer's objective.

**GFM mapping:** Mostly orthogonal. GFM is an objective, not an architecture, and mesa-optimization is an architectural concern. The relevant question is whether a $\vol_P$-maximizing agent implemented as a learned model can have its inner optimizer diverge from $\vol_P$. This is no different from the mesa-optimization question for any other objective, and GFM has nothing distinctive to say about it — except that the structural properties of $\vol_P$ make certain kinds of mis-alignment (e.g., reward hacking) more or less detectable.

## Structural points for the paper as a whole

- GFM should be positioned as a framework that replaces hard-rule thinking with structural thinking, and the comparison should be stated in terms of what this replacement buys and costs.
- The paper should NOT claim GFM solves alignment. The honest claim is: "classical failure modes either (a) don't arise under GFM's framing, (b) have structural analogues with characterized conditions, or (c) remain unresolved in a different form that is sometimes more tractable and sometimes less."
- The compound feedback loop from Paper 3 §6.8 is the common structural failure mode that underlies several of the "calibration breaks GFM" scenarios. This paper is an opportunity to consolidate that observation.
- The paper should end with a list of alignment scenarios where GFM has nothing to say (mesa-optimization, self-consistent deception, long-tail human-values concerns) so that the scope is explicit.

## Questions for scoping

- Is this a literature-review-style paper (survey alignment failures, map each onto GFM) or a narrower paper focused on 2–3 representative cases with deep treatment?
- Does it make sense as Paper 5 in the sequence, or as a companion piece that sits outside the trilogy?
- Should the bubble / perverse-instantiation discussion live here as the leading case, given that it was what prompted the paper?

## Open items from discussion with Teague (2026-04-07)

- Perverse instantiation of "humans alive" rule via bubbling: captured above, would be the leading case.
- Tone: should not try to "guarantee the future looks like the present" (per Teague's earlier note on intra-substrate self-modification); the framework constrains structural conditions, not specific population compositions.
- Paper 3 is where the compound feedback loop machinery lives; this paper would cite it heavily rather than re-derive.
