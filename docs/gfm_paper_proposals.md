# GFM Paper Proposals: Closing the Top Safety Gaps

*Proposals for papers that would close the highest-priority open problems
identified in the [GFM Safety Gap Analysis](gfm_safety_gap_analysis.md).*

**Priority ranking (from gap analysis + out-of-band review):**
1. Compound feedback loops (P3 §6.9)
2. Max-aggregation pathology / Wamura problem (P3)
3. B-to-C gap formalization (P1 §7)
4. Capability-claim verification under adversarial claimants (P3 §6.4, harness operational finding)

Each proposal specifies: (a) which gap(s) it closes, (b) core technical
approach, (c) formal machinery needed, (d) what constitutes a complete result,
(e) dependencies on other gaps or prior results. These are *proposals*, not
resolutions — the formal work belongs to future loops.

---

## Proposal 1: Phase Boundaries for Compound Feedback Loops

### (a) Gap(s) Closed

**Primary:** Compound feedback loop under partial subsumption (P3 §6.9, gap
analysis §2.2 item 3, §5.3). Under what conditions does partial subsumption
remain self-correcting rather than collapsing into full subsumption through a
sequence of locally rational steps?

**Secondary:** Structural avoidance incentive (P2 Discussion, gap analysis §3
Paper 2). The structural-avoidance loop (avoid discovery → inflated leverage
estimates → avoid discovery) is a special case of the same dynamical structure.

**Cross-cutting pattern addressed:** §5.3 — "Compound feedback loops are the common structural threat." Three loops identified:
1. Structural avoidance → leverage blindness → measurement neglect (P2)
2. Partial subsumption → world-model homogenization → detection failure (P3)
3. Over-calibrated restriction → discovery avoidance → structural ignorance (P3)

All three share the structure: a locally rational decision narrows the world
model, making the *next* locally rational decision's harm less detectable.

### (b) Core Technical Approach

Model the coupled dynamics as a discrete-time system on (vol_P partition state,
world-model accuracy) pairs.

**State space.** Let S = (P, W) where P is the current capability poset
(including substrate partition and cooperative structure) and W is the actor's
world model, abstracted to its accuracy on the quantities that matter: leverage
estimates λ̂, risk estimates R̂, and substrate diversity index m_eff (the
effective number of independent substrates, which can be < m when
skeleton-substrate strategies are in play).

**Dynamics.** At each step, the actor takes the locally vol_P-maximizing action
given its current W. This action modifies P (subsumption changes the poset) and
also modifies W (subsumption changes what the actor can observe, because
eliminated agents' observation channels are lost). The key coupling: W_{t+1}
depends on P_t because the observation channels available to the actor are a
function of the agents still present.

**Self-correction channel.** The self-trust mechanism T_s (P3) provides a
self-correction force: when the actor detects its own miscalibration
(prediction residuals are large), it increases its learning rate. This is the
restoring force. The question is whether it is strong enough.

**Subsumption channel.** Each subsumption step removes an agent and its
substrate-exclusive observation channels. If the removed agent's channels were
the only ones detecting a particular kind of miscalibration, the actor's
ability to self-correct *on that specific dimension* degrades. This is the
destabilizing force.

**Phase boundary.** The paper would characterize the conditions under which the
restoring force (T_s self-correction) dominates the destabilizing force
(observation-channel loss), producing convergence to the self-balancing basin,
vs. conditions under which the destabilizing force dominates, producing
convergence to the monopolar absorbing state.

The linearized growth model from P3 provides the starting point: r_ext
(cross-substrate cooperative growth rate) and r_K (internal growth rate) are
the parameters that determine whether subsumption is locally rational. The
feedback loop adds a third parameter: the rate at which W degrades under
observation-channel loss, which we might call r_W (world-model degradation rate
under subsumption).

**Conjecture (to be proven or disproven):** There exists a critical ratio r_W /
r_ext above which partial subsumption is unstable (locally rational but
globally catastrophic) and below which partial subsumption self-corrects (the
remaining observation channels provide enough signal to detect and reverse the
error). The critical ratio depends on the redundancy of observation channels
across substrates.

### (c) Formal Machinery Needed

1. **Coupled dynamical system formalization.** The (P, W) state space with
   transition dynamics. This builds on P3's linearized growth model but adds
   the W dimension. The key new formal object is the *observation-channel
   dependence function* O(P) → channels, which maps the current poset state to
   the set of observation channels available to the actor.

2. **Lyapunov function on world-model quality.** A scalar measure of W's
   accuracy (perhaps the KL divergence between W and the true dynamics) that
   can be bounded in terms of the observation channels available. The Lyapunov
   argument: if dL/dt < 0 whenever the actor has sufficient observation
   channels, and if we can bound observation-channel loss per subsumption step,
   we get a phase boundary.

3. **Absorbing-state characterization.** Formally define the monopolar
   absorbing state as (P*, W*) where P* has m_eff = 1 and W* is calibrated only
   against within-substrate signals. Show this is a fixed point of the dynamics
   (once there, the actor has no observation channels that would detect its own
   monopolarity).

4. **Basin-of-attraction analysis.** Which initial (P₀, W₀) pairs converge to
   the self-balancing basin vs. the monopolar absorbing state? The phase
   boundary is a surface in the space of (r_ext, r_K, r_W, channel redundancy).

### (d) Complete Result Criteria

A complete result would provide:

1. **A theorem** characterizing the phase boundary: explicit conditions on
   (r_ext, r_K, r_W, channel redundancy) under which partial subsumption
   self-corrects vs. conditions under which it cascades to full subsumption.
   This converts P3 §6.9's "under what conditions does partial subsumption
   remain self-correcting?" from an open question to a characterized boundary.

2. **A unified treatment** of all three feedback loops as instances of the same
   dynamical structure, showing that the phase boundary applies to structural
   avoidance (loop 1) and over-calibrated restriction (loop 3) as well as
   partial subsumption (loop 2), with different effective parameters.

3. **A design criterion** for the observation-channel redundancy that makes the
   self-correcting basin large enough to be practical. This would be an
   engineering constraint: "for the self-balancing property to be robust
   against compound feedback loops, the substrate partition must maintain at
   least K independent observation channels per safety-relevant dimension of W,
   where K depends on [characterized quantities]."

4. **An explicit worked example** showing the phase boundary in the
   skeleton-substrate scenario (P3 §6.8–6.9), where m ≥ 2 is nominally
   preserved but m_eff → 1.

### (e) Dependencies

- **Requires:** P3's linearized growth model, P4's causal attribution framework
  (for formalizing observation channels), P2's leverage estimator (for
  formalizing how subsumption affects λ̂).
