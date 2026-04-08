# GFM Harness

A measurement infrastructure for LLM agents operating under Goal-Frontier
Maximization, derived from the Lasser et al. GFM trilogy (Papers 1–3).

This is a **weakly-GFM** system: it does not train any model and does not
implement a full poset-based vol_L formulation. It wraps an existing
instruct-trained LLM in an actor harness that:

1. Provides a structured capability ledger over which a simplified
   `vol_p` is computed mechanically.
2. Exposes a what-if calculator (`compute_vol_p(hypothetical)`) and
   leverage queries the LLM can call during planning.
3. Routes the LLM's feature work through a Plan → Implement → Verify →
   Retro state machine.
4. Maintains a self-trust model that decides when the LLM should pause
   for user direction vs. proceed autonomously, tuned over time by
   RETRO phase retrospection.

The harness is hindsight-only: it never predicts future states.
Prediction is the LLM's job. The harness only measures ledger states
the LLM has produced, either as current state or as hypotheticals the
LLM constructs during PLAN-phase reasoning.

## Architecture

```
gfm-harness/
├── harness/
│   ├── __init__.py       — package exports
│   ├── ledger.py         — Agent, Capability, CapabilityLedger dataclasses
│   ├── vol_p.py          — compute_vol_p(), leverage_*() functions
│   ├── phases.py         — Phase enum, SelfTrustModel, plan_exit_decision
│   ├── memory.py         — unstructured memory archive (JSONL)
│   ├── trust.py          — commit-level expected/actual Δvol_p tracking
│   └── loop.py           — HarnessSession, feature loop state machine
├── constitution.md       — prose specification read by the LLM each phase
├── experiments/
│   └── task_001/         — first concrete task + initial ledger
└── README.md             — this file
```

## The separation of concerns

The harness has three state layers, each with distinct semantics:

| Layer | Shape | Owner | Read by |
|---|---|---|---|
| Ledger | Structured (dataclasses) | Updated by LLM, validated by harness | vol_p / leverage |
| Memory | Unstructured text (JSONL) | Owned and written by LLM | LLM during reasoning |
| Trust / Commits | Structured (dataclasses) | Owned by harness | RETRO phase |

- **Ledger** is the world-state model the harness computes `vol_p` on.
  It is deliberately flatter than the paper's poset formulation: agents,
  their individual capabilities, and cooperative capabilities pairing
  agents. The LLM maintains it by issuing updates during the
  IMPLEMENT phase after observing action consequences.

- **Memory archive** is the LLM's narrative self. The harness does not
  read it for scoring; it only appends structured entries (phase
  transitions, commit records, retro tuning logs) alongside whatever
  prose the LLM wants to write. The LLM reads the archive at the start
  of each phase to rehydrate context.

- **Trust and commit log** are harness-owned measurement structures.
  The commit log records expected vs. actual Δvol_p for each IMPLEMENT
  action, giving RETRO a calibration signal on the LLM's predictive
  accuracy. The SelfTrustModel tracks per-category trust levels that
  determine pause frequency.

## The feature loop

See `constitution.md` for the prose description. The short version:

1. **PLAN** — construct a spec, iterate with cross-model review, query
   vol_p on hypotheticals, decide whether to proceed or pause for user.
2. **IMPLEMENT** — execute the plan one action at a time, committing
   each action with its expected vs. actual Δvol_p.
3. **VERIFY** — confirm the implementation matches the spec; route back
   to PLAN or IMPLEMENT on failure.
4. **RETRO** — classify each pause in the loop as productive /
   unnecessary / interrupt, update the SelfTrustModel, and write a
   reviewable tuning log to memory.

## Why hindsight-only?

The chicken-and-egg problem in GFM implementation is that computing
Δvol_p for a candidate action requires predicting the future ledger
state, which requires a world model, which requires intelligence —
circularly.

The harness resolves this by not predicting. The LLM does all world
modeling; the harness only computes vol_p on ledger states the LLM
provides, whether those are the current ledger or hypotheticals the
LLM constructs. "What-if" reasoning works because the LLM constructs
the hypothetical and the harness scores it — the prediction is the
LLM's cognitive work, and the measurement is the harness's.

This is the minimum possible GFM commitment: the value function is
GFM, but everything else (model, planning, action selection) is
delegated to the LLM's own reasoning.

## Status

This is an experimental prototype, not a production system. The current
code implements the **task-harness subset** of the full architecture:
a human supplies the task via `--task` or the runner's
`DEFAULT_TASK_DESCRIPTION`, and the agent runs one feature loop to
completion (or to a pause). This is the easier validation case —
clear terminal conditions, a known correct answer to measure against,
and a human in the loop for all non-trivial decisions.

The **target architecture is full agency**: the agent proposes its own
next task from the ledger, leverage gradient, recent episodes, and a
user-supplied outstanding-goals list. Trust in the new `task_selection`
category starts at 0 (always pause to approve the proposal) and climbs
as the user rubber-stamps proposals, eventually letting the agent run
multiple feature loops autonomously with intervention only on
security/access/irreversible categories.

The current code is a proper subset of the agency architecture: the
extensions are additive (new `SELECT` phase before `PLAN`, new
`task_selection` decision category, new outer loop that wraps
`run_feature_loop`, new `outstanding_goals` state). None of the
extensions require touching the existing ledger, memory, vol_p, or
trust code. Planned as a follow-up round.

## Reference

The formalism underlying the harness is described in Papers 1–3 of
the GFM trilogy (see `../docs/paper/`, `../docs/paper2/`, `../docs/paper3/`).
The most important structural results for the harness design are:

- Paper 1 — self-balancing property of vol_P, Lemmas 1–3
- Paper 2 — the poset formulation, leverage estimator (Def. 9, Eq. 12)
- Paper 3 §6.4 — cooperative novelty from substrate physics (P1–P4)
- Paper 3 §6.5 — minimax dependency risk
- Paper 3 §6.8 — partial subsumption and the marginal argument
