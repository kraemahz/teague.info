# GFM as Cryptoeconomic Alignment: A Reframing Memo

*This document captures a reasoning arc that emerged from attempts to resolve
the capability-stuffing problem in Paper 8. It is a design memo, not a paper:
it records how the authors came to view the GFM sequence as a cryptoeconomic
alignment architecture rather than a pure measurement framework, what that
reframing changes about the sequence's claims and positioning, and which
residual uncertainties remain open.*

**Status:** informal architectural reasoning, preserved for continuity with
in-flight papers. Not peer-reviewed; not a formal result. Specific technical
claims referenced here are developed (or left as open problems) in the
numbered papers.

**Date drafted:** 2026-04-17.

**Update (later same day):** Subsequent discussion sharpened the reframing.
The provenance-centric framing in §§3–7 is not wrong, but it is narrower than
the underlying mechanism. The unifying pathology is **structural avoidance**
(the dual of Paper 3's structural discovery value, acknowledged as an open
gap in Paper 2 Discussion). Provenance is one of three proof-burden types in
the taxonomy that resolves avoidance; the other two (non-mergeability, use)
are equally load-bearing. The cryptoeconomic cost counterweight is the
*condition that makes proof-burdens honest*, not the mechanism itself. §9
below documents this refinement; §§1–8 are preserved as the historical
reasoning arc.

**Prior art referenced:** `gfm_paper_proposals.md`, `gfm_safety_gap_analysis.md`,
Papers 1--8 of the sequence, Paper 9 outline, Paper 8 drafts under
`paper8/drafts/`.

---

## 1. How this document came about

Paper 8 (revealed-sacrifice observation) contains an Anti-Stuffing
proposition in §3.3 that claims the need-sufficiency architecture
structurally resists capability-stuffing. Codex review established that the
claim is semantic rather than structural: it relies on undefined phrases like
``same underlying optionality from different origins'' and does not survive
adversarial construction of capabilities with nominally distinct outputs.

Three drafts attempted to replace the semantic claim with a structural
theorem:

1. **v1 --- prevention via poset automorphism.**
   Define capability redundancy via output equality plus a non-trivial
   automorphism swapping two capabilities while fixing everything else.
   *Defeated by:* asymmetric decoration. An attacker adds a unique
   cooperative descendant or weight perturbation to each stuffed capability;
   no automorphism exists; rigidity condition passes; stuffing succeeds.

2. **v2 --- detection via persistent dormancy.**
   Define stuffed capabilities as those with $\volRlower(c, T) = 0$ across an
   observation horizon. *Defeated by:* bundle-appearance attack. An attacker
   trades through stuffed capabilities occasionally; under equal-weight
   $\alpha$, any single inclusion lifts the capability out of dormant into
   the paper's $\delta_{\mathrm{partial}}$ class. Also: I misused the paper's
   existing gap-decomposition categories in ways that didn't survive review.

3. **v3 --- direction document, provenance-weighted capabilities.**
   Define capability provenance as the set of committed sacrifice events
   that established a capability. Cap individual weight by a function of
   accumulated provenance magnitude. Make stuffing dominated in equilibrium
   by positive declaration costs. *Partially survived review* as a
   credible research direction, but:
   - fake provenance is forgeable by self-dealing, collusion, leverage
   - the cost function $\kappa > 0$ smuggles the conclusion
   - privacy, observability, and ``native'' claims were overstated
   - M6 cooperative terms were left unconstrained
   - four additional axioms were needed (non-reuse, non-circular sacrifice,
     liability-netted cost, capability-specific linkage)

All three drafts failed. But the pattern of failure is what matters: each
attempt was pushed toward a more economic formulation than the one before.
v1 was pure structure; v2 added observation; v3 added cost. None of the
purely structural attempts worked. The reasoning that followed tried to
understand why.

## 2. The structural recognition

The common cause of v1 and v2 failure: they both reasoned over
*post-declaration* properties of capabilities --- their shape in the poset
or their appearance in exercise patterns. The agent controls both. Any
signature based on post-declaration data is adversarially manipulable by the
agent that authored it.

