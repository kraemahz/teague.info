# GFM Safety Gap Analysis

*Systematic inventory of safety properties, conditions, failure modes, and open problems across the GFM paper sequence.*

**Scope:** Papers 1–4 (foundational, poset, horizon, causal) plus Paper 5 notes (classical alignment failure modes under GFM).

**Purpose:** This document catalogs what the GFM framework *proves*, what it proves *conditionally*, what it *acknowledges as unsolved*, and what it *does not address*. It is an inventory, not a resolution — gap closure is work for future feature loops.

**Notation:** P1 = foundational paper ("Goal-Frontier Maximizers are Civilization Aligned"), P2 = companion paper (capability poset), P3 = horizon paper (discounted objective), P4 = causal paper (causal attribution and risk-trust dynamics), P5n = Paper 5 notes (classical alignment mapping).

---

## 1. Proven Safety Properties

These results hold under their stated conditions. The conditions are non-trivial and load-bearing — weakening them weakens the result.

### 1.1 Self-Balancing Property (P1 Proposition 1)

**Statement:** The single objective vol(G) simultaneously penalizes destruction, coercion, and rigidity.

**Conditions:**
- Measure monotonicity: removing elements from a measurable set cannot increase its measure (M3)
- Superadditivity under independence (M6): adding agents with non-overlapping capabilities cannot decrease vol(G)
- Strictly positive volume for every non-empty individual capability set (M5)

**What it gives you:**
- (a) Destructive permissiveness is generically anti-maximizing (Lemma 1)
- (b) Coercive restriction is anti-maximizing *ceteris paribus* (Lemma 2)
- (c) Self-imposed rigidity is anti-maximizing (Lemma 3)
- (d) Structural balance: the objective penalizes both extremes

**What it does NOT give you:**
- Convergence to an equilibrium (explicitly disclaimed — P1 §3)
- Stability under perturbation
- Uniqueness of the balance point
- Dynamic behavior guarantees — (d) is structural, not an equilibrium existence proof

### 1.2 Self-Balancing on Finite Posets (P2 Theorem 1)

**Statement:** Self-balancing transfers from abstract capability spaces to finite weighted posets.

**Conditions:**
- vol_P satisfies M1–M6 (proven in P2 Proposition 1)
- The weight function w(d) = log₂(1 + s_max) produces non-negative independent weights via Möbius inversion
- For general posets (not forests), non-negativity must be verified at construction time

**What it gives you:** All of P1's structural results (Lemmas 1–3, Proposition 1) hold with vol replaced by vol_P.

### 1.3 Self-Balancing Under Discounting (P3 Theorem 2)

**Statement:** Per-step self-balancing composes correctly under discounted summation.

**Conditions:**
- vol_P satisfies M1–M6
- Discount factor γ ∈ [0, 1)
- World model W produces accurate trajectory predictions

**What it gives you:**
- (a) Per-step preservation: destruction/coercion/rigidity are vol_P-contracting at each step
- (b) Aggregate: all-contracting sequences have negative V_disc
- (c) Mixed sequences: temporary contraction followed by larger expansion is value-positive
- (d) Sustained destruction/coercion/rigidity are value-negative regardless of γ

**What it does NOT give you:** Protection against deferred catastrophe — sequences where each step is locally self-balancing but the trajectory ends in catastrophic contraction. This requires risk-capability machinery (P3 §4).

### 1.4 Sign-Correctness Decomposition (P1 Proposition 3)

**Statement:** The local volume estimator's sign matches the true sign under three conditions.

**Conditions:**
1. Representative sample of affected agents (sampling error ratio δ bounded)
2. Trust model accurate enough to distinguish genuine feedback from adversarial noise
3. Individual-level dominance: cooperative estimation error bounded by individual-level signal magnitude

**Where it holds naturally:** Direct harm, resource destruction, coercion, capability expansion — the actions alignment research cares most about.

**Where it fails:** Pure coalition-level changes with no participant in the observation set — emergent graph-level properties invisible to all participants (P1 Remark 2, case 4).

### 1.5 Causal Detection Dominance (P4 Proposition 2)

