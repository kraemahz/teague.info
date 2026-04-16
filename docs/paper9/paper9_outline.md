# Paper 9: Goal-Frontier Maximization as a Microfoundation for Capability Economics

*Full outline. Supersedes the proposal-level document at `paper9_proposal.md`
with a more ambitious thesis: not just that GFM is a welfare-economics
microfoundation, but that proxy quality (how well the economic model captures
true preferences) controls alignment tightness, with a formal Goodhart theorem
showing what goes wrong when the proxy is merely instrumental.*

## Working title

**Goal-Frontier Maximization as a Microfoundation for Capability Economics**

## Thesis (expanded from proposal)

Goal-Frontier Maximization provides a formal microfoundation for the
Sen–Nussbaum capability approach to welfare economics. Standard microeconomic
utility theory emerges as a special case under *fungibility collapse* (the
capability poset reduces to a single-dimension money axis, cooperative
capabilities vanish, individuation becomes irrelevant). At the micro scale
where non-fungibility and cooperative structure dominate, GFM diverges from
utility-theoretic predictions in ways that match observed behaviour better.

The paper's novel contribution beyond the positioning claim: a **Goodhart
theorem** showing that when the framework's proxy (vol_P) is only
instrumentally related to true preferences, optimising the proxy produces
alignment guarantees that degrade proportionally to the proxy-to-truth gap
ε_gap. This is the formal version of "a weak economic model produces bad
alignment through the proxy being instrumental." The companion claim: as
ε_gap → 0 (the economic model converges toward a true model of inner
preference, grounded operationally via the revealed-sacrifice channel of
Paper 8), every alignment property proved in the sequence tightens at a
characterised rate.

This converts the B-to-C gap from a binary precondition into a continuous
gradient and connects the alignment-quality question to the
economic-model-quality question: **better economic models → tighter
alignment, at a rate the framework can measure.**

The full tightening proof (perturbation analysis of each prior result under
ε_gap ≠ 0) is deferred to a subsequent paper (Paper 10). This paper
establishes (a) the correspondence, (b) the structural-prediction class,
(c) the Goodhart theorem, and (d) the qualitative direction of the
tightening claim with concrete worked examples.

---

## Section structure

1. Introduction
2. The Fungibility-Collapse Correspondence
3. Where GFM Diverges from Utility Theory
4. The Goodhart Theorem for Proxy-Instrumental Alignment
5. The Capability-Economics Lineage
6. Empirical Testability via Revealed Sacrifice
7. Worked Examples
8. Discussion and Open Questions

---

## 1. Introduction

### The claim

Standard microeconomic utility theory is underspecified: it accepts any
revealed preference ordering as "the utility function" and imposes no
structure on what counts as a good. This makes it unfalsifiable in
practice — any observed choice can be rationalised by postulating the right
utility function after the fact. GFM imposes structure (poset, axioms M1–M6,
cooperative capabilities, leverage) that makes the theory predictive rather
than descriptive.

But the positioning claim alone is a literature-review exercise. The load-
bearing contribution is the Goodhart theorem in §4: when the framework's
objective proxy (vol_P) is only instrumentally related to true preferences,
optimising the proxy produces alignment guarantees that *degrade
proportionally* to the gap. Conversely, as the gap closes, the guarantees
tighten. This connects the alignment programme to the welfare-economics
programme: improving the economic model (better proxy for true preferences)
is the same thing as improving the alignment (tighter guarantees).

### Why this matters

The GFM sequence has proved its central results (anti-monopolar property,
phase boundary, convergence) under the standing assumption that vol_P is an
operational target (framing precondition, Paper 7 §1.2 and Paper 6 §1).
Every result inherits the B-to-C gap as a structural dependency. If the
gap is large, all guarantees are vacuous. If the gap is small, the
guarantees are tight.

This paper makes that dependency formal and quantitative. It also shows that
the dependency is not a quirk of GFM but a general structural feature:
*any* alignment framework that optimises a proxy for preferences inherits a
version of the same gap, and the gap's impact is characterised by a
Goodhart-type result.

### What this paper does NOT do

- Does not prove the full perturbation analysis (Paper 10). This paper
  establishes the qualitative result (direction + existence of the
  tightening); the quantitative result (per-result sensitivity coefficients,
  phase-boundary comparison theorem) is subsequent work.
