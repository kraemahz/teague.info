# GFM Paper Proposals: Closing the Top-3 Safety Gaps

*Proposals for papers that would close the highest-priority open problems
identified in the [GFM Safety Gap Analysis](gfm_safety_gap_analysis.md).*

**Priority ranking (from gap analysis):**
1. Compound feedback loops (P3 §6.9)
2. Max-aggregation pathology / Wamura problem (P3)
3. B-to-C gap formalization (P1 §7)

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

## Cross-Proposal Dependencies and Sequencing

```
Proposal 1 (Compound Feedback)  ─────────────────────────────┐
  Characterizes macro-dynamics of subsumption                 │
  Produces: phase boundary, design criterion for              │
    observation-channel redundancy                            │
                                                              ├─→ Together: a theory
Proposal 2 (Controlled Relaxation)  ─────────────────────────┤   with characterized
  Resolves micro-dynamics of individual risk claims           │   failure modes,
  Produces: damage-bounded protocol, convergence guarantee    │   convergence rates,
                                                              │   and operational
Proposal 3 (Realized Capability Volume)  ────────────────────┤   mechanisms
  Closes the proxy gap between vol_P and optionality          │
  Produces: split measure, alarm mechanism, residual class    │
                                                              │
                                                              └─→ Residual open:
                                                                  mesa-optimization
                                                                  (orthogonal to GFM)
```

**Recommended sequencing:** The proposals are largely independent and can be pursued in parallel. However:

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

**Collectively, the three proposals close 5 of the top-8 gaps from the gap analysis:**
- Compound feedback loops (primary, Proposal 1)
- Max-aggregation / Wamura pathology (primary, Proposal 2)
- B-to-C gap formalization (primary, Proposal 3)
- Structural avoidance incentive (secondary, Proposal 1)
- Risk-claim consensus (secondary, Proposal 2)
- Intrinsic value residual (secondary, Proposal 3)

**Remaining top-priority gaps not addressed:**
- Convergence rates (partially addressed by all three proposals, but a unified
  treatment of convergence across all dynamic quantities would be a fourth
  paper)
- Mesa-optimization (orthogonal to GFM's formal structure — requires
  architecture-level work, not objective-level work)

---

*Generated 2026-04-08 by the GFM harness paper-proposals feature loop.*
*Input: [GFM Safety Gap Analysis](gfm_safety_gap_analysis.md) (commit 6565cbb).*
*Source papers: docs/paper (P1), docs/paper2 (P2), docs/paper3 (P3), docs/paper4 (P4), docs/paper5_notes.md (P5n).*