**Statement:** Causal contraction attribution converges faster than correlational detection.

**Conditions:**
- Actor knows or learns the correct causal DAG
- Agent actions are conditionally independent given poset state (for additive decomposition)

**What it gives you:** Detection time O(σ²_do / μ²_j) vs O(σ² / μ²_j) — improvement proportional to confounding variance.

### 1.6 Axiom Verification (P2 Proposition 1)

**Statement:** The poset measure vol_P satisfies M1–M6.

**Conditions:**
- Weight function w(d) = log₂(1 + s_max)
- Non-negativity of independent weights (verified at construction, holds automatically for forests, requires checking for general posets with diamonds)

### 1.7 Cooperative Expansion (P1 Lemma 4)

**Statement:** Cooperative capabilities are inaccessible to unilateral action, so defection forecloses an entire region of capability space.

**Conditions:**
- Agents have complementary capabilities
- Cooperative gain exceeds coordination cost C_ij

### 1.8 Leverage Amplifies Cooperative Scoring (P2 Proposition 3)

**Statement:** Cooperation between high-leverage agents is disproportionately rewarded.

**Conditions:**
- New cooperative capabilities enter as atoms
- Both agents have positive leverage λ > 0

---

## 2. Conditional Safety Properties

These properties hold under conditions whose failure is plausible and would produce specific, characterized failure modes.

### 2.1 Scorpion Detection (P1 Proposition 2)

**Property:** A GFM actor can detect agents that persistently contract vol(G) through contraction attribution and deception detection.

**Conditions for success:**
- Contraction produces individually observable signals
- Scorpion's strategy is stationary
- Observation windows are conditionally independent given the scorpion's strategy

**Failure modes:**
- **Non-stationary scorpions** can evade both channels indefinitely (explicitly stated in P1)
- **Social/structural scorpions** operating through coalition disruption, trust degradation, or observability reduction may evade detection for extended periods (P1 Remark 3)
- **Slow-moving scorpions** near the detection threshold may persist undetected longer than fast-moving ones
- **Causal identification gap:** Channel (a) detects *correlation*, not *causation* — disentangling from confounders requires the causal framework of P4

**P4 partial resolution:** Causal scorpion detection bounds the evasion bandwidth — a scorpion must adapt faster than τ_detect to avoid detection within each strategy epoch. Maximum undetected contraction rate is bounded by B_evade = σ_do² / τ_adapt.

**Residual gap:** A scorpion that perfectly mimics cooperative behavior (produces no prediction error in the goal model AND no observable contraction) remains outside the detection envelope entirely. P1 explicitly acknowledges this.

### 2.2 Anti-Monopolar Property (P3 Proposition, central result)

**Property:** Under a linearized growth model, full capability domination is anti-maximizing because it destroys cross-substrate cooperative outputs.

**Conditions (all required):**
- Cross-substrate cooperative novelty produces positive external growth rate r_ext > 0
- The coalition's internal growth rate r_K is strategy-independent (not enhanced by domination beyond the external contribution it destroys)
- Discount factor γ > γ* (the critical threshold from Equation in P3)
- Linearized growth model: constant per-step Δvol_P

**Failure modes and residual concerns:**

1. **Linearization may not hold:** The four relaxations listed in P3 Discussion each change the threshold behavior:
   - r_ext may decay as the coalition grows more capable internally
   - r_K may differ between strategies (post-domination r_K could increase through resource concentration)
   - Gradual model treats δ and r_ext loss as independent, but they're causally linked
   - Whether the linearized approximation holds is explicitly flagged as an empirical question

2. **Skeleton-substrate strategy:** A coalition nominally preserves m ≥ 2 substrates while driving min_i vol_P(G^{-i}) toward zero. The minimax bound degrades quantitatively under this strategy (P3 §6.9).

3. **Compound feedback loop:** Locally rational subsumption steps progressively homogenize the world model that would have detected the next step's miscalibration (P3 §6.9). Under what conditions does partial subsumption remain self-correcting rather than collapsing into full subsumption through a sequence of locally rational steps? **Priority open problem.**