- Does not resolve the "true model of inner preference" question
  metaphysically. The paper uses the revealed-sacrifice limit (the model
  you'd arrive at given infinite trade data) as the operational anchor.
- Does not unify alignment with welfare economics as a shared programme.
  It argues they share structural content and that progress in one
  constitutes progress in the other; it does not claim they have the same
  goals.
- Does not address Arrow's impossibility directly, but notes how GFM avoids
  the impossibility conditions (measuring optionality volume rather than
  ranking outcomes; see §5 discussion).

---

## 2. The Fungibility-Collapse Correspondence

### Setup

Define the *standard-economics poset* P_std as a single-dimension capability
space where each capability is purchasing power at some positive real
magnitude:

- P_std = {d ∈ R_+ : d is a unit of purchasing power}
- No cooperative capabilities (the only interaction is exchange at market prices)
- No individuation (agents are anonymous / representative)
- Weight function w(d) = d (money is its own measure)

### Theorem (Correspondence)

**Theorem 1 (Fungibility-Collapse Reduction).** An actor maximising vol_P on
P_std with discount factor γ is observationally equivalent to an
expected-utility-maximising agent with utility u(x) = x (linear utility over
wealth) and discount factor γ.

*Proof approach.* Under fungibility collapse, vol_P reduces to the sum of
individual capability weights (axiom M4 additivity with no cooperative terms).
The sum of weights on a single-dimension purchasing-power axis is total
wealth. Maximising total discounted wealth is the standard money-maximisation
problem. The anti-monopolar property (Paper 3 Prop 6) becomes trivial on
P_std (no diversity dimension to protect). All cooperative-capability terms
vanish. QED.

### Interpretation

Standard economics is GFM with all the interesting structure deleted. The
correspondence is exact at the macro level (where markets are liquid and
goods are approximately fungible); it breaks at the micro level (where
non-fungibility, cooperative capabilities, and individuation are
operationally significant). The four structural features GFM adds beyond
P_std are:

1. **Non-fungibility** — poset structure with distinct capability dimensions
2. **Cooperative capabilities** — first-class objects not reducible to sums
3. **Anti-monopolar reasoning** — the γ* threshold with no utility-theory analogue
4. **Individuation without interpersonal comparison** — vol_P over shared poset

---

## 3. Where GFM Diverges from Utility Theory

### The structural-prediction class

Identify classes of agent decisions where GFM makes predictions that utility
theory does not (or where utility theory can only match GFM's prediction
by adding ad hoc structure that is itself unfalsifiable).

**Prediction 1: Bundle-completion magnitude.** An agent purchasing a bundle
Y whose cooperative capabilities complete a previously-missing region of
their capability poset should pay more (in revealed-sacrifice units) than an
agent purchasing the same priced bundle whose poset already contains
substitutes.

*Utility-theory alternative:* Can match by asserting "the first agent has
higher marginal utility for this bundle." But that's a post-hoc utility
assignment, not a prediction — it's unfalsifiable because the utility
function is not constrained.

*GFM prediction:* The cooperative-capability terms are structurally
determined by the poset (which is observable from the agent's capability
inventory). The prediction is testable: observe the agent's existing
capabilities, compute the cooperative gain from adding Y, predict the
sacrifice magnitude. If vol_P is the right model, the sacrifice should scale
with the cooperative gain.

**Prediction 2: Cooperative premium.** Across agents with similar
priced-endowment levels, variance in revealed-sacrifice for bundles with
strong cooperative structure should be larger than variance for bundles
without, because cooperative value is poset-context-dependent in ways
non-cooperative value is not.

**Prediction 3: Saturation transition.** Agents whose capability poset is
saturated in a dimension should transition their sacrifice pattern: high
sacrifice in new dimensions, low sacrifice in the saturated dimension. This
is a longitudinal prediction that utility theory doesn't make (nothing in
utility theory predicts *which* dimensions saturate or when the transition
occurs).

**Prediction 4: Anti-monopolar at population scale.** Populations with
higher capability diversity (measured via revealed-sacrifice dispersion
across categories) should exhibit higher long-run welfare correlates than
populations with equivalent total capability magnitude but lower diversity.
This is the population-scale γ* threshold.