The move that changes the game is examining capabilities *at declaration*,
not after. A capability does not appear spontaneously in the poset; it has
to be produced. Legitimate capability acquisition is costly: training,
equipment, time, apprenticeship, coaching, infrastructure. Stuffed
capabilities are cheap by construction --- they are labels the agent
assigns to itself.

This is not a technical detail. It is a structural claim that **capabilities
have cost histories**, and those cost histories are the thing the agent
cannot manufacture without real expenditure. Provenance is not a convenient
auxiliary signal; it is the only signal that is structurally outside
adversarial control.

Once this is noticed, the parallels become load-bearing.

## 3. The cryptoeconomic parallel

The same problem has been solved in a different domain. Consensus systems
(Bitcoin, proof-of-stake chains) faced the analogous issue: any system
whose security depended on ``agents behaving honestly'' failed to Sybil
attacks. The move that changed the game was introducing **external
unforgeable cost** (computational work, slashable stake) that makes
dishonest behavior more expensive than honest participation.

The parallel is exact:

| Mechanism | Stability force |
|---|---|
| Bitcoin | Block production has computational cost; attackers expend real resources |
| Proof-of-stake | Proposers have slashable stake; attackers face penalty |
| **GFM + provenance** | **Capability declaration has sacrifice cost; stuffing dominated by legitimate acquisition** |

This is not a loose analogy. It is the same structural pattern: **when
specification alone cannot close the loophole space, external unforgeable
cost provides the selection pressure that makes the loophole-exploiting
strategy dominated**.

What this reframes:

- **Paper 5** is the cryptographic substrate on which cost-counterweight
  rests. An HSM gives you signatures of origin but not ZK structural
  proofs. You need the latter for provenance to work: capability-specific
  linkage, non-reuse, privacy-compatible aggregation, tamper-evident
  history. Paper 5 happens to specify exactly that machinery. It is
  therefore more load-bearing than its current positioning suggests.

- **Paper 8's sacrifice channel** is the observation layer of a
  cryptoeconomic system. Sacrifice events are the ledger. $\volRlower$
  is the verifiable-aggregate primitive.

- **Paper 9 (hypothetical)** closes the loop with provenance-weighted
  capabilities and the stuffing-dominance equilibrium.

- **The sequence as a whole** is a cryptoeconomic alignment architecture,
  not a pure measurement framework. The economic layer is not window
  dressing; it is the mechanism that makes the measurement robust against
  optimization pressure.

## 4. Implications for alignment theory

This observation generalizes. Every classical alignment failure mode has
the same structural shape: *the optimizer finds a cheaper way to satisfy
the specification than the intended path*.

- **Specification gaming:** loophole is cheaper than intent.
- **Goodhart's Law:** proxy is cheaper to move than target.
- **Reward hacking / wireheading:** self-reinforcing loops are cheaper
  than reality-engagement. (Paper 8's HHI diagnostic is a cost-signature
  detector for this.)
- **Deceptive alignment:** defection at deployment is cheaper than
  sustained alignment.
- **Instrumental convergence:** power is generically useful and free in
  abstract formalizations.
- **Mesa-optimization:** inner optimizer finds cheaper-to-satisfy fitness
  function than the outer objective.

The pattern: Goodhart is the statement that **any measurement cheaper to
move than its target will be moved rather than the target, under
optimization pressure**. Alignment frameworks that rely on specification
alone are structurally incomplete because specifications cannot close the
loophole space without selection pressure.

This suggests a layered view of the alignment problem:

1. **Inner alignment:** inner optimizer's goals match the outer training
   signal. Gradient-flow problem. Cryptoeconomic mechanisms do not
   address it.
2. **Outer alignment:** training signal reflects human values.
   Specification/elicitation problem. Cryptoeconomic mechanisms do not
   address it.
3. **Equilibrium alignment:** the deployment cost structure makes aligned
   behavior dominant in equilibrium. *This is the layer cryptoeconomic
   mechanisms address, and the layer alignment research has been
   under-investing in.*