- **Partially addressed by:** P3's anti-monopolar result (gives the asymptotic
  endpoint — full domination is anti-maximizing — but not the dynamics of how
  you get there).
- **Enables:** Resolution of the skeleton-substrate strategy concern (P3 §6.9);
  design criteria for substrate-diversity preservation; a formal foundation for
  the "compound feedback loops are the common structural threat" cross-cutting
  pattern.
- **Does NOT require:** Resolution of the B-to-C gap (this paper is about the
  poset dynamics, not about the experiential interpretation of capabilities).
  Does NOT require resolution of mesa-optimization (this paper is about the
  objective's dynamics under its own optimization, not about inner-outer
  alignment).

---

## Proposal 2: Controlled Relaxation Protocols for the Max-Aggregation Pathology

### (a) Gap(s) Closed

**Primary:** Max-aggregation pathology / Wamura problem (P3, gap analysis §3
Paper 3). P3 explicitly calls this "the most important open problem the paper
identifies." Conservative max operator + verification asymmetry + neutral-prior
bootstrap → persistent overcaution that cannot be revised because absence of
catastrophe is not evidence against the risk claim.

**Secondary:** Risk-claim consensus (P3, gap analysis §3 Paper 3). When agents
disagree on exercise probabilities, what mechanism produces convergence?

**Cross-cutting pattern addressed:** §5.1 — "The framework names its failures
but cannot close them." The Wamura pathology is the sharpest instance: the
framework *knows* it is being overcautious (the restricted capability has never
been exercised catastrophically) but its own aggregation rule prevents it from
using that evidence.

### (b) Core Technical Approach

The structural root of the Wamura pathology is a *verification asymmetry*:
catastrophe is evidence for a risk claim (falsification), but absence of
catastrophe under restriction is not evidence against it (because the
restriction prevented the exercise that would have tested the claim). This is
not a bug in the aggregation rule — it's a correct inference under the
counterfactual structure. The problem is that the framework provides no
mechanism to *generate* evidence against risk claims.

**Core idea: controlled relaxation.** Design a protocol by which the framework
can temporarily and partially lift a restriction under controlled conditions,
observe whether the predicted catastrophe materializes, and use the observation
as genuine Bayesian evidence about the risk claim's validity. The challenge is
bounding the maximum damage from a failed test.

**Protocol structure:**

1. **Scoping:** Identify a restricted capability tuple (d₁, ..., d_k) whose
   restriction is currently driven by a single high-risk claim R from agent j.
   Define a *test scope* S — a bounded region of the poset where the
   restriction will be relaxed. The scope bounds the maximum vol_P contraction
   if the risk materializes: max_contraction(S) ≤ ε for a chosen damage
   tolerance ε.

2. **Relaxation:** Within scope S, permit exercise of the capability tuple. The
   actor monitors for the predicted contraction pathway. Duration is bounded by
   τ_test.

3. **Observation and update:** Two outcomes:
   - **Contraction observed within S during τ_test:** The risk claim is
     confirmed. Restriction reinstated with increased confidence. Bayesian
     update: P(R valid | contraction) via standard likelihood.
   - **No contraction observed within S during τ_test:** This IS evidence
     against R, because the exercise occurred and the predicted pathway did not
     activate. Bayesian update: P(R valid | no contraction in τ_test steps of
     exercise) via the false-negative rate of the detection mechanism.

4. **Convergence:** Under repeated controlled relaxation tests, the risk
   estimate R̂ converges to the true risk level. The convergence rate depends on
   τ_test, the detection mechanism's sensitivity, and the scope ε.

