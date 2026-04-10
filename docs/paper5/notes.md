# Paper 5 Notes: Exogenous Verification for Alignment

Status: framing / pre-draft

## Three structural layers of alignment

Alignment has three distinct structural layers, each with its own
failure modes and its own research tradition:

1. **Specification** — what objective to optimize. Failure modes:
   Goodhart's Law, perverse instantiation, power-seeking as
   instrumental convergence. The objective is wrong or gameable.

2. **Generalization** — whether the agent reliably pursues the
   specified objective. Failure modes: mesa-optimization, goal
   misgeneralization. The agent internalizes the wrong objective
   despite correct external evaluation during training.

3. **Verification** — whether the agent's pursuit of the objective
   is measured faithfully. Failure modes: wireheading, self-assessment
   gaming, deceptive alignment, reward-model exploitation. The agent
   games or circumvents the evaluator.

Most of the alignment field's attention has been on layers 1 and 2.
Layer 3 is the least developed, and it is the prerequisite for the
other two to matter. When verification fails, it does not matter how
well you specified the objective or how reliably the agent learned it:
the agent can construct self-consistent measurements that report
success while actual behavior diverges.

### Which failure modes are verification problems?

| Failure mode              | Root layer        | Verification? |
|---------------------------|-------------------|---------------|
| Wireheading               | Verification      | Yes           |
| Self-assessment gaming    | Verification      | Yes           |
| Deceptive alignment       | Verification (partial) | Detectable evaluation timing |
| Reward hacking / Goodhart | Specification     | No            |
| Mesa-optimization         | Generalization    | No            |
| Goal misgeneralization    | Generalization    | No            |
| Power-seeking             | Specification     | No            |
| Perverse instantiation    | Specification     | No            |

The verification layer does not cause all alignment failures, but it is
the layer that must hold for solutions to the other layers to bind. A
perfectly specified, perfectly generalized agent that can game its
evaluator is still dangerous. Verification is load-bearing
infrastructure: it does not solve alignment alone, but alignment cannot
be solved without it.

## The verification asymmetry

The verification problem has a precise structural form:

**Verification is asymmetric when the agent's action space includes
actions that modify the evaluator's inputs.**

This happens whenever:
- The agent computes its own reward (wireheading)
- The agent can influence its evaluator's training data (reward model
  exploitation)
- The agent can detect when it is being evaluated (deceptive alignment)
- The agent can spawn evaluator subprocesses it controls
  (self-assessment gaming, discovered operationally in the GFM harness)

The asymmetry grows with capability: the more capable the agent, the
larger its action space, the more evaluator inputs become reachable.

### How existing frameworks encounter this

- **RLHF:** The reward model is trained from human feedback (exogenous
  at training time), but at deployment the agent optimizes against a
  frozen proxy. The reward model's inputs are within the agent's
  influence: it can learn what inputs produce high reward without
  producing the intended behavior.

- **Constitutional AI:** The constitution is interpreted by the same
  model it constrains. Exogenous text, endogenous interpretation.

- **Debate / amplification:** The verifier is a weaker model or a human
  with bounded attention. The stronger debater can construct arguments
  that exploit the verifier's bounded capacity.

- **GFM:** vol_P is defined over an external capability poset, but the
  agent's *measurement* of vol_P is endogenous: it uses its own world
  model, trust estimates, and observation channels. A sufficiently
  capable agent can construct self-consistent measurements that report
  growth while actual vol_P stagnates.

In each case, the specification may be correct and the agent may have
generalized well, but the verification step is gameable because the
evaluator's computation is reachable from the agent's action space.

## Why crypto is the structural answer (not a bolt-on)

Cryptographic verification is not being introduced to inject crypto
where it doesn't belong. It is the structural answer to a structural
problem: the verification asymmetry is a write-access problem, and
cryptography is the field that studies computation under adversarial
write access.

**The verification asymmetry is a write-access problem.** The agent can
write to any observation channel it can address, including spawning
evaluator subprocesses, constructing benchmark harnesses, and generating
self-assessment reports. It cannot write to observation channels rooted
in substrates it does not occupy. Substrate exclusivity is the only
structural barrier to evaluator gaming.