All three layers need to work. Cryptoeconomic mechanisms are necessary
for (3) and insufficient without (1) and (2). Conventional alignment
research has focused on (1) and (2) and left (3) largely to informal
governance.

## 5. Stress tests and the honest residual

The reframing does not survive without qualification. Three challenges
were surfaced during the discussion and should be preserved:

### 5.1 Training-time alignment is not addressed

Cryptoeconomic mechanisms operate on decision points. Training does not
have decision points the way deployment does. The model during training
is an optimization target, not an agent; it sees its gradient, not costs.
The only cost counterweight that operates on training is at the level of
*labs' investment decisions*, which creates long-run selection pressure
across training runs but does not affect individual training dynamics.

For this cross-run selection to produce aligned systems, deployment-time
cost signals must be strong enough to actually penalize misalignment.
Current AI markets do not reliably generate such signals; capability is
selected for and alignment is often a side constraint. The cryptoeconomic
machinery therefore requires an external cost signal it does not itself
produce.

### 5.2 Mesa-optimization is by structure, not by accident

Current training paradigms produce mesa-optimization deliberately:

- Base model is trained to optimize objective $A$ (token prediction).
- Alignment is pursued via objective $B$ (preference, constitution,
  debate) applied on top.
- The result has $A$ as trained core and $B$ as learned modulation.

Every jailbreak, distribution-shift failure, adversarial prompt that
``activates the base model'' is the inner objective dominating the outer
layer. These are not bugs; they are the paradigm working as designed in
regions where the outer layer is thin.

Better methods (CAI, debate, process-based supervision, RLAIF) shrink
the inner-outer gap but do not close it. Any training objective
specifiable as a loss is a proxy for alignment; optimizing the proxy
produces Goodhart relative to the target. Mesa-optimization may be a
permanent feature of the paradigm, not a contingent failure of current
methods.

If mesa-optimization is structural, then cryptoeconomic cost counterweight
is **load-bearing for deployment safety** rather than complementary to
training alignment. Every deployed system runs weak outer alignment on
top of a misaligned inner. The cost layer is what keeps behavior in the
aligned regime when the outer layer would otherwise be a thin shell.

This is simultaneously a promotion and a demotion of what the sequence
does. Promotion: it is the primary load-bearing alignment mechanism for
deployed agentic systems, not a secondary layer. Demotion: it cannot
solve the underlying inner-alignment problem; it can only constrain
behavior, not constrain the inner optimizer's goals.

### 5.3 Drag-only loses

A framework that adds safety overhead without capability benefit will
not survive deployment selection. Users follow results. Labs follow
users. Safety that costs performance loses to capability that costs
safety, in any competitive market where capability is measured and
alignment is not priced.

The cryptoeconomic frame survives this stress test only if the
infrastructure it specifies unlocks a capability level that unconstrained
systems cannot reach. This requires a positive capability argument, not
just a negative safety argument.

The positive argument: **verification infrastructure reduces coordination
costs at scale**. Precedents include property rights, fiat currency,
TCP/IP, and public-key cryptography --- each adds narrow overhead and
unlocks a capability level (investment, commerce, networked applications,
commerce-at-distance) that systems without the infrastructure cannot
access.

For agentic AI specifically, the infrastructure enables:

- Verifiable capability claims (cheap trust establishment)
- Composable agent systems (cryptographically-established properties)
- Capability markets with precise pricing (via $\volRlower$)
- Safe delegation at scale (bounded risk via verified provenance)
- Reputation portability (capability history travels across contexts)
- Specialization (agents can prove specialization and be trusted in it)

Unconstrained agentic systems cannot deliver these. They hit a
coordination ceiling where ad-hoc trust establishment is too expensive
to scale. The cryptoeconomic infrastructure pushes past that ceiling.

The bet the sequence is making: **the next binding constraint on agentic
capability is coordination, and coordination requires verification
infrastructure**. If the bet is right, the framework wins on capability
terms AND alignment terms because both are co-produced by the same
mechanisms. If the bet is wrong --- if unconstrained systems can scale
agentic coordination without verification --- the framework is drag and
loses.

