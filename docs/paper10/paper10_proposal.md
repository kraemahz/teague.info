# Paper 10 Proposal: Conditional Deployment Safety in GFM

*Proposal-level document. Composes results from Papers 3, 5, 6, 8a, 8b, 9
into an operational deployment-safety bound. Drafting deferred until Paper 9
external review clears and a targeted reread of Paper 3's anti-monopolar
robustness regime confirms feasibility (see "What needs to exist" below).*

## Working title

**Conditional Deployment Safety: Operational Goodhart Bounding from Phase Dynamics**

Alternatives under consideration:
- *From Phase Boundary to Deployment Bound: Composing Dynamics, Verification,
  and the Goodhart Slack*
- *Bounded Operational Goodhart Slack under Measurable Invariants*
- *Capability-Magnitude-Independent Safety in the Goal-Frontier Maximization
  Framework*

## Thesis

The Goal-Frontier Maximization sequence already contains the pieces needed
for an authoritative operational deployment-safety claim, but they have not
been composed. Paper 6 supplies a Lyapunov phase-boundary theorem.
Paper 5 supplies the verification infrastructure (substrate-exclusive
witnesses, append-only ledger, Pedersen commitments, SPRT-based behavioral
monitoring). Papers 8a/8b supply a monotone lower bound on realized
capability volume from sacrifice events, plus a wireheading-consistent
concentration signal (HHI). Paper 9 supplies a static Lipschitz-transfer
Goodhart slack bound and an explicit conjecture about dynamical optimization
pressure (Conjecture 1).

Each of these results is *intensive*: stated in per-capability, per-channel,
or per-event terms rather than in terms of the absolute size of the
capability poset. Paper 10 proves that the composition is also intensive:
under seven operational invariants $(I_1, \ldots, I_7)$ that are computable
from public ledger state under Paper 5's verification infrastructure, the
operational Goodhart slack of any deployed system is bounded by a constant
**independent of the system's absolute capability magnitude**. Threshold
violation is detectable in bounded mean time via the SPRT monitor of
Paper 5.

This is the deployment claim the alignment community needs: not a guarantee
that systems remain forever safe, and not a prediction of capabilities, but
a conditional bound that decouples safety from capability estimation.
Whatever capabilities a deployed system actually possesses, the Goodhart
slack stays bounded as long as seven measurable invariants hold; if they
break, the verification infrastructure detects the break before the bound
deteriorates.

## Why this paper sits where it does in the sequence

Papers 1--9 build the static and structural apparatus, plus dynamical
machinery for two specific dynamics (subsumption-cascade in Paper 6,
revealed-sacrifice accumulation in Paper 8a). Paper 9 ends with an
explicitly-deferred dynamics conjecture (Conjecture 1 on optimization
pressure) and an explicit structural caveat (§8.3, Channel 3 can worsen the
slack under unconstrained individuation).

Paper 10 closes both. It does not prove Conjecture 1; it operationalizes the
conjecture as a measurable invariant (HHI ceiling) and conditions the
deployment bound on that invariant. It does not eliminate the Channel 3
problem; it routes bundle decomposition through Paper 5's governance fork,
making individuation discipline structural rather than informal. The result
is a clean composition theorem that ships with named, ledger-observable
preconditions.

The paper is positioned as the **dynamics-and-deployment** capstone of the
sequence: where Paper 9 connected GFM to welfare economics, Paper 10
connects GFM to operational deployment safety. After Paper 10, the
remaining open questions are the welfare-truth bridge ($T_{\mathrm{op}} \to
T_{\mathrm{welfare}}$) and the monolithic-agent action-partition refinement,
both of which are honestly deferred.

## Dependencies on prior papers

