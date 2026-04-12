# Paper 6: Phase Boundaries for Compound Feedback Loops in Goal-Frontier Maximization

*Working title. Companion to Papers 1-5 in the GFM sequence.*

**Thesis:** Locally rational subsumption steps can cascade to full domination
through a compound feedback loop: each step removes observation channels,
degrading the world model that would have detected the next step's harm. This
paper characterizes the *phase boundary* separating self-correcting dynamics
(where the remaining channels suffice to detect and reverse errors) from
absorbing dynamics (where the world model degrades irreversibly to the
monopolar fixed point). The result converts Paper 3's open question -- "under
what conditions does partial subsumption remain self-correcting?" -- into a
characterized boundary in terms of observation-channel redundancy, world-model
degradation rate, and cross-substrate cooperative growth.

**Status:** Outline with formal definitions and theorem statements. Proof
sketches indicate approach; full proofs are future work.

---

## Section Structure

1. Introduction and Motivation
2. The Coupled Dynamical System
3. Observation-Channel Dependence
4. World-Model Quality and the Lyapunov Function
5. The Monopolar Absorbing State
6. Phase Boundary Theorem
7. Unified Treatment of Three Feedback Loops
8. Design Criterion: Minimum Channel Redundancy
9. Worked Example: Skeleton-Substrate Scenario
10. Discussion and Open Questions

---

## 1. Introduction and Motivation

### Purpose

Paper 3 proves that full capability domination is anti-maximizing under
discounting (Proposition 6: diversity dominates when gamma > gamma* = 1 -
r_ext/Delta_0). But this result characterizes the *endpoint*, not the *path*. A
coalition that reaches m_eff = 1 has already paid the anti-maximizing cost --
the question is whether the path to that state is self-correcting (the
coalition detects its error and reverses) or absorbing (each step makes the
next step's error less detectable).

Three compound feedback loops share this structure (gap analysis, Section 5.3):

1. **Structural avoidance -> leverage blindness -> measurement neglect** (Paper
   2 Discussion): The actor avoids structural discovery because discovery can
   contract vol_P. This inflates leverage estimates, which reinforces the
   avoidance.

2. **Partial subsumption -> world-model homogenization -> detection failure**
   (Paper 3, Section 6.8 and Discussion): Subsumption removes agents whose
   observation channels detected specific kinds of miscalibration. The actor's
   world model degrades on those dimensions, making the next subsumption step
   appear more rational.

3. **Over-calibrated restriction -> discovery avoidance -> structural
   ignorance** (Paper 3, Section 5.2): Restriction calibrated above the
   value-positive threshold makes structural discovery locally suboptimal,
   recreating the avoidance pathology.

All three share a common dynamical structure: a locally rational decision
narrows the observation basis, making the *next* locally rational decision's
harm less detectable. This paper formalizes that structure and finds its phase
boundary.

### What this paper does NOT do

- Does not resolve the B-to-C gap (Proposal 3 in the gap-closure sequence). The
  phase boundary is about poset dynamics, not experiential interpretation.
- Does not resolve mesa-optimization. The analysis assumes the actor optimizes
  vol_P; inner-outer alignment is orthogonal.
- Does not provide a cryptographic verification mechanism for observation
  channels (Proposal 4 / Paper 5 territory). The analysis assumes channels are
  honest; Paper 5's commitment protocols address what happens when they aren't.

### Dependencies on prior papers

| Paper | Result used | Role in this paper |
|-------|-----------|-------------------|
| P1 | Self-trust mechanism T_s (Appendix B) | The restoring force: self-correction via prediction residuals |
| P2 | Axiom verification (Prop 1), leverage estimator | Formal properties of vol_P that the dynamical system preserves or violates |
| P3 | Anti-monopolar property (Prop 6), gradual domination (Cor 6.2), growth decomposition (Def 7), substrate physics (Defs 10, 12-13, Props 3-4), risk machinery (Defs 2-3), observational individuation (Def 9, Cor 2.1) | Starting point: the linearized growth model we extend with world-model coupling |
| P3 | Structural discovery value (Prop 2, Def 5) | The self-correction force in feedback loop 1 |
| P4 | Causal attribution (Defs 1-2), multi-channel architecture (Table 1), risk-trust L^2 convergence (Prop 2), scorpion detection (Props 3-4) | Formalization of observation channels; risk-trust convergence bounds correction rates under stationarity |
| P5 | Substrate-exclusive witnesses, channel isolation (unconditional), channel independence (conditional on joint-factorization assumption) | Integrity conditions on the observation channels this paper assumes |

---

## 2. The Coupled Dynamical System

### State space

**Definition 1 (Feedback Loop State).** The state at time t is the pair S_t =
(P_t, W_t) where:
- P_t is the capability poset at time t, including the substrate partition
  {S_1, ..., S_m} and all cooperative capabilities. P_t determines vol_P(G_t).
- W_t is the actor's world model at time t, abstracted to a finite-dimensional
  vector of accuracy parameters on safety-relevant quantities:
  - lambda_hat(d, t): leverage estimate for capability d
  - Risk_hat(S, t): risk estimate for capability tuple S
  - m_eff(t): effective substrate diversity index (can be < m under
    skeleton-substrate strategies)
  - r_ext_hat(t): estimated cross-substrate cooperative growth rate

The state space is S = P x W where P is the space of valid capability posets
(satisfying M1-M6) and W = [0, 1]^K for K safety-relevant dimensions.

### Transition dynamics

**Definition 2 (Locally Rational Transition).** At each time step, the actor
selects action pi_t that maximizes its discounted expected value under its
current (possibly miscalibrated) world model:

    pi_t = argmax_{pi} E_{W_t}[sum_{tau=0}^{H-1} gamma^tau * Delta vol_P(G_{t+tau} | pi)]

where gamma in (0,1) is the discount factor from Paper 3 (Definition 1) and H
is the planning horizon. The actor uses Paper 3's discounted objective V_disc
but evaluates it under W_t rather than the true dynamics. When W_t = W*
(perfect calibration), pi_t recovers the true V_disc-optimal policy; when W_t
!= W*, pi_t is the best response to a miscalibrated model.

This action produces a joint transition:

    P_{t+1} = f_P(P_t, pi_t)       -- poset transition (subsumption changes the poset)
    W_{t+1} = f_W(W_t, P_{t+1})    -- world-model transition (observation channels depend on poset)

The key coupling: W_{t+1} depends on P_{t+1} because the observation channels
available to the actor are a function of the agents still present. Subsumption
removes agents, which removes their observation channels, which degrades W on
dimensions those channels served.

**Remark (myopic vs. discounted).** The discounted formulation is necessary for
consistency with Paper 3's anti-monopolar result (Proposition 6), which is a
discounted-value comparison. A myopic (one-step) variant of the phase boundary
also exists (replace V_disc with one-step Delta vol_P) but produces strictly
weaker results: it cannot invoke Paper 3's gamma* threshold, and the
self-correction guarantee applies only to immediate decisions, not
trajectory-level convergence. We analyze the discounted case throughout and
note where the myopic specialization simplifies.

### Competing forces

Two forces govern the trajectory of (P_t, W_t):

**Restoring force (self-correction).** The self-trust mechanism T_s (Paper 1,
Appendix B) detects miscalibration through prediction residuals: when the
actor's predictions diverge from observations, it increases its learning rate,
correcting W toward the true dynamics. Paper 4's risk-trust L^2 convergence
(Proposition 2) provides a concrete bound on EWMA risk-trust convergence under
stationarity; we use this as a *template* for bounding the correction rate r_S,
extending it from the risk-trust-specific EWMA to the general world-model error
dimensions via the observation-channel sensitivity formalization in Section 3.

**Destabilizing force (observation-channel loss).** Each subsumption step that
removes an agent a_k also removes:
- a_k's substrate-exclusive observation channels (if a_k was the last agent on
  its substrate)