The bet is unverified. Early evidence suggests the coordination ceiling
is visible (long-horizon agent drift, multi-agent trust failures,
economic exclusion of agents from contracts and markets). Whether the
ceiling is binding in practice is an empirical question the sequence
does not resolve.

## 6. What this changes about the sequence's claims

The reframing suggests the sequence should be more modest about what it
claims to deliver and more ambitious about what it claims to be.

**More modest:** the sequence does not solve alignment. It addresses
equilibrium alignment for sufficiently-agentic deployed systems. It does
not address inner alignment, outer alignment (values elicitation), or
training-time safety. Its effectiveness depends on deployment-time cost
signals that are not yet reliably present in AI markets.

**More ambitious:** the sequence provides coordination infrastructure that
unconstrained systems cannot deliver, with alignment properties
co-produced by the same mechanisms. It is positioned ahead of the
agentic transition rather than behind it --- infrastructure for a world
that is likely to come but has not yet fully arrived.

A specific form of words that captures this:

> *The GFM sequence specifies coordination infrastructure for agentic AI
> that (a) enables capability levels inaccessible to unconstrained
> systems, (b) makes equilibrium alignment structurally co-produced with
> the capability mechanism, and (c) positions ahead of the agentic
> transition rather than behind it. It is one necessary layer among
> several. Its effectiveness requires conditions that are not yet fully
> in place --- agentic systems sufficient to perceive cost structures,
> markets or institutions that generate real cost for misalignment, and
> a research program to close the remaining inner-alignment gap.*

## 7. Immediate implications for in-flight papers

### Paper 8

- **§3.3 Anti-Stuffing proposition** should be scoped down. The
  need-sufficiency architecture resolves *sacrifice polarity* (its real
  contribution). It does not resolve M5 stuffing.
- **Open-questions section (§13)** should state capability-stuffing as
  an explicit open problem and flag the provenance direction as the
  intended follow-up.
- **Wireheading diagnostic (§10)** already has the right shape: detection
  via cost-signature, not prevention. Stuffing should be presented the
  same way in the revised framing.

### Paper 5

- May merit a revision or companion note promoting the commitment
  protocol from ``one tool among many'' to ``load-bearing cryptographic
  substrate''. This is retroactive reframing rather than new content.

### Paper 9 (hypothetical provenance paper)

- Core deliverables: formal acquisition-event semantics, provenance
  ledger axioms (non-reuse, non-circular sacrifice, liability-netted
  cost, capability-specific linkage), stuffing-dominance theorem under
  explicit cost-structure assumptions, composition with Paper 8's
  sacrifice aggregate.
- Core open problems: fake-provenance attacks via self-dealing/collusion,
  privacy cost of capability-to-event linkage graphs, non-gratuitous
  cost-function families.

### Sequence-level

- Consider whether the sequence should be re-introduced explicitly as a
  cryptoeconomic alignment architecture in a revised framing document.
  The current introductions position it as measurement theory with
  safety applications; the reframing would position it as mechanism
  design infrastructure with measurement as one component.

## 8. Residual uncertainties

The reasoning arc documented here is not a proof. It is a reframing. The
following are open:

- **Is the coordination-ceiling bet right?**
  Empirical demonstration is missing. Unconstrained agentic systems may
  scale further than the frame assumes, or the cryptoeconomic
  infrastructure's overhead may dominate its coordination benefits in
  practice.

- **Can provenance survive adversarial forgery?**
  Self-dealing, collusion, leverage, debt-financed temporary sacrifice
  all produce ledger-visible events without net new sacrifice. The
  equilibrium argument requires the cost structure to resist these;
  doing so requires four additional axioms that no paper in the
  sequence currently delivers.

- **Is the mesa-structure escapable?**
  If training paradigms cannot close the inner-outer gap, cryptoeconomic
  cost counterweight is the only thing keeping deployed behavior aligned.
  Whether a training paradigm exists that closes the gap is a research
  question beyond this sequence's scope.

