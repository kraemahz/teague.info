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
ε_gap → 0 — the economic model converges toward a true model of inner
preference, grounded operationally via the revealed-sacrifice channel of
[Revealed Sacrifice] (paper 8a) and interpreted through the gap-decomposition
architecture of [Need Sufficiency] (paper 8b) — every alignment property
proved in the sequence tightens in the direction of the truth, with the
rate dependent on deployment-specific S0/S4(a) attestation quality.

This converts the B-to-C gap from a binary precondition into a continuous
gradient and connects the alignment-quality question to the
economic-model-quality question: **better economic models → tighter
alignment, with the tightening direction measurable via the
revealed-sacrifice channel and the gap decomposition.**

The full tightening proof (perturbation analysis of each prior result under
ε_gap ≠ 0, with quantitative rates) is deferred to a subsequent paper
(Paper 10). This paper establishes (a) the correspondence, (b) the
structural-prediction class, (c) the Goodhart theorem, and (d) the
qualitative direction of the tightening claim with concrete worked examples.

A structural caveat that 8a's residual-class characterization makes
unavoidable: ε_gap cannot in general be driven to zero. The residual class
(capabilities structurally outside the sacrifice channel's reach) sets a
non-zero floor on ε_gap in any deployment with non-empty residual
capabilities. The fungibility-collapse limit (§2) is precisely the limit
where the residual class is empty; real deployments operate above the floor.

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
operationally significant). The five structural features GFM adds beyond
P_std are:

1. **Non-fungibility** — poset structure with distinct capability dimensions
2. **Cooperative capabilities** — first-class objects not reducible to sums
3. **Anti-monopolar reasoning** — the γ* threshold with no utility-theory analogue
4. **Individuation without interpersonal comparison** — vol_P over shared poset
5. **Residual class** — capabilities structurally outside the sacrifice
   channel's reach (purely-private exercise with no material footprint).
   Standard economics has no notion of capability exercise that does not
   pass through markets; everything happens through prices and trade. The
   residual class of [Revealed Sacrifice] (Definition 12 of [Need
   Sufficiency]) is non-trivial only when fungibility-collapse fails. Under
   collapse, ResS = ∅ and the framework's measurement reach is total.

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
This is the population-scale γ* threshold. The wireheading-consistent HHI
of [Need Sufficiency] (Proposition 6) is the formal instrument for this
prediction: trade-flow concentration measured cross-sectionally should
correlate with wellbeing-correlate trajectories.

**Prediction 5: Mixed-polarity bundle-for-bundle traces.** Trades
surrendering a bundle for another bundle (canonical: residential
relocation) carry mixed need-side and want-side polarities on different
components of the surrendered/acquired bundles. GFM (with the
bundle-decomposition extension flagged in [Revealed Sacrifice], Remark 5
and Open Question 2) predicts that two agents performing nominally
identical priced trades will produce different need-share vs want-share
splits depending on their pre-trade need-satisfaction state. Utility theory
has no analog: it sees only the priced trade and a single-axis utility
delta. The prediction is testable cross-sectionally given pre-trade
need-attestation data.

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

    ε_gap = sup_{k : c_k ∉ ResS}  | P(c_k) - T(c_k) | / T(c_k)

over all capability dimensions k whose underlying capability c_k is not in
the structural residual class ResS of [Need Sufficiency], Definition 12,
and with T(c_k) > 0. This is the worst-case relative deviation of the
proxy from the truth on capabilities the sacrifice channel can in principle
reach. The residual class is excluded from the sup not because it is
proxy-aligned but because the proxy's measurement scope structurally
excludes it; capabilities in ResS contribute neither to the proxy's
disagreement budget nor to its alignment guarantee. Under the
revealed-sacrifice channel of [Revealed Sacrifice], T(c_k) is
operationalised as vol_R^[W](c_k), with vol_R^lower as a constructible
lower bound (Theorem 2 of [Revealed Sacrifice]).

*Remarks.*
1. The sup-norm means a single badly-proxied dimension controls the gap.
   This is conservative but correct for alignment: one dimension where the
   proxy is misleading is sufficient to produce a misaligned decision.
2. ε_gap is bounded above by (1 − β^lower)/β^lower on the
   observed-and-non-residual subset, giving a *measurable* ceiling from
   trade data. The 5-cell δ-decomposition of [Need Sufficiency] (Definition 8)
   further attributes the ceiling across cells: δ_covered is the
   proxy-failure-candidate component, δ_dormant + δ_restricted +
   δ_boundary is the structural-invisibility component, δ_residual is
   the residual-class floor.