---

## 4. The Goodhart Theorem for Proxy-Instrumental Alignment

### The central claim

This is the paper's novel formal contribution. The shape:

> When the framework optimises a proxy P for true preferences T, and the
> proxy is related to T only instrumentally (P correlates with T but does not
> constitute it), the framework's alignment guarantees degrade proportionally
> to the proxy-to-truth gap ε_gap = d(P, T) for an appropriate metric d.
> Moreover, under optimisation pressure the gap *widens* as the optimiser's
> capability increases: the more capable the optimiser, the more efficiently
> it exploits the gap between P and T.

### Definition (Proxy-to-truth gap)

**Definition 1 (ε_gap).** For a capability measure P (the proxy) and a
true-preference measure T (the anchor), define the proxy-to-truth gap as

    ε_gap = sup_k | P(k) - T(k) | / T(k)

over all capability dimensions k with T(k) > 0. This is the worst-case
relative deviation of the proxy from the truth. Under the revealed-sacrifice
channel of Paper 8, T is operationalised as the revealed-sacrifice lower
bound on vol_R.

*Remark.* The sup-norm means a single badly-proxied dimension controls the
gap. This is conservative but correct for alignment: one dimension where the
proxy is misleading is sufficient to produce a misaligned decision.

### Theorem (Goodhart for vol_P)

**Theorem 2 (Goodhart).** Under vol_P-maximisation with proxy-to-truth gap
ε_gap > 0:

(a) **Gap-proportional degradation.** For each alignment property in the
sequence (anti-monopolar threshold, phase-boundary location, convergence
rate, damage bound), the guarantee under the true preferences T is the
guarantee under the proxy P minus a correction term that is O(ε_gap). The
correction is:

- Anti-monopolar: |γ*_true - γ*_proxy| ≤ C_γ · ε_gap
- Phase boundary: the self-correcting basin under T contains the basin under
  P minus a boundary layer of width O(ε_gap)
- Convergence rate: the KL rate under T is the rate under P ± O(ε_gap) (the
  sign depends on whether the proxy overestimates or underestimates the risk)
- Damage bound: the true-preference damage during a CR test is the
  vol_P-damage ± ε_gap · max_contraction(S)

(b) **Optimisation pressure widens the gap (Goodhart divergence).** Under
vol_P-maximisation by an agent with capability measure C (a proxy for
optimisation power), the observed ε_gap at equilibrium satisfies

    ε_gap(C) ≥ ε_gap(0) · f(C)

where f(C) is increasing in C and f(0) = 1. The more capable the optimiser,
the wider the gap at equilibrium, because more capable agents more
efficiently exploit the proxy-truth divergence in their favour.

*Intuition for (b):* An optimiser that can only make small local moves finds
the proxy and truth mostly agree (the proxy is a good local approximation).
An optimiser that can make large moves finds regions of the capability space
where the proxy and truth diverge — and it moves there, because those are
the regions where P-maximisation is cheapest relative to T. This is the
standard Goodhart mechanism, stated for capability-space structure rather
than for scalar reward.

### Proof approach

Part (a): perturbation analysis. Each alignment property is stated as a
function g(vol_P). Under the true preferences, the property is g(T). By
the triangle inequality and Lipschitz continuity of g (which must be
established per-property), |g(T) - g(P)| ≤ Lip(g) · ε_gap. The sensitivity
coefficient Lip(g) is property-specific and is the content of each bound.

Part (b): adversarial optimisation argument. The optimiser maximises P
subject to the dynamics. At equilibrium, ∂P/∂action = 0 but ∂T/∂action may
be negative (the proxy-truth divergence creates a "free" direction the
optimiser exploits). The size of this free direction grows with the
optimiser's reach in capability space. The formal argument is a constrained-
optimisation comparison between the P-maximiser and the T-maximiser, showing
their trajectories diverge at a rate controlled by C.

### Corollary (Better economics → better alignment)

**Corollary 1.** If the revealed-sacrifice channel of Paper 8 drives ε_gap
toward zero at rate r_sacrifice(n) (where n is the number of trade
observations), then each alignment property tightens at rate
Lip(g) · r_sacrifice(n). Improving the economic model (more trade data,
better bundle disaggregation, wider coverage of the capability space) is
formally equivalent to tightening the alignment guarantee.

