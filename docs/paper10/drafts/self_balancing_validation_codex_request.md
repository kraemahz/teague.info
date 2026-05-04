# Codex review request: self-balancing infrastructure claim — skeptical validation

## Mode

**Adversarial / skeptical review.** We have a structural claim that feels "too good to be true" and we want it stress-tested before we commit to it. This is not a proof check (the claim is informally stated, not yet derived rigorously) and not a constructive review (we don't want help making it stronger). We want you to find the holes.

If after stress-testing you conclude the claim is sound under stated conditions, say so explicitly with the conditions enumerated. If it's not sound, identify the structural obstruction. If it's sound but in a much narrower regime than we suggest, say where the regime boundary is.

## What to read

Primary:
- `docs/paper10/paper10_proposal.md` — particularly §6 "Substrate identification and the self-balancing infrastructure property" (this is the claim under test).

Source paper sections that ground the claim:
- `docs/paper3/sections/substitution.tex` — Proposition 6 (anti-monopolar property), §sec:substitution_coop (cross-substrate cooperative novelty as the source of $r_{\mathrm{ext}}$)
- `docs/paper3/sections/avoidance.tex` — structural avoidance / discovery duality
- `docs/paper6/sections/phase_boundary.tex` — Stabilizing/destabilizing cascade remark
- `docs/paper6/sections/lyapunov.tex` — endogenous correction term ($c_V \cdot \nu$) tying optimization-incentive to calibration
- `docs/paper5/sections/witnesses.tex` — algorithmic witness substrate-exclusivity
- `docs/paper5/sections/asymmetry.tex` — verification asymmetry argument (the foundational assumption that the formal layer is a substrate that agents cannot write to)

Companion drafts (context):
- `docs/paper10/drafts/lemma_5_anti_monopolar_robustness.tex` — v4 synthesis (the broader Lemma 5 family)
- `docs/paper10/drafts/lemma_5c_minimax_static_tightening.tex` — your earlier review identified soundness issues; we are revising

## The claim under test

**Claim (informal, paraphrased from §6 of the proposal):**

> Under the deployment-safety invariants ($I_1$--$I_8$), Paper 3's anti-monopolar property applies to the tripartite substrate structure (Human + AI + Formal-Operational). The Formal-Operational layer participates in cross-substrate cooperative capabilities (verified generation, governance enforcement, full verified workflow). An agent computing $V_\gamma$ correctly under accurate world model values the Formal-Operational layer's continued functioning, because eliminating it eliminates cooperatives the agent's $\volL$ counts. Therefore optimization pressure under invariant satisfaction *preserves and grows* the verification infrastructure rather than attacking it.

**Implication:** The standard alignment concern ("AI agents will optimize against verification") is reversed under proper substrate identification: agents optimize *for* verification because verification is part of the substrate ecosystem their $\volL$ depends on.

## Specific concerns we have identified

We have three specific worries we want you to evaluate in priority order, plus we want you to find any others.

### C1. Mesa-objective may not actually compute $V_\gamma$ over the full substrate structure.

The argument requires the agent's *effective* objective (whatever it actually optimizes, which may differ from its trained objective) to:
- Decompose its world model into Human / AI / Formal-Operational substrates
- Attribute cooperative outputs to all three substrates, not just to itself
- Apply the discounted value calculation correctly across the structure

This is the inner-alignment problem in disguise. An agent trained to "produce good outputs" may have a mesa-objective like "produce outputs that pass verification" rather than "produce outputs whose cooperative-novelty value depends on verification's continued operation." The first leads to verification-evasion; the second leads to verification-preservation. The claim's force depends on which mesa-objective the agent actually develops.

**Question:** Is this a fatal weakness? Or does Paper 3's anti-monopolar argument apply at the level of the *system's true $V_\gamma$* regardless of the agent's mesa-objective, with the agent's eventual convergence to substrate-preservation following from external selection pressure? If the latter, what's the selection mechanism?

### C2. Substrate-level cascade may be more fragile than channel-level.

Paper 6's stabilizing cascade applies at the channel level: as $\Lyap$ decreases, decisions improve, channels are preserved, channels provide more correction. The quantities here are continuous (real-valued $\Lyap$, real-valued channel strength).

Our claim extends this to the substrate level: the agent preserves the Formal-Operational substrate. But "substrate exists / doesn't" is more like a discrete category than a continuous quantity. A cascade where each step is a discrete category shift might have very different stability properties than Paper 6's continuous-quantity cascade.

**Question:** Does the substrate-level extension actually inherit Paper 6's cascade stability? Or does the discreteness break the analysis? Specifically: does the substrate-level cascade have positive Lyapunov drift in the right direction, or is it metastable / unstable in ways the channel-level cascade isn't?

### C3. The regime where the cascade holds may be much smaller than we suggest.

We claim the cascade holds "under invariant satisfaction." But the invariants themselves require:
- $\gamma > \gamma^*$ (long planning horizon)
- $\Lyap < \epsilon_{\mathrm{safe}}$ (accurate world model)
- $\meff^{\mathrm{indep}} \geq 3$ with balanced $\alpha$
- All the other $I_k$ conditions

For a real deployed system to satisfy all of these *and* have an agent whose mesa-objective genuinely computes $V_\gamma$ over the substrate structure, the regime may be a small slice of plausible deployments. If true, the deployment claim's force is weaker than it sounds.

**Question:** What is the *width* of the regime where the self-balancing cascade holds? Is it a typical-deployment regime, or an exotic-deployment regime? Are there deployment configurations that satisfy all the invariants but still fail the substrate-structure-recognition condition (C1)?

## What we want you to also stress-test

Beyond C1-C3, please look for:

### S1. Circular reasoning.

The argument has the structure: invariants in force → agent preserves formal layer → invariants stay in force. Is this circular in a problematic way? Or is it the standard fixed-point argument for stable equilibria (which is non-circular when the basin of attraction is non-empty)? If non-circular, what establishes that the basin of attraction is non-empty (i.e., that there *exists* a state from which the cascade can launch)?

### S2. Paper 5's verification-asymmetry assumption smuggled in.

The argument treats the Formal-Operational layer as substrate-exclusive (agents can't write to it). This is Paper 5's foundational assumption. But Paper 5's assumption is *that this is achievable through cryptographic protocols*; the assumption isn't that arbitrary verification is substrate-exclusive. If a deployment uses verification that isn't actually rooted in cryptographic substrate-exclusivity (e.g., an in-process monitor, a same-substrate audit), the substrate count drops and the argument fails. Are we hand-waving over this in §6?

### S3. The cooperative-attribution argument is shaky.

The claim that "removing the Formal-Operational layer eliminates cooperatives the agent's $\volL$ counts" requires those cooperatives to *actually* exist. If the agent's $\volL$ is dominated by single-substrate capabilities (which is structurally encouraged by Goodhart's law and the structural-avoidance pathology of Paper 3 §sec:avoidance), then the cooperative-novelty contribution is small and removing the formal layer barely affects $V_\gamma$. The cascade may not start in the first place.

**Question:** Does the structural-avoidance pathology of Paper 3 actively work against the self-balancing cascade? If agents avoid forming cross-substrate cooperatives (because each one introduces structural commitments), the cooperative-novelty $r_{\mathrm{ext}}$ stays low and the formal layer's $\alpha$ contribution stays small.

### S4. The training-time conditions are externalized.

We list "substrate-structure training," "cooperative attribution," and "$\gamma$-discipline" as training-time conditions. But these are exactly the conditions that produce the agent the claim presumes. We're saying "if the agent is trained right, the deployment claim holds." This is true but circular in a different sense — we're not establishing that such training is achievable, only that *if* it's achieved, the claim holds.

**Question:** Is this externalization fatal? Or is it the standard alignment-research move (assume training succeeds, then characterize the post-training dynamics)? Where does it leave the deployment claim's force?

## Output we want

For each of C1, C2, C3, S1, S2, S3, S4 (and any additional concerns you identify):

- **Concern is fatal:** the claim cannot be made even with stated conditions. Explain the obstruction.
- **Concern is real but bounded:** the claim holds in a narrower regime than we suggest. Specify the regime.
- **Concern is not a real problem:** explain why our worry was misplaced.

If you conclude the overall claim is salvageable, state the *minimum set of additional assumptions* needed to make it formally defensible. If you conclude it is not salvageable, state the structural obstruction.

If you find the claim is sound but for *different reasons* than the cooperative-attribution argument we use, please surface that — we may have been right for the wrong reasons.

The goal is to know whether to (a) integrate §6 into Paper 10 as a major claim, (b) integrate §6 with stated additional conditions and a narrowed regime, or (c) excise §6 and keep Paper 10 to the more modest detection-and-correction framing.