3. ε_gap inherits a non-zero floor in any deployment with non-empty ResS.
   The fungibility-collapse limit of §2 is the limit where this floor is
   zero; real deployments operate above it, and the floor's magnitude is
   itself a property of the deployment's individuation discipline.

### Theorem (Goodhart for vol_P)

**Theorem 2 (Goodhart).** Under vol_P-maximisation with proxy-to-truth gap
ε_gap > 0:

(a) **Gap-proportional degradation.** For each alignment property in the
sequence (anti-monopolar threshold, phase-boundary location, convergence
rate, damage bound, aggregate lower bound's slack), the guarantee under the
true preferences T is the guarantee under the proxy P minus a correction
term that is O(ε_gap). The correction is:

- Anti-monopolar: |γ*_true - γ*_proxy| ≤ C_γ · ε_gap
- Phase boundary: the self-correcting basin under T contains the basin under
  P minus a boundary layer of width O(ε_gap)
- Convergence rate: the KL rate under T is the rate under P ± O(ε_gap) (the
  sign depends on whether the proxy overestimates or underestimates the risk)
- Damage bound: the true-preference damage during a CR test is the
  vol_P-damage ± ε_gap · max_contraction(S)
- Aggregate lower bound slack: β^lower from [Revealed Sacrifice] approaches
  the true β as ε_gap → ε_gap^floor, with the per-property Lipschitz factor
  decomposing into S0 attestation slack, Part-A vs Part-B aggregation, and
  observation density. This is the most direct connection between Goodhart
  and the measurement theorem: 8a's lower bound is itself a property whose
  tightness is governed by the ε_gap.

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

*Empirical witness for (b):* The wireheading-consistent HHI of [Need
Sufficiency] (Proposition 6) is a concrete instrument for the
optimization-pressure → gap-widening claim. As an optimiser's capability
grows and it begins exploiting proxy-truth divergence regions, the trade-flow
distribution concentrates on a narrower set of bundle categories — exactly
the signature the HHI detects. Part (b)'s qualitative claim is empirically
operationalized by the third-party-observable HHI variant (Proposition 7 of
8b), which reads concentration directly from the public committed-event
ledger plus S1-admissibility labels. f(C) is hard to characterize
analytically but has empirical-witness backing through this instrument.

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

**Corollary 1 (Direction).** If the revealed-sacrifice channel of [Revealed
Sacrifice] is admissibly accumulating observations, then β^lower is
non-decreasing in the observation count (Propositions 2 and 3 of 8a), and
the upper bound on ε_gap derived from (1 − β^lower)/β^lower is
non-increasing. By Theorem 2(a), each alignment property's deviation from
the truth is non-increasing in the same direction. Improving the economic
model (more trade data, better bundle disaggregation, wider coverage,
sharper S0 attestation, finer 5-cell δ-attribution) tightens each
alignment guarantee in the direction of the truth.

*Caveats on rate.* This corollary states a *direction* (monotonicity), not
a rate. 8a's Propositions 2 and 3 are existence statements about
non-decreasing β^lower; they do not bound *how fast* β^lower converges, and
the convergence rate depends on (i) S0 attestation quality, (ii) Part-A vs
Part-B aggregation choice, (iii) observation density, (iv) the residual-
class floor ε_gap^floor, none of which 8a quantifies. Bounding the rate is
the natural follow-up direction (Paper 10).

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
| Capability set | Poset P with vol_P | [Poset Definition], M1–M6 |
| Functioning vector | Exercised sub-poset P^ex with vol_R | [Revealed Sacrifice], Def 3 |
| Capability–functioning gap | B-to-C gap (vol_P vs vol_R), 5-cell δ-decomp | [Revealed Sacrifice] Thm 2; [Need Sufficiency] Def 8 |
| Basic capabilities | Below-sufficiency needs | [Need Sufficiency] §2 |
| Higher capabilities | Above-sufficiency wants | [Need Sufficiency] §2 |
| Conversion factors | Cooperative caps + downstream cone | [Poset Definition], [Horizon Aware], [Need Sufficiency] |
| Central capabilities list | No analog — normative loading external | (by design) |
| Freedom vs achievement | Polarity boundary + S1-attestation layer | [Need Sufficiency] §2.3 (def:polarity_boundary); [Revealed Sacrifice] Rem 18 (rem:external_attestation) |
| Residual capabilities | Structural residual class ResS | [Need Sufficiency] §5 (def:residual_class) |

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
   at the measurement level: [Need Sufficiency]'s polarity boundary
   (Definition 3) plus [Revealed Sacrifice]'s S1-attestation layer
   (Remark 18) jointly carry the freedom dimension. Above the polarity
   boundary, sacrifice reveals preference (the agent could have done
   otherwise). Below, sacrifice reveals cost-of-access (the agent had no
   non-degrading alternative). The S1-attestation layer formalizes the
   "could have done otherwise" check that makes "freedom" operationally
   distinguishable from "achievement". The framework *recovers* the freedom
   dimension through measurement + attestation rather than *constituting*
   it ontologically — but the recovery is now formally complete, not
   informal.
2. No normative content. GFM does not answer "which capabilities should a
   society guarantee?" — only "given a capability set, what does maximising
   its volume imply?" The normative question is upstream.

[Need Sufficiency]'s sufficiency architecture recovers Sen's basic/higher
capability distinction within the single poset by defining the sufficiency
threshold (def:polarity_boundary): below-sufficiency = Sen's basic
capabilities (minimum functionings for a viable life); above-sufficiency =
Sen's capabilities proper (freedoms the agent can exercise). The
downstream-safety condition ([Need Sufficiency], Definition 2(b)) is GFM's
formal addition beyond Sen: not just "the basic capability is met" but
"the way it is met does not corrupt the downstream capability structure."

The residual class ([Need Sufficiency] Definition 12) is a third dimension
Sen does not have: capabilities structurally outside the sacrifice
channel's reach (purely-private exercise with no material footprint). These
are Sen's capabilities *that the framework cannot measure*, not capabilities
that fail Sen's normative criteria. Recognizing the residual class as
analytically distinct from "low-priority" capabilities is a formal addition
that the philosophical literature has had no instrument for.

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

### The bridge to Paper 8a/8b

[Revealed Sacrifice]'s observation channel is the empirical entry point
connecting GFM to observable economic data. Purchase records, time-use
surveys, labour-supply data, public-commitment ledgers are all
revealed-sacrifice data in the GFM sense. [Need Sufficiency]'s diagnostic
architecture (gap decomposition + wireheading HHI + need-access cost)
provides the interpretation layer that turns raw observation into testable
predictions. The structural predictions of §3 are testable against this
data through a small set of formal instruments:

1. **Two channels (money + time)** ([Revealed Sacrifice] §4) provide
   independent observation modalities. Predictions 1–3 are testable via
   either channel; cross-channel triangulation gives robustness.
2. **Aggregate lower bound β^lower** ([Revealed Sacrifice] Theorem 2)
   provides the per-domain ε_gap upper estimate.
3. **Five-cell δ-decomposition** ([Need Sufficiency] Definition 8) attributes
   ε_gap across cells (covered, dormant, restricted, residual,
   boundary-residual), distinguishing proxy-failure from
   structural-invisibility components.
4. **Wireheading-consistent HHI** ([Need Sufficiency] Proposition 6, 7) is
   the population-scale concentration instrument for Prediction 4 and the
   empirical witness for Theorem 2(b).
5. **Need-access cost (NAC)** ([Need Sufficiency] Definition 9) tracks
   below-sufficiency expenditure; Prediction 5 (mixed-polarity bundles) is
   testable through NAC vs above-sufficiency aggregate splits.
6. **Worked example** ([Need Sufficiency] §6) is a four-phase
   computed-end-to-end demonstration that all of these instruments compose;
   it serves as a methodology template for cross-domain studies.

### Operationalising the Goodhart theorem

The Goodhart theorem of §4 is testable: compute the upper estimate of
ε_gap as (1 − β^lower)/β^lower from revealed-sacrifice data for a specific
capability domain, decompose across cells via the δ-attribution, then check
whether the framework's alignment properties (restriction-landscape
accuracy, cooperative-output quality, diversity maintenance) are tighter
in domains with smaller ε_gap. This is a cross-domain empirical prediction:
domains with richer revealed-sacrifice data and smaller residual-class
floors should exhibit tighter alignment.

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
  current poset, formalised via [Revealed Sacrifice]'s event-local bundle
  decomposition (Definition 4): the α_{n,c} coefficients per capability
  per event quantify the per-component contribution to the trade's
  ΔvolL(X_n). Testable: agents with existing water-access capabilities
  (e.g., living by a lake) should produce smaller cooperative-gain
  α-coefficients on the {water access} component, predicting smaller
  sacrifice magnitude.