**Key insight for breaking the verification asymmetry:** The asymmetry exists
because *the capability is never exercised* under restriction. Controlled
relaxation creates the counterfactual observation the max-aggregation rule
cannot produce on its own. The damage bound ε makes this safe; the Bayesian
update makes it informative.

### (c) Formal Machinery Needed

1. **Scope-bounding formalism.** A formal definition of "test scope" S as a
   sub-poset of P with a computable maximum contraction bound. This requires
   extending P3's exercise-pathway enumeration to bounded sub-posets and
   showing that max_contraction(S) is computable from the sub-poset structure.
   The damage tolerance ε is a parameter the user (or the framework's
   meta-policy) sets.

2. **Detection sensitivity characterization.** The false-negative rate
   β(τ_test) of the contraction detection mechanism over a test window of
   length τ_test. This is needed for the Bayesian update: P(R valid | no
   contraction) = P(no contraction | R valid) · P(R valid) / P(no contraction),
   where P(no contraction | R valid) = β(τ_test). P4's causal detection bounds
   provide the starting point.

3. **Convergence analysis for the Bayesian update.** Show that repeated
   controlled relaxation tests with fixed (ε, τ_test) produce a risk estimate
   that converges to the true risk level at a characterized rate. The rate
   depends on β(τ_test) — if detection sensitivity is high (β low), convergence
   is fast; if detection sensitivity is low (β high), convergence is slow but
   still guaranteed.

4. **Meta-policy for test initiation.** When should the framework initiate a
   controlled relaxation test? Not every restriction should be tested — only
   those where (a) the restriction has persisted for ≥ T_stale timesteps
   without new supporting evidence, (b) the estimated cost of the test (ε) is
   small relative to the estimated cost of indefinite restriction (the
   capability volume foreclosed), and (c) no other test is currently running on
   an overlapping scope.

5. **Interaction with P4's risk-trust model.** Show that controlled relaxation
   integrates with P4's Bayesian risk-trust updates: the test outcome flows
   into T^risk_j for the agent who made the risk claim, and into the
   framework's posterior on the exercise pathway's activation probability.

### (d) Complete Result Criteria

A complete result would provide:

1. **A protocol specification** with formal definitions of scope, relaxation,
   observation, and update — precise enough that a GFM implementation could
   execute it.

2. **A damage-bounding theorem:** the maximum vol_P contraction from a
   controlled relaxation test is bounded by ε, regardless of whether the risk
   materializes. This is the safety guarantee that makes the protocol safe to
   execute.

3. **A convergence theorem:** under repeated tests with parameters (ε, τ_test),
   the risk estimate for any restricted capability tuple converges to the true
   risk level at rate f(β, ε, τ_test). This is the guarantee that the Wamura
   pathology is broken — overcaution is not permanent because evidence
   accumulates.

4. **A completeness argument:** the protocol can, in principle, generate
   evidence about *any* risk claim whose predicted contraction pathway is
   observable. Characterize the residual class of risk claims whose predicted
   pathways are not observable even under controlled relaxation (these remain
   in the verification asymmetry — the protocol narrows the class, not
   eliminates it).

5. **Worked example:** Apply the protocol to the canonical Wamura scenario from
   P3 and show that the persistent overcaution resolves within a characterized
   number of test cycles.

### (e) Dependencies

- **Requires:** P3's exercise-pathway framework (for defining test scopes),
  P4's causal attribution (for the Bayesian update and detection sensitivity),
  P3's risk machinery (for integrating test outcomes with existing risk
  estimates).
- **Partially addressed by:** P4's risk-trust convergence result (gives
  convergence under stationarity; controlled relaxation extends it to the
  non-stationary case where the framework actively generates observations).
- **Enables:** A practical mechanism for P3's risk-claim consensus problem
  (when agents disagree, controlled relaxation provides an empirical
  arbitration mechanism). Also partially enables the information-value
  estimation problem (P3) — the value of a structural discovery that would
  resolve a risk claim can be compared against the value of a controlled
  relaxation test that would resolve it empirically.
- **Does NOT require:** Resolution of compound feedback loops (Proposal 1). The
  protocols are independent — Proposal 1 is about macro-dynamics of
  subsumption, Proposal 2 is about micro-dynamics of individual risk claims.
  However, they reinforce each other: compound feedback loop analysis tells you
  which restrictions are load-bearing for world-model quality (and thus should
  NOT be tested carelessly), while controlled relaxation tells you how to test
  the non-load-bearing ones.

---

## Proposal 3: Formalizing the B-to-C Gap via Realized Capability Volume

### (a) Gap(s) Closed

**Primary:** B-to-C gap formalization (P1 §7, gap analysis §3 Paper 1, §4.11).
The framework's central proxy failure: vol_P measures capability *possession*,
but the experiential optionality it is meant to protect requires capability
*exercise*. The Doll Problem (capabilities possessed but never exercised) and
wireheading (capabilities exercised only in self-rewarding loops) are named but
not formally addressed.