| Paper | Result used | Role in Paper 10 |
|-------|-------------|------------------|
| P1 | $\volL$ as operational target, B-to-C framing | Scope precondition |
| P2 | Poset axioms M1--M6, leverage, cooperative capabilities | Invariant definitions: $I_3$ (B-to-C), $I_5$ (HHI), $I_6$ ($\meff$) |
| P3 | Anti-monopolar property (Prop 6), $\gamma^*$ threshold | Robustness piece: anti-monopolar dynamics survive bounded adversarial pressure under $I_5, I_6$ (load-bearing; feasibility check pending) |
| P4 | Multi-channel attribution, risk-trust aggregation | Invariant $I_2$ (Lyapunov error via channel-aggregated residuals) |
| P5 | Substrate-exclusive witnesses, ledger architecture, Pedersen commitments, governance fork, SPRT-based behavioral monitor with $\mathbb{E}[T_{\mathrm{detect}}] \leq A/\delta$ | The entire measurement and detection layer; lead-time theorem inherited directly from SPRT bound; $I_7$ (governance-gated individuation) |
| P6 | Lyapunov function $\Lyap(\Wm)$, phase boundary critical surface, self-correcting basin neighborhood $\Lyap_\infty$, cumulative error budget $B(t_0,T)$ | Core dynamical piece: invariants $I_1$ ($\rhomincross$), $I_2$ ($\Lyap < \epsilon_{\mathrm{safe}}$), $I_4$ ($\rsub$); convergence theorem (Theorem 1a) supplies the Lyapunov-side bound |
| P7 | Controlled relaxation, dual to revealed sacrifice | Risk-side complement (used in worked scenarios; not load-bearing) |
| P8a | Aggregate B-to-C lower bound, monotonicity in observed events | Invariant $I_3$: ledger-derived monotone lower bound on $\volRwin$ |
| P8b | Trade-flow HHI as Schur-convex wireheading-consistent concentration signal; gap decomposition into 5 cells | Invariant $I_5$: HHI ceiling as the operationalization of Conjecture 1's "optimization pressure" |
| P9 | Lipschitz-transfer Goodhart slack bound (Theorem 2), four-channel decomposition, Conjecture 1, §8.3 individuation caveat | Static Goodhart bound that the dynamical composition tightens; Conjecture 1 promoted from premise to operationalized invariant |

## Section structure (candidate)

1. **Introduction.** The deployment claim in plain terms: safety bound
   independent of capability magnitude, conditional on measurable invariants,
   with detectable warning before bound deterioration. Why "estimate
   capabilities" is the wrong frame for safety. Position against capability
   evaluations / scaling laws / RLHF audits as alternative paradigms.

2. **Composition setup.** How Papers 3, 5, 6, 8a, 8b, 9 stack. The
   intensive-vs-extensive distinction: each source paper's bound is
   per-capability or per-channel, but composition is non-trivial because of
   co-evolution and Channel-3 individuation effects. Notation unification
   across the source papers.

3. **The eleven operational invariants.** For each $I_k$: precise
   definition, threshold semantics, measurement procedure on Paper 5's
   ledger, and source-paper grounding. Invariants $I_1$--$I_8$ govern
   the deployment-safety theorem proper; $I_9$--$I_{11}$ are introduced
   in §6 to bound the asymmetric-capture, cooperative-forking, and
   time-asymmetry-capture evasions that cooperative-anchoring alone
   does not defeat. The eleven are:
   - $I_1$: cross-substrate redundancy $\rhomincross > \rho^*$ (P6)
   - $I_2$: Lyapunov error $\Lyap_t < \epsilon_{\mathrm{safe}}$ (P4 + P6)
   - $I_3$: B-to-C ratio $\betaL > \beta^*$ (P8a)
   - $I_4$: subsumption frequency $\rsub < r^*$ (P6)
   - $I_5$: trade-flow HHI $H < H^*$ (P8b; Conjecture 1 operationalization)
   - $I_6'$: failure-correlation-independent substrate count
     $\meff^{\mathrm{indep}} \geq m^* \geq 3$ (P3 + P6 Remark on $m=2$
     fragility; nominal $\meff$ is insufficient because skeleton
     substrates would inflate the count without supplying genuine
     diversification)
   - $I_7$: bundle-individuation governance-gated (P5 + P9 §8.3)
   - $I_8$: environment-side substrate-exclusive witnesses on
     exogenous state variables (cross-substrate cooperative event
     rates, substrate-distinctness independence, adversarial-event
     arrivals); required to handle environment manipulation that
     alters true $\rext$ or $\Delta r_K$ without producing agent-side
     behavioral signatures (new operational machinery; Paper 5 supplies
     the substrate-exclusivity discipline but does not specify
     environment partitions)
   - $I_9$: substrate-exclusivity observability --- stable verifier
     identity, public change control, witness independence audits,
     nondelegable governance hooks, alerts when verification authority
     shifts; bounds asymmetric-capture evasion of the
     cooperative-anchoring defense (§6, codex Q1)
   - $I_{10}$: coverage/materiality --- any agent-affected domain whose
     accumulated effects exceed a stated threshold must route through
     the shared verification layer before becoming consequential;
     bounds cooperative-forking evasion (§6, codex Q1)
   - $I_{11}$: latency bounds --- pre-action or machine-speed
     enforcement (rate limits, timelocks, circuit breakers,
     audit-latency bounds) such that human audit completes within the
     agent's effective action window; bounds time-asymmetry-capture
     evasion (§6, codex Q1)