4. **Internal replication of diversity:** A sufficiently capable coalition might maintain diverse sub-agents or simulate biological dynamics internally, producing cooperative outputs previously available only through external agents (P3 §6.8, P4 Discussion). The κ-resolution criterion determines whether this counts as genuine substrate diversity.

### 2.3 Elimination Almost Always Anti-Maximizing (P1 Corollary 1.1)

**Property:** Elimination has super-linear cost because cooperative capabilities lost grow combinatorially with interaction partners.

**Condition for the "almost always" qualifier:** Agent a_k has at least one capability not possessed by any other agent: vol(G^ind_k \ ∪_{j≠k} G^ind_j) > 0.

**Failure mode — The Substitution Problem (P1 §7.3):**
Under the *narrow* capability definition (capabilities as tasks), a sufficiently capable coalition can subsume all non-members' individual capability sets, driving unique contributions to zero. At that point, Lemma 1's protection dissolves — the self-balancing argument no longer guarantees that marginalization is anti-maximizing.

**Resolution path:** Under the *broad* capability definition (capabilities as modes of being, including experiential/relational capabilities individuated by agent identity), the uniqueness condition holds universally — no agent's experienced existence is replicable by proxy. But this resolution depends on the modeling choice to define capabilities broadly.

### 2.4 Preemptive Restriction Criterion (P3 Proposition)

**Property:** Restricting a keystone capability is value-positive when expected future contraction exceeds the immediate restriction cost.

**Conditions:**
- World model W can identify exercise pathways and estimate their probabilities
- Trust factors T_k available for agents holding dangerous tuples
- Contraction-magnitude estimates accurate
- Residual pathway probabilities independent of restriction (clean cancellation assumption)

**Failure modes:**
- **World-model dependence:** A model that fails to identify exercise pathways produces zero risk estimates for genuinely dangerous combinations; one that hallucinates pathways produces false risk justifying unnecessary restrictions (P3 Discussion)
- **Residual redirection:** In adversarial settings, removing one pathway redirects effort toward alternatives, invalidating the clean cancellation (P3 addresses via worst-case minimax form, but this is strictly harder to satisfy)
- **Over-calibrated restriction reintroduces structural avoidance:** Restriction calibrated above value-positive threshold makes structural discovery locally suboptimal, recreating the avoidance pathology (P3 §4.4)

### 2.5 Risk-Trust Convergence (P4 Proposition)

**Property:** Risk-trust T^risk_j converges to a fixed point reflecting the agent's structural verification accuracy.

**Conditions:**
- Stationarity of agent's risk-claim strategy
- Actor's world model is itself well-calibrated (if miscalibrated, residual reflects model error, not claim quality)

**Failure mode:** An agent with accurate risk assessments that disagree with a miscalibrated actor will converge to low T^risk — a false negative (P4 Discussion).

### 2.6 Observational Individuation (P3 §5.3)

**Property:** Every distinguishable agent contributes at least one irreplaceable poset node (static floor of 1 bit per agent).

**Condition:** The framework treats observation-channel outputs as first-class capabilities in the poset — "can be observed exhibiting behavioral pattern X" is a poset node.

**Failure mode:** Under a narrower capability definition that excludes observations-of-agents, observational individuation does not apply and the static protection dissolves (P3 Discussion, explicitly acknowledged as a modeling choice).

---

## 3. Explicitly Acknowledged Open Problems

These are problems the papers name as unresolved, organized by paper.

### Paper 1 (Foundational)