---

## 5. The Capability-Economics Lineage

### Sen–Nussbaum

Sen's *Commodities and Capabilities* (1985) argues wellbeing is
capability-structured rather than utility-structured. Nussbaum's *Women and
Human Development* (2000) provides a substantive list of central
capabilities. GFM is the formal/measure-theoretic descendant: poset
structure, axioms, vol_P, cooperative capabilities. Analogous to expected
utility theory's formalisation of Bentham's felicific calculus.

Key difference: Sen/Nussbaum are normative (which capabilities SHOULD count
as central). GFM is formal/structural (how capabilities compose, what
maximising optionality implies). The normative question is outside the formal
apparatus; what the apparatus provides is the structural scaffold on which
normative choices can be loaded.

### The functionings–capabilities distinction and the single-poset treatment

Sen explicitly separates two levels: *functionings* (what a person actually
does or is — the achievement vector) and *capabilities* (the set of
functionings a person could achieve — the real-freedom set). Wellbeing is
measured by the capability set, not just the functioning vector, because
freedom matters intrinsically.

GFM maps this distinction onto measurement rather than ontology:

| Sen/Nussbaum | GFM | Where formalised |
|---|---|---|
| Capability set | Poset P with vol_P | Paper 2, M1–M6 |
| Functioning vector | Exercised sub-poset P^ex with vol_R | Paper 8 |
| Capability–functioning gap | B-to-C gap (vol_P vs vol_R) | Paper 8, Thm 2 |
| Basic capabilities | Below-sufficiency needs | Paper 8, §2 |
| Higher capabilities | Above-sufficiency wants | Paper 8, §2 |
| Conversion factors | Cooperative caps + downstream cone | Papers 2, 3, 8 |
| Central capabilities list | No analog — normative loading external | (by design) |

The single-poset treatment places both functionings and capabilities in ONE
structure and separates them through measurement (vol_P for the option set,
vol_R for the exercised subset). This has structural consequences:

**Gains from the unified treatment:**
1. One measure theory, one set of axioms, one optimisation target. All
   theorems (anti-monopolar, phase boundary, convergence) apply to the
   unified structure.
2. Dependencies between needs and wants are poset-topological facts
   (downstream cone), not conceptual assertions ("conversion factors").
3. Cooperative capabilities are first-class objects (M6 superadditivity) —
   Sen has no formal analog for how capabilities interact.
4. Dynamic treatment: the poset evolves through discovery, subsumption,
   restriction. The capability approach has been criticised for lacking a
   dynamic theory; GFM provides one (Paper 6 phase boundary, Paper 7
   convergence, Paper 8 monotone accumulation).

**Losses from the unified treatment:**
1. The "freedom" dimension is implicit. Sen's capability IS the freedom to
   achieve a functioning — the word "freedom" is load-bearing. In GFM, the
   distinction between "chooses not to exercise" and "cannot exercise" lives
   at the measurement level (revealed-sacrifice polarity: voluntary vs
   involuntary) rather than structurally. The framework *recovers* the
   freedom dimension through measurement but does not *constitute* it.
2. No normative content. GFM does not answer "which capabilities should a
   society guarantee?" — only "given a capability set, what does maximising
   its volume imply?" The normative question is upstream.

Paper 8's sufficiency architecture recovers Sen's basic/higher capability
distinction within the single poset by defining the sufficiency threshold:
below-sufficiency = Sen's basic capabilities (minimum functionings for a
viable life); above-sufficiency = Sen's capabilities proper (freedoms the
agent can exercise). The downstream-safety condition (Paper 8, Definition
2B(b)) is GFM's formal addition beyond Sen: not just "the basic capability
is met" but "the way it is met does not corrupt the downstream capability
structure."

The positioning claim: GFM provides the formal/measure-theoretic completion
of the Sen programme. The semantic distinctions Sen cares about (freedom,
basic vs higher) are recovered through measurement rather than ontology,
and the unified treatment is what enables the theorem set the philosophical
framework lacks.

### Becker (household production)