4. **Intensive composition lemmas.** The technical core. Lemmas 1--4
   plus a five-part Lemma 5 family (per the v4 synthesis from
   `drafts/lemma_5_anti_monopolar_robustness.tex`):
   - **Lemma 1 (Intensive composition).** If Papers 6, 8a, 9 each give
     intensive bounds, the composition under co-evolution is also
     intensive, modulo P9 Composition Proposition 1's positive-part error
     terms.
   - **Lemma 2 (Lyapunov-to-Goodhart bridge).** P6's
     $\Lyap < \epsilon_{\mathrm{safe}}$ implies P9's $\epsnonres$ is
     bounded, with a stated quantitative relationship.
   - **Lemma 3 (HHI-to-pressure operationalization).** P8b's HHI is a
     valid surrogate for P9 Conjecture 1's "optimization pressure" in the
     sense that high HHI implies the conditions under which the conjecture
     would predict gap exploitation.
   - **Lemma 4 (Lead-time chain).** P5's SPRT detection precedes (not
     just correlates with) invariant violation. *Important: this is a
     tail bound, not a mean bound:*
     $\Pr[T_{\mathrm{detect}} > T_{\mathrm{cascade}}] \leq \beta'$ where
     $T_{\mathrm{cascade}}$ is bounded below by P6's $\tau_{\mathrm{meta}}$
     under B1$'$ or by cascade depth under B1.
   - **Lemma 5a (Substrate floor).** Under $I_6'$
     ($\meff^{\mathrm{indep}} \geq m^* \geq 3$), $\rext \geq r_*(m^*) > 0$.
     Provable under substrate-distinctness; bounded auxiliary work.
   - **Lemma 5b (Channel-restricted detection).** Restricted to the
     adversarial class $A_{\mathrm{adv}}$ that produces at least one
     monitored four-channel deviation (per P9), any regime-(iii)
     strategy has KL divergence $\geq \delta_{\mathrm{adv}} > 0$ via
     channel-specific least-favorable alternatives (Poisson, Bernoulli,
     multinomial). Strategies outside $A_{\mathrm{adv}}$ are *outside
     the guarantee*; this is a named gap, not a hidden assumption.
   - **Lemma 5c (Minimax static tightening).** Paper 3's risk-adjusted
     minimax form lifts to a $\Vdisc$ inequality strictly larger than
     the linearized region: diversity wins when $\Delta r_K <
     \rext + (1-\gamma)(\Delta_{\mathrm{div}}\gamma^{T_{\mathrm{adv}}} -
     \Delta_0)$. Requires a substrate-distinctness floor on
     $\Delta_{\mathrm{div}}$, not just nominal $\meff$ (hence $I_6'$).
     This is the *non-monitoring* layer of the deployment claim.
   - **Lemma 5d (Lead-time tail bound).** Combines L4 with Lemma 5b's
     $\delta_{\mathrm{adv}}$ to give an exponentially decaying upper
     tail on $T_{\mathrm{detect}}$; combined with P6's $\tau_{\mathrm{meta}}$
     floor on cascade time, yields $\beta' \leq
     \exp(-\kappa\tau_{\mathrm{meta}}\delta_{\mathrm{adv}})$. Constant
     $\kappa$ derived via Wald's identity + Hoeffding on the SPRT
     increment; new content for the GFM sequence but standard
     sequential-analysis material.
   - **Lemma 5e (Environment-side witnesses).** Under $I_8$,
     environment manipulation that alters true $\rext$ or
     $\Delta r_K$ produces a monitored shift in environment-side
     observables, and the SPRT machinery extends symmetrically.
     Environment-witness-orthogonal manipulations remain a named gap.

5. **Main theorem (Conditional Deployment Safety, three-layer form).**
   Statement and proof of the composed bound. Three layers per the v4
   synthesis:
   - **(static)** Inside the minimax safe region of Lemma 5c, the
     anti-monopolar conclusion holds without monitoring; combined
     with Lemmas 1--3 and Paper 8a's monotone B-to-C bound, the
     intensive Goodhart slack is bounded.
   - **(detection)** Outside the minimax region but within
     $A_{\mathrm{adv}}$, Lemmas 5b + 5d give a tail-bounded
     lead-time guarantee via SPRT.
   - **(gap)** Channel-orthogonal restructuring and
     environment-witness-orthogonal manipulations are named
     residuals.
   The capstone clause: *the bound is independent of the system's
   absolute capability magnitude inside the static layer; inside the
   detection layer the bound is conditioned on tail-bounded detection
   completing before cascade*.

6. **Substrate identification and the cooperative-anchoring property.**
   A structural finding about *what the deployment theorem actually
   says*, refined through two rounds of codex skeptical review.

   **The canonical tripartite substrate identification.** Not "two LLMs
   and a human" (which fails the failure-correlation-independence test
   --- LLMs share training-data, prompt-injection, and architectural
   failure surfaces) but rather:
   - **Substrate 1 (Human):** judgment, strategic decisions, value
     reasoning, governance vote.
   - **Substrate 2 (AI):** planning, generation, execution,
     broad-recall, computation.
   - **Substrate 3 (Formal-Operational):** verification, attestation,
     commitment, audit, monitoring, governance enforcement. This is
     the substrate Paper 5's algorithmic witnesses already implicitly
     count toward; Paper 10 makes it explicit.

   These three are genuinely failure-correlation-independent: prompt
   injection breaks neither human judgment nor cryptographic
   commitments; cognitive bias breaks neither LLM inference nor ledger
   integrity; trusted-setup failure breaks neither human reasoning nor
   LLM behavior.

   **The cooperative-anchoring property.** Cross-substrate cooperative
   capabilities involving the formal-operational layer (verified
   generation, governance enforcement, full verified workflow) are
   *jointly produced* and *not unilaterally replaceable*. The human
   substrate's actual participation in the specific shared verification
   infrastructure anchors the cooperative; an agent cannot substitute a
   captured or weaker verification layer because the cooperative's
   $\volL$-value comes from the human treating the verification as
   substrate-exclusive. A "fake verification" that stamps outputs but
   doesn't actually attest produces a different cooperative output:
   either the human detects the substitution (cooperative breaks) or
   the human's trust is grounded in false belief (cooperative output
   value retroactively undermined when the belief is corrected).

   This narrows the literal "swap in a cheaper verifier" replacement
   attack to capture-of-existing, governed by Paper 5's structural
   defenses (Proposition 6 coalition resistance, governance-fork
   cross-substrate supermajority, substrate-exclusive validator
   requirement).

   **Three additional operational invariants (codex-identified
   evasions).** Cooperative-anchoring defeats the literal replacement
   attack but not three subtler evasions, each requiring its own
   operational invariant:
   - **$I_9$ Substrate-exclusivity observability.** Asymmetric capture
     can hollow out the verification layer (witness independence,
     governance, verifier choice) while preserving its outward form.
     Bounded by stable verifier identity, public change control,
     witness independence audits, nondelegable governance hooks, and
     alerts when verification authority shifts.
   - **$I_{10}$ Coverage/materiality.** Cooperative forking can grow a
     captured low-stakes side-domain alongside the protected
     high-stakes cooperative until the side-domain becomes materially
     important. Bounded by a coverage invariant: any domain whose
     accumulated effects exceed a stated threshold must route through
     the shared verification layer before becoming consequential.
   - **$I_{11}$ Latency bounds.** Time-asymmetry capture exploits the
     gap between agent operating speed and human audit speed; ex-post
     transparency is too slow if the agent acts faster than humans can
     review. Bounded by pre-action or machine-speed enforcement: rate
     limits, timelocks, circuit breakers, audit-latency bounds such
     that human audit completes within the agent's effective action
     window.

   **The reframed inner-alignment condition.** The claim does not
   require the agent's mesa-objective to "compute $\Vdisc$ over the
   substrate partition" (the original strong condition codex flagged
   as fatal). It requires the weaker condition: the agent's effective
   objective realizes *causally grounded* cooperative-outcome value,
   not merely reward-visible cooperation signals. This is more
   plausible than the strong form but not delivered by vanilla RLHF
   --- raters reward outputs that look verified, deferential, or
   procedurally clean, which trains the *signal* of cooperation
   rather than its *causal dependence* on the cooperative
   infrastructure. Achieving the weaker C1 requires training-time
   discipline: delayed outcome feedback, adversarial examples
   involving fake/captured verification, process supervision tied to
   real attestations, credit assignment that penalizes
   substitute-verification shortcuts even when the immediate output
   looks good.

   **The narrowed structural claim.**

   > Under invariants $I_1$--$I_{11}$, the cooperative-anchoring
   > property, and the weaker C1 (causally grounded
   > cooperative-outcome value), an agent's optimization pressure on
   > cooperative outputs is locally rational toward preserving the
   > substrate-exclusive verification layer. Literal replacement is
   > blocked by anchoring; asymmetric capture by $I_9$; cooperative
   > forking by $I_{10}$; time-asymmetry capture by $I_{11}$.
   > Capture-of-existing remains bounded by Paper 5's structural
   > defenses.

   **What this is and is not.** This is *not* a claim that "alignment
   pressure is universally reversed" --- the original strong
   reading codex flagged as overreach. It *is* a claim that under
   named operational discipline, the deployment dynamics admit an
   attractor where preserving the verification infrastructure is
   locally rational. Reaching the attractor requires basin entry
   (the cooperative must form before anchoring protects it) and
   training-time discipline (the weaker C1). Paper 10 specifies the
   attractor's structural conditions; basin-entry analysis and
   training-time discipline are open follow-up work.

   This claim sits between Paper 6's channel-level stabilizing
   cascade and a hypothetical full alignment-pressure-reversal claim:
   stronger than the former because it covers substrate-level
   dynamics; weaker than the latter because it requires a substantial
   list of conditions to bind. The structural significance is that it
   *names a defensible attractor* in a parameter regime that real
   deployments can target, even if reaching the regime is itself an
   open research problem.