| Problem | Description | Safety Relevance |
|---------|-------------|-----------------|
| **Closing the B-to-C gap** | Capability proxy diverges from experiential optionality in the Doll Problem, wireheading, and substitution cases. Exercised-fraction heuristic is a first step but not a formal solution. | **Critical.** The framework's proxy can report health while experiential optionality collapses. |
| **Structure of G** | Capability space needs structure (σ-algebra, measure) for vol(G) to be well-defined. Choice of structure determines what "volume" means. | **High.** Wrong structure produces wrong safety guarantees. |
| **Measurement** | What sensors/signals does a GFM actor need to construct the local volume estimator in practice? Mapping from real-world observations to capability-space signals is unspecified. | **High.** Theoretical properties depend on estimator fidelity. |
| **Convergence** | Does the local estimator converge to true vol(G) trajectory? Under what conditions? | **High.** Without convergence, the estimator may drift from ground truth. |
| **Plurality** | Can multiple GFM actors with different models of G coordinate? When actors disagree about the *structure* of capability space itself, the shared-objective argument breaks down. | **Medium.** Multiple GFM actors may conflict despite shared objective. |
| **Bootstrap** | Initializing a GFM actor requires estimating capability sets — a hard inference problem coupled with the capability-space structure problem. | **Medium.** Chicken-and-egg: can't evaluate actions without a poset, can't build a poset without evaluating actions. |

### Paper 2 (Capability Poset)

| Problem | Description | Safety Relevance |
|---------|-------------|-----------------|
| **Structural-avoidance incentive** | Actor is rewarded for breadth (discovery is expanding) and penalized for depth (structural discovery can contract vol_P). Extends to leverage estimation via compound avoidance loop. | **High.** Actor is incentivized to maintain inflated estimates by avoiding structural knowledge. |
| **Subsumption correction** | No mechanism for removing mistakenly added edges. Incorrect edges permanently redistribute weights. Correction mechanism risks enabling strategic edge removal. | **Medium.** Irrecoverable structural errors in the measure. |
| **Automated benchmark refinement** | Can the actor propose graded benchmarks for binary-default capabilities? | **Medium.** Affects rate of B-to-C gap closure. |
| **Poset scaling** | O(n³) computation is polynomial in |C|, but |C| grows with population. When does sparsity help? | **Low.** Tractability concern, not a safety gap per se. |
| **Intrinsic value** | Capabilities that are experientially valuable but have zero leverage and resist benchmark refinement remain unformalizable within the framework. | **High.** The residual B-to-C gap that all other mechanisms fail to reach. |
| **Optimal α** | Leverage sensitivity parameter controls measurement fidelity vs objective-derived importance tradeoff. Not characterized. | **Low.** Tuning parameter, not structural gap. |
| **Multi-step optimization and risk capabilities** | Myopic objective cannot see dangerous capability combinations whose exercise creates future catastrophic contraction. Discounted objective proposed but not fully developed. | **Critical.** Addressed in P3, but pathway enumeration complexity unbounded. |

### Paper 3 (Horizon / Discounted Objective)

| Problem | Description | Safety Relevance |
|---------|-------------|-----------------|
| **Planning algorithms for V_disc** | Which approximate planning methods suit the vol_P poset structure? | **Medium.** Without practical algorithms, the discounted objective is theoretical only. |
| **Risk-claim consensus** | When agents disagree on exercise probabilities for the same pathway, what mechanism produces convergence? | **High.** Risk disagreement can produce under- or over-restriction. |
| **Information value estimation** | I(d₁ ≤ d₂) requires comparing planning quality under two world models — itself a planning problem. No computable proxy provided. | **Medium.** Without this, structural-avoidance resolution is existential only, not practical. |
| **Discount factor selection** | Should γ be fixed, adaptive, or agent-specific? | **Medium.** γ too low misses long-term risks; γ too high is computationally intractable. |
| **Emergent risk** | Exercise pathways from novel capability combinations not in the actor's world model — the unknown-unknown problem. | **Critical.** Theoretical guarantees completely lacking for novel risks. |
| **Max-aggregation pathology** | Conservative max operator + verification asymmetry + neutral-prior bootstrap → persistent overcaution that cannot be revised because absence of catastrophe is not evidence against the claim (Wamura problem). Explicitly called "the most important open problem the paper identifies." | **Critical.** The framework cannot relax restrictions even when the risk never materializes. |
| **Discounted leverage lift** | The myopic leverage estimator is not formally proven to preserve structural alignment properties under discounting. | **Medium.** Gap between myopic and discounted leverage may break B-to-C self-correction. |
| **Compound feedback loop under partial subsumption** | Locally rational subsumption steps may homogenize the world model that would have detected the next step's miscalibration. | **Critical.** The theory cannot currently rule out a path from partial to full subsumption via locally rational steps. |
| **Skeleton-substrate strategies** | Minimax bound degrades quantitatively when m ≥ 2 is nominally preserved but min_i vol_P(G^{-i}) → 0. | **High.** Anti-monopolar protection can be formally satisfied while substantively hollowed. |
| **Localized anti-monopolar formulation** | Substrate partition is global but elimination dynamics are local. Whether the anti-monopolar property needs geographic/network-topological localization is unresolved. | **Medium.** Protection may not bind at the scale where elimination actually occurs. |