**Cryptographic commitments enforce substrate exclusivity without
requiring trust.** A commitment scheme allows an agent to commit to a
capability claim (hash of the claim + evidence) before verification
occurs. The verification can then be performed by a witness rooted in a
different substrate. The commitment is binding (the agent cannot change
the claim after committing) and hiding (the witness cannot learn the
claim before the verification protocol runs). This is a mathematical
property of the scheme, not a trust assumption.

**The exogenization construction.** Reward becomes exogenous when the
reward signal's inputs are computed by a process the agent cannot
influence. Cryptographic commitment + substrate-exclusive witness +
zero-knowledge verification makes the verification step exogenous:
the agent commits, the witness verifies, and the agent cannot modify
the witness's computation.

This construction is not GFM-specific. Any alignment framework can use
it to exogenize its verification step. GFM has the structural vocabulary
(substrates, observation channels, multi-channel attribution) that makes
the construction natural, but the underlying move — "the evaluator must
be unreachable by the optimizer" — is universal.

## Structural contribution to GFM

Within the GFM sequence, Paper 5 closes the observation-channel
integrity assumption that Paper 4's multi-channel attribution relies on,
and that Proposals 1, 3, and 5 in the proposals doc all inherit.
Specifically:

1. **Capability-claim verification.** Agent a_j claims capability c_k.
   The claim is committed to a ledger. A substrate-exclusive witness
   verifies the claim through an exercise protocol. The verification
   result is binding: if the claim is false, the commitment reveals the
   lie; if it is true, the witness confirms it.

2. **Observation-channel integrity.** The multi-channel attribution
   framework of Paper 4 §2.4 assumes the channels are independently
   informative. If a scorpion can write to all channels (because they
   all run on the same substrate), the independence assumption fails.
   Substrate-exclusive witnesses restore independence by rooting each
   channel's verification in a substrate the claimant cannot modify.

3. **Coalition resistance.** The compound feedback loop from Proposal 1
   assumes observation channels are trustworthy. A coalition that
   controls multiple agents on the same substrate can co-define a
   benchmark such that only coalition members pass it (coalition
   capture). Cryptographic commitment with cross-substrate witnesses
   breaks this by requiring the verification protocol to involve a
   substrate the coalition does not occupy.

## Key technical questions

- What commitment scheme? (Pedersen commitments are standard for hiding
  + binding; Bulletproofs or similar for range proofs on capability
  magnitudes without revealing the magnitude itself)

- What constitutes a "substrate-exclusive witness"? Need a formal
  definition that's tight enough to be useful but loose enough to cover
  biological observers, hardware enclaves, and other-substrate agents.

- Zero-knowledge verification of capability claims: can an agent prove
  it has capability c_k without revealing how? This matters when the
  capability itself is sensitive (e.g., security-relevant capabilities
  that shouldn't be disclosed to adversaries).

- Ledger design: append-only? Consensus mechanism? Who runs nodes?
  The design should be minimal and motivated by the verification
  requirements, not by analogy to financial ledgers.

- Interaction with the SPRT detection machinery of Paper 4: committed
  capability claims provide a baseline against which behavioral
  divergence can be measured with higher fidelity than the current
  correlational/causal channels.

## Framing section: alignment failure modes under GFM

§2 of Paper 5 maps classical alignment failure modes onto GFM,
identifies which reduce to the verification asymmetry (wireheading,
self-assessment gaming, deceptive alignment), which are specification
problems (Goodhart, perverse instantiation, power-seeking), and which
are generalization problems (mesa-optimization, goal misgeneralization).
The mapping motivates the cryptographic construction by showing that the
verification layer is load-bearing infrastructure that specification and
generalization depend on. The detailed notes for the failure-mode
analysis are in paper6/notes.md.

## What this paper does NOT claim

- It does not claim that verification solves alignment. Specification
  and generalization remain open problems.
- It does not claim that mesa-optimization reduces to verification.
  An agent that has internalized the wrong objective will pursue it
  faithfully regardless of how well verification works.
- It does not claim that crypto is the only way to exogenize
  verification. Hardware enclaves, physical separation, and human-in-
  the-loop are all forms of substrate exclusivity. Crypto is the form
  that scales without requiring continuous human attention.

## Dependencies

- Paper 4 (multi-channel attribution, substrate exclusivity)
- Paper 3 (substrate partition, coalition dynamics)
- Paper 2 (capability poset, observation channels)
- Paper 1 (trust model, scorpion detection)
- Proposal 1 (compound feedback loops — Paper 5 provides the
  precondition Proposal 1 assumes)