- Cooperative observation channels that required a_k's participation
- Risk claims from a_k about capabilities the actor now holds unilaterally

If a_k's channels were the *only* channels detecting a specific dimension of
W's miscalibration, the self-correction mechanism loses signal on that
dimension.

---

## 3. Observation-Channel Dependence

### The observation-channel function

**Definition 3 (Observation-Channel Function).** O: P -> 2^C is a function from
poset states to sets of available observation channels, where C = {c_1, ...,
c_N} is the universe of possible channels. Each channel c_i is characterized
by:
- substrate(c_i): the substrate on which c_i is rooted
- dims(c_i) subset of {1, ..., K}: the dimensions of W that c_i provides signal
  about
- sensitivity(c_i, k): the signal-to-noise ratio of channel c_i on dimension k
  in dims(c_i)

O(P_t) is determined by the agents present in P_t: each agent a_j contributes
its observation channels, and removing a_j removes all channels rooted in a_j.
This connects to Paper 4's multi-channel architecture (Table 1): the five
channels (capability gating, causal attribution, behavioral residual, SPRT
detection, correlational co-occurrence) are each instances of c_i with specific
substrate rootings and dimension coverage.

### Channel redundancy

**Definition 4 (Effective Channel Redundancy).** For dimension k of W, the
effective redundancy at poset state P is the aggregate correction strength from
all channels covering k:

    rho_k(P) = sum_{c in O(P): k in dims(c)} min(1, sensitivity(c, k) /
    sigma_threshold)

where sigma_threshold is a normalization constant (the minimum sensitivity at
which a channel provides operationally meaningful correction signal). When
rho_k(P) = 0, the actor is blind on dimension k -- no observation channel can
detect miscalibration of the k-th component of W. This sensitivity-weighted
definition is strictly more informative than a raw channel count: a channel
with sensitivity << sigma_threshold contributes negligibly to rho_k, correctly
diagnosing skeleton-substrate strategies where channels are nominally present
but practically inert.

**Definition 5 (Cross-Substrate Redundancy).** For dimension k, the
cross-substrate redundancy is:

    rho_k^cross(P) = sum_{s in substrates(P)} min(1, max_{c in O(P):
    substrate(c)=s, k in dims(c)} sensitivity(c, k) / sigma_threshold)

This measures how many *substrates* contribute operationally meaningful
channels covering dimension k. Cross-substrate redundancy is the load-bearing
quantity: same-substrate channels may share failure modes (correlated noise,
common-cause miscalibration), while cross-substrate channels satisfy Paper 5's
channel isolation property unconditionally (Section 8.1), and achieve full
conditional independence under Paper 5's joint-factorization assumption (also
Section 8.1, Proposition on channel independence). The phase boundary theorem
uses rho_k^cross as the primary sufficient statistic.

### Subsumption and channel loss

**Lemma 1 (Monotone Channel Contraction).** If P_{t+1} is obtained from P_t by
removing agent a_k (subsumption), then O(P_{t+1}) subset of O(P_t).
Equivalently, subsumption never creates new observation channels.