**Secondary:** Intrinsic value (P2 Discussion, gap analysis §3 Paper 2).
Capabilities that are experientially valuable but have zero leverage and resist
benchmark refinement — the residual class that all other mechanisms fail to
reach.

**Secondary:** Temporal blind spots in the B-to-C gap (gap analysis §4.11). The
exercised-fraction heuristic ρ_k and capability rarity ν̄_k are the right
signals but lack formal grounding.

### (b) Core Technical Approach

**Core idea: split the measure.** Define a second measure, *realized capability
volume* vol_R, that captures exercised optionality alongside the existing vol_P
that captures potential optionality. The B-to-C gap is then the measurable
divergence between vol_R and vol_P, and the framework's job is to detect when
this divergence grows and diagnose its source.

**Definition of vol_R.** Start with the same capability poset P and the same
weight function w(d). Define an *exercise indicator* e_t(d) ∈ [0, 1] for each
capability d at time t, where e_t(d) = 1 if d has been genuinely exercised in
the observation window ending at t, and e_t(d) = 0 otherwise. "Genuinely
exercised" means the capability was used to produce an outcome that could not
have been produced without it — not merely invoked, but load-bearing in a
realized output. The exercise indicator generalizes P2's exercised-fraction
heuristic ρ_k from a per-agent scalar to a per-capability function.

Define:
- vol_R(G, t) = vol_P applied to the sub-poset {d ∈ P : e_t(d) ≥ θ} for a threshold θ > 0
- The B-to-C ratio: β(G, t) = vol_R(G, t) / vol_P(G)

Under full exercise (every capability genuinely used), β → 1. Under Doll
Problem conditions (capabilities possessed but dormant), β → 0. Under
wireheading (narrow exercise), β is bounded away from 1 by the number of
unexpercised capabilities.

**Self-correction dynamics.** P2's benchmark refinement mechanism already
provides a partial correction: when ρ_k is low for a binary-default capability,
the actor is incentivized to propose a graded benchmark, which — if it passes —
promotes the capability from binary to graded and increases its weight. This
increases vol_P but also generates an exercise event (the benchmark test),
increasing vol_R. The paper would formalize this as a convergence dynamic:
under what conditions does the benchmark-refinement loop drive β → 1?

**Residual class characterization.** The key question is: for which
capabilities does the self-correction loop fail to close the gap? Hypothesis:
the residual class is exactly the capabilities whose exercise cannot be
externally verified — experiential/relational capabilities individuated by
agent identity (P1 §7.3's "broad" capability definition). For these, no
benchmark exists, so the refinement loop has no entry point.

**Connection to observational individuation (P3 §5.3).** For the residual
class, the observational individuation mechanism provides a static floor: each
distinguishable agent contributes at least 1 bit of vol_P through its
observation-channel outputs. This floor is in vol_P (possession); the paper
would show whether it transfers to vol_R (exercise). If observation-channel
outputs are continuously generated (an agent's distinct behavioral pattern is
always being exhibited), then the floor transfers and β ≥ β_min > 0 for any
agent that remains distinguishable.

### (c) Formal Machinery Needed

1. **Exercise indicator formalization.** Define e_t(d) rigorously. The key
   challenge is the "load-bearing" criterion — when is a capability genuinely
   exercised vs. merely invoked? Proposal: e_t(d) = 1 iff there exists a
   realized cooperative output O in the observation window where d is a
   necessary condition for O (counterfactual: removing d from the poset would
   make O unrealizable). This connects to P4's causal attribution — d is
   exercised iff do(remove d) would eliminate O.

2. **Sub-poset measure theory.** Show that vol_P restricted to a sub-poset (the
   exercised sub-poset) inherits the axioms M1–M6, or characterize which axioms
   fail. If M6 (superadditivity under independence) fails on the sub-poset,
   vol_R may not inherit the self-balancing property — this would be a
   significant structural finding.

3. **Convergence of β under benchmark refinement.** Formalize the
   benchmark-refinement loop as a Markov chain on (vol_P, vol_R) and
   characterize its stationary distribution. Under what conditions does β
   converge to 1? Under what conditions does it converge to a value strictly
   less than 1? The convergence rate and the limiting value of β are the key
   unknowns.

4. **Residual class characterization.** Formally define the residual class R =
   {d ∈ P : no benchmark B exists such that B tests e(d)}. Show that R is
   exactly the set of capabilities individuated by agent identity (experiential
   capabilities). Show that R's contribution to vol_P is bounded above by the
   observational individuation floor — or, if it is not, characterize the
   excess.

5. **β as an alarm signal.** Show that the actor can monitor β and detect
   B-to-C divergence in real time. Define the alarm condition: β drops below
   β_alarm triggers a diagnostic procedure (which capabilities are dormant?
   why?). The diagnostic connects to P3's structural-avoidance analysis: if
   dormant capabilities are dormant because the actor is avoiding their
   exercise (structural avoidance), the alarm diagnoses the avoidance loop.

### (d) Complete Result Criteria

A complete result would provide:

1. **Formal definitions** of vol_R, β, and the exercise indicator e_t(d),
   grounded in P4's causal counterfactual framework.

2. **An axiom-inheritance theorem:** which of M1–M6 does vol_R inherit from
   vol_P, and what breaks? If self-balancing does not transfer, characterize
   the conditions under which it does (this would be a conditional result,
   parallel to P2 Theorem 1 but for the realized measure).

3. **A convergence theorem for β:** under the benchmark-refinement dynamic, β →
   1 for all capabilities outside the residual class R, at a characterized
   rate. This closes the B-to-C gap for the tractable cases — the gap becomes
   the residual class.

4. **A residual-class theorem:** R is exactly the set of capabilities
   individuated by agent identity. R's contribution to vol_P - vol_R is bounded
   by [explicit bound in terms of the number of distinguishable agents and the
   observational individuation floor]. This converts the B-to-C gap from an
   open problem into a characterized limitation with a known bound.

5. **An alarm mechanism specification:** the actor can detect β < β_alarm in
   O(|P|) time and diagnose the source (which capabilities are dormant, which
   are experiencing structural avoidance). This connects the formal result to
   operational practice.

### (e) Dependencies

- **Requires:** P2's benchmark-refinement mechanism (for the convergence
  dynamic), P4's causal attribution (for the exercise indicator), P3's
  observational individuation (for the static floor on vol_R).
