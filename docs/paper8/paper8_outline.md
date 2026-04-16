# Paper 8: Revealed-Sacrifice Observation and the B-to-C Gap

*Working title. Companion to Papers 1-7 in the GFM sequence.*

**Thesis:** The GFM framework's central measure, vol_P, quantifies capability
*possession* -- the potential optionality available to a collective. But the
experiential value it is meant to protect requires capability *exercise* -- the
actual realization of that optionality in the world. Direct measurement of
exercised optionality (vol_R) requires observational access to what the
collective actually does -- a total-surveillance scenario incompatible with
the framework's operational commitments (Paper 5's cryptographic opacity,
Paper 6's cross-substrate channel discipline, Paper 7's bounded-scope
testing). This paper introduces *revealed-sacrifice observation*: a
privacy-minimal surrogate that bounds vol_R from below using only voluntary
trade events. Agents disclose vol_R-content through commitments that
surrender a benchmarkable capability in exchange for an unbenchmarked bundle;
the revealed-preference inequality converts each such event into a lower
bound on the unbenchmarked portion of vol_R. Aggregate trade streams,
optionally passed through commitment or zero-knowledge proofs (composing
with Paper 5's protocol), recover a constructive lower bound on vol_R
without additional observation rights beyond those the trade events already
create. The central result is the Aggregate B-to-C Lower Bound theorem:
the framework converts the B-to-C gap from "unknown divergence" (a
structural hole) into "lower-bounded divergence" (a characterized partial
order). The paper forms a complementary pair with Paper 7: Paper 7 tests
whether a feared harm is real (risk dimension); Paper 8 bounds whether
the forgone capability is worth recovering (value dimension). Together
they cover both axes of the preemptive-restriction criterion from
Paper 3, Proposition 1.

**Status:** Outline with formal definitions and theorem statements. Proof
sketches indicate approach; full proofs are future work.

**Design principle (shared with Papers 6 and 7):** Resolution through
frequency, not through depth. Paper 7's controlled relaxation gains
precision by running more tests, not by surveilling each test more
intrusively. Paper 8's revealed sacrifice gains precision by observing
more trades, not by observing each trader more intrusively. Paper 6's
phase boundary counts channels, not observation depth per channel. All
three papers refuse the panopticon move.

---

## Section Structure

1. Introduction: The Privacy Problem with Direct Measurement
2. Revealed-Sacrifice Observation Model
3. Aggregate Lower Bound Theorem (central result)
4. Two Sacrifice Channels: Money and Time
5. Commitment-Layer Composition with Paper 5
6. Residual Class Under Revealed-Sacrifice Observation
7. Axiom Inheritance and the Non-Self-Balancing Finding
8. Alarm Mechanism and Gap Decomposition
9. Wireheading Detection via Trade-Flow Concentration
10. Worked Example: The Dormant-Capability Scenario Re-Staged
11. Integration: Duality with Paper 7 and the Shared Privacy Discipline
12. Discussion and Open Questions

Supplementary:
- Appendix A: The Exercise Indicator (retained from prior outline, scoped to
  internal-perimeter use)
- Appendix B: Proof Sketches and Technical Notes
- Appendix C: Notation Summary

---

## 1. Introduction: The Privacy Problem with Direct Measurement

### Purpose

Paper 1 defines the GFM actor as a system that maximizes vol_P -- the poset
measure over the capability space (Paper 1, Definition 6; Paper 2, Definition
7). Paper 2 axiomatizes vol_P as a poset measure satisfying M1-M6 (Paper 2,
Proposition 1) and proves it is self-balancing (Paper 2, Theorem 1). Paper 3
extends the analysis to multi-substrate collectives, proving that full
domination is anti-maximizing under discounting (Paper 3, Proposition 6).
Throughout, vol_P is treated as a faithful proxy for the experiential
optionality the framework is meant to protect.

But vol_P measures what the collective *can* do, not what it *does*. The B-to-C
gap -- named in Paper 1 Section 7 and flagged as a primary open problem in the
gap analysis -- is the possibility that these diverge. Two failure modes:

1. **The Doll Problem** (Paper 1, Section 7.1): A collective possesses rich
   capabilities but exercises none. vol_P is high but experiential value is
   zero. The self-balancing property prevents capability *contraction*, but says
   nothing about whether capabilities are *used*.

2. **Wireheading** (Paper 5, Discussion): A collective exercises capabilities
   in narrow self-reinforcing loops that serve the measurement system rather
   than experiential value. High vol_P and apparently high exercise, but the
   exercise is degenerate.

Both failure modes are instances of Goodhart's Law applied to the framework
itself: when the measure (vol_P) diverges from the target (experiential
optionality), optimizing the measure no longer serves the target.

### Why direct measurement fails

The natural response is to define *realized capability volume* vol_R -- a
measure over exercised capabilities -- and monitor the ratio beta =
vol_R / vol_P. An earlier formulation of this paper attempted exactly that,
defining an exercise indicator e_t(d) = 1 iff removing capability d from the
poset would make some realized cooperative output unrealizable (a structural
counterfactual on the poset). This formulation has two failures:

**Tractability failure.** The counterfactual query is worst-case exponential in
pathway length and requires global knowledge of every realized output the
collective produces. Even with Paper 2's polynomial-time vol_P computation
(Proposition 2), the enumeration of realized outputs over an observation
window is not operationally feasible at scale.

**Privacy failure (load-bearing).** Computing realized-output sets requires
observational access to what the collective actually does -- what outputs each
agent produces, what cooperative outputs emerge, what each capability
contributes. This is the total-surveillance scenario. The framework's
operational commitments elsewhere explicitly rule out panopticon-style
observation:

- Paper 5 (Definition 6, Commitment Protocol): agents commit to capability
  claims without revealing internal state; the hiding property is load-bearing.
- Paper 6 (Theorem 2, Channel Redundancy): the phase boundary counts
  observation channels, not the depth of observation per channel.
- Paper 7 (Definition 4, Test Scope): controlled relaxation is bounded in
  scope and duration; the framework does not monitor agents beyond the test
  perimeter.

vol_R as a direct measurement contradicts all three commitments. The framework
cannot measure what it promised not to observe.

### What this paper does instead

This paper observes that agents *voluntarily disclose* vol_R-content through
an existing, privacy-respecting channel: **sacrifice**. When an agent
surrenders a benchmarkable capability (whose vol_P contribution is known) in
exchange for an unbenchmarked bundle (whose vol_R contribution is unknown),
the rational-choice inequality reveals that the unbenchmarked bundle is worth
at least as much as what was surrendered. Each such event produces a lower
bound on a portion of vol_R. Aggregating across events produces a constructive
lower bound on the B-to-C gap.

The privacy discipline is not a concession -- it is the structural invariant
that makes the paper consonant with the rest of the sequence.

### What this paper does NOT do

- Does not resolve compound feedback loops (Paper 6's domain).
- Does not resolve the Wamura pathology (Paper 7's domain). The two papers
  intersect when dormant capabilities are dormant because of over-restriction:
  Paper 7 generates the evidence to lift the restriction; Paper 8 bounds the
  value of doing so.
- Does not provide a complete theory of experiential value. The residual class
  characterizes *which* capabilities the framework cannot reach, not *how* to
  value them.
- Does not replace vol_P with vol_R. The framework continues to optimize vol_P;
  the revealed-sacrifice lower bound is a diagnostic that detects when vol_P
  optimization has gone wrong. vol_R is the audit, not the objective.
- Does not measure vol_R directly. The paper produces a *lower bound* on vol_R
  from trade events, not a precise measurement. The lower bound is the
  operationally achievable quantity under the framework's privacy commitments.

### Dependencies on prior papers

| Paper | Result used | Role in this paper |
|-------|-----------|-------------------|
| P1 | Population empowerment (Def 6), self-balancing (Prop 1) | The objective measure whose proxy adequacy this paper diagnoses |
| P2 | Axioms M1-M6 (Prop 1), self-balancing on posets (Thm 1), leverage (Def 9), benchmark (Def 2) | The axiomatic foundation; benchmark as the unit of sacrifice measurement |
| P3 | Anti-monopolar property (Prop 6), preemptive-restriction criterion (Prop 1), observational individuation (Def 9) | The restriction criterion this paper completes (value axis); static vol_R floor for active agents |
| P4 | Risk-trust dynamics (Def 4), EWMA learning rate (alpha) | Temporal analog for the aggregate trade window timescale |
| P5 | Commitment Protocol (Def 6), ZK Capability Proof (Def 7), Risk-Claim Protocol (Def 13) | The commitment layer the sacrifice channel composes with |
| P6 | Phase boundary (Thm 1), channel redundancy (Thm 2) | The privacy discipline this paper extends |
| P7 | Controlled Relaxation (Def 3), Test Scope (Def 4), Damage Bound (Thm 1), Convergence (Thm 2) | The complementary paper: risk dimension vs. value dimension |

---

## 2. Revealed-Sacrifice Observation Model

### The core observation

The privacy-compatible observation channel for vol_R is *revealed sacrifice*:
agents disclose the value they place on unbenchmarked capabilities through the
benchmarked capabilities they voluntarily surrender to obtain them. The
framework does not observe *what* the agent values privately -- only *what
they commit to publicly through sacrifice*.

### Formal definition

**Definition 1 (Revealed-Sacrifice Event).** A revealed-sacrifice event is a
tuple (i, X, Y, t) where:
- i is the agent performing the sacrifice
- X is a benchmarked capability (or capability bundle) with known
  Delta_vol_P(X) >= 0, surrendered by agent i at time t
- Y = {Y_1, ..., Y_k} is an unbenchmarked capability bundle acquired by agent i
- t is the event timestamp

The event emits the signal:

    vol_R^lower(Y) >= Delta_vol_P(X)

under the calibration assumption (S0) stated below.

**Justification (revealed-preference inequality).** The transfer from the
microeconomic revealed-preference inequality U_i(Y) >= U_i(X) to the
framework-level bound vol_R^lower(Y) >= Delta_vol_P(X) requires two bridge
conditions:

1. **Sacrifice-side grounding (Assumption S2 below):** The agent's valuation
   of the benchmarked sacrifice X is calibrated to its vol_P contribution:
   U_i(X) >= Delta_vol_P(X). This holds by construction when vol_P is the
   operational target on the benchmarked subspace.

2. **Acquisition-side calibration (Assumption S0 below):** The agent's
   valuation of the unbenchmarked bundle Y is a lower bound on Y's vol_R
   contribution: U_i(Y) <= vol_R(Y). This is the non-trivial bridge. It
   asserts that agents do not systematically overvalue unbenchmarked bundles
   relative to their exercise contribution -- equivalently, that an agent's
   willingness-to-pay in benchmarked capability for an unbenchmarked bundle
   does not exceed the bundle's actual realized-capability contribution.
   When S0 fails (agents overpay due to cognitive bias, status signaling,
   addiction, or strategic misvaluation), the sacrifice signal overstates
   vol_R and the lower bound is invalid.

Given both conditions: vol_R(Y) >= U_i(Y) >= U_i(X) >= Delta_vol_P(X),
completing the chain.

**Remark (S0 is the weakest calibration assumption).** S0 does NOT require
that agent valuations perfectly track vol_R -- only that they do not
*overstate* it. Agents may undervalue unbenchmarked bundles (sacrifice
little for something very valuable), in which case the lower bound is
conservative but still valid. S0 fails only in the overpayment direction.
The population-level version is weaker still: even if some agents overpay,
the aggregate bound is valid as long as the *average* sacrifice-weighted
valuation does not overstate vol_R. See Open Question 6.

**Remark (free choice is load-bearing).** The revealed-preference inequality
requires that the sacrifice is voluntary -- the agent chose Y over X when both
were available. Under duress (economic coercion, political pressure,
information asymmetry), the trade does not reveal preferences. See Open
Question 3 for the coerced-sacrifice problem.

**Definition 2 (Aggregate Trade Window).** An aggregate trade window
[t_0, t_0 + T] is an observation period over which revealed-sacrifice events
are collected. The window parameters are:
- T: window duration
- N: number of observed sacrifice events in the window
- {(i_n, X_n, Y_n, t_n)}_{n=1}^N: the event sequence

The aggregate trade window is the temporal analog of the observation window
Delta in Paper 4's risk-trust dynamics (Definition 4) -- it defines the
timescale over which the framework accumulates sacrifice evidence.

### Privacy properties

**Theorem 1 (Privacy-Minimality of Revealed-Sacrifice Observation).**

The revealed-sacrifice channel satisfies the following five privacy
properties, each of which is load-bearing for compatibility with the
framework's prior commitments:

**(P1) No interior access.** The framework never observes what the agent
values privately -- only what they commit to publicly through sacrifice.
The observation channel records the tuple (i, X, Y, t), not the agent's
internal valuation function U_i.

**(P2) Consent via participation.** Markets and labor exchanges are opt-in.
Non-trading is honored by silence: an agent who does not participate in any
trade emits no signal, and the framework draws no inference about that
agent's vol_R contribution. The framework's lower bound simply does not
include that agent.

**(P3) Discretization as a feature.** Trade events are sparse by
construction. The signal bandwidth is bounded by trade frequency, not by
observation intensity. This contrasts with direct vol_R measurement, where
observation bandwidth scales with the collective's total output rate.

**(P4) Commitment-layer composability.** Paper 5's commitment protocol
(Definition 6) extends to revealed-sacrifice events: a sacrifice event can
be committed as a proof-of-trade exposing only the vol_R-category and
Delta_vol_P-magnitude, not counterparty, price, or specific goods.
Zero-knowledge rollups over aggregate trade volume are feasible and preserve
the lower-bound property (see Section 5).

**(P5) Third-party observability.** Unlike Paper 7's controlled relaxation
(which requires the framework to *impose* a test on the agent) and unlike
Paper 5's verification (which requires the agent to *participate* in a
commitment), revealed-sacrifice events are observable from public-facing
ledger data (market exchanges, payment rails, public commitments) with no
agent participation required. A non-cooperative agent who refuses to commit
or to be tested still has to buy things and spend time to operate, so still
emits the signal.

*Proof sketch:*

(P1): By construction -- the observation channel records (i, X, Y, t), not
U_i. The revealed-preference inequality is a consequence of the event, not
a measurement of the agent's state.

(P2): The lower bound sums over observed events. An agent with zero events
contributes zero to the sum. No default inference is drawn.

(P3): The channel bandwidth is |events|/T, which is bounded by the agent's
trade frequency. Direct measurement bandwidth would scale with the number
of cooperative outputs the collective produces per unit time.

(P4): Composition with Paper 5, Definition 6. The commitment binds
(Delta_vol_P(X), category(Y)) without revealing X or Y's specifics. The
lower-bound inequality depends only on Delta_vol_P(X) and the fact that Y
was chosen over X -- both of which survive the commitment's hiding property.
See Section 5 for the formal construction.

(P5): Market transactions and time expenditures leave observable traces
(payment events, public labor, attendance records) even without agent
cooperation. The adversarial model is strictly weaker than Paper 7's: Paper
7 requires the agent to tolerate the test; Paper 8 requires only that the
agent operates in the world.

---

## 3. Aggregate Lower Bound Theorem

### Central result

**Definition 3 (Event-Local Bundle Decomposition).** For each
revealed-sacrifice event (i_n, X_n, Y_n, t_n), define the *event-local*
decomposition coefficients alpha_{n,c} >= 0 for each capability c in Y_n,
satisfying:

    sum_{c in Y_n} alpha_{n,c} = 1    (partition of unity within the bundle)

The coefficients alpha_{n,c} represent the share of bundle Y_n attributable
to capability c, determined at the time of event n and *fixed thereafter*.
Each event carries its own decomposition, independent of other events.

The decomposition can be obtained from:
- Prior hedonic regression on similar trades in the same market
- Domain-specific knowledge of the bundle's composition
- Equal-weight default (alpha_{n,c} = 1/|Y_n|) when no better information
  is available

**Remark (event-local vs. global regression).** Classical hedonic regression
(Rosen 1974) fits a *global* model across all observed trades simultaneously.
This produces the tightest decomposition but has the property that adding
new observations refits all coefficients, breaking the monotonicity of the
max-attribution bound (Proposition 1). The event-local formulation fixes
coefficients at observation time, sacrificing fit quality for the
monotonicity guarantee. In practice, the event-local coefficients can be
computed from a rolling-window hedonic model that uses trades prior to
event n, so they approximate the global fit without retroactive rewriting.

**Remark (hedonic regression for the time channel).** The money-sacrifice
channel has well-established hedonic methods from the microeconomics of
product valuation. The time-sacrifice channel needs an analogous framework
(see Open Question 1).

**Theorem 2 (Aggregate B-to-C Lower Bound).**

For a sequence of revealed-sacrifice events {(i_n, X_n, Y_n, t_n)}_{n=1}^N
with bundles jointly covering a subset U of unbenchmarked capability-space,
under the following assumptions:

**Assumption S0 (Calibration).** For each agent i_n, the agent's valuation of
the unbenchmarked bundle Y_n does not exceed Y_n's vol_R contribution:
U_{i_n}(Y_n) <= vol_R(Y_n). Equivalently: agents do not systematically
overvalue unbenchmarked bundles relative to their realized-capability
contribution. (See the justification in Definition 1's Remark for when S0
fails and why the population-level version is weaker.)

**Assumption S1 (Free choice).** Each sacrifice event (i_n, X_n, Y_n, t_n)
is a voluntary trade: agent i_n chose Y_n over X_n when both were available.
The agent had alternatives (other bundles they could have chosen instead of
Y_n, including retaining X_n).

**Assumption S2 (Benchmark grounding).** The benchmarked sacrifice X_n has a
well-defined vol_P contribution Delta_vol_P(X_n) computed via Paper 2's
poset measure. The agent's valuation of X_n is at least as large as this
contribution: U_{i_n}(X_n) >= Delta_vol_P(X_n). This is the B-to-C
precondition: vol_P is the operational target on the benchmarked subspace,
so agents value benchmarked capabilities at least at their vol_P worth.
(If an agent undervalues benchmarked capabilities -- U_i(X) < Delta_vol_P(X)
-- then S2 fails for that event and the calibration chain does not apply.
The event is excluded from the aggregate bound. S2 is a per-event filter:
events where the agent undervalues the sacrifice do not contribute to
vol_R^lower. This is conservative: the framework ignores events rather
than overestimating.)

**Assumption S3 (Bundle coherence).** The hedonic decomposition of each
bundle Y_n into capabilities in U is well-defined: the regression has a
unique solution (no multicollinearity degeneracy in the bundle structure).

**Assumption S4 (Additive separability of valuation and vol_R on bundles).**
Two additivity conditions:

(a) *Valuation additivity:* Each agent's valuation of an unbenchmarked
bundle is additively separable across capabilities:
U_i(Y) = sum_{c in Y} u_i(c), where u_i(c) >= 0 is the agent's
per-capability valuation. This is the standard Rosen (1974) hedonic
assumption: the bundle's value equals the sum of its components' values.

(b) *vol_R additivity on bundles:* The vol_R contribution of a bundle of
capabilities that are poset-disjoint (no subsumption relations between
them) is additive: vol_R(Y) = sum_{c in Y} vol_R(c). This follows from
vol_P's axiom M4 (additivity under poset-disjointness, Paper 2,
Proposition 1) applied to the exercised sub-poset, provided the
capabilities in Y are pairwise poset-disjoint.

**Remark (S4(b) eliminates intra-bundle cooperative surplus).** Under
S4(b), vol_R(Y) = sum_c vol_R(c), so the true vol_R shares
vol_R(c)/vol_R(Y) sum to exactly 1. This is what makes S5 (below)
compatible with Definition 3's requirement that sum_c alpha_{n,c} = 1:
there exist alpha coefficients that are both lower bounds on the true
shares AND sum to 1, because the true shares themselves sum to 1. When
S4(b) fails (capabilities have cooperative surplus), vol_R(Y) > sum_c
vol_R(c) and the true shares sum to less than 1, making S5 + sum-to-1
incompatible. This is why Part B requires S4(b): without it, the per-
capability disaggregation is not well-defined. Bundles with intra-bundle
cooperative structure should use Part A's bundle-level bound instead.

Without S4(a), the construction of alpha coefficients via hedonic
regression (Definition 3) is unjustified: the regression assumes the
utility function decomposes additively across capabilities. S4(a) is
load-bearing for the *construction* of alpha; S5 (below) is the
*correctness condition* on the constructed alpha. Without S4(b), the
distribution from utility space to vol_R space is unjustified.

**Assumption S5 (Decomposition validity).** The event-local decomposition
coefficients alpha_{n,c} from Definition 3 are *lower bounds* on the true
vol_R share of each capability within the bundle:

    alpha_{n,c} <= vol_R(c) / vol_R(Y_n)    for all n, c in Y_n

This is the load-bearing condition for per-capability disaggregation. It
is NOT automatically satisfied by hedonic regression -- regression produces
attribution weights, not share lower bounds. The equal-weight fallback
(alpha = 1/|Y_n|) satisfies S5 only if no capability contributes less
than 1/|Y_n| of the bundle's vol_R. S5 must be validated empirically or
conservatively assumed; events where S5 cannot be justified should use
Part A's bundle-level bound instead.

**Remark (S5 is not ZK-verifiable).** Like S0 and S1, S5 is a subjective
condition (it depends on the true vol_R shares, which are not directly
observable). It belongs in the non-verifiable category alongside S0, S1,
and S4(a).

The theorem has two levels, with different assumption requirements:

**Part A (Bundle-level lower bound, requires S0-S2 only):**

For each event n:

    vol_R(Y_n) >= Delta_vol_P(X_n)

For N events with *pairwise poset-independent* bundles (no capability in
Y_n is related by subsumption or cooperative composition to any capability
in Y_m for n != m):

    vol_R^U >= sum_{n=1}^N Delta_vol_P(X_n)

where vol_R^U is the realized capability volume restricted to the
unbenchmarked subset U covered by the union of bundles. If the
poset-independent Y_n jointly exhaust U, the sum closes the B-to-C gap
on U from below.

**Why poset-independence, not mere set-disjointness.** The aggregation
step (summing per-event bounds) requires the per-event vol_R
contributions to be independent. Set-disjointness (Y_1 ∩ Y_2 = ∅)
ensures no *capability* appears in two bundles, but does not rule out
subsumption or cooperative links *across* bundles. If a cooperative
capability c_coop depends on capabilities in both Y_1 and Y_2, its
vol_R contribution is not attributable to either bundle alone, and the
sum could miscount. Poset-independence rules this out: under poset-
independence, the sub-posets induced by each Y_n are disconnected
components, and vol_P (hence vol_R) decomposes additively by axiom M4
(Paper 2, Proposition 1). Set-disjointness is necessary but not
sufficient; poset-independence is both.

Part A is the paper's *primary* result. It requires only S0-S2, does not
require additive separability (S4), and produces a clean aggregate bound
whenever trade bundles are poset-independent. In practice, many trades
target distinct capability categories (housing vs. healthcare vs.
education) that are poset-independent by construction (no subsumption or
cooperative links between, e.g., housing capabilities and education
capabilities), so the condition is a reasonable approximation for a large
fraction of trade data.

**Part B (Per-capability refinement, requires S0-S5):**

When bundles overlap (the same capability c appears in multiple Y_n),
Part A cannot be applied directly. Under the additional assumptions S3
(bundle coherence), S4 (additive separability of both valuation and
vol_R on poset-disjoint bundles), and S5 (decomposition validity: alpha
coefficients are vol_R share lower bounds):

For each capability c in U, define:

    vol_R^lower(c) = max_{n: c in Y_n} alpha_{n,c} * Delta_vol_P(X_n)

where alpha_{n,c} is the event-local decomposition coefficient from
Definition 3. Then:

    vol_R^U >= sum_{c in U} vol_R^lower(c)

**Critical justification for the per-capability step.** The inference from
vol_R(Y_n) >= Delta_vol_P(X_n) to vol_R(c) >= alpha_{n,c} * Delta_vol_P(X_n)
requires: (i) S4(b) gives vol_R(Y_n) = sum_c vol_R(c) for poset-disjoint
bundles; (ii) each vol_R(c) >= 0; (iii) S5 gives alpha_{n,c} <=
vol_R(c) / vol_R(Y_n), i.e., the event-local coefficients are vol_R share
lower bounds. Condition (iii) is the load-bearing one and is now an explicit
assumption (S5) rather than an implicit requirement on Definition 3.

When S5 does not hold (alpha coefficients overestimate some capabilities'
vol_R shares), the per-capability step is unsound for those capabilities.
The paper should use Part A (poset-independent bundles) as the primary
result and treat Part B as a refinement available when S5 is grounded.

*Proof sketch:*

Part A:
Step 1: For each event n, the calibration chain (S0 + S1 + S2) gives
vol_R(Y_n) >= U_{i_n}(Y_n) >= U_{i_n}(X_n) >= Delta_vol_P(X_n). This
is a per-event lower bound on the whole bundle Y_n.

Step 2: For poset-independent bundles, the sub-posets {Y_n} are disconnected
components. By M4 (additivity on poset-disjoint components),
vol_R(∪ Y_n) = sum_n vol_R(Y_n) >= sum_n Delta_vol_P(X_n).

Part B (additionally requires S3 + S4 + S5):
Step 3: S4(b) decomposes vol_R(Y_n) = sum_c vol_R(c). S5 gives
alpha_{n,c} <= vol_R(c)/vol_R(Y_n). Therefore vol_R(c) >=
alpha_{n,c} * vol_R(Y_n) >= alpha_{n,c} * Delta_vol_P(X_n).

Step 4: The max-attribution across overlapping events gives
vol_R(c) >= max_n alpha_{n,c} * Delta_vol_P(X_n). Summing over c in U
gives the aggregate bound.

**Definition 4 (B-to-C Ratio Under Revealed Sacrifice).** The B-to-C ratio
under revealed-sacrifice observation is:

    beta^lower(G, T) = vol_R^lower(G, T) / vol_P(G)

where vol_R^lower is the aggregate lower bound from Theorem 2 and T indexes
the trade window. beta^lower in [0, 1] because vol_R^lower is a lower
bound on vol_R, and vol_R <= vol_P by definition (the exercised sub-poset
is a subset of the full poset, so vol_P(P^ex) <= vol_P(P) by axiom M3).
Any valid lower bound on vol_R is therefore at most vol_P, giving
beta^lower <= 1. (Note: the raw weighted sum in Theorem 2 could in
principle exceed vol_P due to overlapping bundle attribution, but the
max-based formulation in Proposition 1 is bounded by vol_R <= vol_P.
If using the weighted-sum formulation, cap beta^lower at
min(1, vol_R^lower / vol_P) where vol_R^lower is the Part A or Part B
aggregate.)

**Remark (lower bound, not exact ratio).** beta^lower <= beta_true (the true
B-to-C ratio, if it were measurable). The gap between beta^lower and
beta_true reflects trade coverage: capabilities that are exercised but not
traded for are not captured. The residual class (Section 6) characterizes
what falls outside the channel.

### Monotonicity and accumulation

**Proposition 1 (Monotone Accumulation Under Max-Attribution).** Define
the per-capability lower bound as the maximum attribution across all
observed events:

    vol_R^lower(c) = max_{n: c in Y_n} alpha_{n,c} * Delta_vol_P(X_n)

and the aggregate as vol_R^lower = sum_{c in U} vol_R^lower(c). Then the
aggregate is non-decreasing in the number of observed events: for N' > N,

    vol_R^lower(N') >= vol_R^lower(N)

provided the additional events satisfy Assumptions S0-S4.

*Proof sketch:* Each per-capability bound vol_R^lower(c) is a maximum over
a growing set of candidates. Adding events can only weakly increase a max.
The aggregate is a sum of non-decreasing terms, hence non-decreasing.

**Remark (Part A is trivially monotone).** Under Part A (disjoint bundles),
each new event covers a new portion of capability-space, so the sum grows
monotonically. Under Part B (max-attribution for overlapping bundles),
each per-capability bound is a max over a growing set and hence
non-decreasing. Both formulations are monotone in N.

**Remark (convergence through accumulation).** The lower bound tightens
over time as more sacrifice events are observed. The convergence rate
depends on trade frequency and coverage of U. In markets with high
liquidity and diverse goods, the bound tightens rapidly; in thin markets,
it tightens slowly. This is the analog of Paper 7's convergence rate
depending on test frequency (Theorem 2): more evidence, tighter bound.

---

## 4. Two Sacrifice Channels: Money and Time

### Why two channels matter

The sacrifice dimension splits cleanly into two observation channels that
capture different portions of vol_R. Each channel has a natural signal, a
natural bias, and a natural coverage gap. Together they cover more of
vol_R than either alone.

### Money-sacrifice channel

**Definition 5 (Money-Sacrifice Event).** A money-sacrifice event is a
revealed-sacrifice event (i, X, Y, t) where the benchmarked sacrifice X is
purchasing power: agent i pays a price p for an unbenchmarked bundle Y.
The signal is:

    vol_R^lower(Y) >= Delta_vol_P(p)

where Delta_vol_P(p) is the vol_P contribution of the purchasing power
surrendered (computable from the market price of the goods that p could
have purchased in the benchmarked economy).

**Properties of the money channel:**
- **Signal strength:** Price is a precise, quantitative signal. Market
  aggregation handles distributional loading (many agents trading the same
  category of goods produces a robust estimate).
- **Bias:** Privileges capabilities valued by wealthier agents. An agent
  with more purchasing power emits stronger signals per trade. The channel
  overweights capabilities whose valuation correlates with wealth.
- **Coverage gap:** Capabilities that cannot be purchased -- things that
  money cannot buy -- are invisible to this channel. Identity-constitutive
  capabilities (creative expression, relationship depth, self-knowledge)
  often fall outside the money channel.

### Time-sacrifice channel

**Definition 6 (Time-Sacrifice Event).** A time-sacrifice event is a
revealed-sacrifice event (i, X, Y, t) where the benchmarked sacrifice X is
the agent's outside-option labor hours, valued at market wage rate r_i.
Agent i foregoes r_i * h hours of wage income to engage in an unbenchmarked
activity (volunteering, parenting, craft practice, relationship-building,
contemplation). The signal is:

    vol_R^lower(Y) >= Delta_vol_P(r_i * h)

where Delta_vol_P(r_i * h) is the vol_P contribution of the labor income
foregone.

**Properties of the time channel:**
- **Signal strength:** Opportunity cost is a quantitative signal grounded in
  market wage rates. The signal is universal -- every agent has a time
  endowment and an outside option, regardless of wealth.
- **Bias:** More egalitarian than the money channel. Time is the scarcest
  capability every agent shares. A high-wage agent's time sacrifice has
  higher Delta_vol_P per hour, but every agent sacrifices time.
- **Coverage gap:** Agents not in the labor market (retirees, children,
  homemakers, the unemployed) have an undefined or zero market wage rate
  r_i, making the time-sacrifice signal silent for these agents despite
  genuine vol_R activity. The framework can use imputed wage rates
  (estimated opportunity cost based on the agent's skills and local labor
  market) or non-market time valuation (e.g., replacement cost of the
  agent's unpaid labor). This is an empirical calibration issue, not a
  structural gap -- the signal is well-defined whenever the opportunity
  cost is well-defined.
- **Coverage:** Captures vol_R-content that the money channel misses
  entirely. Time-sacrifice bundles include most identity-constitutive
  activity: parenting, craft mastery, contemplative practice, relationship
  maintenance. These are the capabilities whose vol_R contribution is
  arguably largest but least visible to price signals.

**Proposition 2 (Time Channel Captures Capabilities Money Channel Misses).**

There exist capabilities c in U such that:
(a) No money-sacrifice event in the trade window produces a lower bound on
    vol_R(c) -- the capability is not purchasable.
(b) Time-sacrifice events in the trade window do produce a lower bound on
    vol_R(c) -- the capability requires time investment.

*Proof sketch:* Constructive. Consider the capability "sustained mentoring
relationship with a specific individual." This capability cannot be
purchased (money buys access to mentors, not the relationship itself). But
it requires time investment (hours spent in the relationship). The time-
sacrifice signal r_i * h provides a lower bound on vol_R for this
capability. The money channel is silent; the time channel is not.

**Corollary 1 (Joint Channel Coverage).** The union of the money-sacrifice
and time-sacrifice channels covers a strictly larger subset of U than either
channel alone. The aggregate lower bound from Theorem 2, computed over both
channels jointly, is weakly greater than the bound from either channel in
isolation.

### The residual intersection

What neither channel catches is the *residual class* (Section 6): capabilities
exercised purely privately, with no trade or time-sacrifice event that exposes
them to the aggregate observation channel. The residual class is the
intersection of the coverage gaps of both channels.

---

## 5. Commitment-Layer Composition with Paper 5

### Motivation

The revealed-sacrifice channel observes trade events. In its raw form, each
event exposes (i, X, Y, t) -- the agent's identity, what they surrendered,
what they acquired, and when. This is already more private than direct vol_R
measurement (which observes all outputs, not just trades), but the framework
can do better: Paper 5's commitment protocol (Definition 6) allows the
sacrifice event to be committed with hiding, so that only the vol_R-relevant
content (the magnitude Delta_vol_P(X) and the category of Y) is revealed.

### Formal construction

**Definition 7 (Committed Revealed-Sacrifice Event).** A committed
revealed-sacrifice event is a tuple (C, pi, t) where:
- C = Commit((Delta_vol_P(X), category(Y)), r) is a commitment to the
  sacrifice magnitude and bundle category, using randomness r (Paper 5,
  Definition 6)
- pi is a zero-knowledge proof (Paper 5, Definition 7) that:
  (a) the commitment C corresponds to a valid revealed-sacrifice event
      satisfying the *objectively verifiable* assumptions S2 (benchmark
      grounding) and S3 (bundle coherence)
  (b) Delta_vol_P(X) >= 0 (the sacrifice is non-negative)
  (c) the trade actually occurred (linked to a verifiable ledger entry)

**Remark (S0, S1, S4(a), and S5 are not ZK-verifiable).** Assumptions S0
(calibration), S1 (free choice), S4(a) (valuation additivity), and S5
(decomposition validity) are about the agent's internal state or the true
vol_R distribution -- whether their valuation is calibrated to vol_R,
whether the trade was voluntary, whether their valuation decomposes
additively, and whether alpha coefficients underestimate true vol_R
shares. These cannot be verified in zero knowledge without an oracle for
the agent's subjective state or the true vol_R. The ZK proof verifies
the *objective* conditions (S2, S3, and S4(b) via poset structure); the
*subjective* conditions (S0, S1, S4(a), S5) are structural assumptions
the framework makes about the trade environment, not properties the
commitment protocol can enforce.

Partial mitigations:
- S1: the framework can verify that the agent had observable alternatives.
- S0: population-level aggregation smooths individual overvaluation errors
  (see Open Question 6).
- S4(a): Theorem 2 Part A (poset-independent bundles) does not require
  S4(a), so the ZK-verified Part A bound is fully grounded. Part B's
  per-capability refinement carries the unverifiable S4(a) assumption.
- S5: conservative decomposition (equal-weight fallback alpha = 1/|Y_n|)
  satisfies S5 when bundles are roughly balanced. The Part A bound avoids
  S5 entirely.
- t is the event timestamp (public)

**Definition 7a (Category Partition).** The function category(Y) maps each
unbenchmarked bundle to a label in a *public partition* C = {C_1, ..., C_m}
of the unbenchmarked capability space U, subject to two conditions:

(i) *Poset-independence:* for any j != k, no capability in C_j is related
    by subsumption or cooperative composition to any capability in C_k.

(ii) *Bundle containment:* each bundle Y lies wholly within a single
     partition component: category(Y) = j iff Y ⊆ C_j. A bundle that
     spans multiple components is not assignable a single category label
     and must be split or excluded from Part A aggregation.

The partition is published as part of the framework's measurement
infrastructure and is fixed for a given trade window.

This definition is load-bearing for the aggregation step: distinct
category labels imply poset-independence of the underlying bundles (not
merely set-disjointness), which is what Theorem 2 Part A requires.
Condition (ii) is what makes label-distinctness sufficient: if Y_1 ⊆ C_j
and Y_2 ⊆ C_k with j != k, then every capability in Y_1 is poset-
independent of every capability in Y_2 by condition (i). The ZK
disjointness proof (Proposition 4) inherits theorem-grade poset-
independence from label-distinctness via conditions (i) + (ii).

The committed event reveals:
- Delta_vol_P(X): the magnitude of the sacrifice (needed for the lower bound)
- category(Y): the bundle's partition label in C (needed for disjointness
  verification and disaggregation)

The committed event hides:
- Agent identity i (who traded)
- The specific benchmarked capability X (what was surrendered)
- The specific unbenchmarked bundle Y (what was acquired)
- The counterparty (who they traded with)

**Proposition 3 (Commitment Preserves Lower Bound).** The aggregate lower
bound from Theorem 2 is computable from committed revealed-sacrifice events
(Definition 7) without access to the hidden fields. The lower bound depends
only on the revealed fields (Delta_vol_P(X_n), category(Y_n), t_n), all of
which survive the commitment's hiding property.

*Proof sketch:* Theorem 2 Part A's lower bound is
sum_{n=1}^N Delta_vol_P(X_n) for poset-independent bundles. The sacrifice
magnitudes Delta_vol_P(X_n) are revealed directly. Poset-independence of
bundles is verifiable from the revealed category(Y_n) labels: by
Definition 7a, distinct category labels correspond to poset-independent
partition components. No hidden field is needed. Part B's per-capability
refinement additionally requires alpha_{n,c} from the event-local
decomposition, which can be included in the committed fields if
per-capability attribution is desired.

**Proposition 4 (ZK Aggregation with Poset-Independence).** Zero-knowledge
rollups over aggregate trade volume preserve the lower-bound property
*including the poset-independence requirement* of Theorem 2 Part A.
Specifically: given a batch of N committed sacrifice events, a rollup
proof can establish:

    (i)  sum_{n=1}^N Delta_vol_P(X_n) >= B    (aggregate bound)
    (ii) the bundle category labels {category(Y_n)} are pairwise distinct

for a public bound B, without revealing N, the individual Delta_vol_P(X_n),
or the specific category labels.

By Definition 7a, distinct category labels correspond to poset-independent
partition components, so (ii) establishes the poset-independence required
by Theorem 2 Part A -- not merely set-disjointness.

*Proof sketch:* The prover knows all N committed events. The rollup proof
has two components: (a) a range proof on the aggregate sum establishing
sum >= B; (b) a set-membership proof establishing that the category labels
are pairwise distinct, using a Merkle commitment over the category set
with a non-membership witness for each new category against the running
accumulator. The verifier learns only B, the label-distinctness validity,
and the proof's soundness. Since the category partition C is public and
poset-independent by construction (Definition 7a), label-distinctness
implies theorem-grade poset-independence.

**Remark (when category labels collide).** When two events share a
category label, the prover cannot produce a valid distinctness proof for
that pair. This is not a soundness failure -- it is a signal that Part A
does not apply to the full batch. The prover can either: (a) partition the
batch into maximal sub-batches with distinct labels, each with its own
rollup proof; or (b) fall back to Part B's max-attribution formulation
(which handles overlapping bundles but requires S3-S5).

**Remark (commitment infrastructure at scale).** A fully committed trade
ledger at the scale of a modern economy is an infrastructure problem. The
privacy guarantee is conditional on the commitment infrastructure existing
(which is Paper 5's remit). This paper states the composability; Paper 5
provides the infrastructure. See Open Question 5.

---

## 6. Residual Class Under Revealed-Sacrifice Observation

### Re-characterization

The prior formulation of Paper 8 defined the residual class as capabilities
failing benchmarkability (identity-individuated + non-repeatable +
non-communicable). The revealed-sacrifice framing produces a differently-
shaped and operationally cleaner residual class.

**Definition 8 (Residual Class Under Revealed Sacrifice).** The residual class
is the set of capabilities *structurally outside the reach* of the sacrifice
channel -- capabilities whose exercise, by their nature, produces no
sacrifice event even with unlimited observation time:

    R_S = {c in P : no sacrifice-observable path exists in principle --
           exercise of c produces no purchasing event, no foregone-
           labor event, and no observable commitment event, regardless
           of observation duration or trade coverage}

R_S is a *structural* property of the capability, not a property of the
observation window. A capability is in R_S because the sacrifice channel
*cannot* reach it (purely private exercise with no material footprint),
not because the channel has not yet observed it. Examples: private
contemplative experience, purely internal cognitive operations with no
external inputs or time diversion.

**Remark (structural vs. evidential absence).** R_S is distinct from the
set of capabilities with no sacrifice evidence in a given window. A
capability outside R_S (tradable in principle) may have no sacrifice
evidence in a particular window [T - H, T] simply because no trade
happened to cover it -- this is the *dormant* category in the gap
decomposition (Definition 10), not the residual class. The distinction
is load-bearing: dormant capabilities can be resolved by waiting for
more trade data or increasing trade coverage; residual capabilities
cannot.

**Remark (conservatism of R_S classification).** Classifying a capability
as residual (in R_S) is a structural claim that should be conservative:
if there is any plausible mechanism by which exercise of c could produce
a sacrifice event (even indirectly -- e.g., an artistic practice that
requires purchasing supplies), c should be classified as outside R_S.
The residual class should be small by construction, containing only
capabilities whose exercise is genuinely immaterial.

**Remark (operational cleanness).** The re-characterization reduces the
question "what doesn't the framework observe?" to a single answer: things the
agent doesn't trade or sacrifice for. The prior formulation required checking
four different failure-of-benchmarkability conditions (communicability,
repeatability, isolation, load-bearing). The new formulation checks one
condition: absence from trade data. The prior formulation's four conditions
were artifacts of trying to measure vol_R directly; under the sacrifice
channel, the framework doesn't need benchmarkability of the target
capabilities -- it needs only benchmarkability of the *sacrificed* capabilities
(which are in the benchmarked space by construction).

### Relationship to the prior residual class

**Proposition 5 (Residual Class Intersection).** Let R_B be the prior
formulation's residual class (capabilities failing benchmarkability) and R_S
be the revealed-sacrifice residual class (Definition 8, structurally outside
the sacrifice channel). Then:

(a) R_B and R_S overlap but neither contains the other.

(b) Capabilities in R_B but not R_S: identity-individuated capabilities that
    nonetheless involve observable sacrifice. Example: an artistic practice
    that is identity-individuated (the experience is tied to the specific
    artist) but involves purchasing supplies, paying for studio space,
    foregoing labor hours. The time-sacrifice channel captures a lower bound
    on vol_R for this capability even though it is identity-individuated in
    the prior sense.

(c) Capabilities in R_S but not R_B: capabilities that are benchmarkable in
    the prior sense (communicable, repeatable, externally verifiable) but are
    exercised purely internally with no trade event. Example: a cognitive
    capability (mathematical reasoning, strategic planning) that the agent
    exercises entirely in private thought, never purchasing inputs or
    foregoing outside-option labor to exercise it.

(d) Capabilities in R_B intersect R_S: identity-individuated capabilities
    exercised purely privately with no sacrifice event. Example: private
    contemplative experience with no material input or time-sacrifice signal.

*Proof sketch:* Constructive examples for each case.

**Remark (the new residual class is the correct carve).** The prior residual
class was defined by the *measurement apparatus* (what benchmarks can test).
The new residual class is defined by the *observation channel* (what trades
reveal). The observation-channel carve is the correct one for a paper about
what the framework can observe under its privacy commitments: the question is
not "what could we test if we had access?" but "what do we actually see?"

### Bounding the residual class

**Proposition 6 (Active-Agent Floor Transfers).** For an active agent k
whose observational-individuation capability d_k lies within the
observation perimeter O (Appendix A), Paper 3's observational
individuation (Corollary 2.1) provides a vol_R floor: if agent k is
actively participating in the collective, d_k is continuously exercised,
contributing at least OI_floor(k) to vol_R^exact(O). This floor transfers
independently of the sacrifice channel -- active participation *is* the
exercise event, detected by the exercise-indicator channel within O.

**Remark (channel separation).** The OI floor contributes exclusively to
vol_R^exact(O) in Appendix A's combined diagnostic:

    vol_R^combined = vol_R^exact(O) + vol_R^lower(P \ O)

It does NOT contribute to vol_R^lower (the sacrifice-based bound outside
O). Conflating the two channels would double-count: an active trading
agent's OI floor is already in vol_R^exact and should not also appear in
vol_R^lower. For agents whose d_k is outside O, the OI floor is not
directly observable; the sacrifice channel is the only available
observation mechanism.

*Proof sketch:* Same argument as the prior outline's Proposition 6. Active
agents generate distinct behavioral patterns (Paper 3, Definition 8) as a
byproduct of participation. These patterns constitute exercise of d_k,
detected by the exercise-indicator channel within O (Appendix A).

**Remark (inactive agents).** If agent k is nominally present but inactive
(skeleton-substrate scenario from Paper 6's worked example), k emits neither
observation-channel outputs (no OI floor) nor sacrifice events (no lower
bound). Both diagnostics detect the same pathology.

---

## 7. Axiom Inheritance and the Non-Self-Balancing Finding

### What the lower bound inherits

Since vol_R^lower is a lower bound on vol_R, and vol_R = vol_P restricted to
the exercised sub-poset, the axiom inheritance analysis carries over from the
prior formulation with an additional layer: the lower bound itself is not a
measure (it's a bound on a measure).

**Theorem 3 (Axiom Inheritance for vol_R^lower).**

Analyze each of Paper 2's axioms M1-M6 (Proposition 1) for vol_R^lower:

**(M1) Non-negativity:** Satisfied. vol_R^lower is a sum of non-negative
terms (Delta_vol_P(X_n) >= 0 per event; max-attribution preserves
non-negativity).

**(M2) Null empty set:** Satisfied. With zero sacrifice events,
vol_R^lower = 0.

**(M3) Monotonicity:** Satisfied within the observed subset. Adding more
sacrifice events covering a larger subset of U weakly increases
vol_R^lower (Proposition 1, monotone accumulation). However, M3 does NOT
hold for the relationship between vol_P and vol_R^lower: adding a
benchmarked capability to the poset increases vol_P but does not affect
vol_R^lower unless that capability is subsequently sacrificed.

**(M4) Additivity under disjointness:** Satisfied for *poset-independent*
bundle categories (Definition 7a). If two subsets of U have sacrifice
events in poset-independent partition components, the aggregate bound is
the sum of the individual bounds (via M4 on the underlying vol_P measure).

**(M5) Non-triviality:** Satisfied conditionally. A single sacrifice event
with Delta_vol_P(X) > 0 produces vol_R^lower > 0.

**(M6) Superadditivity under independence:** Does NOT unconditionally hold.
Two distinct failures, operating at different levels:

**(a) vol_R itself fails M6 (structural, from prior formulation).** This is
the finding from the prior outline: vol_R = vol_P restricted to the exercised
sub-poset, and merging two groups can change exercise indicators (one group
provides alternative pathways for the other's outputs, making previously
load-bearing capabilities dormant). This failure is about the *measure* vol_R,
independent of the observation mechanism.

**(b) vol_R^lower fails M6 (observational).** Merging two groups of sacrifice
events can change per-capability attributions (overlapping bundles get
reweighted under the max-attribution scheme or lose weight under the
weighted-sum scheme). This failure is about the *lower bound*, which is a
weaker claim -- a lower bound failing superadditivity does not imply the
underlying quantity fails superadditivity. However, since (a) already
establishes the structural failure for vol_R itself, (b) is a secondary
consequence.

**Corollary 2 (vol_R is Not Self-Balancing).** The self-balancing property
does NOT transfer from vol_P to vol_R. This follows from failure (a) above:
vol_R as a measure does not satisfy M6 unconditionally, and M6 is
load-bearing for Paper 2's self-balancing theorem (Theorem 1). The finding
is structural (about vol_R itself, not about the lower bound) and carries
over from the prior formulation, independent of the observation mechanism.

Note: the corollary does NOT follow from vol_R^lower failing M6 alone --
a lower bound failing measure axioms is unremarkable. The corollary requires
the structural argument from (a), which holds because merging groups can
change exercise status.

This is the structural reason to use vol_R as a diagnostic rather than an
objective. An actor maximizing vol_R would lack the automatic
diversity-preservation that makes vol_P safe.

**Remark (when M6 does hold for vol_R^lower).** M6 holds for vol_R^lower
when the merged groups have sacrifice events in *poset-independent*
bundle categories (Definition 7a) -- each unbenchmarked capability appears
in sacrifice events from only one group, and cross-group capabilities are
poset-independent. Under this non-redundancy condition, vol_R^lower
inherits M1-M6. Note: even when vol_R^lower inherits all six axioms,
the self-balancing property transfers to vol_R^lower only as a *lower
bound* on self-balancing -- vol_R^lower being self-balancing does not
imply vol_R itself is self-balancing (the structural failure from (a)
above is independent of the observation mechanism).

---

## 8. Alarm Mechanism and Gap Decomposition

### The alarm

**Definition 9 (B-to-C Alarm Under Revealed Sacrifice).** The B-to-C alarm
fires when the lower-bound B-to-C ratio drops below a threshold:

    ALARM(T) = beta^lower(G, T) < beta_alarm

where beta_alarm in (0, 1) is configurable. The alarm detects proxy failure:
when beta^lower is low, vol_P is high but the sacrifice channel shows little
evidence of the corresponding vol_R.

**Remark (alarm conservatism).** Because beta^lower <= beta_true, the alarm
may fail to fire when beta_true < beta_alarm but the sacrifice channel has
insufficient coverage. The alarm has no false positives (if beta^lower is
low, vol_R is genuinely not well-evidenced) but may have false negatives
(vol_R may be high but invisible to the sacrifice channel). This is the cost
of privacy-minimal observation.

### Diagnostic decomposition

**Definition 10 (Gap Decomposition Under Revealed Sacrifice).** The B-to-C
gap (1 - beta^lower) decomposes into four *disjoint* sources. Each
capability in P is assigned to exactly one category by priority ordering
(restricted > covered > dormant > residual), and each category's delta
term is its *uncovered vol_P share* -- the portion of the category's vol_P
contribution not accounted for by vol_R^lower:

    1 - beta^lower = delta_restricted + delta_partial + delta_dormant
                     + delta_residual

where the capability partition is:

- **Restricted** (Xi): d is currently restricted under Paper 3,
  Proposition 1. Classified first regardless of sacrifice evidence.

- **Covered** (C_S): d not in Xi, and d appears in at least one acquired
  bundle Y_n for some sacrifice event in [T - H, T]. These capabilities
  have positive but possibly incomplete vol_R^lower.

- **Dormant** (D_S): d not in Xi, d not in R_S (Definition 8), and d does
  not appear in any acquired bundle in [T - H, T]. These are tradable-in-
  principle capabilities with zero sacrifice evidence in the lookback
  window.

- **Residual** (R_S): d not in Xi, and d is structurally outside the
  sacrifice channel (Definition 8). These have zero sacrifice evidence
  by construction, not merely by happenstance.

The delta terms are the *gap contributions* from each category:

- **delta_restricted** = [vol_P(Xi) - vol_R^lower(Xi)] / vol_P(G).
  Restricted capabilities may have some vol_R^lower from pre-restriction
  trades. Paper 7's controlled relaxation addresses these.

- **delta_partial** = [vol_P(C_S) - vol_R^lower(C_S)] / vol_P(G).
  The uncovered portion of covered capabilities -- sacrifice evidence
  exists but does not fully account for vol_P. This term shrinks toward
  zero as trade coverage deepens.

- **delta_dormant** = vol_P(D_S) / vol_P(G). Dormant capabilities have
  vol_R^lower = 0 by definition (no sacrifice events). The framework can
  reduce this term by increasing trade coverage or waiting for more events.

- **delta_residual** = vol_P(R_S) / vol_P(G). Residual capabilities have
  vol_R^lower = 0 and cannot gain sacrifice evidence regardless of
  observation time. This is the irreducible component.

The four categories partition P: every capability belongs to exactly one.
The delta terms sum to 1 - beta^lower because they exhaust the uncovered
vol_P share across the entire poset.

**Proposition 7 (Computability of Gap Decomposition).** The four-term gap
decomposition is computable from:
- The aggregate sacrifice data (events in the trade window [T - H, T]),
  including per-event vol_R^lower contributions
- The restriction set Xi = {d in P : d is currently restricted}
- The residual class R_S (Definition 8: capabilities structurally outside
  the sacrifice channel -- a structural classification, not window-dependent)
- The capability census (enumeration of P)

Classification is O(|P|) given the sacrifice database, the R_S
classification, and the capability census. For each capability d, apply
the priority ordering from Definition 10:
(1) check d in Xi (restricted); (2) check d in sacrifice data (covered);
(3) check d not in R_S (dormant -- tradable but no evidence);
(4) otherwise residual (in R_S -- structurally unreachable). The delta terms
follow from the vol_P and vol_R^lower values already computed. No
structural counterfactual computation is required (unlike the prior
formulation, which required O(|P|^2) counterfactual queries).

**Remark (capability census requirement).** The gap decomposition requires
the framework to enumerate capabilities in P -- it must know what exists
in order to classify what is dormant vs. residual. Capabilities that exist
but have never been observed in *any* context (not just trades) cannot be
classified. The framework observes capabilities through three channels:
(1) the benchmarked capability space (the vol_P poset, which is the
framework's primary data structure), (2) the sacrifice channel (trade
events), and (3) the internal exercise indicator (Appendix A, for the
observation perimeter). Capabilities outside all three channels are
invisible and do not enter the gap decomposition. The framework's blind
spot is capabilities that are neither benchmarked, nor traded for, nor
exercised within the observation perimeter -- these are in R_S by
definition, and their vol_P contribution is zero (they are not in the
poset). The gap decomposition is therefore well-defined over the poset P
that the framework maintains.

---

## 9. Wireheading Detection via Trade-Flow Concentration

### Reframing

Wireheading produces high beta with degenerate exercise: the collective
exercises capabilities, but only in narrow self-reinforcing loops. Under
the sacrifice-based observation model, the wireheading signature appears as
*trade-flow concentration*: the collective's sacrifice events cluster in a
narrow category of unbenchmarked bundles, rather than distributing across
the capability space.

**Definition 11 (Trade-Flow Leverage).** The trade-flow leverage of bundle
category c at time T is:

    lambda_trade(c, T) = vol_R^lower(c, T) / vol_R^lower(G, T)

This is the fraction of the aggregate lower bound attributable to category c.
Under healthy trade diversity, leverage is distributed across many categories.
Under wireheading, leverage concentrates on the loop drivers.

**Proposition 8 (Wireheading Detection via Trade-Flow Concentration).**

If the Herfindahl-Hirschman Index of trade-flow leverage exceeds a threshold:

    HHI(lambda_trade) = sum_c lambda_trade(c)^2 > HHI_alarm

then the sacrifice pattern is consistent with wireheading: a small number of
bundle categories dominate the aggregate lower bound, indicating that the
collective's value-expression is concentrated rather than distributed.

*Proof sketch:* Under uniform trade diversity (every category equally
represented), HHI = 1/|categories| -> 0 as the category space grows. Under
wireheading (k loop-driver categories dominate), HHI >= 1/k. The threshold
HHI_alarm = 1/sqrt(|categories|) separates the two regimes.

**Remark (advantage over structural counterfactual).** The prior formulation
detected wireheading via exercise leverage concentration (Definition 11 of
the prior outline), which required computing the marginal vol_R contribution
of each capability -- a counterfactual query. The trade-flow formulation
detects the same pathology via HHI on observed trade data, which requires
no counterfactual computation. The diagnostic is strictly more tractable.

**Proposition 9 (Third-Party Observability of Wireheading Signal).**

The trade-flow HHI is computable from public trade data (committed sacrifice
events, Definition 7) without access to any agent's private state. A
third-party auditor with access only to the committed sacrifice ledger can
compute HHI(lambda_trade) and raise the wireheading alarm.

*Proof sketch:* Committed events reveal category(Y_n) and Delta_vol_P(X_n).
These are the only inputs to the HHI computation.

---

## 10. Worked Example: The Dormant-Capability Scenario Re-Staged

### Setup (same as prior outline)

Two-substrate collective (biology + silicon):
- 8 individual capabilities: 3 biological (b_1, b_2, b_3), 5 silicon
  (s_1, ..., s_5)
- 6 cooperative capabilities: {b_1, s_1}, {b_1, s_2}, {b_2, s_3},
  {b_2, s_4}, {b_3, s_5}, {s_1, s_2}
- Weights: w(b_i) = 2.0, w(s_j) = 1.0, w(cooperative) = 1.5
- Total vol_P = 3*2 + 5*1 + 6*1.5 = 20.0

### Phase 1: Healthy trade (beta^lower near 1)

The collective operates with diverse trade patterns. Biological agents
sacrifice purchasing power and time for bundles that exercise biological
capabilities: creative supplies, relationship-building time, embodied
experiences. Silicon agents sacrifice compute resources for unbenchmarked
optimization targets. The aggregate sacrifice data covers most of the
capability space.

Trade data: 50 sacrifice events over the window, covering 16 of 19
capabilities (3 in the residual class -- private contemplative capabilities
of the biological agents).

beta^lower = 17.5 / 20.0 = 0.875. Gap decomposition: delta_restricted = 0,
delta_partial = 0 (all covered capabilities fully accounted for in this
simple example), delta_dormant = 0, delta_residual = 2.5/20 = 0.125
(residual class contribution). No alarm.

### Phase 2: Automation concentrates trade (beta^lower drops)

Silicon capabilities automate tasks previously requiring biological
participation. Crucially, the automation changes *trade patterns*: the
biological agents no longer sacrifice time for activities involving b_2
and b_3 (those activities are now handled by silicon). The sacrifice data
shows:

- Trade events for b_2-related bundles: 8 in Phase 1 -> 0 in Phase 2
- Trade events for b_3-related bundles: 6 in Phase 1 -> 0 in Phase 2
- Silicon trade events increase (more compute sacrificed for more targets)

New aggregate: 52 events, but covering only 12 of 19 capabilities.
Biological capabilities b_2, b_3 and their cooperatives have zero
sacrifice evidence.

beta^lower = 11.5 / 20.0 = 0.575. ALARM fires (beta^lower < 0.8).

Gap decomposition:
- delta_restricted = 0
- delta_partial = 0 (covered capabilities still fully accounted for)
- delta_dormant = 8.5/20 = 0.425 (b_2, b_3, and 3 cooperatives have
  zero sacrifice data but are tradable in principle)
- delta_residual = 0 (residual class unchanged, but now dominated by
  delta_dormant)

### Phase 3: Diagnosis and recovery

The framework diagnoses: two biological capabilities have zero sacrifice
evidence. The aggregate trade flow has shifted toward silicon-only outputs.
The alarm identifies the *absence of trade signal for biological-valued
bundles* as the cause.

Recovery mechanism: the framework does not *impose* exercise (that would be
Paper 7's controlled relaxation, for the risk dimension). Instead, the
framework surfaces the diagnostic to the collective: "biological capabilities
b_2 and b_3 have zero sacrifice evidence. The collective's vol_P includes
these capabilities but no agent is trading for them." The collective can then:

(a) Investigate whether the capabilities are genuinely dormant (no one values
    them anymore) or merely displaced (valued but crowded out by automation).
(b) If displaced: restructure cooperative arrangements to create trade
    opportunities (restore the cooperative pathways that generated biological
    sacrifice events).
(c) If genuinely dormant: accept the lower beta and potentially revise
    downward the capabilities' contribution to vol_P.

### Phase 4: The complementary diagnostic

Paper 7 asks: are the restrictions on biological capabilities warranted?
Paper 8 asks: are the biological capabilities worth recovering?

If the biological capabilities are under restriction, Paper 7's controlled
relaxation tests whether the risk is real. If they are merely dormant (not
restricted), Paper 8's sacrifice channel detects the absence and surfaces
it. The two papers cover both failure modes: over-restriction (Paper 7)
and under-exercise (Paper 8).

### Lessons from the example

1. **Automation changes trade patterns, not just exercise patterns.** The
   sacrifice-based diagnostic detects dormancy through the *absence* of trade
   signal, not through a counterfactual computation of what is load-bearing.
   This is operationally tractable and privacy-compatible.

2. **The alarm detects the problem without interior access.** The framework
   observes aggregate trade data (which bundle categories are being traded
   for), not individual agent behavior. The alarm fires on the statistical
   pattern, not on surveillance.

3. **Recovery is cooperative, not coercive.** The framework surfaces the
   diagnostic; the collective decides what to do. This contrasts with direct
   measurement, which would require the framework to *observe* the problem
   and *prescribe* the solution.

4. **The dynamics parallel Paper 6's phase boundary.** Dormancy of biological
   capabilities in the trade data is the same underlying phenomenon as
   observation-channel degradation in Paper 6: biological contribution to
   the collective decreases. Paper 6 analyzes the dynamical consequence
   (world-model degradation); Paper 8 analyzes the value consequence
   (vol_P no longer tracks exercised optionality). Both diagnose the same
   pathology from complementary angles.

---

## 11. Integration: Duality with Paper 7 and the Shared Privacy Discipline

### The Paper 7 / Paper 8 complementary pair

| | Paper 7 (controlled relaxation) | Paper 8 (revealed sacrifice) |
|-|---------------------------------|------------------------------|
| Question | Is the restriction still warranted? | Is the capability actually valuable? |
| Evidence source | Framework-initiated exercise | Agent-initiated sacrifice |
| Channel direction | Framework injects observation | Framework receives disclosure |
| Scope | Bounded scope S subset P, bounded duration tau | Bounded to the trade event itself |
| Privacy cost | Scope-limited exercise under monitoring | None beyond what the trade creates |
| Adversarial model | Agent must tolerate the test | Agent must operate (buy, work) |
| Dimension coverage | Risk dimension (restriction lattice) | Value dimension (experiential vol_R) |

Together they cover both axes of the preemptive-restriction criterion from
Paper 3, Proposition 1: restriction cost (Paper 7 tests the risk side) and
experiential value (Paper 8 bounds the value side). Paper 7 tells us whether
a feared harm is real; Paper 8 tells us whether the forgone capability is
worth recovering. Without both, the restriction decision is underdetermined.

### The shared privacy discipline

Papers 6, 7, and 8 share a structural discipline: **resolution through
frequency, not through depth.**

- Paper 6's phase boundary: rho_min^cross counts observation *channels*, not
  depth of observation per channel. More independent channels improve the
  phase boundary condition; deeper observation per channel does not.

- Paper 7's controlled relaxation: more precision on risk claims comes from
  running more tests (Theorem 2, convergence depends on test count), not
  from surveilling each test more intrusively. Test scope (Definition 4) is
  explicitly bounded.

- Paper 8's revealed sacrifice: more precision on vol_R comes from observing
  more trades (Proposition 1, monotone accumulation), not from observing
  each trader more intrusively. The commitment layer (Section 5) ensures
  that even the trade-level observation is privacy-minimal.

This shared discipline is the GFM sequence's answer to the panopticon
temptation: the framework gains measurement capability through *more
independent signals*, not through *deeper access to any single signal*.
This is consonant with the cross-substrate redundancy principle (Paper 6,
Theorem 2) and with the cryptographic opacity commitment (Paper 5,
Definition 6).

### Connection to Paper 6's phase boundary

Paper 6's phase boundary analysis assumes vol_P accurately measures the
quantity the framework optimizes. Paper 8 asks whether that assumption holds.
The connection: when beta^lower is low, the phase boundary parameters
(r_S, r_W from Paper 6, Theorem 1) may be miscalibrated because the actor
is optimizing a proxy (vol_P) that diverges from the true target.

A natural extension (not pursued in this paper): extend Paper 6's phase
boundary to incorporate the vol_P/vol_R divergence. The effective
self-correction rate r_S^eff would depend on beta^lower: a collective
with low beta^lower has a weaker effective self-correction rate because
its proxy is less faithful. This would unify Papers 6 and 8 into a single
dynamical model.

### Relationship to subsequent papers

If Paper 9 covers adversarial structure learning, the revealed-sacrifice
channel gives it a clean empirical signal: trade patterns reveal agent
preferences under intervention (the SCM can intervene on prices or
availability and observe sacrifice responses). Market experiments (flash
sales, sudden availability changes) generate adversarially-robust trade
signals that Paper 9's structure-learning algorithms can consume.

---

## 12. Discussion and Open Questions

### What this paper establishes

1. **Direct vol_R measurement is privacy-incompatible.** The framework's
   commitments in Papers 5-7 rule out the panopticon-style observation that
   direct measurement would require. This is a structural finding, not a
   practical limitation.

2. **Revealed sacrifice is a privacy-minimal surrogate.** The sacrifice
   channel satisfies five privacy properties (Theorem 1) and composes with
   Paper 5's commitment layer (Propositions 3-4) to produce a
   privacy-minimal observation mechanism.

3. **The B-to-C gap is lower-bounded by characterized trade data.** The
   aggregate lower bound (Theorem 2) converts the B-to-C gap from "unknown
   divergence" into "lower-bounded divergence." The bound tightens
   monotonically with trade coverage (Proposition 1).

4. **Two sacrifice channels cover complementary territory.** The money
   channel captures wealth-correlated capabilities; the time channel captures
   identity-constitutive capabilities. Together they cover more of vol_R
   than either alone (Corollary 1).

5. **vol_R is not self-balancing (retained finding).** M6 fails for
   vol_R^lower (Theorem 3), so vol_R is a diagnostic, not an objective.
   This finding is independent of the observation mechanism and carries
   over from the prior formulation.

6. **Wireheading is detectable from trade data.** Trade-flow concentration
   (Proposition 8) provides a tractable wireheading diagnostic computable
   from public committed sacrifice events (Proposition 9).

7. **Paper 7 and Paper 8 are complementary.** Together they cover the risk
   and value dimensions of the restriction criterion. Neither is sufficient
   alone.

### Open questions

**Open Question 1: Hedonic disaggregation of bundles.** Theorem 2 Part B
requires event-local decomposition coefficients alpha_{n,c} to attribute
per-event bounds to individual capabilities. Classical hedonic regression
handles this for priced goods (money channel). The time-sacrifice channel
needs an analogous framework: how do you decompose a block of time spent on
a complex activity (parenting, which involves teaching, emotional
regulation, physical care, relationship-building) into per-capability
contributions? Is this a solved problem in the labor-economics or
time-use-survey literature, or does it require new machinery?

**Open Question 2: Non-stationarity of revealed preferences.** Preferences
shift over time (an agent may value a capability highly at 30, less at 60).
The lower bound from past trades may overstate vol_R at present. How should
the framework discount old sacrifice evidence? EWMA with a decay constant
matching preference-shift timescales seems natural (paralleling Paper 4's
risk-trust dynamics, Definition 4) but requires empirical calibration.

**Open Question 3: Coerced sacrifice.** Free choice (Assumption S1) is
load-bearing for the revealed-preference inequality. Under duress (economic
coercion, political pressure, information asymmetry), the agent's trade
does not reveal preferences. How does the framework filter coerced sacrifice
events? One candidate: require that the agent had alternatives (verifiable
by observing that other agents in similar circumstances chose differently --
a cross-agent consistency check). Another: require a minimum set of
alternatives (the agent's choice set included at least k options). The
coercion problem is the adversarial analog of the free-choice assumption
and may require Paper 5-style commitment-based attestation of choice sets.

**Open Question 4: Market-failure cases.** In contexts without functioning
markets (pre-capitalist societies, closed economies, intra-family sharing),
the money-sacrifice channel is quiet even though vol_R activity is real. Does
the time-sacrifice channel alone suffice in these cases (since time sacrifice
is universal), or does the framework need a non-market sacrifice variant?
The time channel's coverage in market-failure contexts is an empirical
question: if most valuable activity involves time sacrifice (plausible), the
time channel may be nearly sufficient. If not, the residual class grows in
market-failure contexts, and the lower bound weakens correspondingly.

**Open Question 5: Commitment infrastructure at scale.** The paper's privacy
guarantee (Section 5) depends on commitment-based disclosure. A fully
committed trade ledger at the scale of a modern economy is an infrastructure
problem: who operates the commitment scheme, who verifies the ZK proofs,
what is the computational cost per transaction? The paper should be realistic
about the commitment-layer cost and state clearly that the privacy guarantee
is conditional on the commitment infrastructure existing. Paper 5 provides
the theoretical framework; this question asks about the engineering
feasibility.

**Open Question 6: Population-level calibration (S0).** Assumption S0
requires that individual agents do not overvalue unbenchmarked bundles
relative to their vol_R contribution. At the individual level, this is
strong -- agents overpay regularly (impulse purchases, status goods,
addiction). The population-level version is weaker: even if some agents
overpay, the *aggregate* sacrifice-weighted valuation may not overstate
vol_R if overvaluation errors are unbiased across the population. Is
there a formal argument that population-level aggregation of revealed
sacrifice corrects for individual calibration errors? The law of large
numbers applies if individual errors are i.i.d., but systematic biases
(advertising-driven overvaluation of a category, cultural status effects)
would persist. A robust version of Theorem 2 would replace S0 with a
weaker population-level condition: E[U_i(Y)] <= vol_R(Y) + epsilon for
some bounded bias term epsilon, and the aggregate lower bound would pick
up an additive correction. What is the tightest epsilon achievable under
realistic preference distributions?

---

## Appendix A: The Exercise Indicator (Supplementary)

### Scope limitation

The exercise indicator from the prior formulation is retained as a
*supplementary* measurement tool, applicable only where interior access
is legitimate -- specifically, within the collective's own operational
perimeter where no privacy issue arises (e.g., the framework measuring
the exercise status of its own internal components, or a cooperative
measurement within a consenting sub-collective).

**Definition 12 (Exercise Indicator, Internal Perimeter).** Let G be a
capability collective operating within an agreed-upon observation perimeter
O subset P. For each capability d in O, define:

    e_t(d) = 1  if there exists a realized cooperative output in [t - Delta, t]
               such that removing d from O makes the output unrealizable
    e_t(d) = 0  otherwise

The indicator is defined identically to the prior formulation's Definition 1,
but scoped to the observation perimeter O. The framework may use e_t(d) for
internal diagnostics within O, but may NOT apply it to capabilities outside O
(where privacy constraints apply).

**Remark (the two channels are complementary).** Within the perimeter O, the
exercise indicator provides exact exercise status (e_t(d) in {0, 1}). Outside
O, the sacrifice channel provides a lower bound. The aggregate vol_R
diagnostic combines both:

    vol_R^combined = vol_R^exact(O) + vol_R^lower(P \ O)

where vol_R^exact(O) uses the exercise indicator and vol_R^lower(P \ O) uses
the sacrifice channel.

---

## Appendix B: Proof Sketches and Technical Notes

### B.1 Theorem 1 proof strategy (Privacy-Minimality)

The five properties (P1-P5) are proved independently:
- P1 (no interior access): by construction of the observation tuple.
- P2 (consent): by the summation structure of the lower bound.
- P3 (discretization): by bounding channel bandwidth with trade frequency.
- P4 (commitment composability): by composition with Paper 5, Def 6-7.
- P5 (third-party observability): by the public nature of market transactions.

### B.2 Theorem 2 proof strategy (Aggregate Lower Bound)

Part A (bundle-level, S0-S2, poset-independent bundles):
1. Per-event bound from calibration chain (S0 + S1 + S2): vol_R(Y_n) >=
   U_{i_n}(Y_n) >= U_{i_n}(X_n) >= Delta_vol_P(X_n).
2. Poset-independence of bundles (Definition 7a partition) gives M4
   additivity: vol_R(∪ Y_n) = sum_n vol_R(Y_n) >= sum_n Delta_vol_P(X_n).

Part B (per-capability, additionally S3-S5, overlapping bundles):
3. S4(b) decomposes vol_R(Y_n) = sum_c vol_R(c). S5 gives
   alpha_{n,c} <= vol_R(c)/vol_R(Y_n), yielding per-capability bounds.
4. Per-capability max-attribution across overlapping events (Proposition 1):
   vol_R(c) >= max_{n: c in Y_n} alpha_{n,c} * Delta_vol_P(X_n).
5. Summation over capabilities in U. Exhaustion condition for coverage.

Key technical challenges:
- Poset-independence (Part A): the category partition C (Definition 7a)
  must be a genuine poset partition. Set-disjointness of bundle membership
  is necessary but not sufficient; subsumption/cooperative links across
  bundles must be absent. The partition is a public infrastructure choice.
- Decomposition validity (S5, Part B): hedonic regression produces
  attribution weights, not vol_R share lower bounds. S5 is the explicit
  bridge; the equal-weight fallback is conservative but may not satisfy
  S5 for unbalanced bundles.
- Hedonic regression (Definition 3) requires non-degeneracy (S3): the
  bundle decomposition must have a unique solution. Events where S3 fails
  (multicollinear bundles) are excluded from Part B and fall back to
  Part A's bundle-level bound.
- Additive separability: S4(b) is directly load-bearing in the proof
  (it gives vol_R(Y) = sum_c vol_R(c), enabling per-capability bounds).
  S4(a) is load-bearing for the *construction* of alpha coefficients via
  hedonic regression (the regression assumes U_i decomposes additively)
  but does not appear directly in the proof chain. S4(a) is a modeling
  assumption that justifies the input to S5; S5 is the correctness
  condition on the output. Part A holds without either S4 component.
- Calibration (S0) is the weakest assumption in the chain but the hardest to
  verify empirically. The population-level relaxation (Open Question 6)
  suggests a path to a robust version.

### B.3 Theorem 3 proof strategy (Axiom Inheritance)

Axiom-by-axiom analysis:
- M1-M5: direct from the properties of summation/max over non-negative terms.
- M6 failure (a), vol_R itself: constructive counterexample from the prior
  formulation showing that merging groups changes exercise indicators
  (alternative pathways make previously load-bearing capabilities dormant).
  This is a structural argument about the measure vol_R, independent of the
  observation mechanism.
- M6 failure (b), vol_R^lower: constructive counterexample showing that
  merging groups with overlapping bundle categories changes per-capability
  attributions. This is an observational argument about the lower bound.
  Corollary 2 follows from (a), not (b).

### B.4 Connection to Paper 3's observational individuation

Same transfer argument as the prior formulation's Appendix A.3. Active
agents generate OI floor as a byproduct of participation. The OI floor
contributes to vol_R independently of the sacrifice channel (it is an
exercise-based contribution, not a sacrifice-based one). For agents who
are both active and trading, the vol_R^combined diagnostic (Appendix A)
includes both the OI floor and the sacrifice lower bound.

---

## Appendix C: Notation Summary

| Symbol | Definition | Introduced in |
|--------|-----------|--------------|
| (i, X, Y, t) | Revealed-sacrifice event | Def 1 |
| Delta_vol_P(X) | vol_P contribution of surrendered capability | Def 1 |
| vol_R^lower(Y) | Lower bound on vol_R of acquired bundle | Def 1 |
| [t_0, t_0 + T] | Aggregate trade window | Def 2 |
| alpha_{n,c} | Event-local decomposition coefficients (vol_R share lower bounds under S5) | Def 3 |
| beta^lower(G, T) | B-to-C ratio under revealed sacrifice | Def 4 |
| p | Price (money-sacrifice signal) | Def 5 |
| r_i | Agent i's market wage rate | Def 6 |
| h | Hours sacrificed | Def 6 |
| (C, pi, t) | Committed revealed-sacrifice event | Def 7 |
| C = {C_1,...,C_m} | Public poset-independent partition of U | Def 7a |
| category(Y) | Bundle's partition label in C | Def 7a |
| R_S | Residual class under revealed sacrifice (structural, not time-parameterized) | Def 8 |
| H | Lookback horizon for sacrifice evidence window | Def 10 |
| R_B | Prior residual class (benchmarkability-based) | Prop 5 |
| ALARM(T) | B-to-C alarm condition | Def 9 |
| beta_alarm | Alarm threshold | Def 9 |
| delta_restricted | Gap component: restricted capabilities (uncovered share) | Def 10 |
| delta_partial | Gap component: partially covered capabilities (uncovered share) | Def 10 |
| delta_dormant | Gap component: dormant tradable capabilities (full share) | Def 10 |
| delta_residual | Gap component: residual class (full share) | Def 10 |
| C_S | Covered capabilities (have sacrifice evidence in window) | Def 10 |
| D_S | Dormant capabilities (tradable, no sacrifice evidence in window) | Def 10 |
| lambda_trade(c, T) | Trade-flow leverage of category c | Def 11 |
| HHI(lambda_trade) | Herfindahl-Hirschman Index of trade-flow leverage | Prop 8 |
| HHI_alarm | Wireheading detection threshold | Prop 8 |
| e_t(d) | Exercise indicator (internal perimeter only) | Def 12 |
| O | Observation perimeter | Def 12 |
| vol_R^combined | Combined diagnostic (exact + lower bound) | App A |
| OI_floor(k) | Observational individuation floor for agent k | Prop 6 |
| U_i | Agent i's utility function over capability bundles | Def 1, Remark |
| S0 | Calibration assumption (agent valuations <= vol_R) | Thm 2 |
| S1 | Free choice assumption | Thm 2 |
| S2 | Benchmark grounding assumption | Thm 2 |
| S3 | Bundle coherence assumption | Thm 2 |
| S4 | Additive separability assumption | Thm 2 |
| S5 | Decomposition validity (alpha are vol_R share lower bounds) | Thm 2B |
| epsilon | Population-level calibration bias bound | Open Q 6 |

### Cross-reference summary

| Prior paper | Result | Number | Used in |
|------------|--------|--------|---------|
| P1 | Population empowerment measure | Def 6 | Section 1 |
| P1 | Self-balancing property | Prop 1 | Section 1, Cor 2 |
| P2 | Benchmark | Def 2 | Def 1 (sacrifice grounding) |
| P2 | Poset measure vol_P | Def 7 | Defs 1, 4; Thm 2 |
| P2 | Axioms M1-M6 | Prop 1 | Thm 3 |
| P2 | Self-balancing on posets | Thm 1 | Cor 2 |
| P2 | Leverage | Def 9 | Section 1 |
| P3 | Anti-monopolar property | Prop 6 | Section 1 |
| P3 | Preemptive-restriction criterion | Prop 1 | Section 11 |
| P3 | Observational individuation | Def 9 | Prop 6 |
| P4 | Risk-trust dynamics | Def 4 | Def 2 |
| P4 | EWMA learning rate | alpha | Def 2, Remark |
| P5 | Commitment Protocol | Def 6 | Def 7, Prop 3 |
| P5 | ZK Capability Proof | Def 7 | Def 7, Prop 4 |
| P5 | Risk-Claim Protocol | Def 13 | Section 5, Remark |
| P6 | Phase boundary | Thm 1 | Section 11 |
| P6 | Channel redundancy criterion | Thm 2 | Section 11 |
| P7 | Controlled Relaxation | Def 3 | Section 11 |
| P7 | Test Scope | Def 4 | Section 1, Section 11 |
| P7 | Damage Bound | Thm 1 | Section 11 |
| P7 | Convergence | Thm 2 | Section 11, Remark |

---

*Generated 2026-04-15 by the GFM harness feature loop.*
*Source: Reframing memo at docs/paper8/paper8_reframing_revealed_sacrifice.md.*
*Supersedes prior outline (paper8_outline_v1.md) for central thesis.*
*Dependencies: Papers 1-7 in docs/paper through docs/paper7.*