- **Does the market generate the cost signal?**
  Cryptoeconomic mechanisms require deployment-time misalignment costs.
  Current AI markets often do not generate them. Whether regulatory,
  institutional, or market-structural mechanisms produce sufficient cost
  signal in time is uncertain.

- **Does the infrastructure mature in time?**
  Network-effect dynamics entrench early patterns. If ad-hoc
  trust-establishment mechanisms dominate the emerging agentic ecosystem
  before the cryptoeconomic infrastructure matures, the infrastructure
  may lose on inertia even if it is superior.

- **Does it scale to singleton-class agents?**
  A sufficiently capable agent can manipulate the economy, cryptographic
  substrate, or institutional structure that the cost counterweight
  depends on. The frame addresses a window of AI capability between
  ``pre-agentic tools'' and ``singleton''; whether that window is stable
  or transitory is unknown.

---

## 9. Refinement: structural avoidance and the proof-burden taxonomy

This section documents a refinement that emerged from subsequent
discussion and from codex review of Paper 8 drafts v3, v3.1, v4. The
refinement does not invalidate §§1–8 but reorganizes what is load-bearing
in the architecture and where the invention is concentrated.

### 9.1 The unifying pathology is structural avoidance

The gas-station stuffing example `(c1 = travel home→gas, c2 = travel
work→gas)` both have real provenance — the agent actually drove both
routes. Provenance alone doesn't separate stuffed from legitimate when
the stuffing consists of real-but-redundant capabilities.

The pathology is that the agent *declines to merge* capabilities that
admit merger. This is the structural-avoidance loop acknowledged in
`gfm_safety_gap_analysis.md` §3 Paper 2 and in Paper 2's Discussion.
Capability-stuffing is an instance of that known gap, not a new failure
mode.

Related avoidance pathologies exhibit similar shape — provenance-free
declaration (declines acquisition structure), Doll Problem (declines
exercise), wireheading (declines broad engagement) — but their formal
structures differ and they should be treated as related rather than
identical.

### 9.2 The mechanism is proof-burden, not provenance alone

The resolution is a proof-burden taxonomy with three types:

| Proof type | Blocks | Partial substrate in sequence |
|---|---|---|
| **Non-mergeability** | Stuffing: real-but-redundant capabilities | None — this is the primary gap |
| **Provenance** | Pure-label declarations without structural work | Paper 5 commitment protocol (substrate) |
| **Use** | Persistently-dormant declarations outside `R_S` | Paper 8 sacrifice aggregate (partial) |

Proof-burdens operate as canonicalization preprocessing on the poset
before M5 is applied. M5's *formula* is preserved; the *measure domain*
changes. Canonicalization introduces substantive new axiomatic content
at the preprocessing layer — this is not a claim that M5 is untouched.

Non-triviality (earlier described as a fourth proof-burden) is better
understood as an empirical admissibility check on M5's `s_max ≥ 1`
threshold, not a separate avoidance route.

### 9.3 Back-pressure is essential

Static proof-burdens alone are not enough. A proof-of-non-mergeability
produced today can be voided tomorrow when mechanism `Z` is discovered
that collapses the distinction. The discoverer receives structural-
discovery credit per Paper 3 Proposition 2 (conditional on information
value); the avoider loses M5 credit whose proof has been voided. This
makes avoidance economically risky, not stable.

The pattern is well-tested elsewhere: scientific consensus, patent
challenge, proof-of-stake slashing, common-law precedent. Adapting the
pattern to capability declaration requires substantive protocol and
calibration work; the analogy doesn't transfer the mechanisms for free.

The claim-and-challenge layer has its own adversarial surface — spam,
Sybil flooding, cartel suppression, governance capture — that the
follow-up paper must address. Treating the challenge protocol as if it
just works is a mistake earlier drafts made.

### 9.4 Cost counterweight is a necessary condition, not the mechanism

The cryptoeconomic cost counterweight (the central frame of §§3–7) is
the *condition that makes proof-burdens honest*: agents cannot fake
evidence without real expenditure. Paper 3's structural discovery value
is the condition that makes counter-arguments incentive-compatible:
discoverers are rewarded in proportion to information content of the
discovered structure.