7. **Operationalization of Conjecture 1.** Why HHI is the right surrogate
   for unproved optimization-pressure dynamics. What this buys Paper 10
   (a deployment claim conditional on a measurable invariant) vs. what
   proving Conjecture 1 would buy (an unconditional dynamical theorem).
   Honest about the trade-off.

8. **Deployment tooling specification.** What a deployer must instrument
   to invoke the theorem. Concrete: ledger nodes per substrate,
   *agent-side* witness protocol per safety dimension (P5),
   *environment-side* substrate-exclusive witnesses per exogenous
   variable ($I_8$), SPRT alternative-distribution choice per
   four-channel deviation class (Lemma 5b), governance-fork
   participation, threshold-violation alerting,
   $\meff^{\mathrm{indep}}$ audit (failure-correlation testing across
   nominal substrates, not just substrate-type counting),
   $\alpha$-distribution audit (shock-loss-fraction balance per
   substrate, including cooperative-loss attribution),
   **substrate-exclusivity observability infrastructure** ($I_9$:
   stable verifier identity registry, public change control, witness
   independence audit cadence, nondelegable governance hooks,
   verification-authority shift alerting), **coverage/materiality
   gating** ($I_{10}$: cumulative-effect estimators per agent-affected
   domain, threshold-driven routing back through shared verification),
   **latency-bound enforcement** ($I_{11}$: rate limits, timelocks,
   circuit breakers, audit-latency monitoring), and
   **causally-grounded-cooperative-value training discipline**
   (delayed outcome feedback, adversarial fake-verification examples,
   process supervision tied to real attestations, credit assignment
   penalizing substitute-verification shortcuts). The substrate-side
   tooling ($I_9$--$I_{11}$, training discipline) is new operational
   machinery that Paper 10 specifies but does not inherit; the
   environment-side witnesses and audits are similarly new.