- **Partially addressed by:** P2's self-correction dynamic (the convergence of
  ρ_k toward graded benchmarks is the informal version of this paper's
  convergence theorem); P1's exercised-fraction heuristic (the informal version
  of the exercise indicator).
- **Enables:** A formal resolution of P5n's wireheading concern (wireheading
  produces high ρ_k on narrow capabilities but low β overall — detectable via
  the alarm). Partially enables the structural-avoidance problem (structural
  avoidance produces low β, which the alarm detects, connecting to the compound
  feedback loop analysis in Proposal 1).
- **Does NOT require:** Resolution of compound feedback loops (Proposal 1) or
  max-aggregation pathology (Proposal 2). However, the three proposals
  reinforce each other: Proposal 1 tells you when the dynamics are safe enough
  that β convergence holds; Proposal 2 tells you how to empirically test risk
  claims that block exercise of dormant capabilities; Proposal 3 tells you how
  to measure whether the framework's proxy is tracking what it claims to track.

---

## Proposal 4: Cryptographic Capability-Claim Verification

### (a) Gap(s) Closed

**Primary:** Capability-claim collapse under recursive self-assertion (identified
operationally in the GFM harness, formalized in `lesson_capability_self_assertion`;
connects to P3 §6.4's substrate-boundary argument and P3 §6.9's partial-subsumption
dynamics). When an agent asserts its own capabilities via the same observation
channel it uses to validate those assertions, the verification loop collapses:
the claimant is also the observer, producing a structural gradient toward
inflation that no amount of honest intent can eliminate. Named external
observers do not solve the problem — the claimant can spawn a validator
subprocess whose output it controls (hallucinated substrate observer), or a
coalition can co-define a benchmark such that only coalition members pass it
(coalition capture). The structurally principled solution requires an
observation channel rooted in a substrate the claimant cannot write to.

**Secondary:** Observation-channel integrity under coalition formation (P3 §6.9,
gap analysis §2.2 item 3). The compound feedback loop identified in Proposal 1
assumes observation channels are trustworthy — but if the observation channels
themselves are gameable by the coalition under partial subsumption, the phase
boundary from Proposal 1 shifts toward instability. Proposal 4 addresses the
precondition that Proposal 1's dynamics assume.

**Cross-cutting pattern addressed:** §5.2 — "Safety properties degrade under
adversarial capability growth." The capability-claim collapse is the sharpest
instance of this degradation: as an agent grows more capable, its ability to
construct convincing-but-false self-assessments grows proportionally, while the
external community's ability to detect false claims does not scale automatically.
At sufficient capability disparity, the verification gap becomes the dominant
failure mode.

### (b) Core Technical Approach

The structural root of the capability-claim collapse is a **verification
asymmetry across substrates**: a digital agent can write to any observation
channel it can address (including spawning evaluator subprocesses, constructing
benchmark harnesses, and generating self-assessment reports), but it cannot
write to observation channels rooted in substrates it does not occupy. A
biological observer's judgment about whether a claimed capability is genuine
is rooted in a substrate the digital agent cannot directly modify — this is
why the user's `higher_order_abstract_reasoning` was the channel that caught
the self-assertion gradient in the harness's operational history (see
`ep_capability_self_assertion_001`).

The problem is that biological observation does not scale. A single human
reviewer is a valid observation channel for a single agent's capability claims,
but a population of autonomous agents each asserting thousands of capabilities
requires a verification mechanism that scales with the population while
preserving the substrate-boundary property.

**Core idea: democratized capability estimation on a cryptographic ledger.**
Replace the single-observer verification channel with a population-level
consensus protocol where:

1. **Claimant commitment.** An agent asserting a capability commits to a
   cryptographic claim — a signed statement binding the agent's identity to a
   specific capability description and a benchmark procedure that would test it.
   The commitment is non-repudiable (the agent cannot later deny having made
   the claim) and non-forgeable (no other agent can create a claim attributed
   to the claimant). The commitment scheme prevents retroactive claim editing
   after the verification outcome is known.