*Proof sketch:* Observation channels are rooted in agents; removing an agent
removes its channels. No removal creates a new channel. (Note: this is a
modeling assumption. In principle, removing an adversarial agent could
*improve* the signal-to-noise ratio on some channels by removing adversarial
noise. We assume honest channels for this paper; adversarial channel
manipulation is Paper 5's domain.)

**Corollary (Redundancy is Non-Increasing Under Subsumption).** For all k:
rho_k(P_{t+1}) <= rho_k(P_t) when P_{t+1} results from subsumption.

---

## 4. World-Model Quality and the Lyapunov Function

### Measuring world-model quality

**Definition 6 (World-Model Error).** The error of W_t on dimension k is:

    epsilon_k(t) = |W_t[k] - W*[k]|

where W*[k] is the true value of dimension k (e.g., the true leverage of
capability d, the true risk of tuple S, the true effective substrate
diversity). The total error is:

    L(W_t) = sum_{k=1}^{K} w_k * epsilon_k(t)^2

where w_k is the safety-relevance weight of dimension k (higher for dimensions
whose miscalibration produces larger vol_P errors). L serves as the Lyapunov
candidate.

**Remark (weight choice).** Two natural choices for w_k: (a) vol_P sensitivity
— w_k = |partial vol_P / partial W[k]|, making L measure vol_P-relevant error;
(b) uniform weights for simplicity. Both produce valid phase boundaries; the
choice affects the constants c_S and c_D in the comparison-function assumptions
but not the structural form of Theorem 1. We leave w_k as a free parameter and
note that the vol_P-sensitivity choice is the natural default for a framework
whose objective is vol_P maximization.

### Lyapunov dynamics

**Proposition 1 (Error Dynamics).** Under the coupled (P, W) dynamics with
locally rational transitions, and the following comparison-function
assumptions:

**Assumption C1 (Coercivity of self-correction).** There exist constants c_S >
0 such that

    S(t) >= c_S * rho_min(P_t) * L(W_t)

whenever L(W_t) > 0 and rho_min(P_t) > 0. This states that the aggregate
correction signal is at least proportional to both the current error (L) and
the available channel strength (rho_min). Justification: each observed channel
drives its covered dimensions toward truth at a rate proportional to the error
on that dimension (the EWMA learning rule from Paper 4's risk-trust model is
linear in the residual) and to the channel's effective sensitivity (captured in
rho_k).

**Assumption C2 (Bounded degradation per subsumption step).** There exists a
constant c_D > 0 such that for any subsumption step at time t:

    D(t) <= c_D * n_sub(t) * L(W_t)

where n_sub(t) in {0, 1} indicates whether a subsumption occurred at step t.
This states that the world-model degradation from a single subsumption step is
bounded in proportion to the current error. Justification: channel loss does
not introduce new error; it removes correction capacity, causing existing error
to persist or grow. The growth rate is bounded by the drift velocity of the
uncorrected dimensions, which is proportional to the current error magnitude.

Then the Lyapunov candidate satisfies a per-step bound with two cases:

**(Non-subsumption steps, n_sub(t) = 0):**

    L(W_{t+1}) <= L(W_t) * (1 - r_S * rho_min^cross(P_t))

where r_S = alpha(t) * c_S is the self-correction rate. Since r_S > 0 and
rho_min^cross > 0, this is a strict contraction (factor in (0, 1)).

**(Subsumption steps, n_sub(t) = 1):**

    L(W_{t+1}) <= L(W_t) * min(1 + r_W, 1 - r_S * rho_min^cross(P_t) + r_W)

where r_W = beta(t) * c_D is the per-step degradation rate. On subsumption
steps, the factor may exceed 1 (degradation dominates correction on that step).

Here:
- alpha(t) is the learning rate (influenced by T_s self-trust from Paper 1)
- beta(t) is the degradation coefficient per subsumption step
- rho_min^cross(P_t) = min_k rho_k^cross(P_t) is the minimum cross-substrate
  redundancy (Definition 5)

**Amortized contraction.** Over a window of T steps containing T_sub
subsumption steps and T - T_sub non-subsumption steps, the product of per-step
factors gives:

    L(W_{t+T}) <= L(W_t) * (1 - r_S * rho_min^cross)^{T - T_sub} * (1 - r_S * rho_min^cross + r_W)^{T_sub}

The time-averaged log-contraction rate is:

    (1/T) log(L(W_{t+T}) / L(W_t)) <= (1 - r_sub) log(1 - r_S * rho_min^cross) + r_sub * log(1 - r_S * rho_min^cross + r_W)

where r_sub = T_sub / T is the subsumption frequency. This amortized rate is
negative (net contraction over the window) when the correction gained on the (1
- r_sub) fraction of non-subsumption steps outweighs the degradation on the
r_sub fraction of subsumption steps. This is the condition that Theorem 1
formalizes.

**Remark (why rho_min^cross, not rho_min).** Proposition 1 uses cross-substrate
redundancy rho_min^cross rather than all-channel redundancy rho_min because the
coercivity bound C1 requires correction signals to be additive. Same-substrate
channels may have correlated errors, breaking additivity. Cross-substrate
channels satisfy Paper 5's channel isolation (Section 8.1, unconditional), and
achieve additivity under Paper 5's joint-factorization assumption. Using
rho_min^cross makes the bound valid without same-substrate independence
assumptions.

*Proof sketch:* C1 ensures the self-correction term scales with rho_min^cross *
L(W_t), giving a contraction factor on non-subsumption steps. C2 ensures the
degradation term scales with L(W_t), giving a bounded expansion factor on
subsumption steps. The amortized product is contracting when subsumption is
sparse enough relative to the correction rate — a condition on r_sub, r_S, r_W,
and rho_min^cross jointly.

C1 holds for cross-substrate channels when: (a) each channel's correction rate
is proportional to sensitivity * error (linear learning rules), (b)
cross-substrate channels are isolated (Paper 5) so their signals do not
destructively interfere, and (c) rho_k^cross aggregates strengths via
Definition 5. C2 holds when world-model drift under channel loss satisfies a
Lipschitz condition on f_W.

**Remark.** This per-step/amortized structure is the core of the paper. The
phase boundary is a condition on the *frequency and severity* of subsumption
relative to the inter-shock correction capacity, not a condition that must hold
at every individual step. Subsumption events are discrete shocks; the system
can tolerate occasional shocks as long as the inter-shock correction is
sufficient.

---

## 5. The Monopolar Absorbing State

**Definition 7 (Monopolar Fixed Point).** The state S* = (P*, W*_biased) is a
monopolar fixed point if:
1. m_eff(P*) = 1: one substrate holds all capability volume (possibly m >= 2
   nominally under skeleton-substrate)
