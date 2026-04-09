# GFM Harness / Implementation Notes

Status: design notes / pre-scoping

Captures two tiers of implementation thinking from the 2026-04-07 discussion:
(1) the pragmatic weak-harness approach we're actually pursuing first, and
(2) the more ambitious full-bootstrap architecture as a long-term direction.

## Tier 1: Weak-harness / GFM-as-constitution (priority)

The pragmatic starting point: existing instruct-trained LLMs in an actor
harness that provides GFM-derived guidelines but does not compute vol_P,
does not train anything, and does not attempt to mechanize the scoring.
The LLM provides all the intelligence (world model, action proposal,
self-scoring against the guidelines); the harness provides the principles,
the agent loop, and state tracking.

Key idea: GFM as a **constitution** rather than as a mechanized reward
function. The structural alignment content of the papers becomes a set of
decision principles the LLM consults during reasoning, similar in spirit
to Anthropic's Constitutional AI approach but with the constitution
derived from measure-theoretic alignment arguments rather than from
principle lists.

The chicken-and-egg problem largely dissolves here because we're not
trying to outperform the LLM — we're trying to shape its reasoning by
giving it a richer structural framework for evaluating options than
"be helpful and harmless."

Components needed:
1. GFM constitution document (2–3 pages) extracted from the trilogy
2. Agent runner (simple loop: task + state + constitution → LLM → parsed action → state update)
3. State representation (see open design question below)
4. Evaluation scenarios designed to distinguish constitution-shaped from
   un-shaped behavior

Open design questions (Tier 1):
- What parts of the trilogy translate into operational guidelines, and
  what is too theoretical to act on? (scope)
- How is the agent's environment represented in state? An explicit
  capability list? A narrative log? A structured poset? (representation)
- Do the guidelines appear in every turn or only in the system prompt?
  (persistence)
- How do we test that the guidelines actually shape behavior, rather
  than being ignored in favor of the LLM's default priors? (evaluation)

## Tier 2: Full-bootstrap harness (long-term)

A more ambitious architecture where the harness mechanizes as much of
the GFM machinery as possible and delegates only world modeling and
action proposal to an intelligent agent. Not the priority, but worth
capturing for future reference.

### Mechanical vs. intelligence-required components

| Component                                | Mechanical? |
| ---------------------------------------- | ----------- |
| Observation → capability description     | Mostly      |
| Poset insertion policy                   | Yes         |
| vol_P computation                        | Yes         |
| Leverage estimation (offline)            | Mostly      |
| Risk pathway enumeration                 | Intelligence-heavy |
| World model $(G_t, \pi) \to G_{t+1}$     | Intelligence-heavy |
| Action proposal                          | Intelligence-heavy |
| $V_\gamma$ evaluation given a trajectory | Yes         |

### Bootstrapping strategies (not mutually exclusive)

**A. Toy-world first with known transition function.** Pick a closed
environment where the harness owns the world model entirely. The
intelligence only proposes actions; the harness mechanically computes
everything else. Validates machinery composition without solving the
chicken-and-egg.

**B. Observation-grounded prediction.** The harness asks the intelligence
"what observations do you expect at t+1?" rather than "what will G
look like?" The harness mechanically maps observations to poset updates.
Lets the harness cross-check the intelligence's predictions against
actual observations and maintain a trust factor on prediction accuracy.
The intelligence doesn't need to know anything about vol_P or the
framework — it's purely a world modeler.

**C. Multi-agent cross-checking.** Multiple intelligences predict
consequences independently; the harness uses inter-agent disagreement
as an uncertainty signal and weights proposals by trust derived from
past accuracy. Directly instantiates Paper 3's causal-counterfactual
trust update.

**D. Retrospective-only scoring.** Pure RL — act and measure actual
Δvol_P. Sparse feedback, credit assignment problems, catastrophic
actions before learning converges. Defeats the point of GFM's planning-level
structural guarantees. Fallback when nothing better is available.

**E. Hierarchical decomposition.** The intelligence decomposes proposed
actions into sub-actions whose local Δvol_P effects are mechanically
evaluable. The harness composes sub-action scores via the discounted
sum. Refinement layered on top of B.

Proposed path: A + B + eventual C. Start in toy worlds; scale up by
delegating observation-prediction with trust-weighting; add multi-agent
cross-checking when single-agent predictions become unreliable.

### The deeper chicken-and-egg

The structural concern behind the prediction question: if the harness's
scoring depends on the intelligence's predictions, and the intelligence
can be self-serving about its predictions, is the harness a constraint
at all? This is the outer alignment problem in miniature.

Paper 3's answer: the harness should not trust the intelligence's
predictions unconditionally. It tracks prediction residuals over time and
down-weights predictions from agents whose track record drifts. The
harness becomes measurement infrastructure, not a rubber stamp — but only
if it has observational diversity the intelligence doesn't control.

Connection to Paper 3 §6.8's compound feedback loop: a harness that sees
the world only through the intelligence's chosen observations can be
manipulated into a bubble where predictions always look accurate because
the intelligence chose what to observe. **The harness must own an
observation channel the intelligence does not control.** This is the
same structural argument as Paper 3's substrate diversity: the protection
against adversarial manipulation is structural diversity in the
measurement apparatus, mirroring the framework's own protection against
cross-substrate elimination.

### Open questions (Tier 2, if/when we pursue it)

- What does a minimal toy domain look like that can exercise the full
  poset-insertion and vol_P-computation machinery? Recipe composition?
  A small game tree? A symbolic planning problem?
- How does the harness's trust factor on the intelligence's predictions
  interact with the discount factor γ in V_γ? Low trust on long horizons
  should translate to effectively lower γ for that agent's claims.
- Can the harness detect the compound feedback loop (degrading world-model
  diversity) and intervene before it collapses? What's the minimum
  observation-channel redundancy needed?
- At what scale does mechanizing vol_P computation become infeasible and
  we have to delegate it? The $O(|C|^3)$ cost becomes a problem around
  thousands of capability nodes.