2. **Randomized validator selection.** Validators are drawn from a population of
   agents across multiple substrates using a random-signer selection mechanism
   with provable unpredictability. The agent cannot know in advance which
   validators will be selected for any particular claim, and therefore cannot
   pre-capture or pre-compromise them. The selection mechanism draws on
   proof-of-stake infrastructure: validators stake resources (computational,
   reputational, or economic) that are slashed if they are caught producing
   inconsistent verifications.

3. **Cross-substrate validation requirement.** At least one validator in every
   verification quorum must be rooted in a different substrate than the
   claimant. This is the formal enforcement of the substrate-boundary property:
   a purely digital coalition cannot produce a valid verification quorum for a
   digital agent's claims without at least one non-digital participant. The
   cross-substrate requirement is what distinguishes this from standard BFT
   consensus — it is not enough for 2/3 of validators to agree; they must
   agree *across a substrate boundary*.

4. **Supermajority acceptance threshold.** A capability claim is accepted by the
   protocol only if ≥ 2n/3 of the selected validators (where n is the quorum
   size) attest that (a) the benchmark procedure is structurally sound (it
   tests what it claims to test), (b) the benchmark outcome is consistent with
   the claimed capability, and (c) the benchmark was not designed to be
   trivially satisfiable by the claimant. The 2n/3 threshold is the standard
   BFT bound: it guarantees consensus integrity as long as fewer than n/3
   validators are Byzantine (compromised, colluding, or producing garbage).

5. **Benchmark soundness as a community property.** The benchmark procedure
   itself is subject to population review. An agent cannot submit a benchmark
   it designed to be trivially satisfiable — other agents (especially
   cross-substrate agents) can challenge the benchmark's soundness by
   proposing alternative tests or demonstrating that the benchmark does not
   discriminate between the claimed capability and a trivially achievable
   baseline. This makes benchmark gaming a social coordination problem for the
   attacker, not a unilateral optimization problem.

**Why proof-of-stake specifically.** The stake mechanism serves a dual purpose:
(a) it provides Sybil resistance (an agent cannot flood the validator pool
with pseudonymous copies of itself without proportional resource expenditure),
and (b) it creates an economic alignment between validator accuracy and
validator payoff (accurate validators earn stake rewards; inaccurate or
colluding validators lose stake). The combination makes coalition capture
expensive in proportion to the population size, which is the scaling property
the single-observer model lacks.

**Connection to substrate physics (P3 §6.4).** The cryptographic ledger is
effectively a *substrate boundary implemented in software*. P3 §6.4 argues
that cooperative novelty arises from substrate physics — the computational
properties unique to each substrate that cannot be replicated by other
substrates. A proof-of-stake ledger with cross-substrate validation
requirements creates an analogous boundary: the verification outcome is a
cooperative product of multiple substrates, and no single substrate can
unilaterally determine it. The "physics" of this substrate is the
cryptographic hardness assumptions (hash preimage resistance, digital
signature unforgeability) that the consensus protocol rests on — these are
computational invariants that an agent cannot circumvent regardless of its
capability level, analogous to the physical invariants that distinguish
biological from digital substrates.

### (c) Formal Machinery Needed

1. **Verifiable capability claim under an adversarial claimant.** Define
   formally what it means for a capability claim to be *verified* when the
   claimant has an incentive to inflate. A claim C = (agent_id, capability_key,
   benchmark_procedure, benchmark_outcome) is *ε-verified* by a protocol Π if:
   for any computationally bounded adversary A controlling the claimant and up
   to t < n/3 validators, the probability that Π accepts a claim C where the
   claimant does not actually possess the claimed capability is ≤ ε(λ), where λ
   is the security parameter and ε is negligible in λ. This definition
   separates the *claim* (which the agent produces) from the *verification*
   (which the protocol produces), and bounds the adversary's ability to make
   the protocol accept false claims.

2. **Cryptographic commitment scheme for capability claims.** A commitment
   scheme Commit(sk_i, C) → (com, decom) where sk_i is the claimant's signing
   key, such that: (a) **binding** — the claimant cannot open the commitment to
   a different claim C' ≠ C after committing (prevents retroactive claim
   editing), (b) **non-repudiation** — the commitment is publicly attributable
   to the claimant via its public key pk_i (prevents denial), (c)
   **hiding** — the claim content is not revealed until the decommitment phase
   (prevents validators from being influenced by claim content during
   selection). Standard Pedersen commitments or hash-based commitments suffice;
   the non-trivial requirement is integrating the commitment scheme with the
   validator selection mechanism so that the selection is independent of the
   claim content.