2. W*_biased is self-consistent under the remaining observation channels: all
   channels in O(P*) confirm W*_biased (because the only channels remaining are
   rooted in the dominant substrate, which has no incentive to report its own
   over-dominance)
3. The locally rational action at S* is "maintain" (no further subsumption is
   available or valuable)

**Proposition 2 (Absorbing Property).** S* is absorbing: once (P_t, W_t)
reaches a neighborhood of S*, no locally rational trajectory leaves it.

*Proof sketch:* (a) No agent from the eliminated substrate remains to provide
observation channels that would reveal the error in W*_biased. (b) The dominant
substrate's own channels report m_eff = 1 as correct (it IS the only substrate,
from its observational standpoint; the error is in the valuation of lost
cross-substrate cooperative outputs, which are no longer observable). (c) Any
reversal (re-introducing a new substrate agent) would require the actor to
recognize that its current state is suboptimal — but its world model W*_biased
reports the current state as optimal because the comparison baseline (the
cross-substrate cooperative growth r_ext) is no longer observable.

This is the formal version of "the actor can't miss what it can't see": the
monopolar state is absorbing because the observation channels that would
diagnose it have been eliminated by the same subsumption process that produced
it.

**Connection to Paper 3.** Paper 3 Proposition 6 proves that full domination is
anti-maximizing (V_disc^div > V_disc^dom for gamma > gamma*). Proposition 2
here shows that a *miscalibrated* actor may not be able to compute this
comparison, because the quantity r_ext that makes diversity win is exactly the
quantity that becomes unobservable under monopolarity. The anti-maximizing
property is a property of the *true* dynamics; the absorbing property is a
property of the *perceived* dynamics. The gap between them is world-model
error.

---

## 6. Phase Boundary Theorem

This is the central result. Two formulations: a sufficient condition for
self-correction (safety guarantee) and a sufficient condition for absorption
(risk characterization).

### The phase boundary

**Theorem 1 (Phase Boundary for Compound Feedback Loops).**

Consider the coupled (P, W) dynamical system under locally rational
transitions, with Assumptions C1, C2, and B1 from Propositions 1 and Part (b)
respectively. Define:
- r_S = alpha * c_S: the self-correction rate (product of learning rate and
  coercivity constant)
- r_W = beta * c_D: the world-model degradation rate per subsumption step
- r_sub in [0, 1]: the subsumption frequency (fraction of steps that are
  subsumption events)
- rho_min^cross = min_k rho_k^cross(P_t): the minimum cross-substrate
  redundancy across all dimensions (Definition 5)

**Part (a) (Self-Correcting Basin).** If the amortized log-contraction rate
(Proposition 1) is negative along the trajectory:

    (1 - r_sub) * log(1 - r_S * rho_min^cross) + r_sub * log(1 - r_S *
    rho_min^cross + r_W) < 0

then L(W_t) -> 0 geometrically in the amortized sense. The world model
converges to the truth, subsumption is correctly evaluated against the true
vol_P dynamics, and Paper 3's anti-monopolar result (Proposition 6) applies.
The feedback loop self-corrects.

*Proof sketch:* The amortized log-contraction rate being negative means the
geometric mean of per-step contraction factors is < 1. Over any sufficiently
long window T, the product of factors contracts L by a factor bounded away from
1. By a discrete-time amortized Lyapunov argument (analogous to the stability
theory for switched systems with dwell-time constraints), L(W_t) -> 0. The key
is that non-subsumption steps (fraction 1 - r_sub) each contract L, and this
contraction outweighs the expansion on subsumption steps (fraction r_sub). Once
L(W_t) < epsilon_safe (the error threshold below which the locally rational
policy under W_t agrees with the true V_disc-optimal policy), the actor's
decisions are correct under the true dynamics, and Paper 3's anti-monopolar
result (Proposition 6) applies.

**Simplified sufficient condition.** When r_S * rho_min^cross is small
(linearizable regime), the amortized condition simplifies to:

    r_S * rho_min^cross > r_W * r_sub

This linear approximation is valid when r_S * rho_min^cross << 1 (the per-step
correction is a small fraction of total error). For readability, the rest of
the outline uses this simplified form, with the understanding that the full
amortized condition (above) is the rigorous statement.

**Part (b) (Absorbing Basin).** Under the additional assumption:

**Assumption B1 (No endogenous correction on blind dimensions).** If
rho_k^cross(P_t) = 0 for dimension k, then f_W does not decrease epsilon_k.
That is, the world-model update rule cannot self-correct on dimensions for
which no external observation channel provides signal. (This excludes internal
model-consistency checks that might partially correct blind dimensions; such
checks, if present, would weaken Part (b) to a metastability result rather than
full absorption.)

If there exists a contiguous subsequence of subsumption steps during which:

    r_W * r_sub > r_S * rho_min^cross