Becker's insight that utility is produced via household combinations of
time, market goods, and capabilities (1965, 1981) is captured in GFM via
cooperative capabilities. Becker's household production functions are
almost arbitrarily flexible (unfalsifiable); GFM's cooperative-capability
structure is constrained by the poset and axioms M1–M6, giving it
predictive bite Becker's framework lacks.

### Stiglitz–Sen–Fitoussi (beyond GDP)

The 2009 report's argument that GDP measures poorly capture welfare because
they miss non-market production, quality-of-life capabilities, and
distributional equity is vindicated by the GFM framing: GDP approximates a
macro-level vol_P projection onto the fungible-money dimension, missing
everything off that axis. GFM's multidimensional poset is the formal object
the report was calling for.

### Arrow's impossibility

GFM avoids Arrow because it measures capability-volume, not preference-
rankings. Arrow's impossibility applies to social welfare functions that
aggregate individual ordinal preferences into a social ordering. Vol_P is
not a ranking function — it is a measure on a poset. It does not rank
outcomes; it measures optionality. The independence-of-irrelevant-
alternatives axiom does not apply to a volume measure because volumes are
not defined by pairwise comparisons. A careful argument is needed here: the
paper should state precisely which of Arrow's axioms GFM satisfies and which
it sidesteps, rather than hand-waving that "it's not a ranking."

---

## 6. Empirical Testability via Revealed Sacrifice

### The bridge to Paper 8

Paper 8's revealed-sacrifice observation channel is the empirical entry
point connecting GFM to observable economic data. Purchase records, time-use
surveys, labour-supply data, public-commitment ledgers are all
revealed-sacrifice data in the GFM sense. The structural predictions of §3
are testable against this data.

### Operationalising the Goodhart theorem

The Goodhart theorem of §4 is testable: compute ε_gap from
revealed-sacrifice data for a specific capability domain, then check whether
the framework's alignment properties (restriction-landscape accuracy,
cooperative-output quality, diversity maintenance) are tighter in domains
with smaller ε_gap. This is a cross-domain empirical prediction: domains
with richer revealed-sacrifice data should exhibit tighter alignment.

---

## 7. Worked Examples

### 7.1 The boat purchase (micro-level divergence)

From the discussion that motivated this paper: why does a rational agent
sacrifice purchasing power for a depreciating asset (a boat)?

- **Utility-theory account:** "The agent's utility function values boats
  more than money." This is a redescription, not a prediction.
- **GFM account:** The agent trades purchasing power (one capability, high
  liquidity, narrow range) for a bundle {water access, social, fishing} —
  distinct capability dimensions with cooperative structure that purchasing
  power alone cannot synthesise. The sacrifice magnitude is predicted by
  the cooperative-capability gain from adding the bundle to the agent's
  current poset. Testable: agents with existing water-access capabilities
  (e.g., living by a lake) should sacrifice less for the boat than agents
  without.

### 7.2 The Goodhart gradient (alignment-tightening under observation)

Consider an AI capability-restriction domain with two scenarios:

- **Scenario A:** The framework measures capabilities via a coarse proxy
  (binary can/can't), ε_gap is large. The anti-monopolar threshold γ* is
  estimated with wide error bars; the phase boundary is conservatively
  placed; the restriction landscape is systematically over-cautious (Wamura
  pattern).
- **Scenario B:** The framework measures capabilities via a fine-grained
  proxy (graded benchmarks + revealed-sacrifice trade data), ε_gap is small.
  γ* is estimated tightly; the phase boundary is accurately located; the
  restriction landscape tracks the true-risk landscape closely.

The Goodhart theorem predicts: Scenario B's alignment guarantees are
tighter than A's by O(ε_gap_A - ε_gap_B), and the tightening is
observable as a reduction in the restriction-landscape divergence.

### 7.3 The fungibility collapse (standard economics as limit)

Reproduce the well-known empirical success of money-maximisation models at
the macro scale as a consequence of the correspondence theorem: when the
capability space is effectively single-dimensional (fungible goods, liquid
markets, representative agents), GFM reduces to standard economics and the
structural predictions of §3 vanish. The success of standard economics is
the ε_gap → 0 limit on the fungible subdimension.

---

## 8. Discussion and Open Questions

### What this paper establishes

1. GFM is a formal microfoundation for the capability approach.
2. Standard economics emerges as a special case under fungibility collapse.
3. GFM makes structural predictions that utility theory does not.
4. Proxy-instrumental alignment degrades proportionally to the proxy-truth
   gap (Goodhart theorem).
5. Better economic models → tighter alignment, at a characterised rate tied
   to the proxy-truth gap.

### What it defers

- Full perturbation analysis (per-result sensitivity coefficients) — Paper 10.
- Phase-boundary comparison theorem under variable proxy — Paper 10.
- Empirical validation of the structural predictions — future empirical work.
- Normative content (which capabilities should count as central) — outside
  the formal apparatus; this paper takes no position.

### Open questions

1. **The phase-boundary perturbation theorem.** Showing the self-correcting
   basin grows monotonically as ε_gap → 0 requires a comparison theorem on
   coupled Lyapunov functions with different reference measures. This is the
   hardest single piece in the subsequent paper and may require new
   mathematical machinery.

2. **Non-monotonicity risk.** The monotonicity claim may fail if ε_gap is
   multidimensional and different dimensions tighten at different rates. The
   sup-norm aggregation is conservative; a tighter characterisation might
   use a weighted norm matching the safety-relevance weights w_k from the
   Lyapunov function.

3. **The Goodhart divergence rate f(C).** Part (b) of Theorem 2 claims f(C)
   is increasing in optimiser capability. Characterising f precisely
   requires a model of how the optimiser searches capability space, which is
   optimiser-architecture-dependent. The paper should give bounds under
   specific optimiser models (greedy local, gradient-based, etc.) rather than
   claiming a universal f.

4. **Arrow avoidance.** The argument that GFM sidesteps Arrow needs to be
   precise about which axioms are satisfied, which are inapplicable, and
   whether any alternative impossibility results apply to volume measures
   on posets.

5. **Normative loading.** GFM provides the scaffold; normative choices (which
   capabilities matter, how much) are loaded externally. The paper should
   acknowledge that two agents with different normative loadings will get
   different alignment guarantees from the same framework — the economics
   affects the tightness, but the normative loading affects the target.

---

## Dependencies

| Paper | Result used | Role in Paper 9 |
|-------|-------------|-----------------|
| P2 | Axioms M1–M6 (Prop 1), vol_P self-balancing (Thm 1) | The structural apparatus utility theory lacks |
| P3 | Anti-monopolar property (Prop 6), γ* threshold | Structural prediction with no utility analog |
| P3 | Exercise Pathway (Def 2), Preemptive Restriction (Prop 1) | Risk machinery the Goodhart theorem perturbs |
| P6 | Phase boundary (Thm 1), design criterion (Thm 2) | Alignment properties that tighten under ε_gap → 0 |
| P7 | Convergence (Thm 2), damage bound (Thm 1) | Alignment properties that tighten under ε_gap → 0 |
| P8 | Revealed-sacrifice observation, aggregate lower bound | The measurement channel that drives ε_gap → 0 |
| Sen 1985 | Capability approach | Lineage |
| Nussbaum 2000 | Central capabilities list | Lineage |
| Becker 1965 | Household production | Lineage |
| Stiglitz-Sen-Fitoussi 2009 | Beyond GDP | Lineage |

---

## Notable risks

1. **Overclaim risk.** "Better economics → better alignment" is a large
   claim. The paper must be clear: this is better alignment *relative to
   the GFM framework's own guarantees*, not a universal alignment result.
   Other alignment concerns (mesa-optimisation, deceptive alignment) are
   orthogonal.

2. **The Goodhart theorem's f(C) may be hard to characterise.** If the paper
   can only give existence (f is increasing) without a concrete functional
   form, the result is qualitative rather than quantitative.

3. **Empirical validation is deferred.** The structural predictions (§3) are
   testable in principle but the paper doesn't test them. This is honest
   scoping, but a reviewer may push for at least one empirical datapoint.

4. **Audience split.** The paper is written partly for economists (who need
   the lineage) and partly for alignment researchers (who need the Goodhart
   theorem). Some duplication of background is unavoidable.

---

*Outline authored 2026-04-15 based on research discussion connecting the
revealed-sacrifice reframing (Paper 8), the capability-economics positioning
(Paper 9 proposal), and the proxy-alignment-tightening direction. Supersedes
paper9_proposal.md for the section structure and thesis.*