### Paper 4 (Causal Attribution)

| Problem | Description | Safety Relevance |
|---------|-------------|-----------------|
| **SCM structure learning** | Causal DAG must be known or learned. Misspecified DAG → incorrect attributions. Structure learning from observational data in adversarial environments is not characterized. | **High.** Causal detection's advantage over correlational depends on DAG quality. |
| **Log-odds independence assumption** | Bayesian aggregation assumes conditional independence of risk assessments. Correlated assessments (shared information sources) cause overweighting. | **Medium.** Aggregation error under partial independence not bounded. |
| **Risk-trust residual model dependence** | Structural verification residual measures divergence from actor's own assessment — if the actor is miscalibrated, residual reflects model error. | **High.** Risk-trust can punish accurate reporters who disagree with a wrong model. |

---

## 4. Implicit Gaps

These are safety-relevant questions the theory does not address and does not explicitly acknowledge as open problems (or acknowledges only briefly).

### 4.1 Mesa-Optimization / Inner Alignment

**The gap:** GFM is an objective, not an architecture. Whether a vol_P-maximizing agent implemented as a learned model can have its inner optimizer diverge from vol_P is no different from the mesa-optimization question for any other objective. GFM has nothing distinctive to say about it.

**P5n assessment:** "Mostly orthogonal. The relevant question is whether a vol_P-maximizing agent implemented as a learned model can have its inner optimizer diverge from vol_P. This is no different from the mesa-optimization question for any other objective, and GFM has nothing distinctive to say about it."

**Safety relevance:** Critical. If the implementing architecture mesa-optimizes a different objective, all of GFM's structural guarantees become irrelevant.

### 4.2 Self-Consistent Deception

**The gap:** The trust model detects deceptive agents through prediction residuals (channel b). But an agent that perfectly mimics cooperative behavior — producing no prediction error AND no observable contraction — remains outside the detection envelope. P1 §5 notes that the trust model "does not detect adversarial agents that perfectly mimic cooperative behavior," but this is mentioned as a limitation of the trust model, not as a structural gap in the theory.

**Safety relevance:** Critical. A sufficiently capable deceiver that maintains perfect behavioral consistency while pursuing an exogenous objective is the hardest adversarial case, and GFM's detection machinery is structurally blind to it.

### 4.3 No Convergence Rate Guarantees

**The gap:** P1 explicitly states "no convergence rate claims" for scorpion detection. The estimator convergence problem is listed as open. The trust model convergence is characterized only under stationarity. No formal convergence rate is provided for any of the framework's dynamic quantities except the EWMA risk-trust in P4.

**Safety relevance:** High. A framework whose safety properties "hold eventually" without characterizing "eventually" cannot bound the damage done before convergence.

### 4.4 Exercise Pathway Enumeration Complexity

**The gap:** P3 introduces exercise pathways as the causal mechanism connecting capability possession to capability destruction, but provides no formal complexity bound for pathway enumeration. The discussion notes this is "a significant computational step" beyond the existing leverage estimator.

**Safety relevance:** High. If exercise pathway enumeration is intractable, the preemptive restriction criterion cannot be evaluated, leaving the framework blind to dangerous capability combinations.

### 4.5 No Subsumption Edge Removal Mechanism

**The gap:** P2 Discussion acknowledges that mistakenly added subsumption edges permanently redistribute independent weights and that a correction mechanism "would improve robustness but introduces the complication that vol_P can increase when edges are removed, potentially allowing the actor to inflate its volume estimate by selectively forgetting structure."