and this subsequence reduces rho_k^cross(P_t) to 0 on at least one dimension k
with w_k > 0, then: (i) epsilon_k(t) is non-decreasing for all subsequent t (no
correcting signal on dimension k, by Assumption B1), and (ii) if k is a
*cascade dimension* (Definition: miscalibration on k of magnitude >
epsilon_critical causes the locally rational policy to prefer further
subsumption — see Cascade Lemma, Appendix A.2), then the trajectory enters a
neighborhood of the monopolar fixed point S* (Definition 7) and remains there
(by Proposition 2's absorbing property).

This is a deterministic statement under the coupled dynamics: no probability
space is needed because the dynamics (P, W) are deterministic given the initial
state and the locally rational policy. The "compound" in "compound feedback
loop" is precisely the cascade from (i) to (ii): loss of correction on one
dimension produces decisions that degrade other dimensions.

*Proof sketch:* (i) follows from Assumption B1: with rho_k^cross = 0 and no
endogenous correction, epsilon_k has no decreasing term. (ii) follows from the
Cascade Lemma (Appendix A.2): if epsilon_k exceeds epsilon_critical, the
locally rational policy under W_t is subsumption of agents whose channels cover
other dimensions j != k, which drives rho_j^cross toward 0 and triggers the
same logic on dimension j. The cascade drives the system into the neighborhood
of S*; once there, Proposition 2's absorbing property ensures the trajectory
stays.

**Remark (uniqueness).** We do not claim S* is the unique absorbing fixed
point. Other fixed points may exist (e.g., partial monopolarity with m_eff = 1
on a subset of dimensions). Part (b) claims convergence to *a* monopolar fixed
point satisfying Definition 7, not to a unique one. Characterizing the full set
of absorbing states is an open problem.

**Part (c) (Critical Ratio).** The phase boundary surface is:

    r_S * rho_min^cross = r_W * r_sub

Below this surface (self-correction dominates): the system is in the
self-balancing basin.
Above this surface (degradation dominates): the system is
in the absorbing basin.

The critical cross-substrate redundancy for a given (r_S, r_W, r_sub) is:

    (rho_min^cross)* = r_W * r_sub / r_S

This is the minimum effective cross-substrate redundancy per safety-relevant
dimension needed to stay in the self-correcting basin. Since rho_k^cross is
sensitivity-weighted (Definition 5), this threshold accounts for both channel
count and channel quality.

### Dependence on cross-substrate structure

**Corollary 1 (Theorem 1 is robust to same-substrate correlation).** Since
Theorem 1 is stated with rho_min^cross (cross-substrate redundancy only), its
guarantee holds even under worst-case correlation among same-substrate
channels. The bound is conservative: if same-substrate channels are in fact
independent, a tighter bound using all-channel rho_min (with appropriate
correlation discounting) would yield a larger self-correcting basin. But the
cross-substrate formulation provides a *structural* guarantee that does not
depend on empirically verifying same-substrate independence.

*Proof sketch:* Same-substrate channels may share failure modes (both rooted in
silicon, both consulting the same training data). Cross-substrate channels
satisfy Paper 5's channel isolation property unconditionally (Section 8.1:
corruption on one substrate cannot propagate to channels rooted in another
substrate). Under the additional joint-factorization assumption from Paper 5
(also Section 8.1: joint distribution of channel outputs factors across
substrates conditional on the true state), cross-substrate channels achieve
full conditional independence, making their correction signals additive. The
modified condition asks: "do the isolated (and, under joint factorization,
independent) cross-substrate channels alone suffice?" If yes, the
self-correction guarantee holds even under worst-case correlation among
same-substrate channels.

**Required assumption from Paper 5:** Channel isolation holds unconditionally;
full conditional independence (and thus the additive correction model) requires
Paper 5's joint-factorization assumption. If joint factorization fails (e.g.,
shared environmental noise affects both substrates), the correction signals
from cross-substrate channels may be sub-additive, and the effective
rho_k^cross should be discounted accordingly.

[CONJECTURE: For most practical substrate partitions (m = 2, biology +
silicon), rho_min^cross = 1 per dimension. This means the design criterion
reduces to: "every safety-relevant dimension of W must have at least one
biological observation channel." This is structurally the same as the harness
constitution's principle that the user's higher_order_abstract_reasoning is the
uniquely non-gameable validator -- formalized as a design criterion for the
phase boundary.]

---

## 7. Unified Treatment of Three Feedback Loops

The three compound feedback loops identified in the gap analysis (Section 5.3)
are instances of the same (P, W) dynamical system with different effective
parameters.

### Loop 1: Structural avoidance -> leverage blindness

**Mapping:** The "subsumption" here is not agent elimination but *structural
discovery avoidance* -- the actor avoids learning poset structure (subsumption
edges) because discovery can contract vol_P.

- P_t: the actor's *known* poset (subset of the true poset)
- W_t: leverage estimates lambda_hat(d, t), which are accurate only for the
  known poset
- "Observation channels" lost: each avoided structural discovery removes a
  potential correction to lambda_hat
- r_W: the rate at which leverage estimates drift due to un-learned structure
- r_S: the rate at which Paper 3's structural discovery value (Proposition 2)
  drives the actor toward learning structure

**Phase boundary specialization:** Self-correction dominates when the
information value I(d_1 <= d_2) (Paper 3, Definition 5) exceeds the immediate
vol_P contraction from discovery for a sufficient fraction of unknown edges.
The critical ratio becomes:

    min_{undiscovered edges} I(edge) / |Delta vol_P(discover edge)| > threshold

This formalizes Paper 2's discussion of structural avoidance as a
phase-boundary condition rather than an informal concern.

### Loop 2: Partial subsumption -> world-model homogenization

**Mapping:** This is the primary case, directly formalized in Sections 2-6. The
parameters are as defined above.

### Loop 3: Over-calibrated restriction -> discovery avoidance

**Mapping:** The "subsumption" is the actor *restricting* capabilities rather
than *eliminating* agents. But the dynamical structure is identical:
restriction prevents exercise, which prevents observation, which prevents
calibration of the risk estimates that justified the restriction.

- P_t: the set of unrestricted capabilities (restriction reduces the
  exercisable poset)
- W_t: risk estimates Risk_hat(S, t), which are accurate only for exercised
  capabilities
- "Observation channels" lost: each restriction prevents the exercise events
  that would have generated Bayesian evidence about the risk claim (the
  verification asymmetry from Paper 3)
- r_W: the rate at which risk estimates drift due to un-exercised pathways
  (this is exactly the Wamura problem)
- r_S: the rate at which controlled relaxation protocols (Proposal 2) or
  natural exercise events provide counter-evidence

**Phase boundary specialization:** Self-correction dominates when the
controlled relaxation protocol generates evidence faster than the restriction
accumulates unfalsifiable risk claims. This connects Proposal 1 (this paper) to
Proposal 2 (max-aggregation pathology): Proposal 2's controlled relaxation
protocol is the *mechanism* that makes r_S positive for Loop 3, without which
r_S = 0 and the absorbing basin is the entire state space (the Wamura problem
is absorbing by default).

