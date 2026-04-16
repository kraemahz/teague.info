# Paper 8 Reframing Addendum: Need-Sufficiency Architecture and Benchmark Polarity

*Second reframing memo, written 2026-04-15 after the revealed-sacrifice
reframing (`paper8_reframing_revealed_sacrifice.md`) was sent to the
drafting agent. This memo does NOT supersede the first reframing — it
adds structural requirements that the first reframing's observation
channel depends on. The drafting agent should integrate both memos.*

## The problem this memo addresses

The revealed-sacrifice observation channel (first memo) assumes all
sacrifices have the same polarity: more sacrifice = more revealed value.
This is wrong. Some sacrifices are involuntary — the agent pays them not
because it values the outcome highly but because it has no cheaper
option for satisfying a requirement it cannot opt out of. For these
need-satisfying sacrifices, more sacrifice = worse situation (the
agent's needs are more expensive to meet).

The framework needs a structural requirement on poset construction —
before defining the measurement channel — that distinguishes
need-satisfaction from want-pursuit and orients benchmarks so that
vol_P-maximisation aligns with the agent's actual interest in both
regimes.

## Three discoveries from the discussion

### 1. Needs are not purely minimising

Initial intuition: needs should be minimised (minimise cost, distance,
time-of-access). Exhaustive check on basic needs (food, water, shelter,
healthcare, mobility) reveals: every need has BOTH maximising dimensions
(quality, quantity, reliability) and minimising dimensions (cost,
distance, time). Needs are not a single-polarity class.

What IS true: the cost dimensions of needs are where the polarity
problem lives, because cost-of-access is involuntary (the agent must
pay it regardless of preference).

### 2. Scalar sufficiency hides structural defects

A single "water access: sufficient" measurement hides that the water is
contaminated. The agent has water (passes the scalar threshold) but the
way the need is met is actively degrading future vol_P through
downstream effects (health, cognition, reproduction). The framework
reports green while the system corrodes from the root.

### 3. The correct structure is downstream-safe bundle sufficiency

Three levels of sufficiency, each strictly stronger:

**Level 1: Scalar threshold (insufficient).** "Water: yes/no."
Hides quality, reliability, and cost defects.

**Level 2: Bundle threshold (necessary but not sufficient).** All
dimensions of the need must independently meet their thresholds
simultaneously:

- Quantity ≥ s_quantity
- Quality ≥ s_quality (contamination ≤ s_contamination)
- Reliability ≥ s_reliability
- Accessibility ≤ s_access (distance, time)
- Price ≤ s_price

This catches lead contamination (quality dimension fails). But it
misses a subtler failure: what if the water passes all thresholds at the
measurement point but the satisfaction pathway degrades downstream
capabilities over time?

**Level 3: Downstream-safe bundle (the correct formulation).** The
bundle thresholds are all met AND the need-satisfaction pathway does not
produce net-negative effects on capabilities in the need's downstream
cone in the poset.

## Formal definition of downstream-safe sufficiency

A need N at position p_N in the poset has:

- **Dimensions** {d_1, ..., d_m} with thresholds {s_1, ..., s_m}
- **Downstream cone** Down(p_N) = {c : c depends on N in the poset}
- **Satisfaction pathway** π_N: the specific way the agent meets the
  need (which source, at what quality, at what cost)

**Definition (Downstream-safe sufficiency).** Need N is
downstream-safe sufficient under satisfaction pathway π_N iff:

(a) **Bundle thresholds met:** d_k(π_N) ≥ s_k for all dimensions k

(b) **Downstream non-degradation:** For every capability
c ∈ Down(p_N), the N-mediated contribution to c's quality under π_N
is non-negative:

    Δ_c(π_N) = quality_c(with N satisfied via π_N)
             - quality_c(with N at bare threshold) ≥ 0

Condition (b) says: satisfying the need via this pathway doesn't make
downstream capabilities worse than they'd be under bare-threshold
satisfaction. Lead-contaminated water violates (b) because health under
lead water is worse than health under threshold-clean water, even if the
lead concentration passes the quality threshold (EPA action level 15 ppb;
chronic effects occur below that).

## Connection to Paper 3's exercise-pathway machinery

The need-satisfaction pathway π_N is structurally an exercise pathway
(Paper 3, Definition 2). The downstream Δvol_P of the pathway is
evaluable using Paper 3's concentration-risk apparatus. Contaminated
water as a need-satisfaction pathway is a pathway with negative
downstream Δvol_P on health-dependent capabilities.

The framework should detect pathological need-satisfaction the same way
it detects risk claims: via the exercise-pathway contraction analysis.
The distinction from risk claims is that need-satisfaction pathways are
not "optional" — the agent must satisfy the need — so the framework's
response is "find a better satisfaction pathway" rather than "restrict
the capability."

## The sufficiency threshold as the polarity boundary

The sufficiency bundle is the structural boundary where revealed-
sacrifice polarity flips:

**Below sufficiency on any dimension:** The agent is investing to reach
minimum viable functionality. Sacrifice is involuntary (the agent must
reach sufficiency to operate). Sacrifice magnitude reveals
**cost-of-access** (how expensive is it for this agent to reach baseline
on this dimension). Larger sacrifice = worse situation. The
revealed-sacrifice channel should register this as a COST signal with
negative polarity.

**Above sufficiency on all dimensions:** The agent has reached
functionality and is choosing to invest further. Sacrifice is voluntary
(the agent could stop at "good enough"). Sacrifice magnitude reveals
**preference strength** (how much the agent values the improvement
beyond baseline). Larger sacrifice = higher revealed value. The
revealed-sacrifice channel should register this as a VALUE signal with
positive polarity, per the first memo's mechanism.

## The benchmark-construction discipline

Each dimension of each capability needs:

1. A **sufficiency threshold** s_k
2. A **polarity-correct benchmark** that makes vol_P-maximisation align
   with the agent's interest in BOTH regimes

Below sufficiency: benchmark = min(actual_k / s_k, 1). Climbs from 0
toward 1 as the agent approaches sufficiency. Caps at 1. Maximising
this = closing the sufficiency gap = what the agent wants.

Above sufficiency: benchmark = 1 + α_k · max((actual_k - s_k) / s_k, 0)
where α_k < 1 discounts above-sufficiency gains relative to below-
sufficiency gains. This makes closing the sufficiency gap more valuable
per unit of improvement than enhancing beyond sufficiency — the correct
incentive structure for needs.

For cost dimensions (distance, price, time): actual_k = 1/cost_k,
with sufficiency at s_k = 1/max_acceptable_cost.

## How sufficiency thresholds are set

Four mechanisms, not mutually exclusive:

**(a) Poset-structural:** Capabilities with high fan-out (many downstream
dependents) have their sufficiency level set by the minimum required for
downstream capabilities to function. Computable from poset topology.

**(b) Empirical / cross-sectional:** Observe the population's actual
capability levels and identify the threshold below which agents
demonstrably cease functioning on downstream capabilities.

**(c) Revealed-sacrifice-derived:** Sufficiency is the level at which
sacrifice-polarity flips. Below sufficiency, sacrifice is involuntary
and increasing; above sufficiency, sacrifice becomes voluntary and
choice-driven. The transition point in the sacrifice data identifies
the threshold empirically. This is the most framework-native option.

**(d) Normative / external:** A human authority or governance process
declares sufficiency levels. This is the Sen/Nussbaum approach. The
framework's formal apparatus is agnostic to the source; it needs the
thresholds as input.

Primary mechanism: (c) with (a) as structural validation. The
revealed-sacrifice data shows where the transition from involuntary to
voluntary sacrifice occurs; the poset topology confirms the transition
corresponds to a structurally meaningful threshold.

## How this resolves capability-stuffing

Stuffed capabilities (distance from A to gas station, distance from B to
gas station, ...) all measure the same need from different vantage
points. Under downstream-safe bundle sufficiency:

- The bundle has ONE set of thresholds (fuel accessibility ≥ threshold on
  each dimension)
- Once the bundle is sufficient, additional measurements don't change the
  sufficiency status
- Stuffed capabilities provide no downstream-quality improvement
- The benchmark caps at 1 on the below-sufficiency component and the
  above-sufficiency component gives credit only for genuine quality
  improvement (cheaper fuel, faster access), not for re-measurement from
  different positions

The bundle structure + downstream-safety naturally resists stuffing
without needing a separate anti-stuffing mechanism.

## What this means for Paper 8's structure

Paper 8 should establish this architecture BEFORE defining the
revealed-sacrifice observation channel:

1. **§2 (new): Need-sufficiency architecture.** Define needs as
   multi-dimensional bundles with downstream-safety constraints. Establish
   the sufficiency threshold as the polarity boundary. Define the
   benchmark-construction discipline (below-sufficiency capping,
   above-sufficiency discounting, cost-dimension inversion).

2. **§3 (first memo's contribution): Revealed-sacrifice observation
   channel.** Now operates with correct polarity: below-sufficiency
   sacrifices are cost signals; above-sufficiency sacrifices are
   preference signals.

3. The aggregate B-to-C lower bound (first memo) becomes:

    vol_R ≥ Σ (want-sacrifice values) - Σ (need-access costs)

   The subtraction is the key structural move: need-costs reduce
   effective vol_R because they consume capability budget.

## Connection to Paper 9 (Goodhart theorem)

The need-sufficiency architecture gives the Goodhart theorem a specific
mechanism: a framework that fails to distinguish needs from wants (or
fails to invert cost-dimension benchmarks) produces a proxy vol_P that
is systematically misaligned with vol_R on the need dimensions. The
proxy rewards agents for having expensive-to-satisfy needs (high cost =
high sacrifice = high "revealed value") when the correct interpretation
is the opposite. The Goodhart divergence f(C) has a concrete driver:
more capable agents find more ways to re-frame need-costs as want-values,
inflating vol_P without improving vol_R.

## Connection to Sen/Nussbaum lineage

Sen's distinction between "basic capabilities" (functionings required for
a minimally decent life) and "complex capabilities" (freedoms to choose
among valuable life-options) maps exactly to below-sufficiency vs.
above-sufficiency. What the framework adds beyond Sen:

1. The downstream-safety condition that makes "sufficient" structurally
   rigorous rather than normatively asserted
2. The polarity-correct benchmark discipline that makes vol_P-max align
   with the agent's interest on BOTH sides of the threshold
3. The revealed-sacrifice transition as an empirical method for
   identifying the sufficiency threshold without normative declaration

## Open questions

1. **Threshold sensitivity.** How sensitive are the alignment properties
   to the exact placement of sufficiency thresholds? If the threshold is
   set too low (declaring "sufficient" when the agent isn't really
   functional), the polarity is wrong for the gap between threshold and
   true sufficiency. If set too high, the framework over-constrains the
   need and under-credits genuine above-sufficiency enhancement.

2. **Dynamic thresholds.** Sufficiency levels may shift over time as
   technology and social context evolve. What was sufficient water access
   in 1900 (a well within walking distance) is insufficient today
   (piped, treated, on-demand). The framework needs a mechanism for
   updating thresholds, which connects to Paper 7's controlled-relaxation
   idea applied to sufficiency standards themselves.

3. **Cross-cultural variation.** Different cultures may set sufficiency
   thresholds differently (what counts as "sufficient food" varies
   enormously). The framework should handle this as a normative input
   (mechanism (d) above) without asserting a universal threshold.

4. **Interaction with the axioms.** M5 (non-triviality) gives every
   capability positive weight. Under the capped-benchmark discipline,
   sufficiency-met needs contribute a fixed cap (not zero). But the
   weight of the cap (how much vol_P credit do you get for having your
   needs met?) is a design parameter that affects the relative
   importance of need-satisfaction vs. want-pursuit in the vol_P
   measure. This is a structural design choice the framework must take
   explicitly.

5. **Need identification.** How does the framework identify which
   capabilities are needs vs. wants? The poset-structural approach
   (high fan-out = need) is a good heuristic but not infallible
   (healthcare has relatively low fan-out in the capability poset but
   is clearly a need). A hybrid of structural position + revealed-
   sacrifice polarity transition is probably required.

---

*End of second reframing memo. The drafting agent should integrate this
with the first memo's revealed-sacrifice framing: this memo provides the
poset-architectural precondition that the measurement channel depends on.*