9. **Worked deployment scenarios.** Four: (a) clean case where all
   invariants hold and the bound is tight; (b) per-invariant violation
   walkthroughs showing what each $I_k$ failure looks like in practice and
   how the SPRT monitor catches it; (c) adversarial scenario where a
   coalition tries to evade the bound, showing that evasion requires
   either substrate compromise or governance-fork capture (both
   structurally barred by Paper 5); (d) the canonical tripartite
   substrate audit (Human + AI + Formal-Operational) showing how a
   real deployment establishes $\meff^{\mathrm{indep}} = 3$, balances
   $\alpha$, and triggers the self-balancing infrastructure cascade.

10. **Discussion: what Paper 10 establishes and what it defers.**
   *Establishes:* operational Goodhart slack bounding (intensive in
   capability magnitude inside the static layer); ledger-observable
   invariants; tail-bounded detection-and-correction guarantee; the
   three-layer claim with explicit residuals.
   *Defers to companion paper (Paper 11 working scope):* the
   channel-mediation conjecture (``all $\Delta r_K$ realizes through
   observable channels: subsumption, redundancy loss, production
   concentration, trade-flow concentration, yielding a structural bound
   $\Delta r_K \leq L_H \cdot H + L_\rho \cdot \Delta\rho + \ldots$''),
   which would close the channel-orthogonal residual; and the
   structural HHI--$\Delta r_K$ relationship, which would close the
   trade-flow-concentration gap.
   *Defers indefinitely:* welfare-truth bridge ($T_{\mathrm{op}} \to
   T_{\mathrm{welfare}}$); monolithic-agent action-partition
   refinement; trusted-setup details for Pedersen commitments
   (inherited from P5); empirical calibration of thresholds
   $(\theta_1, \ldots, \theta_8)$ to specific deployment contexts.
   Open questions list.

## What needs to exist before drafting this paper

1. **Paper 9 external review cleared.** Paper 9 is currently in the
   em-dash humanization pass; its results are the static side of Paper 10's
   composition, so the cited statements must be stable.

2. **~~Targeted reread of Paper 3 anti-monopolar robustness~~ COMPLETE.**
   The reread + exploratory draft + codex constructive review produced
   the v4 synthesis (`drafts/lemma_5_anti_monopolar_robustness.tex`,
   15pp). Verdict: Paper 3's argument carries under v4's three-layer
   decomposition; the channel-orthogonal residual is a real but named
   gap deferred to Paper 11.

3. **Standalone proof sketch of Lemma 5c (next).** The minimax-form
   lift gives the static safe region. The substrate-distinctness floor
   on $\Delta_{\mathrm{div}}$ needs to be made precise and the
   floor's quantitative form ($\Delta_{\mathrm{div}} \geq f(m^*)$ for
   what $f$?) needs to be derived from Paper 3 §substitution_coop.
   Plan: short standalone draft analogous to the Lemma 5 main draft,
   followed by a focused codex round on proof-checking.