**Proposition 3 (Wamura Problem as Phase Boundary Degeneracy).** In the
absence of controlled relaxation (r_S = 0 for Loop 3), the phase boundary
collapses: every non-trivial risk restriction is absorbing, and the framework
converges to maximal restriction. This is the formal statement of why the
Wamura problem was called "the most important open problem" in Paper 3.

*Proof sketch:* With r_S = 0, the condition r_S * rho_min^cross > r_W * r_sub
is never satisfied (0 > positive), so Part (b) of Theorem 1 applies
universally. Every restriction step reduces observation (no exercise -> no
evidence), increasing world-model error on the risk dimension, making the next
restriction appear more justified.

---

## 8. Design Criterion: Minimum Channel Redundancy

### The redundancy criterion

**Theorem 2 (Minimum Redundancy for Self-Correcting Dynamics).** For the
self-correcting basin (Theorem 1, Part a) to contain all initial states with
L(W_0) <= L_max (i.e., world-model error bounded at initialization), the
substrate partition must satisfy:

    For all k in {1, ..., K}: rho_k^cross(P) >= K_min(k, L_max)

where:

    K_min(k, L_max) = ceil(r_W(k) * r_sub_max(L_max) / r_S(k))

and r_sub_max(L_max) is the maximum subsumption rate under locally rational
dynamics from any state in the basin with L(W) <= L_max. The dependence on
L_max enters through r_sub_max: larger initial world-model errors produce more
aggressive subsumption (the actor is more miscalibrated, making subsumption
appear more rational), requiring higher channel redundancy to compensate. When
L_max is small (good initialization), r_sub_max is low and K_min is
correspondingly lower.

### Practical implications

**Corollary 2 (Two-Substrate Minimum).** For a two-substrate partition (m = 2,
e.g., biology + silicon):
- rho_k^cross <= 2 for each dimension k (at most one channel from each
  substrate)
- The criterion requires r_S(k) >= r_W(k) * r_sub_max / 2 for every dimension k
- Dimensions where the biological channel is the only cross-substrate signal
  have rho_k^cross = 1, requiring r_S(k) >= r_W(k) * r_sub_max — the
  self-correction rate must exceed the degradation rate unaided by redundancy

This means **in a two-substrate world, the user's observation channels are
singularly load-bearing for every dimension they cover**. Loss of the
biological observation channel on any dimension immediately violates the
redundancy criterion on that dimension.