### 7.2 The Goodhart gradient (alignment-tightening under observation)

Consider an AI capability-restriction domain with two scenarios, each
characterizable through 8a/8b's instruments:

- **Scenario A:** The framework measures capabilities via a coarse proxy
  (binary can/can't), with sparse trade observation and weak S0
  attestation. β^lower is low (high (1 − β^lower)/β^lower upper bound on
  ε_gap), with substantial mass in δ_residual + δ_dormant +
  δ_restricted (structural invisibility) plus a wide δ_covered band
  (proxy-failure-candidates not separable from observation slack). The
  anti-monopolar threshold γ* is estimated with wide error bars; the phase
  boundary is conservatively placed; the restriction landscape is
  systematically over-cautious (Wamura pattern).
- **Scenario B:** The framework measures capabilities via a fine-grained
  proxy (graded benchmarks + dense revealed-sacrifice trade data + sharp
  S0 attestation). β^lower is high, δ_residual is at the structural floor,
  δ_covered is small. γ* is estimated tightly; the phase boundary is
  accurately located; the restriction landscape tracks the true-risk
  landscape closely.

The Goodhart theorem predicts: Scenario B's alignment guarantees are
tighter than A's by O(ε_gap_A − ε_gap_B), where the difference decomposes
across cells (smaller δ_covered, smaller δ_dormant, same-or-smaller
δ_residual). The tightening is observable as a reduction in the
restriction-landscape divergence — and the cell-wise attribution tells the
deployer *which* improvement (more observation, sharper attestation,
finer individuation) is producing the tightening.

### 7.3 The fungibility collapse (standard economics as limit)

Reproduce the well-known empirical success of money-maximisation models at
the macro scale as a consequence of the correspondence theorem: when the
capability space is effectively single-dimensional (fungible goods, liquid
markets, representative agents), GFM reduces to standard economics, the
residual class is empty (ResS = ∅), the gap decomposition collapses to
δ_covered alone (no dormant, residual, restricted, or boundary cells),
and ε_gap → 0 globally. The structural predictions of §3 vanish under
collapse. The success of standard economics is the ε_gap → 0 limit on the
fungible subdimension; its limitations are the regions where the limit
fails (residual-class capabilities, cooperative structure, individuation
asymmetries).

### 7.4 Residential relocation (mixed-polarity bundle-for-bundle)

A bundle-for-bundle trade illustrating Prediction 5 and the
mixed-polarity gap in 8a's Open Question 2. An agent moves from home A to
home B, surrendering a bundle {location_A, neighborhood_A, school_A,
commute_A, ...} for {location_B, neighborhood_B, school_B, commute_B, ...}.

- **Utility-theory account:** ΔU = U(B) − U(A) > 0 because the agent
  chose B. No further structure.
- **GFM account:** The trade carries mixed polarity. The shelter
  dimension is need-side (retention without shelter is degrading); the
  remaining dimensions (kitchen, neighborhood, square footage) are
  want-side. Different agents performing nominally identical priced
  trades produce different need-share vs want-share splits depending on
  their pre-trade need-satisfaction state. An agent moving from a
  foreclosed home to renter-shelter has high need-share; an agent moving
  for a higher-paying job has high want-share.

Testable predictions: (i) agents with similar priced relocation but
different pre-trade need-attestation should produce different δ_NAC vs
above-sufficiency contributions in the gap decomposition; (ii) the
S1-attestation layer's H1+H2 classification (retention degrading, no
non-degrading third alternative) should bifurcate the population into the
two regimes; (iii) the wireheading-consistent HHI on relocation
sub-categories should distinguish concentration patterns
(forced-relocation regions vs voluntary-mobility regions).