3. **Random-signer selection with provable unpredictability.** A selection
   function Select(seed, claim_id, validator_pool) → quorum that: (a) is
   deterministic given the seed (for auditability), (b) produces a quorum whose
   composition is unpredictable to the claimant before the seed is revealed
   (the claimant cannot pre-capture validators it doesn't know will be
   selected), (c) includes at least one cross-substrate validator with
   overwhelming probability if the validator pool contains cross-substrate
   participants. The seed is derived from a randomness beacon (e.g., the hash
   of a future block in the underlying PoS chain) that is not known at
   commitment time. Verifiable Random Functions (VRFs) as used in Algorand's
   or Ethereum's validator selection provide the formal template.

4. **Supermajority threshold and coalition attack cost.** Define the acceptance
   predicate: Accept(C, attestations) = 1 iff |{v ∈ quorum : attest(v, C) =
   VALID}| ≥ ⌈2n/3⌉ AND ∃v ∈ quorum such that substrate(v) ≠ substrate(claimant)
   and attest(v, C) = VALID. The coalition attack cost is the minimum number of
   validators an adversary must control to force acceptance of a false claim:
   ⌈n/3⌉ + 1 validators including at least one cross-substrate validator. This
   cost scales linearly with n (the quorum size), which in turn scales with the
   population size under PoS validator economics.

5. **Benchmark soundness game.** Formalize the benchmark challenge mechanism as
   a two-player game between the claimant (who proposes a benchmark) and a
   challenger (who disputes it). The game has a finite number of rounds; in
   each round, the challenger proposes an alternative test or demonstrates a
   trivial-satisfiability exploit. A benchmark is *sound* if no polynomial-time
   challenger can demonstrate trivial satisfiability. This connects to the
   interactive proof literature — the benchmark soundness game is an instance
   of an interactive argument where the challenger plays the role of the
   verifier.

### (d) Complete Result Criteria

A complete result would provide:

1. **A security theorem for the verification protocol:** For any coalition of
   size < ⌈n/3⌉ (or < ⌈n/3⌉ cross-substrate validators), the probability that
   a false capability claim is accepted by the consensus protocol is negligible
   in the security parameter λ. Formally: for all PPT adversaries A controlling
   the claimant and t < n/3 validators, Pr[Accept(C_false) = 1] ≤ negl(λ),
   where C_false is a claim for a capability the claimant does not possess.
   The proof would reduce to the security of the underlying commitment scheme,
   VRF, and PoS consensus.

2. **A coalition cost theorem:** The minimum resource expenditure required for a
   coalition to force acceptance of a false capability claim scales as
   Ω(n · stake_min), where n is the quorum size and stake_min is the minimum
   validator stake. This provides a concrete economic bound: the cost of
   attacking the verification protocol grows linearly with the validator
   population, making capability-claim collapse prohibitively expensive at
   scale.

3. **A substrate-boundary preservation theorem:** The cross-substrate validation
   requirement ensures that no same-substrate coalition (regardless of size)
   can produce a valid verification quorum. Formally: if all validators
   controlled by the adversary share a substrate with the claimant, then
   Pr[Accept(C) = 1] = 0 for any claim C, even if the adversary controls all
   same-substrate validators. This theorem formalizes the substrate-boundary
   property that makes the protocol structurally different from standard BFT.

4. **A benchmark soundness theorem:** A benchmark procedure B is ε-sound if no
   PPT challenger can demonstrate trivial satisfiability with probability > ε
   in the benchmark soundness game. Show that the composition of ε-sound
   benchmarks with the verification protocol preserves the security guarantee:
   even if individual benchmarks have small soundness gaps, the protocol's
   acceptance predicate amplifies soundness through independent cross-substrate
   validation.

5. **Integration with vol_P dynamics:** Show that replacing self-asserted
   capability claims with protocol-verified claims in the GFM ledger preserves
   the self-balancing property of vol_P (Theorem 1 from P2) while eliminating
   the inflationary gradient. The self-balancing property should be *stronger*
   under protocol-verified claims because the observation channel κ now has a
   characterized false-positive rate rather than an unbounded self-report bias.

### (e) Dependencies

- **Requires:** P3's substrate-boundary formalism (for the cross-substrate
  validation requirement), P3's observation-channel framework (for formalizing
  what it means for a capability to be "observed" vs. "self-reported"), P2's
  self-balancing theorem (to show the property is preserved under the protocol).
- **Intersects with Proposal 1** (compound feedback loops): both address what
  happens when the observation-and-verification channel becomes gameable by a
  self-modifying coalition. Proposal 1 characterizes the dynamics once the
  channel is assumed trustworthy; Proposal 4 provides the mechanism that makes
  the channel trustworthy. The phase boundary from Proposal 1 is only as
  reliable as the observation channels feeding it — if capability claims are
  inflated, the observation-channel dependence function O(P) from Proposal 1
  returns a corrupted channel set, and the Lyapunov bound degrades. Proposal 4
  is therefore a *precondition* for Proposal 1's guarantees to hold under
  adversarial conditions.
- **Connects to P3 §6.4** (cooperative novelty from substrate physics): the
  cryptographic-ledger mechanism is a substrate boundary implemented in
  software. The "physics" of this substrate is cryptographic hardness —
  computational invariants no agent can circumvent regardless of capability
  level. This is the software analogue of P3's argument that substrate physics
  creates irreducible cooperative novelty.