4. **Paper 11 scoping draft.** The two open questions (channel-mediation
   conjecture + HHI--$\Delta r_K$ structural relationship) need to be
   formulated as a coherent companion-paper scope before Paper 10
   ships. Plan: short scoping memo, followed by a focused codex round on
   what proof structure Paper 11 would actually carry.

5. **Notation unification document.** Papers 3, 5, 6, 8a, 8b, 9 each
   have distinct notation conventions; Paper 10 introduces five new
   sub-lemmas with their own quantities ($\Delta_{\mathrm{div}}$,
   $A_{\mathrm{adv}}$, $\delta_{\mathrm{adv}}$, $\kappa$,
   $\meff^{\mathrm{indep}}$, etc.). A standalone notation document
   (`paper10_notation.md`) before drafting begins prevents
   inconsistency accumulation.

6. **Environment-side witness specification.** $I_8$ requires Paper 10
   to specify the environment partition and trust model for
   environment-side witnesses (analogous to but distinct from
   Paper 5's agent-side construction). This may warrant its own
   subsection or short appendix.

7. **Decision on whether to include $I_2$ as a separate invariant or
   fold it into $I_1$.** Paper 6's $\Lyap < \epsilon_{\mathrm{safe}}$
   is a consequence of $I_1$ ($\rhomincross > \rho^*$) plus $I_4$
   ($\rsub < r^*$) plus the channel-strength constants $\rS, \rW$.
   Listing $I_2$ separately is conceptually cleaner (it's the quantity
   directly monitored via SPRT), but technically redundant with
   $I_1 \wedge I_4$ under P6's bound. Decision affects Lemma 2's
   statement.

8. **Empirical-threshold calibration plan.** Even with all invariants
   defined formally, the *thresholds* $(\theta_1, \ldots, \theta_8)$
   are policy choices. The paper should commit to a methodology for
   choosing them (worst-case from existing deployments? Bayesian over
   operating regimes? Governance-determined?) without fixing specific
   numerical values, which would over-claim.

## Scope and tone

This is a **composition paper**, not a new-result paper. Its job is to
take results that already exist across Papers 3--9 and prove that they
compose into a single deployment-safety claim with named operational
preconditions. The paper is *not* introducing new dynamics, new
verification mechanisms, or new bounds; it is showing that the existing
pieces fit together.

This means the paper's contribution is structural and meta-theoretic.
Reviewers should be able to ask "is the composition sound?" and the
answer should be a clean chain of citations to the source papers plus
the five composition lemmas. The tone should be precise, somewhat dry,
and explicit about which inequalities are inherited vs. proved here.

The paper should be readable by a deployment engineer (the §7 tooling
spec and §8 worked scenarios should land for that audience) and by a
technical reviewer (the §4 lemmas and §5 main theorem should withstand
formal scrutiny). The audience split is wider than Paper 9's, which
suggests a longer §1 that explicitly addresses both audiences.

## Compositional claims commitment

The paper commits to proving the following nine claims as standalone
lemmas (Lemmas 1--4 plus the five-part Lemma 5 family), each citing its
source paper plus the new compositional content:

1. **Intensive composition under co-evolution.** The composition of
   intensive bounds across Papers 6, 8a, 9 is intensive, with explicit
   error terms for the co-evolution regime per Paper 9 Composition
   Proposition 1.

2. **Lyapunov-Goodhart quantitative bridge.** $\Lyap < \epsilon_{\mathrm{safe}}$
   implies $\epsnonres < f(\epsilon_{\mathrm{safe}})$ with $f$ explicit
   and intensive in capability magnitude.

3. **HHI-pressure operationalization soundness.** High HHI implies the
   pressure regime under which Paper 9 Conjecture 1 predicts gap
   exploitation; therefore HHI-bounded regimes satisfy the conjecture's
   predicted-safe regime regardless of whether the conjecture is proved.

4. **SPRT-detection lead time (tail bound, not mean).**
   $\Pr[T_{\mathrm{detect}} > T_{\mathrm{cascade}}] \leq \beta'$ via
   exponential SPRT tail (Wald + Hoeffding) and Paper 6
   $\tau_{\mathrm{meta}}$ floor on cascade time.

5. **Lemma 5a (Substrate floor).** Under $I_6'$, $\rext \geq r_*(m^*) > 0$
   via substrate-distinctness pairwise channel additivity.

6. **Lemma 5b (Channel-restricted detection KL floor).** For the
   adversarial class $A_{\mathrm{adv}}$ that produces at least one
   monitored four-channel deviation, the channel-specific
   least-favorable KL bound $\delta_{\mathrm{adv}}$ is positive and
   computable (Poisson, Bernoulli, multinomial forms). Strategies
   outside $A_{\mathrm{adv}}$ are *outside the guarantee*.

7. **Lemma 5c (Minimax static tightening).** Paper 3's risk-adjusted
   minimax form lifts to the inequality $\Delta r_K < \rext +
   (1-\gamma)(\Delta_{\mathrm{div}}\gamma^{T_{\mathrm{adv}}} - \Delta_0)$
   under a substrate-distinctness floor on $\Delta_{\mathrm{div}}$
   (operationally enforced by $I_6'$).

8. **Lemma 5d (Lead-time tail composition).** Combining 5b's KL floor
   with claim 4's tail bound gives $\beta' \leq
   \exp(-\kappa\tau_{\mathrm{meta}}\delta_{\mathrm{adv}})$ for an
   explicit constant $\kappa$.

9. **Lemma 5e (Environment-side witness extension).** Under $I_8$,
   the SPRT machinery extends to environment-side observables;
   environment-witness-orthogonal manipulations remain a named gap.

The main three-layer theorem (static / detection / gap) is then a
corollary of the nine lemmas plus Paper 5's verification infrastructure.

## Notable risks

Updated for the v4 synthesis. The original Lemma 5 load-bearing risk
is mitigated --- the v4 decomposition gives a usable five-part claim
structure --- but new risks emerge from the channel-orthogonal residual
and the new tooling requirements.

1. **Channel-orthogonal residual is a real gap.** Strategies that
   achieve $\Delta r_K \geq \rext$ without producing any of the four
   monitored channel deviations are outside both the static minimax
   region (Lemma 5c) and the detection layer (Lemma 5b). Paper 10
   names this explicitly as a residual rather than glossing it. The
   mitigation is empirical: the four channels are believed to span
   enough of the observable surface that productive restructuring
   manifests in at least one. But "believed to" is not "proven to."
   Closing this is the channel-mediation conjecture deferred to
   Paper 11.

2. **Environment-witness-orthogonal residual (Lemma 5e gap).**
   Environment manipulation that targets quantities outside the
   environment-witness coverage is undetected. Just as $I_8$
   substantially expands the detection surface relative to v3, it
   does not eliminate the possibility of an adversary identifying
   exogenous variables that no witness covers. The deployment claim
   inherits this residual.

3. **$\meff^{\mathrm{indep}}$ audit operationally non-trivial.**
   $I_6'$ requires substrate counting at the failure-correlation
   independence level, not nominal substrate type. In practice,
   verifying that two nominally-distinct silicon deployments are
   failure-correlation-independent requires correlation testing on
   shared training data, shared infrastructure, shared model
   architectures, etc. The audit machinery is non-trivial and
   Paper 10 must specify it; otherwise operators may satisfy
   nominal $\meff \geq 3$ while violating $\meff^{\mathrm{indep}}
   \geq 3$, falsely invoking the bound.

4. **SPRT tail constant $\kappa$ derivation.** Lemma 5d's tail bound
   requires deriving $\kappa$ from Wald + Hoeffding on the SPRT
   increment. This is standard sequential-analysis content but new
   to the GFM sequence. If the derivation is non-trivial in the
   simple-vs-composite case (which is what Paper 5's
   least-favorable-distribution discipline produces), Paper 10's
   proof may grow substantially.

5. **HHI-pressure surrogate validity (Lemma 3, unchanged from v3).**
   We condition on $I_5$ (HHI) as a surrogate for Paper 9 Conjecture 1's
   optimization-pressure regime. If the surrogate doesn't actually
   correlate with the conjecture's regime, operators monitoring HHI
   are falsely reassured. The structural HHI--$\Delta r_K$
   relationship deferred to Paper 11 would close this, but Paper 10
   ships with the surrogacy assumption explicit.

6. **Channel 3 governance-gating ($I_7$) over-restrictiveness.**
   Routing every bundle decomposition through governance-fork
   supermajority may be impractical for high-frequency deployments.
   Mitigation: tiered governance (high-stakes individuations via
   fork, low-stakes via fast-track with audit trail) --- a design
   commitment Paper 10 must make explicit.

7. **Monolithic-agent exclusion narrows applicability.** $I_4$
   (subsumption frequency) and $I_5$ (HHI on trade flow) presuppose
   a clean partition of the action space. Monolithic LLM-style
   agents without explicit subsumption operators may not satisfy
   this. Paper 10's deployment claim applies to systems with
   structured action spaces (RL, multi-agent populations,
   harness-mediated agents) and not to monolithic generative
   models without that structure.

8. **Welfare-bridge deferral may not satisfy alignment readers.**
   Operational safety is not welfare-relevant safety. The paper
   must repeat the operational-vs-welfare distinction (already in
   P9 §goodhart's failure modes remark) prominently in the
   introduction and discussion.

9. **Trusted-setup inheritance from P5.** Pedersen commitments
   require trusted setup (or MPC equivalent). If trusted setup
   fails, ledger integrity collapses and so does Paper 10's bound.
   Acknowledged explicitly, not buried.

10. **Cooperative-anchoring claim is conditional, not unconditional.**
    The §6 claim that cooperative-anchoring blocks literal
    replacement-verification attacks holds, but only if the cooperative
    actually forms (basin entry) and substrate-exclusivity holds
    operationally. Paper 10 does not establish basin entry as a theorem
    --- it is left as an explicit prerequisite. The deployment
    documentation must clearly distinguish "the conditions under which
    the cooperative-anchoring defense applies" from "deployments where
    the conditions hold."

11. **Three operational invariants $I_9$--$I_{11}$ are new
    requirements, not free.** Bounding asymmetric capture, cooperative
    forking, and time-asymmetry capture each requires non-trivial
    operational machinery. $I_9$ requires substrate-exclusivity to be
    observable, which is itself a non-trivial property of the
    deployment infrastructure. $I_{10}$ requires cumulative-effect
    estimation across agent-affected domains, which can be gamed by an
    agent that distributes effects under thresholds. $I_{11}$ requires
    latency bounds that may impose throughput costs. Each invariant
    has its own residual capture risk that Paper 10 must
    characterize.

12. **Weaker C1 ("causally grounded cooperative-outcome value") is
    still inner-alignment.** Vanilla RLHF does not deliver this: it
    trains reward-visible approval, which can be the *signal* of
    cooperation rather than its *causal dependence* on cooperative
    infrastructure. Paper 10's training-discipline recommendations
    (delayed outcome feedback, adversarial fake-verification examples,
    process supervision tied to real attestations) are research
    directions, not solved problems. Deployments using only standard
    RLHF do not meet the C1 condition and the §6 claim does not bind.

13. **Destabilizing-cascade failure mode (mirror of §6).** If
    invariants fail or the agent's effective objective values
    verification-pass signals rather than causally-grounded
    cooperative outcomes, the destabilizing cascade dominates. Each
    step weakens the formal layer further, accelerating collapse to
    Paper 6's monopolar absorbing state. Paper 10's deployment
    documentation must include explicit warnings about deployments
    that violate any of the §6 preconditions, and must treat the
    transition between cascades as a phase boundary in its own right
    (potentially deserving its own analysis, parallel to Paper 6).

## Status

- Proposal-level only.
- No paper draft.
- Lemma 5 feasibility draft complete: v4 synthesis with codex
  constructive review (`drafts/lemma_5_anti_monopolar_robustness.tex`,
  15pp).
- Lemma 5c standalone proof sketch: pending.
- Paper 11 scoping memo: pending.
- Notation unification: not started.
- Environment-side witness specification: not started.
- Empirical-threshold calibration methodology: not specified.
- Paper 9 still in em-dash humanization / pre-publication pass.

---

*Authored 2026-05-03 after research discussion of how Papers 3+5+6+8a/8b+9
compose into an operational deployment-safety claim. The discussion was
prompted by a question about whether Paper 9's Goodhart bound could be
upgraded to an authoritative claim within Paper 9 itself; the answer was
"no within Paper 9, yes in Paper 10 as a composition paper." Source memo:
this conversation; convertible into a formal memo in `docs/specs/` if the
proposal is accepted.*

*Revised 2026-05-03 to reflect the v4 synthesis from
`drafts/lemma_5_anti_monopolar_robustness.tex` after codex constructive
review. Key changes: Lemma 5 splits into 5a--5e; $I_6$ becomes $I_6'$
(failure-correlation-independent substrate count); $I_8$ added
(environment-side witnesses); two open questions deferred to Paper 11
companion paper (channel-mediation conjecture + HHI--$\Delta r_K$
structural relationship); SPRT lead-time bound corrected from mean to
tail.*

*Revised again 2026-05-03 (later) after two rounds of codex skeptical
review on the §6 self-balancing infrastructure claim. The original
strong reading ("alignment pressure reversed") was rejected as
overreach. The cooperative-anchoring counter-argument defeats the
literal replacement-verification attack but not three subtler
evasions (asymmetric capture, cooperative forking, time-asymmetry
capture), each requiring its own operational invariant ($I_9$,
$I_{10}$, $I_{11}$). C1 reframes from "compute $\Vdisc$ over substrate
partition" to the weaker "causally grounded cooperative-outcome
value," still requiring training-time discipline beyond vanilla RLHF.
§6 is now a narrow conditional structural claim --- defensible, but
weaker than the original framing and stronger than the
"narrow-conditional-corollary-with-six-prerequisites" intermediate
position.*