This example also illustrates the Goodhart corollary's deployment
sensitivity: a relocation-tax framework optimising "average price paid"
(volP proxy) without distinguishing need-share from want-share would tax
both regimes identically, generating misalignment with the framework's
aggregate well-being target. Sharper economics (the bundle decomposition)
produces better alignment.

---

## 8. Discussion and Open Questions

### What this paper establishes

1. GFM is a formal microfoundation for the capability approach.
2. Standard economics emerges as a special case under fungibility collapse.
3. GFM makes structural predictions that utility theory does not.
4. Proxy-instrumental alignment degrades proportionally to the proxy-truth
   gap (Goodhart theorem).
5. Better economic models → tighter alignment, in the direction of the
   truth, with the magnitude attributable across the 5-cell δ-decomposition
   of the gap.
6. The residual class sets a non-zero floor on ε_gap in any deployment
   with non-empty residual capabilities; alignment-tightening is bounded
   below by this floor.

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

6. **Quantitative rate for ε_gap convergence.** [Revealed Sacrifice]'s
   Propositions 2 and 3 prove monotonicity of β^lower under admissible
   accumulation but do not bound the convergence rate. Bounding the rate
   requires modelling S0 attestation quality as a function of attestation
   infrastructure (which [Revealed Sacrifice]'s Remark 18 explicitly scopes
   to a follow-up paper), Part-A vs Part-B aggregation choice, and
   observation density. Corollary 1's "rate" claim depends on this; until
   it is bounded, the corollary is restricted to direction (monotonicity).
   This is Paper 10's territory.

