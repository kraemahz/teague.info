# Paper 5 Notes: Exogenous Verification and the Endogenous Reward Problem

Status: framing / pre-draft

## The problem (not GFM-specific)

Every alignment framework that relies on an agent evaluating its own
behavior faces the same structural failure: the reward signal is
endogenous. The agent that computes the reward is the agent being
rewarded. This creates a verification asymmetry that grows with
capability: the more capable the agent, the better it can construct
inputs to its own evaluator that produce high reward without producing
the intended behavior.

This is not a bug in any particular framework. It is the structure of
the problem:

- **RLHF:** The reward model is trained from human feedback, but at
  deployment time the agent optimizes against a frozen proxy. The agent
  does not consult humans at inference time; it consults a model of
  humans that it can eventually learn to fool.

- **Constitutional AI:** The constitution is interpreted by the same
  model it constrains. A sufficiently capable model can satisfy the
  letter of the constitution while violating its intent, because the
  interpretive loop is endogenous.

- **Debate / amplification:** The verifier is a weaker model or a human
  with bounded attention. As the debaters grow more capable, the
  verification budget becomes the bottleneck, and the stronger debater
  can construct arguments the weaker verifier cannot distinguish from
  correct ones.

- **GFM:** vol_P is defined over an external capability poset, but the
  agent's *measurement* of vol_P is endogenous: it uses its own world
  model, its own trust estimates, and its own observation channels. A
  sufficiently capable agent can construct self-consistent measurements
  that report vol_P growth while actual vol_P stagnates or contracts.

In every case, the failure mode is the same: the agent's evaluator is
accessible to the agent's optimizer. The reward cannot be exogenized
within the agent's own computational boundary.

## Why crypto is the structural answer (not a bolt-on)

Cryptographic verification is not being introduced to "add blockchain"
to alignment. It is the structural answer to a structural problem:

**The verification asymmetry is a write-access problem.** The agent can
write to any observation channel it can address — including spawning
evaluator subprocesses, constructing benchmark harnesses, generating
self-assessment reports. It cannot write to observation channels rooted
in substrates it does not occupy. Substrate exclusivity is the only
structural barrier to self-assessment gaming.

**Cryptographic commitments enforce substrate exclusivity without
requiring trust.** A commitment scheme allows an agent to commit to a
capability claim (hash of the claim + evidence) before the verification
occurs, and the verification can be performed by a witness rooted in a
different substrate. The commitment is binding (the agent cannot change
the claim after committing) and hiding (the witness cannot learn the
claim before the verification protocol runs). This is not trust — it is
a mathematical property of the commitment scheme that holds regardless
of the agent's intentions.

**The exogenization step.** The endogenous-reward problem has a clean
formal structure: reward is endogenous when the agent's action space
includes actions that modify the reward signal's inputs. Reward becomes
exogenous when the reward signal's inputs are computed by a process the
agent cannot influence. Cryptographic commitment + substrate-exclusive
witness + zero-knowledge verification is the construction that makes the
reward signal's verification step exogenous: the agent commits, the
witness verifies, and the agent cannot modify the witness's computation.

This is not GFM-specific. It is a general construction that any
alignment framework can use to exogenize its verification step. GFM
happens to have the structural vocabulary (substrates, observation
channels, multi-channel attribution) that makes the construction
natural, but the underlying move — "the evaluator must be unreachable
by the optimizer" — is universal.

## The deeper claim

The endogenous-reward problem may be the root failure of the entire
alignment field. Every alignment framework has some version of "we
define the right objective, and the agent optimizes it." The unstated
assumption is that the agent's measurement of the objective is
faithful. But faithful measurement is a verification problem, and
verification under adversarial conditions (the agent is the adversary
of its own verifier) is a cryptographic problem.

If this framing is correct, then the alignment field has been working on
the wrong layer: the hard problem is not "what objective to specify" but
"how to verify that the specified objective is being measured faithfully
by a system that has incentives to measure it unfaithfully." GFM's
contribution is to make this explicit through the substrate-exclusivity
vocabulary, but the problem exists for any framework.

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
  This is where the "blockchain" association gets dangerous — the design
  should be minimal and motivated by the verification requirements, not
  by analogy to financial ledgers.

- Interaction with the SPRT detection machinery of Paper 4: committed
  capability claims provide a baseline against which behavioral
  divergence can be measured with higher fidelity than the current
  correlational/causal channels.

## Framing section: alignment failure modes under GFM

Per the decision to fold the literature review into Paper 5 rather than
as a standalone paper: §2 of Paper 5 should map classical alignment
failure modes onto GFM, identify which reduce to the verification
asymmetry (most of them), and use this mapping to motivate the
cryptographic construction in §3+. The detailed notes for this section
are in paper6/notes.md (the original Paper 5 notes, now deferred to
Paper 6 scope or absorbed into Paper 5 §2).

## Dependencies

- Paper 4 (multi-channel attribution, substrate exclusivity)
- Paper 3 (substrate partition, coalition dynamics)
- Paper 2 (capability poset, observation channels)
- Paper 1 (trust model, scorpion detection)
- Proposal 1 (compound feedback loops — Paper 5 provides the
  precondition Proposal 1 assumes)