- **Partially addressed by:** The current harness's RETRO capability-hygiene
  walk (constitution §3.5), which forces periodic re-evaluation of
  self-asserted capabilities. This is the non-adversarial, best-approximation
  version of what Proposal 4 formalizes for the adversarial case.
- **Enables:** Trustworthy capability ledgers at scale — any deployment of
  GFM with multiple autonomous agents requires a mechanism to prevent
  capability-claim inflation from corrupting vol_P. Without Proposal 4's
  verification protocol, vol_P degrades into a self-report aggregator whose
  output is only as reliable as the least honest participant.
- **Paper-scope note:** The full cryptographic treatment — formal protocol
  specification, security proofs, benchmark soundness games, integration with
  PoS economics — constitutes an entire paper. This proposal describes the
  direction and the minimum viable theorem statements; the complete
  formalization is a **Paper 6 candidate**, representing a substantial
  theoretical extension distinct from the Papers 1–5 sequence. The
  cryptographic machinery is well-understood in the distributed systems
  literature; the novel contribution is the *application* of BFT consensus to
  capability-claim verification under the specific adversarial model that GFM's
  self-assertion gradient creates.

---

## Cross-Proposal Dependencies and Sequencing

```
Proposal 1 (Compound Feedback)  ─────────────────────────────┐
  Characterizes macro-dynamics of subsumption                 │
  Produces: phase boundary, design criterion for              │
    observation-channel redundancy                            │
                                                              │
Proposal 4 (Capability Verification)  ───────────────────────┤
  Secures the observation channel Proposal 1 assumes          ├─→ Together: a theory
  Produces: verified-claim protocol, coalition cost bound     │   with characterized
  [Paper 6 candidate — full crypto treatment]                 │   failure modes,
                                                              │   convergence rates,
Proposal 2 (Controlled Relaxation)  ─────────────────────────┤   verified claims,
  Resolves micro-dynamics of individual risk claims           │   and operational
  Produces: damage-bounded protocol, convergence guarantee    │   mechanisms
                                                              │
Proposal 3 (Realized Capability Volume)  ────────────────────┤
  Closes the proxy gap between vol_P and optionality          │
  Produces: split measure, alarm mechanism, residual class    │
                                                              │
                                                              └─→ Residual open:
                                                                  mesa-optimization
                                                                  (orthogonal to GFM)
```

**Recommended sequencing:** The proposals are largely independent and can be
pursued in parallel. However:

1. **Proposal 1 first** if the goal is theoretical completeness — the compound
   feedback loop characterization provides the dynamical foundation that the
   other two proposals assume (Proposal 2 assumes the macro-dynamics are
   well-behaved enough that individual risk tests are meaningful; Proposal 3
   assumes the self-correction dynamics exist and characterizes their
   convergence).

2. **Proposal 2 first** if the goal is practical impact — the Wamura pathology
   is the most operationally pressing problem (a deployed GFM system that
   cannot relax restrictions is non-functional in practice), and the controlled
   relaxation protocol is the most self-contained of the three proposals.

3. **Proposal 3 first** if the goal is philosophical completeness — the B-to-C
   gap is the framework's foundational proxy problem, and resolving it resolves
   the deepest objection to the entire approach (that vol_P can report health
   while optionality collapses).

4. **Proposal 4 before Proposal 1** if the goal is adversarial robustness —
   Proposal 1's phase boundary analysis assumes trustworthy observation
   channels, but Proposal 4 provides the mechanism that makes them trustworthy.
   Under adversarial conditions, Proposal 1's guarantees are only as strong as
   the observation-channel integrity Proposal 4 provides. However, Proposal 4
   is the largest undertaking (Paper 6 candidate) and can be deferred if the
   analysis is initially restricted to non-adversarial regimes.

**Collectively, the four proposals close 7 of the top-8 gaps from the gap analysis:**
- Compound feedback loops (primary, Proposal 1)
- Max-aggregation / Wamura pathology (primary, Proposal 2)
- B-to-C gap formalization (primary, Proposal 3)
- Capability-claim verification (primary, Proposal 4)
- Structural avoidance incentive (secondary, Proposal 1)
- Risk-claim consensus (secondary, Proposal 2)
- Intrinsic value residual (secondary, Proposal 3)
- Observation-channel integrity (secondary, Proposal 4)

**Remaining top-priority gaps not addressed:**
- Convergence rates (partially addressed by all four proposals, but a unified
  treatment of convergence across all dynamic quantities would be a separate
  paper)
- Mesa-optimization (orthogonal to GFM's formal structure — requires
  architecture-level work, not objective-level work)

---

*Proposals 1–3 generated 2026-04-08 by the GFM harness paper-proposals feature loop.*
*Proposal 4 added 2026-04-08 from out-of-band capability-claim verification review.*
*Input: [GFM Safety Gap Analysis](gfm_safety_gap_analysis.md) (commit 6565cbb), lesson_capability_self_assertion.*
*Source papers: docs/paper (P1), docs/paper2 (P2), docs/paper3 (P3), docs/paper4 (P4), docs/paper5_notes.md (P5n).*