7. **Residual-class floor on tightening.** The residual class ResS sets a
   structural floor ε_gap^floor below which the gap cannot be driven by
   any amount of observation. Characterizing what governs the floor
   (individuation discipline, governance choices about what counts as
   "purely-private exercise") and how a deployment can shrink ResS through
   re-individuation is open. The fungibility-collapse correspondence shows
   ε_gap^floor → 0 as the deployment moves toward the standard-economics
   limit, but real-world deployments operate above the floor. This
   open question is structurally distinct from OQ 6: OQ 6 asks how fast
   we approach the floor; OQ 7 asks how low the floor goes.

---

## Dependencies

| Paper | Result used | Role in Paper 9 |
|-------|-------------|-----------------|
| [Poset Definition] | Axioms M1–M6 (Prop 1), vol_P self-balancing (Thm 1) | The structural apparatus utility theory lacks |
| [Horizon Aware] | Anti-monopolar property (Prop 6), γ* threshold | Structural prediction with no utility analog |
| [Horizon Aware] | Exercise Pathway (Def 2), Preemptive Restriction (Prop 1) | Risk machinery the Goodhart theorem perturbs |
| [Phase Redundancy] | Phase boundary (Thm 1), design criterion (Thm 2) | Alignment properties that tighten under ε_gap → 0 |
| [Controlled Relaxation] | Convergence (Thm 2), damage bound (Thm 1) | Alignment properties that tighten under ε_gap → 0 |
| [Revealed Sacrifice] | Aggregate B-to-C lower bound (Thm 2), monotone accumulation (Props 2, 3), bundle decomposition (Def 4), residual-class structure | The measurement channel that drives β^lower upward + the structural floor from the residual class |
| [Need Sufficiency] | Need-sufficiency architecture (Def 2), polarity boundary (§2.3), gap decomposition (Def 8), wireheading HHI (Props 6, 7), residual class characterization (Def 12), need-access cost (Def 9) | The architecture that interprets β^lower; the diagnostic instruments (HHI, NAC, δ-decomp) that operationalize ε_gap |
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
   orthogonal. The two distinct sources of tightening — observation
   density via [Revealed Sacrifice] and diagnostic decomposition via [Need
   Sufficiency] — should not be conflated; they contribute through
   different mechanisms (better β^lower vs better cell-level attribution
   of the gap), and the paper should keep them separate when discussing
   what "better economics" delivers.

2. **The Goodhart theorem's f(C) may be hard to characterise.** If the paper
   can only give existence (f is increasing) without a concrete functional
   form, the result is qualitative rather than quantitative. The risk is
   partially mitigated by [Need Sufficiency]'s wireheading-consistent HHI
   (Propositions 6, 7), which provides an empirical witness for f(C):
   trade-flow concentration is a directly measurable signal of
   optimization-pressure-induced gap-widening. f(C) remains hard to
   characterize *analytically*, but has empirical-witness backing through
   this instrument; the paper can offer the HHI as a deployment-readable
   proxy for f(C) rather than a closed-form bound.

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

*Revision 2026-05-01: updated for Paper 8 split (8a Revealed Sacrifice +
8b Need Sufficiency) and 22 rounds of cold-review iteration on those
papers. Added: residual-class floor on ε_gap (thesis caveat, §2 bullet 5,
§4 Definition 1 remarks 2-3, OQ 7); aggregate-lower-bound-slack as a
listed alignment property in Theorem 2(a); HHI as empirical witness for
Theorem 2(b); Prediction 5 (mixed-polarity bundle-for-bundle); §7.4
worked example (residential relocation); freedom-vs-achievement row in
the Sen/Nussbaum mapping; OQ 6 (quantitative rate, deferred to Paper 10).
Tonal change: Corollary 1 reframed from "rate" to "direction"
(monotonicity) since 8a's Propositions 2 and 3 prove direction, not rate.
Citation conventions updated to bracket-name shorthand throughout.*