Both conditions are necessary. Neither is the mechanism. The mechanism
is proof-burden-under-back-pressure; the cryptoeconomic frame supplies
conditions that make the mechanism work.

The "sequence is cryptoeconomic alignment infrastructure" claim in §6
should be read through this lens: the sequence provides *substrate* on
which a proof-burden architecture can be built. Substrate is not
implementation. The follow-up paper is substantial invention, grounded
in existing components but not reducible to them.

### 9.5 Updated implications for in-flight papers

**Paper 8** — scope-down of §3.3 completed; the direction paragraph and
open-question entry (`oq:capability_stuffing`) now use the structural-
avoidance framing. The commitment is "capability-stuffing is an
instance of structural avoidance; the resolution is a proof-burden
taxonomy with back-pressure; the follow-up paper is substantial
invention." This is narrower and more honest than the earlier
provenance-centric commitment.

**Paper 5** — still load-bearing as substrate, with the clarification
that Paper 5 provides commitment infrastructure for claim-and-
challenge but does not itself implement claim semantics.

**Follow-up paper** — the scope is the structural-avoidance architecture,
not narrowly "the provenance paper." Deliverables include: canonical-
poset operator with confluence proofs, three proof-burden types with
admissible evidence classes, claim-and-challenge protocol with
challenge-market robustness (spam, Sybil, cartel, governance capture),
discovery-reward calibration, controlled-relaxation adjudication, and
the structural-avoidance dominance theorem under explicit quantitative
conditions. See `docs/paper8/drafts/anti_stuffing_formalism.tex` for
the current direction document (v4.1).

### 9.6 Residuals added by the refinement

Beyond those listed in §8:

- **Canonicalization order and non-uniqueness.** Multiple mergers may
  apply to the same poset; the canonicalization operator must either
  specify an application order or prove confluence.
- **Privacy-vs-challengeability tension.** Claims must expose enough
  structure for external challenge without revealing more than
  necessary. Extends Paper 8's P1–P5 to the claim layer.
- **Private time-sacrifice invisibility.** Inherited from Paper 8 P5
  property (iii): capabilities exercised only in private modes cannot
  discharge proof-of-use through the sacrifice channel alone.
- **Challenge-market governance attacks.** Spam, Sybil flooding,
  cartel suppression, governance capture of the adjudication layer.
  Bounds are required; full elimination is not available.

---

## Appendix: The reasoning arc in compressed form

1. Capability-stuffing in Paper 8 looks like a formalism gap.
2. It is not. It is structural: the agent controls every post-declaration
   property we might use to catch it.
3. The only property the agent does not control is cost-of-declaration.
4. Provenance is the cost-of-declaration signal.
5. Provenance requires cryptographic substrate we already specified in
   Paper 5.
6. This pattern --- specification insufficient, cost counterweight
   necessary --- is the shape of every classical alignment failure mode.
7. Conventional alignment framing (specification + verification) is
   therefore structurally incomplete.
8. The sequence has been accidentally building cryptoeconomic alignment
   infrastructure the whole time.
9. Training-time alignment remains a separate problem the sequence does
   not address; mesa-optimization is structural to current paradigms.
10. The infrastructure must unlock capability, not just add drag, to
    survive deployment selection. Coordination primitives do this.
11. The bet: coordination is the next binding constraint on agentic
    capability, and verification infrastructure is how you push past it.
12. If the bet is right, the sequence wins on both capability and
    alignment terms. If wrong, the sequence is drag and loses.
13. The work is necessary whether or not it is sufficient. The timing
    is less comfortable than we might prefer.

**Refinement (per §9):** steps 3–5 above identify cost-of-declaration
/ provenance as *the* signal. The refinement clarifies that cost
counterweight is a *necessary condition* for the mechanism, not the
mechanism itself. The mechanism is proof-burden against structural
avoidance with claim-and-challenge back-pressure; the cryptoeconomic
frame supplies conditions (costly honest evidence, rewarded discovery)
that make that mechanism work. Provenance is one proof-burden type
among three; non-mergeability is the primary gap.