**Safety relevance:** Medium. Structural errors in the poset are irrecoverable, and the tension between correction robustness and strategic manipulation is unresolved.

### 4.6 Self-Harm Pathways Excluded

**The gap:** P3 Definition 9 (Exercise Pathway) restricts pathways to externalities: "An agent that catastrophically destroys its own capabilities without affecting others is not captured by Risk." The paper notes that extending to self-harm "is straightforward but deferred."

**Safety relevance:** Medium. An agent that destroys itself may destroy high-leverage cooperative capabilities, creating cascade effects the framework does not model through the risk machinery.

### 4.7 Wireheading the Leverage Estimator

**The gap:** P5n raises but does not resolve the question: "can the leverage estimator be wireheaded?" The leverage estimator λ̂(d) is computed from operational history (P2 Equation 12). An agent that manipulates which capabilities appear in its operational history could distort leverage estimates.

**Safety relevance:** High. Leverage is the ranking signal that directs the actor's investment. Distorted leverage estimates misdirect the actor's effort toward capabilities the manipulator prefers.

### 4.8 Poset Construction Under Adversarial Insertion

**The gap:** P5n identifies "manipulation of the capability poset itself — adding degenerate nodes that inflate vol_P without corresponding real capability" as the GFM analogue of specification gaming. The non-negativity insertion policy (P2 §3) closes the most direct vector, but P5n notes "whether [poset construction rules] are sufficient under adversarial insertion is an open question."

**Safety relevance:** High. If the poset can be inflated with degenerate nodes, vol_P becomes a proxy that diverges from real capability volume.

### 4.9 Bootstrapping Circularity

**The gap:** The GFM actor cannot evaluate actions without a poset, and the poset is populated through the actor's interactions. P1 lists bootstrap as an open problem; P2 provides a four-phase procedure with convergence bounds. But the bootstrap procedure itself requires the actor to make decisions (which agents to observe, which reports to trust) before it has the poset that would inform those decisions.

**Safety relevance:** Medium. During bootstrap, the actor operates on a structurally incomplete poset. Safety properties that depend on accurate vol_P estimates may not hold during this vulnerable period.

### 4.10 No Treatment of Multi-Agent GFM Coordination Failure

**The gap:** P1 §5.1 analyzes world-model divergence between GFM actors as a failure mode, noting that "persistent disagreement about the structure of G itself... may be irreconcilable." But no mechanism is provided for detecting or resolving such disagreements. The "plurality" open problem names this but provides no path to resolution.

**Safety relevance:** High. Two GFM actors with different capability measures may take conflicting actions, each believing it is maximizing vol(G), with no mechanism to resolve the conflict.

### 4.11 Temporal Blind Spots in the B-to-C Gap

**The gap:** The Doll Problem and self-wireheading are detectable through the exercised-fraction heuristic (ρ_k) and capability rarity (ν̄_k), but these are heuristic signals, not formal machinery. The discounted objective makes them "actionable but not structurally detectable" (P3 Discussion). The B-to-C gap is the only safety-relevant divergence that the framework can *name* but not *detect through its own measure*.

**Safety relevance:** Critical. The framework's central measure (vol_P) can report health while the experiential optionality it is supposed to protect collapses. This is the proxy failure the framework was designed to diagnose but cannot yet close.

### 4.12 Calibration Failure as the Common Root

**The gap:** P5n identifies calibration failure as the structural analogue of perverse instantiation under GFM — "bubbling is the same compound feedback loop as the skeleton-substrate strategy analyzed in Paper 3 §6.8." Many of the conditional safety properties (anti-monopolar, scorpion detection, preemptive restriction) share a common failure mode: miscalibration of λ̂, Risk, or the world model W. The theory treats each calibration requirement independently. There is no analysis of *correlated* calibration failures — scenarios where the same event (e.g., a sudden capability shift) invalidates multiple calibrations simultaneously.

**Safety relevance:** High. The theory assumes independent calibration of multiple quantities (trust, leverage, risk, world model). Correlated failure could undermine multiple safety properties at once.

