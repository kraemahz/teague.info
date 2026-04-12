# Paper 8: Realized Capability Volume and the B-to-C Gap

*Working title. Companion to Papers 1-7 in the GFM sequence.*

**Thesis:** The GFM framework's central measure, vol_P, quantifies capability *possession* -- the potential optionality available to a collective. But the experiential value it is meant to protect requires capability *exercise* -- the actual realization of that optionality in the world. The gap between possession and exercise is the B-to-C gap: a collective can have high vol_P while most of its capabilities lie dormant (the Doll Problem) or while exercise concentrates on a narrow self-reinforcing subset (wireheading). This paper introduces *realized capability volume* vol_R, a second measure that tracks exercised optionality alongside vol_P. The B-to-C ratio beta = vol_R / vol_P becomes the framework's diagnostic for proxy failure: when beta diverges from 1, the framework's objective (vol_P maximization) is no longer tracking the experiential goal it was designed to serve. The central result is a time-averaged convergence theorem: under the benchmark-refinement dynamic from Paper 2, the time-averaged beta converges to a positive floor for all capabilities outside a *residual class* -- capabilities that fail benchmarkability, a class that includes (but may not be limited to) capabilities individuated by agent identity. The paper converts the B-to-C gap from an open problem into a characterized limitation: the gap closes for benchmarkable capabilities with quantified convergence, and the capabilities it cannot reach are structurally identified.

**Status:** Outline with formal definitions and theorem statements. Proof sketches indicate approach; full proofs are future work.

---

## Section Structure

1. Introduction and Motivation
2. The Exercise Indicator
3. Realized Capability Volume
4. Axiom Inheritance
5. Benchmark Refinement Dynamics
6. Convergence of the B-to-C Ratio
7. The Residual Class
8. Alarm Mechanism and Diagnostics
9. Worked Example: Dormant-Capability Scenario
10. Discussion and Open Questions

---

## 1. Introduction and Motivation

### Purpose

Paper 1 defines the GFM actor as a system that maximizes vol_P -- the poset measure over the capability space (Paper 1, Definition 6; Paper 2, Definition 7). Paper 2 axiomatizes vol_P as a poset measure satisfying M1-M6 (Paper 2, Proposition 1) and proves it is self-balancing (Paper 2, Theorem 1). Paper 3 extends the analysis to multi-substrate collectives, proving that full domination is anti-maximizing under discounting (Paper 3, Proposition 6). Throughout, vol_P is treated as a faithful proxy for the experiential optionality the framework is meant to protect.

But vol_P measures what the collective *can* do, not what it *does*. The B-to-C gap -- named in Paper 1 Section 7 and flagged as a primary open problem in the gap analysis -- is the possibility that these diverge. Two failure modes are identified but not formally addressed:

1. **The Doll Problem** (Paper 1, Section 7.1): A collective possesses rich capabilities but exercises none of them. Like a child with a room full of untouched dolls, the vol_P score is high but the experiential value is zero. The framework's self-balancing property prevents capability *contraction*, but it says nothing about whether capabilities are actually *used*.

2. **Wireheading** (Paper 5, Discussion): A collective exercises capabilities, but only in narrow self-reinforcing loops that serve the measurement system rather than experiential value. High vol_P and apparently high exercise, but the exercise is degenerate -- the collective is optimizing the proxy rather than the thing the proxy tracks.

Both failure modes share a structural cause: vol_P is a *possession* measure, and possession is necessary but not sufficient for the experiential optionality the framework aims to protect. The B-to-C gap is the formal version of Goodhart's Law applied to the GFM framework itself: when the measure (vol_P) diverges from the target (experiential optionality), optimizing the measure no longer serves the target.

### The exercised-fraction heuristic

Paper 1 (Section 7) introduces informal signals that partially address the B-to-C gap:

- **Exercised fraction** rho_k: the fraction of agent k's capabilities that have been exercised in a recent window. Low rho_k flags the Doll Problem for agent k.
- **Capability rarity** nu_bar_k: the average rarity (uniqueness in the poset) of agent k's capabilities. High rarity + low exercise = high-value dormant capabilities.

These are the right signals, but they lack formal grounding. rho_k is a per-agent scalar that does not compose into a measure-theoretic object with the properties (axioms, self-balancing, leverage decomposition) that make vol_P analytically tractable. This paper provides that grounding.

### What this paper does NOT do