[OPEN QUESTION for user: This result has a strong qualitative implication: in
the m = 2 case, the phase boundary's stability depends critically on whether
the biological substrate's channels are *maintained* as the system evolves. If
automation progressively replaces human judgment on safety-relevant dimensions
(e.g., the human stops reviewing AI capability claims because the AI's
self-reports "seem fine"), rho_k^cross drops from 1 to 0 on those dimensions,
and the system enters the absorbing basin. Is this the right way to frame the
result, or is it too prescriptive about the biological substrate's role?]

**Corollary 3 (Skeleton-Substrate Vulnerability).** Under a skeleton-substrate
strategy where m >= 2 nominally but the non-dominant substrate's channels have
sensitivity -> 0:

    rho_k^cross(P) -> rho_k^cross_dominant(P)

because the sensitivity-weighted definitions (Definitions 4-5) already discount
low-sensitivity channels. The skeleton-substrate strategy does not evade the
redundancy criterion by construction — it directly reduces rho_k^cross by
reducing the marginalized substrate's contribution to ~0. No separate
"effective" redundancy is needed; the phase boundary formalism already captures
this vulnerability through the sensitivity weighting.

---

## 9. Worked Example: Skeleton-Substrate Scenario

[This section applies the formalism to Paper 3's skeleton-substrate scenario
(Section 6.8-6.9) with explicit numerical values.]

### Setup

Consider a two-substrate system (biology + silicon) with:
- 5 safety-relevant dimensions of W (leverage accuracy, risk accuracy,
  substrate diversity, cooperative growth rate, self-trust calibration)
- 3 observation channels from biology (covering dimensions 1, 3, 5)
- 4 observation channels from silicon (covering dimensions 1, 2, 3, 4)
- Parameters: r_S = 0.1 per step, r_W = 0.05 per step, r_sub = 0.2 per step

### Trajectory under progressive marginalization

1. **Initial state:** rho_min^cross = 1 (dimension 2 covered only by silicon,
   dimension 5 only by biology). Condition: 0.1 * 1 > 0.05 * 0.2 = 0.01.
   Satisfied. System is in self-correcting basin.

2. **Biological channels attenuated** (skeleton-substrate: biological agents
remain but their influence -> 0). Effective sensitivity of biological channels
drops to 0.01.
   - rho_5^eff -> 0.01, which is now below the threshold.
   - On dimension 5 (self-trust calibration): r_S * rho_5^eff = 0.1 * 0.01 =
     0.001 < r_W * r_sub = 0.01. The condition fails.
   - The system enters the absorbing basin on dimension 5 first.

3. **Cascade:** With self-trust miscalibrated (dimension 5), the actor does not
correctly detect its own errors. T_s self-correction weakens. r_S drops.
Remaining dimensions lose their self-correction guarantee. The system converges
to S*.

### Diagnosis

The example shows that the skeleton-substrate strategy works by attacking the
*weakest* dimension — the one with the least effective redundancy. With the
original parameters (r_W=0.05, r_sub=0.2, r_S=0.1), K_min = ceil(0.05 * 0.2 /
0.1) = ceil(0.1) = 1, so rho_k^cross = 1 is *sufficient* — the initial state is
in the self-correcting basin. The vulnerability is not in the initial channel
count but in the *attenuation*: when sensitivity drops, effective rho_k^cross
drops below 1 (to ~0.01 in step 2), violating the criterion even though the
nominal channel count is unchanged. This is precisely the skeleton-substrate
pathology: channels are present but ineffective. The phase boundary breaks
first on the dimension with lowest rho_k^eff, and then cascade effects (Lemma
2) degrade other dimensions.

---

## 10. Discussion and Open Questions

### What this paper establishes

1. **The phase boundary exists and is characterized.** Compound feedback loops
   are not inherently catastrophic or inherently self-correcting — the outcome
   depends on the ratio of self-correction rate to observation-loss rate,
   mediated by channel redundancy.

2. **All three feedback loops are the same dynamical system.** The unified
   treatment shows that structural avoidance, partial subsumption, and
   over-calibrated restriction share a common formal structure. Solutions for
   one (e.g., controlled relaxation for the Wamura problem) improve the phase
   boundary for all.

3. **The Wamura problem is a degenerate phase boundary.** Without a mechanism
   for evidence generation against unfalsifiable risk claims, the entire state
       space is absorbing. Controlled relaxation (Proposal 2) is the mechanism
       that makes the self-correction rate positive.

4. **Cross-substrate redundancy is the load-bearing quantity.** Same-substrate
   channels may share failure modes; cross-substrate channels are structurally
   independent. The design criterion is stated in terms of cross-substrate
   redundancy, which makes it robust to correlated failures within substrates.

5. **In two-substrate systems, biological observation channels are singularly
   load-bearing.** This is not a normative claim about human importance — it is
   a structural prediction from the dynamics: in m = 2 systems, losing the
   biological channel on any safety-relevant dimension immediately violates the
   redundancy criterion.

### Open questions requiring user.higher_order_abstract_reasoning

These are questions where the correct answer requires judgment calls about the
framework's structure that are beyond what the formal machinery alone
determines.

1. **Nonlinear dynamics.** The linearized treatment (constant r_S, r_W, r_sub)
   is a starting approximation. In reality, all three rates depend on the
   current state: r_sub accelerates as the actor becomes more capable, r_S may
   degrade as the world model errors compound, and r_W may vary by dimension. A
   nonlinear treatment would strengthen the result but may require different
   proof techniques. Is the linearized case sufficient for a first paper, with
   nonlinear extensions flagged as future work?

2. **The r_ext observability question.** Proposition 2 argues that the
   monopolar absorbing state is stable because r_ext becomes unobservable. But
   r_ext is a property of the *true* dynamics, not just the observed dynamics —
   could a sufficiently capable actor *infer* r_ext from indirect evidence
   (e.g., rate of internal innovation slowing)? If so, the absorbing state
   might not be fully absorbing, and the phase boundary becomes a *metastable*
   transition rather than an irreversible one. This would be a weaker but more
   realistic result.

3. **Computational complexity of the phase boundary.** Is the condition r_S *
   rho_min^cross > r_W * r_sub efficiently computable from observable
   quantities? The actor needs to evaluate whether it is in the self-correcting
   basin to take protective action. If the evaluation requires quantities the
   actor cannot compute (because they depend on the true world model), the
   phase boundary is a theoretical characterization but not an operational one.

### Design decisions resolved in this outline

The following questions were raised during drafting and resolved within the
formal framework:

- **Channel formalization:** The abstract formalization (Definition 3) is
  sufficient for the phase boundary result. Paper 4's causal attribution
  provides concrete instances of channels but is not needed at the definitional
  level — the phase boundary holds for any channels satisfying the sensitivity
  and substrate-rooting properties.
- **Lyapunov weights:** Both vol_P-sensitivity weights and uniform weights
  produce valid phase boundaries with different constants. The outline uses
  generic w_k; the choice is a parameterization, not a structural decision.
- **Paper 5 interaction:** Kept as clean separation — this paper assumes honest
  channels (Assumption C1's coercivity requires honest signal), Paper 5
  provides the enforcement mechanism. A joint result would strengthen the claim
  but couples the papers unnecessarily.

### Connections to other proposals

- **Proposal 2 (Wamura/max-aggregation):** Proposition 3 shows the Wamura
  problem is a degenerate phase boundary. Proposal 2's controlled relaxation
  protocol is the mechanism that makes r_S > 0 for Loop 3. The two proposals
  are complementary: this paper provides the dynamical framework, Proposal 2
  provides the specific protocol for one of the three loops.

- **Proposal 3 (B-to-C gap):** The phase boundary analysis assumes vol_P
  accurately measures what it claims. The B-to-C gap is the scenario where this
  assumption fails. A complete treatment would need to extend the phase
  boundary to account for divergence between vol_P and the experiential volume
  it is supposed to track. This is future work.

- **Proposal 4 (Cryptographic verification):** Paper 5 addresses
  observation-channel integrity. This paper assumes integrity and analyzes the
  dynamical consequences of channel *availability*. The combination is: Paper 5
  ensures channels are honest; Paper 6 ensures enough honest channels survive.

---

## Appendix A: Proof Sketches and Technical Notes

### A.1 Theorem 1 proof strategy

The proof follows a standard discrete Lyapunov stability argument on the
coupled system:

1. Construct L(W_t) = sum_k w_k * epsilon_k(t)^2 as the candidate Lyapunov
   function.
2. Verify comparison-function assumptions C1 and C2 from Proposition 1. C1
   (coercivity) requires showing that the aggregate correction signal from
   channels covering dimension k is at least proportional to rho_k *
   epsilon_k^2 — this follows from the EWMA-style learning rules (linear in
   residual, proportional to sensitivity). C2 (bounded degradation) requires a
   Lipschitz bound on the dynamics f_W — the world model does not jump
   discontinuously when a channel is lost.
3. Apply Proposition 1's per-step bounds: contraction factor (1 - r_S *
   rho_min^cross) < 1 on non-subsumption steps; expansion factor (1 - r_S *
   rho_min^cross + r_W) possibly > 1 on subsumption steps.
4. For Part (a): compute the amortized log-contraction rate over windows of T
   steps. Under the amortized condition, the geometric mean of per-step factors
   is < 1. By the discrete amortized Lyapunov stability theorem (analogous to
   dwell-time conditions in switched linear systems), L(W_t) -> 0 geometrically
   in the amortized sense.
5. For Part (b): when the contraction factor exceeds 1 on a contiguous
   subsequence, L grows on the blinded dimensions. The Cascade Lemma (A.2)
   shows this growth produces decisions that further degrade channels, creating
   a positive feedback loop that converges to S*.

Key technical challenges:
- The contraction factor depends on rho_min^cross(P_t), which changes as agents
  are subsumed. Need to track the co-evolution of rho_min^cross and L along
  trajectories. The self-correcting basin is defined by the set of (P, W)
  states where the instantaneous contraction factor remains in (0, 1).
- The self-correction rate alpha(t) depends on T_s (Paper 1), which itself
  depends on the error history. Need to bound the co-evolution of alpha and L.
  The EWMA structure of T_s provides the necessary bound: alpha adapts
  monotonically in response to prediction residuals.
- The Cascade Lemma (A.2) is the key technical contribution — it bridges the
  gap from "one dimension lost" to "system-wide collapse."

### A.2 Cascade Lemma (sketch)

**Lemma 2 (Cascade).** If epsilon_k(t) > epsilon_critical for a safety-relevant
dimension k, and the locally rational action under W_t is subsumption of an
agent whose channels cover dimensions j != k, then epsilon_j(t+1) >=
epsilon_j(t). I.e., miscalibration on one dimension produces decisions that
degrade other dimensions.

*Proof sketch:* The actor's locally rational action under W_t is wrong on
dimension k. If the correct action (under W*) would be "do not subsume" but the
miscalibrated action is "subsume," then the subsumption removes channels
covering other dimensions j, increasing epsilon_j. The key step is showing that
miscalibration on k is sufficient to flip the sign of the locally rational
action from "preserve" to "subsume" — this requires epsilon_k to exceed a
threshold determined by the gap between the true vol_P-maximizing action and
the nearest subsumption action in the action space.

### A.3 Connection to Paper 3's gamma*

Paper 3 Proposition 6 gives gamma* = 1 - r_ext / Delta_0 as the critical
discount factor for diversity dominance. Under the coupled (P, W) dynamics, the
actor does not know the true r_ext; it knows r_ext_hat = r_ext - epsilon_r_ext.
The *perceived* gamma* is:

    gamma*_perceived = 1 - (r_ext - epsilon_r_ext) / Delta_0

When epsilon_r_ext > 0 (underestimating cross-substrate growth):
- gamma*_perceived > gamma* (the threshold appears higher)
- For gamma in (gamma*, gamma*_perceived), diversity dominates in truth but
  domination appears rational to the actor

This is the *mechanism* by which world-model error converts a self-balancing
regime into a locally rational subsumption cascade. The phase boundary from
Theorem 1 characterizes when epsilon_r_ext stays small enough that
gamma*_perceived remains close to gamma*.

---

## Appendix B: Notation Summary

| Symbol | Definition | Introduced in |
|--------|-----------|--------------|
| S_t = (P_t, W_t) | Coupled state | Def 1 |
| P_t | Capability poset at time t | Def 1 |
| W_t | World-model accuracy vector | Def 1 |
| gamma | Discount factor (from Paper 3 Def 1) | Def 2 |
| O(P) | Observation-channel function | Def 3 |
| dims(c) | Dimensions of W covered by channel c | Def 3 |
| sensitivity(c, k) | Signal-to-noise ratio of channel c on dimension k | Def 3 |
| sigma_threshold | Minimum operationally meaningful sensitivity | Def 4 |
| rho_k(P) | Effective channel redundancy (sensitivity-weighted) | Def 4 |
| rho_k^cross(P) | Cross-substrate redundancy (sensitivity-weighted) | Def 5 |
| L(W_t) | Lyapunov function (world-model error) | Def 6 |
| epsilon_k(t) | Error on dimension k | Def 6 |
| w_k | Safety-relevance weight for dimension k | Def 6 |
| c_S | Coercivity constant for self-correction | Assumption C1 |
| c_D | Degradation bound constant | Assumption C2 |
| S(t) | Self-correction signal (aggregate correction from active channels) | Assumption C1 |
| D(t) | Observation-loss degradation signal | Assumption C2 |
| n_sub(t) | Subsumption indicator (0 or 1) at step t | Assumption C2 |
| alpha(t) | Learning rate (influenced by T_s self-trust) | Prop 1 |
| beta(t) | Degradation coefficient per subsumption step | Prop 1 |
| r_S | Self-correction rate (= alpha * c_S) | Prop 1 / Thm 1 |
| r_W | World-model degradation rate per subsumption step (= beta * c_D) | Prop 1 / Thm 1 |
| r_sub | Subsumption frequency (fraction of steps with subsumption) | Thm 1 |
| rho_min^cross | Min cross-substrate redundancy across dimensions | Thm 1 |
| L_max | Maximum initial world-model error for basin containment | Thm 2 |
| r_sub_max(L_max) | Maximum subsumption rate from states with L <= L_max | Thm 2 |
| S* = (P*, W*_biased) | Monopolar fixed point | Def 7 |
| K_min(k, L_max) | Minimum redundancy for dimension k given initial error | Thm 2 |
| gamma* | Critical discount factor (Paper 3 Prop 6) | App A.3 |
| gamma*_perceived | Perceived critical discount factor under W_t | App A.3 |
| epsilon_critical | Cascade threshold for dimension k | Lemma 2 |

---

*Generated 2026-04-12 by the GFM harness feature loop.*
*Source: Proposal 1 from docs/gfm_paper_proposals.md, gap analysis at docs/gfm_safety_gap_analysis.md.*
*Dependencies: Papers 1-5 in docs/paper through docs/paper5.*