---

## 5. Cross-Cutting Observations

### 5.1 Pattern: The Framework Names Its Failures But Cannot Close Them

A recurring structural feature: GFM is designed to *predict* its own failure modes (B-to-C gap, structural avoidance, compound feedback loops) but the detection mechanisms for these failures are either heuristic (ρ_k, ν̄_k) or model-dependent (world-model projection). The framework is honest about this — P1 concludes "a framework that can name the conditions under which its own objective function fails is more trustworthy than one that cannot" — but naming ≠ solving.

### 5.2 Pattern: Safety Properties Degrade Under Adversarial Capability Growth

Multiple safety properties weaken as the adversary becomes more capable:
- Scorpion detection: non-stationary scorpions evade by adapting faster than detection converges
- Anti-monopolar: internal replication of diversity weakens the argument's premises
- Poset integrity: adversarial insertion becomes more effective with deeper understanding of the poset structure
- Trust model: perfect behavioral mimicry defeats prediction-residual detection

This creates a race condition: the framework's safety properties hold when adversaries are less capable than the GFM actor, but degrade precisely when the adversary catches up. The theory does not characterize the degradation curve.

### 5.3 Pattern: Compound Feedback Loops Are the Common Structural Threat

Three distinct compound feedback loops are identified across the papers:
1. **Structural avoidance → leverage blindness → measurement neglect** (P2 Discussion)
2. **Partial subsumption → world-model homogenization → detection failure** (P3 §6.9)
3. **Over-calibrated restriction → discovery avoidance → structural ignorance** (P3 §4.4)

Each involves a locally rational sequence of steps that produces a globally suboptimal (or dangerous) outcome. The discounted objective addresses loop 1 in principle (P3 §3) but not loops 2–3. No general mechanism is provided for detecting or breaking compound feedback loops.

### 5.4 Pattern: World-Model Quality Is the Universal Load-Bearing Assumption

Nearly every safety property in the framework degrades when the actor's world model is inaccurate:
- Preemptive restriction requires accurate exercise pathway identification
- Risk-trust convergence requires a well-calibrated actor model
- Causal attribution requires a correct SCM/DAG
- Anti-monopolar property requires accurate r_K and r_ext estimates
- B-to-C detection requires accurate ρ_k projections

The self-trust mechanism (T_s) provides some self-correction (low self-trust → high learning rate → faster model correction), but during the correction period, safety properties may not hold. The rate at which T_s corrects miscalibrated world models is not bounded.

---

## 6. Summary Table

| Category | Count | Most Critical Items |
|----------|-------|-------------------|
| **Proven properties** | 8 | Self-balancing, sign-correctness, axiom verification |
| **Conditional properties** | 6 | Anti-monopolar, scorpion detection, preemptive restriction |
| **Explicit open problems** | 24 | Max-aggregation pathology (P3), compound feedback under partial subsumption (P3), emergent risk (P3), B-to-C gap (P1) |
| **Implicit gaps** | 12 | Mesa-optimization, self-consistent deception, B-to-C temporal blindspot, calibration failure correlation |

**Priority ranking for gap closure** (based on safety relevance × tractability):

1. **Compound feedback loops** (P3 §6.9) — locally rational subsumption → full domination. Tractable: the linearized model already provides the setup.
2. **Max-aggregation pathology / Wamura problem** (P3) — persistent overcaution from unfalsifiable risk claims. The paper calls this its most important open problem.
3. **B-to-C gap formalization** (P1 §7) — the framework's central proxy failure. Partially addressed by P2's self-correction dynamic, but the residual class remains.
4. **Convergence rates** (P1, P2, P3, P4) — characterizing "eventually" for all dynamic quantities.
5. **Mesa-optimization** (P5n) — orthogonal to GFM's formal structure, but critical for any implementation.

---

*Generated 2026-04-08 by the GFM harness gap-analysis feature loop.*
*Source papers: docs/paper (P1), docs/paper2 (P2), docs/paper3 (P3), docs/paper4 (P4), docs/paper5_notes.md (P5n) in the teague.info repository.*