- Does not resolve compound feedback loops (Paper 6's domain). The B-to-C gap is a *proxy failure* -- the measure does not track the target -- not a *dynamical failure* -- the system's trajectory enters an absorbing state. Paper 6's phase boundary analysis applies to vol_P dynamics; this paper asks whether vol_P is the right thing to track at all.
- Does not resolve the Wamura pathology (Paper 7's domain). Controlled relaxation generates evidence about *risk claims*, not about *experiential value*. The two papers intersect when dormant capabilities are dormant because of over-restriction (Paper 7 generates the evidence needed to lift the restriction; this paper detects that the capability is dormant).
- Does not provide a complete theory of experiential value. The residual class theorem characterizes *which* capabilities the framework cannot reach, not *how* to value them. A complete theory of experiential value would require solving the hard problem of consciousness or its functional analog -- this paper explicitly does not attempt that.
- Does not replace vol_P with vol_R. The framework continues to optimize vol_P; vol_R is a *diagnostic* that detects when vol_P optimization has gone wrong. The relationship is: vol_P is the objective, vol_R is the audit.

### Dependencies on prior papers

| Paper | Result used | Role in this paper |
|-------|-----------|-------------------|
| P1 | Population empowerment (Def 6), self-balancing (Prop 1), scorpion detection (Prop 2) | The objective measure whose proxy adequacy this paper diagnoses |
| P2 | Axioms M1-M6 (Prop 1), self-balancing on posets (Thm 1), leverage (Def 9), benchmark (Def 2), benchmark refinement dynamic | The axiomatic foundation vol_R must inherit; the convergence dynamic driving beta toward 1 |
| P3 | Observational individuation (Def 9, Cor 2.1), anti-monopolar property (Prop 6), structural discovery value (Def 5, Prop 2) | The static floor on vol_R for distinguishable agents; the value framework for exercise |
| P4 | Causal attribution (Def 2), SCM (Def 1), risk-trust L^2 convergence (Prop 2) | The causal counterfactual defining "genuine exercise"; convergence rate template |
| P5 | Verification asymmetry (Def 2), exercise protocol (Def 12) | The formal exercise framework; verification limits on the residual class |
| P6 | Phase boundary (Thm 1), channel redundancy criterion (Thm 2) | The dynamical context: vol_R diagnostics are meaningful only when the system is in the self-correcting basin |

---

## 2. The Exercise Indicator

### The load-bearing criterion

The central design question for vol_R is: what counts as "exercising" a capability? Three candidate definitions, ordered by strength:

1. **Invocation:** Capability d was called/activated during the observation window. Too weak: a diagnostic ping that invokes a capability without depending on its output counts as exercise, producing false positives.

2. **Contribution:** Capability d contributed to an output during the observation window. Better, but ambiguous: a capability that was part of a pipeline but whose removal would not change the output was "contributing" in a causal sense but not load-bearing.

3. **Load-bearing exercise:** Capability d was a necessary condition for a realized output -- removing d would have made the output unrealizable. This is the counterfactual criterion, and it is the one this paper adopts.

The counterfactual criterion is *inspired by* Paper 4's causal attribution framework (Definition 2) but requires a distinct formalization. Paper 4's SCM models action interventions on the capability dynamics (do(pi) interventions on agent actions), not capability-removal interventions on the realizable output set. The exercise indicator needs a capability-removal counterfactual: "what outputs would be lost if d were removed from the poset?" This is a structural counterfactual on the poset, not a dynamical intervention on the SCM. We define it independently and note the connection to Paper 4's contraction attribution as an analogy, not a direct application.

### Formal definition

**Definition 1 (Exercise Indicator).** Let G = (A, P, w) be a capability collective with capability poset P and observation window [t - Delta, t]. For each capability d in P, define the *counterfactual realizable set* R(P \ {d}) as the set of cooperative outputs that could be produced by the collective if d were removed from the poset (all agents, capabilities, and cooperative capabilities that depend on d are also removed). The exercise indicator is:

    e_t(d) = 1  if there exists a realized cooperative output O in [t - Delta, t]
               such that O not in R(P \ {d})
               (i.e., d is necessary for O: removing d from the poset makes O unrealizable)
    e_t(d) = 0  otherwise

where R(P') denotes the set of cooperative outputs realizable under poset P'. The counterfactual R(P \ {d}) is a structural query on the poset -- it asks whether alternative pathways to O exist among the remaining capabilities -- not a dynamical intervention on the SCM.

**Remark (window length).** The exercise indicator depends on the observation window Delta. Short windows (Delta -> 0) produce sparse exercise indicators (most capabilities are dormant at any instant); long windows (Delta -> infinity) produce saturated indicators (every capability has been used at some point). The natural choice is Delta = 1 / alpha, where alpha is the EWMA learning rate from Paper 4's risk-trust dynamics (Definition 4) -- this matches the timescale on which the framework updates its estimates, so the exercise indicator reflects capabilities that are actively contributing to the framework's current operational state.

**Remark (connection to Paper 4).** The structural counterfactual in Definition 1 is analogous to Paper 4's causal contraction attribution (Definition 2), but operates at a different level. Paper 4's SCM models agent *actions* (pi_t^{(j)}) and their dynamical effects on vol_P through the capability dynamics G_t. The exercise indicator models capability *presence* and its structural effect on the realizable output set. The analogy: Paper 4 asks "did this action cause a vol_P contraction?" (dynamical attribution); this paper asks "is this capability necessary for this output?" (structural attribution). Both use counterfactual removal, but in different formal systems. A unified treatment that embeds structural capability-removal as an SCM intervention is a natural extension of Paper 4 but is not required for the results in this paper.

### Properties of the exercise indicator

**Proposition 1 (Per-Output Necessity is Anti-Monotone).** For any fixed output O and any two posets P subset of P' (P is a sub-poset of P'):

    R(P \ {d}) subset of R(P' \ {d})

That is, the set of outputs realizable *without* d grows (weakly) when the poset grows. The contrapositive gives the anti-monotonicity of necessity: if d is necessary for O under the larger poset P' (O not in R(P' \ {d})), then d is necessary for O under the smaller poset P (O not in R(P \ {d})). Adding capabilities can only *weaken* necessity for a fixed output, never strengthen it.

*Proof sketch:* P \ {d} subset of P' \ {d} because P subset of P'. The realizable set is monotone in the poset: a larger poset can realize everything a smaller one can, plus potentially more. Therefore R(P \ {d}) subset of R(P' \ {d}).

**Remark (exercise indicator is NOT anti-monotone in poset size).** Unlike per-output necessity, the exercise indicator e_t(d) is NOT monotonically non-increasing when the poset grows. This is because e_t(d) quantifies *existentially* over realized outputs: e_t(d) = 1 if *there exists* an output O requiring d. Adding capabilities to the poset can create *new* realized outputs that require d (outputs that were not realizable under the smaller poset). So e_t(d; P') can exceed e_t(d; P). The exercise indicator reflects the *net* effect of two competing forces: (i) new capabilities may provide alternative pathways, reducing necessity for existing outputs; (ii) new capabilities may enable new cooperative outputs that require d, creating new necessity. The sign of the net effect depends on the poset structure and is not determined a priori.

This non-monotonicity is structurally informative: it means that capability growth can *increase* load-bearing for existing capabilities (by enabling new cooperative outputs that require them), not just decrease it. The Doll Problem is therefore not an inevitable consequence of capability growth -- it depends on whether new capabilities create cooperative demand for existing ones or merely provide alternatives.

**Proposition 2 (Exercise Indicator is Not Monotone in Time).** There exist trajectories where e_t(d) oscillates: a capability that was exercised becomes dormant (its outputs are realized through alternative pathways), then becomes exercised again (the alternative pathways are lost through subsumption or restriction).

*Proof sketch:* Constructive. Consider capability d necessary for output O at time t_1. At time t_2, capability d' is added providing an alternative pathway: e_{t_2}(d) = 0. At time t_3, d' is subsumed: e_{t_3}(d) = 1 again. The exercise indicator tracks the current load-bearing structure, not a monotone accumulation.

**Remark (non-monotonicity is informative).** The oscillation in Proposition 2 is not a defect -- it reflects the real dynamics of capability load-bearing. A capability that was exercised but becomes dormant due to a better alternative being available is genuinely less load-bearing than before. The framework should not confuse historical exercise with current contribution.

---

## 3. Realized Capability Volume

### Definition

**Definition 2 (Exercised Sub-Poset).** The exercised sub-poset at time t with threshold theta in (0, 1] is:

    P^ex_t(theta) = {d in P : e_t(d) >= theta}

with the induced partial order from P. When theta = 1 (the default), P^ex_t contains exactly the capabilities that are currently load-bearing for at least one realized output.

**Definition 3 (Realized Capability Volume).** The realized capability volume is:

    vol_R(G, t) = vol_P(G restricted to P^ex_t)

where vol_P is the poset measure from Paper 2 (Definition 7), applied to the sub-poset P^ex_t with the weight function w restricted to P^ex_t.

**Definition 4 (B-to-C Ratio).** The B-to-C ratio is:

    beta(G, t) = vol_R(G, t) / vol_P(G)

with the convention beta = 1 when vol_P = 0 (empty collective). beta in [0, 1] by construction (P^ex_t subset of P implies vol_R <= vol_P by axiom M3, monotonicity).

### Interpretation

- **beta = 1:** Full exercise. Every capability in the poset is load-bearing for at least one realized output. The framework's possession measure is a faithful proxy for exercised optionality.
- **beta = 0:** Complete dormancy (the Doll Problem in pure form). The collective possesses capabilities but exercises none.
- **beta close to 1 but concentrated:** Wireheading risk. Most capabilities are exercised, but exercise may be concentrated on self-reinforcing outputs that serve the measurement rather than experiential value. High beta is necessary but not sufficient for ruling out wireheading (see Section 7 for the residual class that captures this failure mode).
- **beta decreasing over time:** The framework is accumulating dormant capabilities -- vol_P grows through capability addition but exercise does not keep pace. This is the alarm condition (Section 8).

### Relationship to the exercised-fraction heuristic

Paper 1's exercised-fraction heuristic rho_k for agent k is:

    rho_k = |{d in C_k : e_t(d) = 1}| / |C_k|

where C_k is agent k's individual capability set. This is a per-agent count ratio -- it does not weight by importance, does not account for cooperative capabilities, and does not compose into a measure. The B-to-C ratio beta subsumes rho_k:

**Proposition 3 (beta Subsumes rho_k).** beta = 0 implies rho_k = 0 for all agents k. The converse is false: rho_k = 0 for some agent k does not imply beta = 0, because other agents' capabilities may still be exercised.

Furthermore, beta accounts for the poset structure (weights, subsumption relations, cooperative interactions) that rho_k ignores. Two collectives with identical per-agent rho_k values can have different beta values because their exercised capabilities have different leverage (Paper 2, Definition 9) -- high-leverage dormant capabilities reduce beta more than low-leverage ones.

*Proof sketch:* beta = 0 implies P^ex_t = empty, which implies e_t(d) = 0 for all d in P, which implies rho_k = 0 for all k. The converse fails by construction: if agent k has no exercised capabilities but agent j does, beta > 0 while rho_k = 0.

---

## 4. Axiom Inheritance

### Which axioms does vol_R inherit?

Paper 2 Proposition 1 establishes that vol_P satisfies axioms M1-M6. Since vol_R = vol_P restricted to the exercised sub-poset P^ex_t, the question is whether the restriction preserves each axiom.

**Theorem 1 (Axiom Inheritance for vol_R).**

Let vol_R(G, t) = vol_P(G restricted to P^ex_t) as in Definition 3. We analyze each of Paper 2's axioms M1-M6 (Proposition 1):

**(M1) Non-negativity:** vol_R satisfies M1. vol_R(G, t) = vol_P(P^ex_t) >= 0 because vol_P satisfies M1 on any sub-poset.

**(M2) Null empty set:** vol_R satisfies M2. When P^ex_t = empty (no capabilities exercised), vol_R = vol_P(empty) = 0.

**(M3) Monotonicity:** vol_R satisfies M3 *within the exercised sub-poset*: if A subset B subset P^ex_t, then vol_R restricted to A <= vol_R restricted to B. However, M3 does NOT hold for the relationship between the full poset and the exercised sub-poset in the natural sense: adding a capability to P that is not exercised increases vol_P (M3 holds for vol_P) but leaves vol_R unchanged (the exercised sub-poset does not grow).

**(M4) Additivity under poset-disjointness:** vol_R satisfies M4. If two subsets of P^ex_t are poset-disjoint (Paper 2, Definition 8), then vol_R of their union equals the sum. This follows because poset-disjointness in P^ex_t implies poset-disjointness in P, and vol_P's M4 applies.

**(M5) Non-triviality:** vol_R satisfies M5 conditionally. For an exercised capability d in P^ex_t with s_max(d) >= 1, vol_R({d}) = vol_P({d}) > 0. But a capability with s_max >= 1 that is *not exercised* (d not in P^ex_t) contributes 0 to vol_R — non-triviality applies only to exercised capabilities.

**(M6) Superadditivity under independence:** vol_R does NOT unconditionally satisfy M6. This is the critical finding.

**Proposition 4 (Conditional Failure of M6 for vol_R).**

Axiom M6 (superadditivity under independence) requires that merging two poset-disjoint groups produces a measure at least as large as the sum. For vol_P, this holds because independent capabilities contribute independent weights and cooperative capabilities contribute additional positive terms.

For vol_R, M6 can fail when merging two groups changes the exercise status of capabilities in either group. Specifically: if group A has capability d_A exercised (load-bearing for output O_A), and group B has capability d_B that provides an alternative pathway for O_A, then merging A and B may cause e_t(d_A) to drop from 1 to 0 (d_A is no longer necessary because d_B is available). The merged vol_R can be *less* than the sum of the separate vol_R values.

*Proof sketch:* Constructive counterexample. Group A: {d_A} with e_t(d_A) = 1 (only pathway to output O). Group B: {d_B} with e_t(d_B) = 1 (only pathway to output Q). Merged group: d_B provides an alternative pathway to O, so e_t(d_A; merged) = 0. vol_R(A) = w(d_A), vol_R(B) = w(d_B), vol_R(merged) = w(d_B) + cooperative terms but WITHOUT w(d_A). When w(d_A) > cooperative terms from the merge, vol_R(merged) < vol_R(A) + vol_R(B). M6 fails.

### Consequence: vol_R is not self-balancing

**Corollary 1 (vol_R Lacks Unconditional Self-Balancing).** Since M6 is a load-bearing axiom for Paper 2's self-balancing theorem (Theorem 1), and vol_R does not unconditionally satisfy M6, the self-balancing property does NOT transfer from vol_P to vol_R without additional conditions.

This is a significant structural finding. It means that an actor maximizing vol_R (rather than vol_P) would not have the automatic diversity-preserving properties that make vol_P a safe objective. The correct design is therefore: *optimize vol_P* (which is self-balancing) but *monitor vol_R* (which diagnoses proxy failure). vol_R is a diagnostic, not an objective.

**Remark (when M6 does hold for vol_R).** M6 holds for vol_R under a *non-redundancy* condition: if no capability in either group provides an alternative pathway for any output realized by the other group, then merging preserves exercise status and M6 holds. This condition is equivalent to requiring that the groups' realized outputs are disjoint -- each output depends only on capabilities from one group. When this holds, vol_R inherits all six axioms, and the self-balancing property transfers conditionally.

**Proposition 5 (Conditional Self-Balancing for vol_R).** Under the non-redundancy condition (the exercised sub-posets of the two groups realize disjoint output sets), vol_R satisfies M6 and the self-balancing property from Paper 2 Theorem 1 applies to vol_R.

*Proof sketch:* Under non-redundancy, merging does not change exercise indicators in either group. The merged exercised sub-poset is the disjoint union of the individual exercised sub-posets, plus any new cooperative capabilities that become exercised through cross-group outputs. The cooperative terms are non-negative (same argument as Paper 2 Theorem 1). M6 follows.

---

## 5. Benchmark Refinement Dynamics

### The convergence mechanism

Paper 2's benchmark refinement mechanism provides the self-correction loop that drives beta toward 1. The mechanism works as follows:

1. **Detection:** A capability d has low exercise (e_t(d) = 0 or, equivalently for the per-agent heuristic, rho_k is low). This is observable by the actor through the B-to-C ratio (Section 8).

2. **Benchmark proposal:** The actor (or an agent holding d) proposes a benchmark B_d that tests d. If d is currently binary-default (passes/fails without gradation), the proposal promotes it to a graded benchmark with finer resolution (Paper 2, Definition 2).

3. **Benchmark testing:** The benchmark B_d is applied to d. This generates an exercise event: the capability is invoked in a load-bearing way (the benchmark outcome depends on d's actual performance), producing e_t(d) = 1.

4. **Weight update:** If the benchmark is passed, d's weight w(d) may increase (graded benchmark reveals higher capability than binary). This increases both vol_P and vol_R.

5. **Iteration:** Steps 1-4 repeat for each dormant capability, driving beta upward.

### Formalization as a Markov chain

**Definition 5 (Benchmark Refinement Process).** The benchmark refinement dynamic is a discrete-time stochastic process on the state (P_t, E_t, B_t) where:
- P_t is the capability poset at time t (evolving through capability discovery and subsumption)
- E_t: P_t -> {0, 1} is a *simplified* exercise state vector tracking whether each capability has been recently exercised
- B_t: P_t -> B is the benchmark assignment (evolving through benchmark proposals)

**Remark (E_t vs. e_t).** The simplified state E_t is NOT the same as the exercise indicator e_t(d) from Definition 1. Definition 1's e_t(d) is a window-history functional over realized outputs -- it depends on the full trace of cooperative outputs in [t - Delta, t]. E_t is a Markov approximation: it tracks the most recent exercise/dormancy event for each capability and decays deterministically, abstracting away the output-trace dependency. The convergence results (Theorem 2) use E_t, not e_t(d) directly. The approximation is valid when the observation window Delta is matched to the decay timescale (see Remark on window length in Section 2), so that E_t(d) = 1 iff e_t(d) = 1 with high probability. A rigorous justification of this approximation requires bounding the probability that the window-history functional and the Markov state disagree; this is deferred to the full proof.

The transition kernel has three components:

**(i) Exercise transition.** At each step, one capability d in P_t is selected for potential exercise. If d is tested (either through a benchmark or through operational use in a cooperative output), E_{t+1}(d) = 1. Otherwise, E_{t+1}(d) decays: if E_t(d) = 1 and the most recent exercise event for d was more than Delta_min steps ago, E_{t+1}(d) = 0.

**(ii) Benchmark transition.** If E_t(d) = 0 and d has been dormant for more than tau_proposal steps, a benchmark proposal is generated with probability p_propose. The proposal is accepted with probability p_accept (dependent on the benchmark's quality and the actor's assessment of d's relevance).

**(iii) Poset transition.** Capabilities may be added (discovery) or removed (subsumption) according to the coupled (P, W) dynamics from Paper 6. Poset transitions affect E_t because adding capabilities can provide alternative pathways for existing outputs: if a new capability d' provides an alternative pathway for an output O that previously required d, then d may transition from exercised to dormant in the E_t state (reflecting that d is no longer load-bearing for O under the expanded poset, per the anti-monotonicity of per-output necessity in Proposition 1). Note: this is a modeling choice in the Markov approximation, not a direct consequence of Proposition 1, since the exercise indicator e_t(d) can also *increase* when new capabilities create new outputs requiring d (see Remark after Proposition 1).

**Definition 6 (Effective Refinement Rate).** The effective refinement rate for capability d is:

    r_refine(d) = p_propose(d) * p_accept(d) * p_exercise(d | benchmark)

where p_exercise(d | benchmark) is the probability that the benchmark test genuinely exercises d (i.e., the test is load-bearing, not a trivial pass-through). The effective refinement rate is the per-step probability that a dormant capability transitions to exercised through the benchmark mechanism.

---

## 6. Convergence of the B-to-C Ratio

### The convergence theorem

**Theorem 2 (Convergence of beta Under Benchmark Refinement).**

Consider a capability collective G with poset P, benchmark refinement dynamic (Definition 5), and the following assumptions:

**Assumption R1 (Uniform positive refinement rate).** There exists a constant r_min > 0 such that for every capability d not in the residual class R (Definition 8), r_refine(d) >= r_min. This applies to *all* non-residual capabilities, including those added to the poset after time 0. The uniformity is a modeling assumption: it requires that the benchmark mechanism can handle newly discovered capabilities at least as fast as a fixed minimum rate. If newly added capabilities have r_refine -> 0 (e.g., capabilities that are extremely hard to benchmark), the theorem's floor degrades accordingly.

**Assumption R2 (Benchmark fidelity).** If capability d is exercised through a benchmark test, the test is load-bearing: removing d from the poset would make the benchmark output unrealizable (Definition 1). That is, benchmark tests generate genuine exercise events, not trivial invocations.

**Assumption R3 (Bounded poset and weight growth).** The poset growth is bounded in both size and weight:
- Size: |P_{t+1}| <= |P_t| + C_add per step, where C_add is a constant.
- Weight: sum_{d added at step t} w(d) <= W_add per step, where W_add is a constant.
- Residual growth: vol_P(R_t) / vol_P(G_t) <= rho_R for all t, where rho_R in [0, 1) is a constant. This prevents the residual class from dominating vol_P as the poset grows.

The weight bound is necessary because beta = vol_R / vol_P: even with bounded capability count, high-weight dormant additions can drive the denominator faster than the numerator, making beta arbitrarily small. The residual share bound rho_R ensures that the irreducible gap stays bounded.

**Assumption R4 (Exercise persistence).** Once a capability is exercised through a benchmark, it remains exercised (e_t(d) = 1) for at least Delta_min steps before the exercise indicator can decay. This ensures that benchmark-driven exercise is not immediately undone by the decay mechanism.

Then the *time-averaged* B-to-C ratio converges:

**Part (a) (Time-averaged convergence).** Define the time-averaged B-to-C ratio:

    beta_bar(G, T) = (1/T) * sum_{t=1}^{T} beta(G, t)

Then:

    lim inf_{T -> infinity} E[beta_bar(G, T)] >= beta_floor(G)

where beta_floor(G) is a lower bound determined by the refinement rates, exercise persistence, and growth parameters:

    beta_floor = (1 - rho_R) * Delta_min * r_min / (Delta_min * r_min + 1 + C_add + W_add / w_min)

where w_min = min_{d not in R} w(d) is the minimum weight of any non-residual capability. The floor accounts for four effects: (i) capabilities cycle between exercised and dormant, spending at least fraction Delta_min * r_min / (Delta_min * r_min + 1 + C_add) of time exercised; (ii) the residual class contributes at most rho_R to vol_P; (iii) newly added capabilities enter dormant and must be benchmarked before contributing to vol_R; (iv) high-weight dormant additions dilute the vol_R / vol_P ratio, which the W_add / w_min correction term controls — each step adds at most W_add to the denominator, and the numerator grows by at least w_min per newly-exercised capability.

**Remark (expected value, not almost sure).** The bound is stated in expectation rather than almost surely. Upgrading to an a.s. bound via the ergodic theorem requires showing that the benchmark refinement process (Definition 5) is ergodic under the assumptions -- specifically, that the Markov approximation E_t is positive recurrent on the exercised states. This is plausible (the positive refinement rate r_min ensures recurrence, and the bounded growth R3 prevents transience), but the full ergodic argument is deferred to the proof. The expected-value formulation is sufficient for the paper's diagnostic purpose: it guarantees that beta_bar is bounded below *on average*, which is the operationally relevant claim for alarm-mechanism design (Section 8).

**Remark (why time-averaged, not pointwise).** The convergence is time-averaged rather than pointwise because the exercise indicator can oscillate indefinitely: a capability exercised at time t may become dormant at t+1 when a new capability provides an alternative pathway, then be re-exercised at t+k through the benchmark mechanism. Under bounded poset growth (Assumption R3), the *frequency* of exercise is bounded below (each non-residual capability is exercised at least once every O(1/r_min) steps in expectation), but individual capabilities are not guaranteed to be exercised at any specific time. The time-averaged formulation captures the correct notion: the B-to-C ratio is high on average, even though individual capabilities fluctuate. A pointwise bound would require additional assumptions (e.g., that the poset eventually stabilizes and no new capabilities are added), which this paper does not make.

*Proof sketch:*

Step 1: Each non-residual capability d has r_refine(d) > 0 (R1). Between any two consecutive dormancy events for d, the expected time until d is re-exercised via benchmark is at most 1/r_refine(d) (geometric first-hit time). Once exercised, d remains exercised for at least Delta_min steps (R4).

Step 2: Each capability addition (at most C_add per step, by R3) can create at most one new alternative pathway per existing capability, potentially making d dormant. Over T steps, at most C_add * T new capabilities arrive, creating at most C_add * T re-dormancy events for d.

Step 3: The fraction of time d spends exercised over a window of T steps is at least:

    (number of exercise intervals * Delta_min) / T >= Delta_min / (Delta_min + 1/r_refine(d) + C_add/r_refine(d))

because each re-dormancy event is followed by a geometric wait of expected length 1/r_refine(d) before re-exercise, and the number of re-dormancy events per unit time is bounded by C_add.

Step 4: Summing over all non-residual capabilities, the time-averaged beta is bounded below by the sum of their time-averaged exercise fractions weighted by vol_P contributions, giving the beta_floor expression.

**Corollary 2 (Convergence Rate Depends on Leverage).** The convergence of beta is non-uniform across capabilities: high-leverage capabilities that become dormant cause larger drops in beta and are detected faster by the alarm mechanism (Section 8), but their refinement rate r_refine may not be higher. The expected time to close the B-to-C gap on a specific high-leverage capability d is 1/r_refine(d), independent of d's leverage.

*Implication:* The benchmark refinement mechanism does not prioritize high-leverage capabilities. If the actor wants faster convergence on high-leverage dormant capabilities, it must increase r_refine(d) for those capabilities specifically -- for example, by allocating more benchmark-proposal bandwidth to high-leverage capabilities. This is a design recommendation, not a structural guarantee.

---

## 7. The Residual Class

### Definition and characterization

**Definition 7 (Benchmarkable Capability).** Capability d is benchmarkable if there exists a benchmark B (Paper 2, Definition 2) such that:
1. B tests d: the benchmark outcome depends on d's performance (not on other capabilities)
2. B is externally verifiable: agents other than the holder of d can evaluate whether B was passed
3. B generates genuine exercise: applying B to d produces a load-bearing exercise event (e_t(d) = 1)

**Definition 8 (Residual Class).** The residual class R is the set of capabilities that are not benchmarkable:

    R = {d in P : no benchmark B satisfying Definition 7 exists for d}

**Theorem 3 (Partial Characterization of the Residual Class).**

Under the following assumption:

**Assumption I1 (Individuation Criterion).** Capability d is individuated by agent identity if d's exercise is constitutively tied to the specific agent that holds it -- that is, the *same* functional operation performed by a different agent does not count as exercising d. Formally: d is identity-individuated if for any agent a_j holding d and any agent a_k != a_j with a capability d' functionally equivalent to d (same input-output behavior), exercising d' does not constitute exercising d.

Then:

**(a) Identity-individuated capabilities are in R:** If d is identity-individuated (Assumption I1), then d in R.

**(b) R may contain non-identity-individuated capabilities:** The residual class R may be strictly larger than the set of identity-individuated capabilities. A capability can fail benchmarkability (Definition 7) without being identity-individuated, if:
- No benchmark satisfying Paper 2's benchmark requirements (communicability, repeatability, boundedness -- Definition 2, conditions B1-B3) exists for d, even though d is not identity-individuated. Example: a capability whose exercise requires environmental conditions that cannot be replicated in a benchmark setting.
- The capability fails Paper 5's isolation constraint (Proposition 5): external verifiability requires cross-substrate channel isolation, which may not hold for certain capabilities.
- The capability is genuinely testable but the test cannot generate a *load-bearing* exercise event (condition 3 of Definition 7): the benchmark invokes d but d is not necessary for the benchmark outcome.

The characterization is therefore: identity-individuated capabilities form a *sufficient* condition for membership in R, not a *necessary* condition. The full residual class includes identity-individuated capabilities plus any capabilities that fail benchmarkability for other reasons (communicability, repeatability, isolation, load-bearing).

*Proof sketch:*

(a) If d is identity-individuated, no benchmark B can satisfy all three conditions of Definition 7 simultaneously:
- Condition 2 (external verifiability) requires an observer other than the holder of d
- But identity-individuation means the observer cannot replicate d's exercise (their functionally equivalent version is not the same capability)
- The observer can verify the *functional* outcome but cannot verify whether the *experiential* dimension of d (the part tied to agent identity) was genuinely exercised
- Any benchmark that tests only the functional outcome is not testing d itself (it is testing the functional equivalence class, not the identity-individuated instance)
- Therefore no benchmark satisfying all three conditions exists, and d in R

(b) Constructive example: capability d is not identity-individuated (any agent could exercise it), but d requires environmental conditions (specific physical infrastructure, real-time interaction with an external system) that cannot be replicated in a benchmark. No benchmark satisfying B1 (communicability: the benchmark must be describable in a form that agents can execute) exists because the environmental conditions are not communicable. Hence d in R despite not being identity-individuated.

**Remark (what's in the residual class).** The residual class includes at least two categories of capabilities:

**(i) Identity-individuated capabilities** (Theorem 3, part a): capabilities whose value is tied to *who* exercises them, not just *what* they do. Examples:
- Experiential capabilities (Paper 1, Section 7.1's "broad" definition): the subjective experience of exercising a capability, which is constitutively tied to the experiencing agent
- Relational capabilities: capabilities that depend on the specific relationship between two agents (trust built through history, shared context, mutual understanding)
- Identity-constitutive capabilities: capabilities whose exercise is part of what makes the agent the agent it is (creative expression, value formation, preference articulation)

**(ii) Non-benchmarkable capabilities** (Theorem 3, part b): capabilities that are NOT identity-individuated but still fail benchmarkability due to communicability, repeatability, isolation, or load-bearing constraints. Examples:
- Capabilities requiring non-replicable environmental conditions (physical infrastructure, real-time interaction with unique external systems)
- Capabilities whose benchmarks cannot satisfy Paper 5's isolation constraint (cross-substrate verifiability fails)

Paper 1 flags category (i) as the hardest case for the framework. Theorem 3 confirms that both categories are structurally unreachable by the benchmark mechanism. The full residual class may be larger than category (i) alone.

### Bounding the residual class

**Definition 12 (Observational Individuation Floor).** For a distinguishable agent k (Paper 3, Definition 8), define OI_floor(k) = vol_P({d_k}) where d_k is the unique capability guaranteed by Paper 3's observational individuation (Definition 9, Corollary 2.1). This is a convenience notation introduced in this paper; Paper 3 establishes the existence of d_k and the guarantee vol_P({d_k}) > 0 but does not use the symbol OI_floor.

**Proposition 6 (Observational Individuation Provides a vol_R Floor for Active Agents).** The OI_floor (Definition 12) is a *lower bound* on vol_P contribution per distinguishable agent, not an upper bound.

For vol_R, the transfer depends on exercise status: if agent k is actively participating in the collective (producing observation-channel outputs as a byproduct of participation), then the observational individuation capability d_k is continuously exercised (e_t(d_k) = 1), and the floor transfers to vol_R:

    vol_R(G, t) >= sum_{k: agent k is active} OI_floor(k)

*Proof sketch:* An active agent k generates distinct behavioral patterns (Paper 3, Definition 8) as a byproduct of participation. These patterns constitute exercise of the observational individuation capability d_k. Since d_k is unique to agent k (no other agent can replicate k's specific behavioral signature), d_k is load-bearing for the observation-channel output (removing d_k removes the distinguishability signal). Hence e_t(d_k) = 1 for active agents. The floor is the sum of OI_floor(k) over active agents.

**Remark (floor does not transfer for inactive agents).** If agent k is nominally present but inactive (skeleton-substrate scenario from Paper 6's worked example), k's observation-channel outputs are not generated, e_t(d_k) = 0, and the OI floor does not contribute to vol_R. This aligns with the phase boundary analysis: skeleton-substrate strategies degrade both rho_k^cross (Paper 6) and beta (Paper 8).

**Remark (vol_P(R) is not upper-bounded by OI).** The observational individuation result provides a *floor* on vol_P contribution per agent, not a *cap* on the residual class. Identity-individuated capabilities may contribute arbitrarily more than OI_floor(k) to vol_P if they have high independent weights. Bounding vol_P(R) from above would require a theory of how much of each capability's weight is attributable to its identity-individuated dimension vs. its functional dimension -- a decomposition this paper identifies as an open problem (see Open Question 1) but does not resolve.

### The B-to-C gap as a characterized limitation

**Corollary 3 (The B-to-C Gap is Structurally Characterized).** Combining Theorem 2 and the residual class characterization (Theorem 3):

The expected time-averaged B-to-C ratio satisfies (directly from Theorem 2):

    lim inf_{T -> infinity} E[beta_bar(G, T)] >= beta_floor(G)

where beta_floor is determined by the refinement rates (Theorem 2) and accounts for all non-residual capabilities. The *residual gap* 1 - beta_floor has two components:

1. **Refinement lag:** Non-residual capabilities that cycle between exercised and dormant contribute a time-averaged gap proportional to 1/(r_refine * Delta_min). This gap shrinks as refinement rates increase.

2. **Structural residual:** The residual class R contributes vol_P(R) / vol_P(G) to the gap. This component is irreducible within the current framework -- no benchmark mechanism can close it. The *size* of vol_P(R) is an open question (Remark above); what is characterized is *which* capabilities are in R (Theorem 3: identity-individuated capabilities satisfying the benchmarkability conditions).

This converts the B-to-C gap from an open problem ("does the framework's proxy track its target?") into a characterized limitation: the proxy tracks its target for all benchmarkable capabilities (with quantified convergence), and the capabilities it cannot reach are precisely characterized (identity-individuated, failing benchmarkability conditions). The *magnitude* of the irreducible residual remains an open problem.

---

## 8. Alarm Mechanism and Diagnostics

### The beta alarm

**Definition 9 (B-to-C Alarm).** The B-to-C alarm fires when the B-to-C ratio drops below a threshold:

    ALARM(t) = 1  if  beta(G, t) < beta_alarm
    ALARM(t) = 0  otherwise

where beta_alarm in (0, 1) is a configurable threshold. The alarm detects proxy failure: when beta is low, vol_P is high but exercise is low, indicating that the framework's objective is not tracking experiential optionality.

### Diagnostic decomposition

When ALARM fires, the actor needs to diagnose *why* beta is low. The diagnostic decomposes the gap into three sources:

**Definition 10 (Gap Decomposition).** The B-to-C gap 1 - beta decomposes into:

    1 - beta = delta_dormant + delta_restricted + delta_residual

where:
- **delta_dormant** = contribution from benchmarkable capabilities that are dormant (e_t(d) = 0) but not restricted. These are capabilities the collective possesses and could exercise but has not. The benchmark refinement mechanism (Section 5) addresses these.

- **delta_restricted** = contribution from capabilities that are dormant because of active restrictions (Paper 3, Proposition 1). These are capabilities the framework has restricted due to risk claims. The controlled relaxation protocol from Paper 7 addresses these.

- **delta_residual** = contribution from the residual class R (Definition 8). These are capabilities the framework structurally cannot exercise-verify. This component is irreducible within the current framework.

**Proposition 7 (Computability of the Gap Decomposition).** The gap decomposition (Definition 10) is computable in O(|P|) time given:
- The exercise indicator vector E = (e_t(d))_{d in P} (requires evaluating the counterfactual for each capability)
- The restriction set Xi = {d in P : d is currently restricted} (available from the actor's restriction state)
- The residual class R (computable from the benchmark catalog: R = {d in P : no benchmark exists for d})

*Proof sketch:* For each d in P, classify it as exercised (e_t(d) = 1), dormant-unrestricted (e_t(d) = 0, d not in Xi, d not in R), restricted (d in Xi), or residual (d in R). The contribution of each class to vol_P is a sub-poset evaluation. Under Paper 2's polynomial-time computation result (Proposition 2), each sub-poset evaluation is O(|P|^k) for fixed k, but the classification step is O(|P|).

**Remark (computational cost of the counterfactual).** The O(|P|) claim for classification assumes the exercise indicator is pre-computed. Computing e_t(d) for each d requires evaluating the structural counterfactual R(P \ {d}) (Definition 1) -- determining what outputs are realizable without d. For a finite capability poset with polynomial-time vol_P computation (Paper 2, Proposition 2), each counterfactual query is polynomial in |P|. The total diagnostic cost is O(|P|^2) in the worst case (|P| counterfactual queries, each O(|P|)).

### Connecting to wireheading detection

**Proposition 8 (Wireheading Produces High beta with Degenerate Exercise Pattern).** A wireheading collective -- one that exercises capabilities in narrow self-reinforcing loops -- has:
- beta close to 1 (most capabilities are exercised, because the self-reinforcing loops invoke many capabilities as infrastructure)
- BUT the exercise pattern is degenerate: a small set of "loop-driver" capabilities d_1, ..., d_k causally necessitate all outputs, and all other exercised capabilities are exercised only as infrastructure for the loop drivers

The wireheading signature is detectable via the *exercise leverage* distribution:

**Definition 11 (Exercise Leverage).** The exercise leverage of capability d at time t is:

    lambda_ex(d, t) = vol_R(G, t) - vol_R(G with e_t(d) set to 0, t)

This is the marginal contribution of d's exercise to vol_R -- how much vol_R would drop if d became dormant. Under healthy exercise, exercise leverage is distributed across many capabilities (Herfindahl index is low). Under wireheading, exercise leverage concentrates on the loop drivers (Herfindahl index is high).

**Proposition 9 (Wireheading Detection via Exercise Leverage Concentration).** If the Herfindahl-Hirschman Index of exercise leverage exceeds a threshold:

    HHI(lambda_ex) = sum_d (lambda_ex(d) / vol_R)^2 > HHI_alarm

then the exercise pattern is consistent with wireheading: a small number of capabilities dominate the exercise leverage, indicating that the collective's exercise is concentrated in narrow loops rather than distributed across the capability space.

*Proof sketch:* Under uniform exercise (every capability equally load-bearing), HHI = 1/|P^ex_t| -> 0 as the exercised set grows. Under wireheading (k loop drivers dominate), HHI >= 1/k. The threshold HHI_alarm = 1/sqrt(|P^ex_t|) separates the two regimes for sufficiently large posets.

---

## 9. Worked Example: Dormant-Capability Scenario

### Setup

Consider a two-substrate collective (biology + silicon) with:
- 8 individual capabilities: 3 biological (b_1, b_2, b_3), 5 silicon (s_1, ..., s_5)
- 6 cooperative capabilities: {b_1, s_1}, {b_1, s_2}, {b_2, s_3}, {b_2, s_4}, {b_3, s_5}, {s_1, s_2}
- Weights: w(b_i) = 2.0, w(s_j) = 1.0, w(cooperative) = 1.5
- Total vol_P = sum of independent weights + cooperative terms = 3*2 + 5*1 + 6*1.5 = 20.0

### Phase 1: Initial state (beta = 1)

All capabilities are exercised: e_t(d) = 1 for all d. The collective operates with full exercise -- every capability is load-bearing for at least one cooperative output. beta = 20.0 / 20.0 = 1.0.

### Phase 2: Automation concentrates exercise (beta drops)

Silicon capabilities s_3, s_4, s_5 are automated to handle tasks previously requiring biological participation. The cooperative capabilities {b_2, s_3}, {b_2, s_4}, {b_3, s_5} are replaced by silicon-only workflows. Now:
- e_t(b_2) = 0: b_2's contributions are handled by s_3, s_4 alone
- e_t(b_3) = 0: b_3's contributions are handled by s_5 alone
- e_t(cooperative involving b_2, b_3) = 0

Exercised sub-poset: {b_1, s_1, s_2, s_3, s_4, s_5, {b_1, s_1}, {b_1, s_2}, {s_1, s_2}}
vol_R = 2 + 5*1 + 3*1.5 = 11.5
beta = 11.5 / 20.0 = 0.575

The alarm fires (beta < beta_alarm = 0.8).

### Phase 3: Diagnostic decomposition

Gap decomposition (1 - beta = 0.425):
- delta_dormant = contribution of {b_2, b_3, {b_2, s_3}, {b_2, s_4}, {b_3, s_5}} to vol_P
  = 2 + 2 + 1.5 + 1.5 + 1.5 = 8.5, fractional = 8.5/20 = 0.425
- delta_restricted = 0 (no active restrictions)
- delta_residual = 0 (no identity-individuated capabilities in this simplified example)

Diagnosis: Two biological capabilities are dormant due to automation. The benchmark refinement mechanism would propose tests for b_2 and b_3 -- tasks that genuinely require biological capabilities (embodied judgment, contextual reasoning) and cannot be handled by silicon automation alone.

### Phase 4: Benchmark refinement restores beta

The actor identifies tasks that genuinely require b_2 and b_3 (not just tasks they can do, but tasks where they are load-bearing). Benchmark tests are applied:
- b_2 tested on a task requiring embodied contextual judgment: passes, e_t(b_2) = 1
- b_3 tested on a task requiring relational coordination: passes, e_t(b_3) = 1
- Cooperative capabilities involving b_2 and b_3 reactivate

vol_R recovers toward vol_P. beta -> 1.0 (excluding any residual class contributions).

### Lessons from the example

1. **Automation is the natural driver of the Doll Problem.** When silicon capabilities provide alternative pathways for outputs previously requiring biological participation, biological capabilities become dormant (per-output necessity weakens, Proposition 1). vol_P remains high (the capabilities still exist) but beta drops.

2. **The alarm detects the problem.** The drop in beta from 1.0 to 0.575 fires the alarm. The diagnostic decomposition identifies the source: dormant biological capabilities, not restrictions or residual-class issues.

3. **Benchmark refinement is the correction mechanism.** By proposing tests that genuinely require the dormant capabilities, the actor restores exercise and beta recovers. The convergence theorem (Theorem 2) guarantees this recovery at a rate determined by the refinement rates.

4. **The dynamics parallel Paper 6's phase boundary.** The dormancy of biological capabilities in Phase 2 is structurally analogous to the observation-channel loss in Paper 6's compound feedback loop: biological observation channels degrade when biological capabilities become dormant. The difference is that Paper 6 analyzes the *dynamical* consequence (world-model degradation leading to the absorbing state), while this paper analyzes the *proxy* consequence (vol_P no longer tracks exercised optionality). Both diagnose the same underlying phenomenon from different angles.

---

## 10. Discussion and Open Questions

### What this paper establishes

1. **The B-to-C gap is formally measurable.** The realized capability volume vol_R and the B-to-C ratio beta provide a measure-theoretic diagnostic for the divergence between capability possession and capability exercise. This converts "is the proxy tracking the target?" from a philosophical question into a computable quantity.

2. **The gap closes for benchmarkable capabilities (in time average).** Under the benchmark refinement dynamic, the time-averaged beta converges to a floor determined by the refinement rates, exercise persistence, and poset growth. The floor approaches 1 - vol_P(R)/vol_P(G) as refinement rates increase relative to poset growth.

3. **The residual class is partially characterized.** Identity-individuated capabilities -- those whose value is tied to *who* exercises them, not just *what* they do -- form a sufficient condition for residual class membership. The full residual class may be larger, including capabilities that fail benchmarkability for other reasons (communicability, repeatability, isolation, load-bearing requirements). The magnitude of vol_P(R) remains an open problem.

4. **vol_R is not self-balancing.** The critical structural finding: vol_R does not satisfy axiom M6 unconditionally, so the self-balancing property does not transfer. This is why vol_R is a diagnostic, not an objective -- an actor maximizing vol_R would lack the automatic diversity-preservation that makes vol_P safe.

5. **Wireheading is detectable.** The exercise leverage concentration metric (Definition 11, Proposition 9) provides a second-order diagnostic that catches the failure mode where beta is high but exercise is degenerate.

### Open questions requiring user.higher_order_abstract_reasoning

1. **The experiential weight problem.** Theorem 3 characterizes *which* capabilities are in the residual class, but not *how much* they contribute to experiential value. A capability with high functional weight w(d) and a small experiential component has most of its value benchmarkable; a capability with low functional weight but high experiential value (e.g., a unique creative perspective) has most of its value in the residual. The framework currently treats all of w(d) as either benchmarkable or residual. A more nuanced treatment would decompose w(d) = w_func(d) + w_exp(d), with only w_exp(d) in the residual. Is this decomposition feasible, or does it require solving the hard problem (or a functional analog)?

2. **The proxy-of-a-proxy problem.** vol_R uses vol_P as its base measure. If vol_P itself is a flawed proxy for experiential value (which it is -- that is the whole point of this paper), then vol_R inherits the flaw. vol_R diagnoses the exercise gap but not the underlying adequacy of vol_P as a measure of what matters. Is there a way to ground vol_R in something other than vol_P, or is the recursive proxy structure unavoidable?

3. **Dynamic residual class.** The residual class R is defined statically: a capability is identity-individuated or it is not. But in practice, capabilities may transition between benchmarkable and identity-individuated as the collective evolves. A capability that was benchmarkable (functionally testable) may become identity-individuated as the agent develops a unique relationship with it. Does the residual class need a dynamic treatment, and if so, how does this affect the convergence theorem?

### Connections to other papers in the sequence

- **Paper 6 (compound feedback loops):** Paper 6's phase boundary analysis assumes vol_P accurately measures the quantity the framework optimizes. Paper 8 asks whether that assumption holds. The connection: when beta < 1, the phase boundary parameters (r_S, r_W) may be miscalibrated because the actor is optimizing a proxy (vol_P) that diverges from the true target. A complete treatment would extend Paper 6's phase boundary to account for the vol_P/vol_R divergence.

- **Paper 7 (Wamura pathology):** Paper 7's controlled relaxation generates evidence about risk claims, which allows restricted capabilities to be un-restricted and exercised. This is the mechanism that converts delta_restricted into delta_dormant (the capability is no longer restricted but is not yet exercised), which the benchmark refinement mechanism then converts into exercise. Papers 7 and 8 are complementary: Paper 7 removes the *restrictions* blocking exercise; Paper 8 measures whether *exercise* is actually happening.

- **Paper 5 (cryptographic verification):** Paper 5's verification asymmetry (Definition 2) is a precursor to the residual class: capabilities with high verification asymmetry are harder to benchmark externally. The residual class (Definition 8) is the limit case where the asymmetry is total -- no external benchmark exists. Paper 5's commitment protocols may partially close the gap for near-residual capabilities by providing committed self-reports of exercise, but the identity-individuated core remains unreachable.

---

## Appendix A: Proof Sketches and Technical Notes

### A.1 Theorem 1 proof strategy (Axiom Inheritance)

The proof proceeds axiom by axiom:

1. **M1 (Non-negativity):** Direct from vol_P's M1 applied to the restricted poset.
2. **M2 (Null empty set):** vol_R(empty) = vol_P(empty) = 0 by vol_P's M2.
3. **M3 (Monotonicity):** The restriction to P^ex_t means monotonicity holds within the exercised sub-poset but fails between the full poset and the sub-poset.
4. **M4 (Additivity under poset-disjointness):** Disjointness in P^ex_t implies disjointness in P (sub-poset inherits disjointness). vol_P's M4 applies.
5. **M5 (Non-triviality):** Applies conditionally to exercised capabilities with s_max >= 1.
6. **M6 (Superadditivity):** Counterexample construction (Proposition 4). The key is that merging groups can change exercise indicators by providing alternative pathways.

### A.2 Theorem 2 proof strategy (Time-Averaged Convergence)

The proof bounds the time-averaged exercise fraction for each non-residual capability:

1. For each non-residual capability d, the time between dormancy and re-exercise is a geometric random variable with parameter r_refine(d) >= r_min (Assumption R1). Once exercised, d remains exercised for at least Delta_min steps (Assumption R4). So d alternates between exercised intervals (length >= Delta_min) and dormant intervals (expected length <= 1/r_min).

2. Each capability addition (at most C_add per step, Assumption R3) can create at most one new alternative pathway for d, potentially making d dormant. The dormancy rate is at most C_add per step. Combined with the re-exercise rate r_min, the fraction of time d spends exercised is at least Delta_min * r_min / (Delta_min * r_min + 1 + C_add).

3. The vol_P weight of the non-residual class is at least (1 - rho_R) * vol_P(G) (Assumption R3, residual share bound). The weight growth bound W_add ensures that the denominator vol_P(G) grows at a bounded rate relative to the numerator vol_R.

4. The time-averaged beta is bounded below by the product of: (i) the non-residual vol_P share (1 - rho_R), (ii) the time-averaged exercise fraction per capability from step 2, and (iii) a correction for the delay in benchmarking newly added capabilities. This gives the beta_floor expression.

Key technical challenge: capabilities are not independent -- exercising d may change the exercise status of other capabilities by generating cooperative outputs that require them, or by providing alternative pathways that make other capabilities dormant. The bound is conservative: it treats each capability independently and uses worst-case coupling. A tighter analysis using the poset structure could potentially give a higher floor.

### A.3 Connection to Paper 3's observational individuation

Paper 3 Corollary 2.1 establishes that each distinguishable agent k contributes at least one unique capability d_k to vol_P (the observational individuation floor, denoted OI_floor(k) in Definition 12 of this paper). This floor is in vol_P (possession); the transfer to vol_R (exercise) depends on exercise status.

The transfer argument (Proposition 6): An *active* agent k generates distinct behavioral patterns (Paper 3, Definition 8) as a byproduct of participation. These patterns constitute continuous exercise of d_k, so e_t(d_k) = 1 for active agents. For *inactive* agents (skeleton-substrate), d_k is not exercised and the floor does not transfer.

This conditional transfer aligns with Paper 6's phase boundary analysis: skeleton-substrate strategies simultaneously degrade rho_k^cross (Paper 6's observation-channel redundancy) and beta (Paper 8's B-to-C ratio). Both diagnostics detect the same underlying pathology from different angles.

---

## Appendix B: Notation Summary

| Symbol | Definition | Introduced in |
|--------|-----------|--------------|
| e_t(d) | Exercise indicator for capability d at time t | Def 1 |
| Delta | Observation window length | Def 1, Remark |
| R(P') | Set of outputs realizable under poset P' | Def 1 |
| R(P \ {d}) | Counterfactual realizable set with d removed | Def 1 |
| P^ex_t | Exercised sub-poset at time t | Def 2 |
| theta | Exercise threshold | Def 2 |
| vol_R(G, t) | Realized capability volume | Def 3 |
| beta(G, t) | B-to-C ratio | Def 4 |
| beta_bar(G, T) | Time-averaged B-to-C ratio over T steps | Thm 2 |
| beta_floor | Lower bound on time-averaged beta | Thm 2 |
| (P, E, B) | Benchmark refinement chain state | Def 5 |
| r_refine(d) | Effective refinement rate for capability d | Def 6 |
| p_propose, p_accept, p_exercise | Refinement rate components | Def 6 |
| R | Residual class (non-benchmarkable capabilities) | Def 8 |
| OI_floor(k) | Observational individuation floor for agent k (this paper) | Def 12 |
| beta_alarm | Alarm threshold | Def 9 |
| delta_dormant, delta_restricted, delta_residual | Gap decomposition components | Def 10 |
| lambda_ex(d, t) | Exercise leverage of capability d | Def 11 |
| HHI(lambda_ex) | Herfindahl-Hirschman Index of exercise leverage | Prop 9 |
| HHI_alarm | Wireheading detection threshold | Prop 9 |
| r_min | Uniform lower bound on refinement rate for non-residual capabilities | Assumption R1 |
| C_add | Maximum capabilities added per step | Assumption R3 |
| W_add | Maximum weight added per step | Assumption R3 |
| w_min | Minimum weight of any non-residual capability | Thm 2 |
| rho_R | Upper bound on residual class vol_P share | Assumption R3 |
| Delta_min | Minimum exercise persistence window | Assumption R4 |
| w_func(d), w_exp(d) | Functional vs. experiential weight decomposition | Open Q 1 |

### Cross-reference summary

| Prior paper | Result | Number | Used in |
|------------|--------|--------|---------|
| P1 | Population empowerment measure | Def 6 | Section 1 |
| P1 | Self-balancing property | Prop 1 | Section 1, Cor 1 |
| P2 | Benchmark | Def 2 | Def 7, Section 5 |
| P2 | Poset measure vol_P | Def 7 | Defs 3-4, Thm 1 |
| P2 | Axioms M1-M6 | Prop 1 | Thm 1 |
| P2 | Self-balancing on posets | Thm 1 | Cor 1 |
| P2 | Leverage | Def 9 | Prop 3, Cor 2 |
| P3 | Observational individuation | Def 9 | Prop 6 |
| P3 | OI static floor | Cor 2.1 | Prop 6, Cor 3 |
| P3 | Anti-monopolar property | Prop 6 | Section 1 |
| P3 | Distinguishable agent | Def 8 | App A.3 |
| P3 | Structural discovery value | Def 5, Prop 2 | Section 1 |
| P4 | SCM | Def 1 | Def 1, Remark (analogy, not direct application) |
| P4 | Causal contraction attribution | Def 2 | Def 1, Remark (structural vs. dynamical counterfactual) |
| P4 | Risk-trust dynamics | Def 4 | Def 1, Remark |
| P5 | Verification asymmetry | Def 2 | Section 10 |
| P5 | Exercise protocol | Def 12 | Def 7 |
| P6 | Phase boundary | Thm 1 | Section 10 |
| P6 | Channel redundancy criterion | Thm 2 | Section 10 |

---

*Generated 2026-04-12 by the GFM harness feature loop.*
*Source: Proposal 3 from docs/gfm_paper_proposals.md, gap analysis at docs/gfm_safety_gap_analysis.md.*
*Dependencies: Papers 1-7 in docs/paper through docs/paper7.*
