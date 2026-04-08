"""
Tool schemas and handlers for the LLM driver.

The harness exposes a small set of operations to the LLM as Anthropic
tool-use tools. Each tool is a method on HarnessSession plus a JSON
schema the Messages API consumes. The handlers apply the tool invocations
to the session and return JSON-serializable results.

Ledger operations are expressed as a small diff language so the LLM can
describe hypothetical ledger changes compactly (rather than sending the
full serialized ledger on every query). A LedgerOp list is applied to
a cloned ledger to produce a hypothetical, and the harness computes
vol_p on the result without touching the real ledger.

This module is pure-Python with no external dependencies. It is safe
to import without the anthropic SDK installed.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any, Callable

from .ledger import (
    Agent,
    Capability,
    CapabilityLedger,
    CooperativeCapability,
)
from .memory import (
    ConsolidationProposal,
    Episode,
    Lesson,
    SideAction,
)
from .vol_p import (
    compute_vol_p,
    leverage_report,
    VolPWeights,
)


# ---------------------------------------------------------------------------
# Ledger diff language
# ---------------------------------------------------------------------------
#
# The LLM constructs hypothetical ledgers by applying a list of operations
# to the current ledger (or to an empty ledger for new constructions).
# Operations are simple dicts so the LLM can emit them as JSON tool inputs.
#
# Supported ops:
#   add_agent          — create a new agent on a substrate
#   remove_agent       — delete an agent entirely
#   add_capability     — add an individual capability to an agent
#   remove_capability  — remove an individual capability from an agent
#   add_cooperative    — add a cooperative capability
#   remove_cooperative — remove a cooperative capability
#
# apply_ledger_ops() validates each op and returns a new ledger (or a list
# of errors). The function never mutates the input ledger.


def apply_ledger_ops(
    base: CapabilityLedger,
    ops: list[dict[str, Any]],
) -> tuple[CapabilityLedger, list[str]]:
    """
    Apply a list of diff operations to a clone of the base ledger.

    Returns (new_ledger, errors). If errors is non-empty, new_ledger
    may be partially mutated — callers should treat a non-empty errors
    list as "do not trust the result."
    """
    ledger = base.clone()
    errors: list[str] = []

    for i, op in enumerate(ops):
        op_type = op.get("type")
        try:
            if op_type == "add_agent":
                _apply_add_agent(ledger, op)
            elif op_type == "remove_agent":
                ledger.agents.pop(op["agent_id"], None)
                ledger.cooperative = {
                    k: c
                    for k, c in ledger.cooperative.items()
                    if op["agent_id"] not in c.participants
                }
            elif op_type == "add_capability":
                _apply_add_capability(ledger, op)
            elif op_type == "remove_capability":
                _apply_remove_capability(ledger, op)
            elif op_type == "add_cooperative":
                _apply_add_cooperative(ledger, op)
            elif op_type == "remove_cooperative":
                ledger.cooperative.pop(op["key"], None)
            else:
                errors.append(f"op {i}: unknown type {op_type!r}")
        except KeyError as e:
            errors.append(f"op {i} ({op_type}): missing required field {e}")
        except Exception as e:  # noqa: BLE001 — we want to report any op failure
            errors.append(f"op {i} ({op_type}): {type(e).__name__}: {e}")

    errors.extend(ledger.validate())
    return ledger, errors


def _apply_add_agent(ledger: CapabilityLedger, op: dict[str, Any]) -> None:
    agent_id = op["agent_id"]
    if agent_id in ledger.agents:
        raise ValueError(f"agent {agent_id!r} already exists")
    caps = {
        Capability(key=c["key"], description=c.get("description", ""))
        for c in op.get("individual_capabilities", [])
    }
    ledger.agents[agent_id] = Agent(
        agent_id=agent_id,
        substrate=op["substrate"],
        individual_capabilities=caps,
        notes=op.get("notes", ""),
    )


def _apply_add_capability(ledger: CapabilityLedger, op: dict[str, Any]) -> None:
    agent_id = op["agent_id"]
    if agent_id not in ledger.agents:
        raise ValueError(f"agent {agent_id!r} does not exist")
    cap = Capability(key=op["key"], description=op.get("description", ""))
    # Dedupe by key — replace if already present
    existing = {c for c in ledger.agents[agent_id].individual_capabilities if c.key != cap.key}
    existing.add(cap)
    ledger.agents[agent_id].individual_capabilities = existing


def _apply_remove_capability(ledger: CapabilityLedger, op: dict[str, Any]) -> None:
    agent_id = op["agent_id"]
    key = op["key"]
    if agent_id not in ledger.agents:
        return  # no-op
    ledger.agents[agent_id].individual_capabilities = {
        c for c in ledger.agents[agent_id].individual_capabilities if c.key != key
    }
    # Also drop any cooperative that required this capability.
    ledger.cooperative = {
        ckey: c
        for ckey, c in ledger.cooperative.items()
        if key not in c.requires.get(agent_id, frozenset())
    }


def _apply_add_cooperative(ledger: CapabilityLedger, op: dict[str, Any]) -> None:
    key = op["key"]
    participants = frozenset(op["participants"])
    requires = {
        aid: frozenset(caps) for aid, caps in op.get("requires", {}).items()
    }
    # Validate participants exist.
    for pid in participants:
        if pid not in ledger.agents:
            raise ValueError(f"cooperative {key!r} references unknown agent {pid!r}")
    # Auto-compute cross_substrate from participants' substrates.
    substrates = {ledger.agents[pid].substrate for pid in participants}
    cross_substrate = len(substrates) >= 2
    ledger.cooperative[key] = CooperativeCapability(
        key=key,
        description=op.get("description", ""),
        participants=participants,
        requires=requires,
        cross_substrate=cross_substrate,
        rationale=op.get("rationale", ""),
    )


# ---------------------------------------------------------------------------
# Tool schemas — Anthropic Messages API tool-use format
# ---------------------------------------------------------------------------

LEDGER_OPS_SCHEMA = {
    "type": "array",
    "description": (
        "A list of diff operations to apply to the current ledger. "
        "Each op is an object with a 'type' field and type-specific fields. "
        "Supported types: add_agent, remove_agent, add_capability, "
        "remove_capability, add_cooperative, remove_cooperative."
    ),
    "items": {"type": "object"},
}


def tool_schemas() -> list[dict[str, Any]]:
    """
    Return the list of tool schemas to pass to client.messages.create(tools=...).

    Each schema describes a single harness operation the LLM can invoke.
    """
    return [
        {
            "name": "compute_vol_p",
            "description": (
                "Score a hypothetical ledger state by applying diff operations "
                "to the current ledger and returning its vol_p. Use this to "
                "evaluate candidate actions during PLAN phase. The base ledger "
                "is not modified."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "ops": LEDGER_OPS_SCHEMA,
                    "rationale": {
                        "type": "string",
                        "description": "Why you're constructing this hypothetical.",
                    },
                },
                "required": ["ops"],
            },
        },
        {
            "name": "leverage_report",
            "description": (
                "Return the current ledger's leverage breakdown: per-agent, "
                "per-capability, and per-cooperative marginal contributions "
                "to vol_p. Use this to identify what is load-bearing."
            ),
            "input_schema": {"type": "object", "properties": {}},
        },
        {
            "name": "read_ledger",
            "description": (
                "Return a structured summary of the current ledger state: "
                "agents, their individual capabilities, cooperative "
                "capabilities, and the substrate partition."
            ),
            "input_schema": {"type": "object", "properties": {}},
        },
        {
            "name": "recall",
            "description": (
                "Search past episodes and lessons by text query. Returns up "
                "to k matches ranked by relevance. Use this at the start of "
                "each feature loop and whenever you suspect prior work is "
                "relevant to the current task."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "k": {"type": "integer", "default": 5},
                },
                "required": ["query"],
            },
        },
        {
            "name": "append_memory",
            "description": (
                "Add a new entry to the working buffer. Use this throughout "
                "PLAN/IMPLEMENT/VERIFY to record observations, reasoning, "
                "and intermediate state. The phase is supplied by the harness."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "kind": {
                        "type": "string",
                        "description": "observation | reasoning | action | note | lesson_seed",
                    },
                    "text": {"type": "string"},
                    "importance": {
                        "type": "number",
                        "description": "Initial importance score in [0,1]. Will be re-scored in RETRO.",
                        "default": 0.3,
                    },
                },
                "required": ["kind", "text"],
            },
        },
        {
            "name": "commit",
            "description": (
                "Commit an IMPLEMENT-phase action. The action has already "
                "been taken in the real world; this call records the pre/post "
                "vol_p residual. ledger_ops should be the set of diff "
                "operations that reflect the observed consequences of the "
                "action. expected_vol_p is the vol_p you predicted when you "
                "planned this action in PLAN."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "description": "One-line description of what was done."},
                    "reasoning": {"type": "string", "description": "Why this action was chosen."},
                    "categories_triggered": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Decision categories the action fell into.",
                    },
                    "ledger_ops": LEDGER_OPS_SCHEMA,
                    "expected_vol_p": {
                        "type": "number",
                        "description": "The vol_p you predicted when planning this action.",
                    },
                },
                "required": ["action", "reasoning", "categories_triggered", "ledger_ops", "expected_vol_p"],
            },
        },
        {
            "name": "transition_to",
            "description": (
                "Move the feature loop state machine into the named phase. "
                "Valid targets depend on the current phase — see constitution "
                "§3 for the transition rules."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "phase": {
                        "type": "string",
                        "enum": ["plan", "implement", "verify", "retro"],
                    },
                    "reason": {"type": "string"},
                },
                "required": ["phase"],
            },
        },
        {
            "name": "pause_for_user",
            "description": (
                "Pause the feature loop and return control to the user. Use "
                "this when the PLAN phase surfaces a decision the self-trust "
                "model gates, or when you have unresolved questions you cannot "
                "answer from the current context."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "reason": {"type": "string"},
                    "questions": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "categories": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "The decision categories that triggered this pause.",
                    },
                },
                "required": ["reason"],
            },
        },
        {
            "name": "consolidate",
            "description": (
                "Apply a memory consolidation proposal. Only valid in RETRO "
                "phase. The proposal describes episodes to create, lessons to "
                "distill, importance updates, supersessions, entries to evict, "
                "and side actions to propose (for externalizing organization "
                "knowledge per rubric category 4)."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "importance_updates": {
                        "type": "object",
                        "description": "Mapping from entry_id to new importance score in [0,1].",
                    },
                    "proposed_episodes": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "New episodes to create.",
                    },
                    "proposed_lessons": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "New lessons to distill.",
                    },
                    "supersessions": {
                        "type": "object",
                        "description": "old_lesson_id -> new_lesson_id mapping.",
                    },
                    "entries_to_evict": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "IDs of working-buffer entries safe to evict.",
                    },
                    "side_actions": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": (
                            "Non-memory actions proposed by consolidation "
                            "(e.g., write file for organization knowledge)."
                        ),
                    },
                },
            },
        },
    ]


# ---------------------------------------------------------------------------
# Tool dispatch
# ---------------------------------------------------------------------------
#
# dispatch_tool_call takes a session, a tool name, and the input dict the
# LLM sent. It returns a JSON-serializable result to send back as the
# tool_result content. Errors are returned with is_error semantics so the
# caller can pass them back to the model.


def dispatch_tool_call(
    session: Any,  # HarnessSession (avoiding circular import)
    tool_name: str,
    tool_input: dict[str, Any],
) -> tuple[str, bool]:
    """
    Execute a tool call against the session.

    Returns (result_text, is_error).
    result_text is always a string (JSON-serialized when structured).
    """
    try:
        if tool_name == "compute_vol_p":
            return _handle_compute_vol_p(session, tool_input), False
        if tool_name == "leverage_report":
            return _handle_leverage_report(session), False
        if tool_name == "read_ledger":
            return _handle_read_ledger(session), False
        if tool_name == "recall":
            return _handle_recall(session, tool_input), False
        if tool_name == "append_memory":
            return _handle_append_memory(session, tool_input), False
        if tool_name == "commit":
            return _handle_commit(session, tool_input), False
        if tool_name == "transition_to":
            return _handle_transition_to(session, tool_input), False
        if tool_name == "pause_for_user":
            return _handle_pause(session, tool_input), False
        if tool_name == "consolidate":
            return _handle_consolidate(session, tool_input), False
        return (f"unknown tool: {tool_name!r}", True)
    except PauseForUser:
        # Control-flow exception — must propagate to the agent loop so it can
        # terminate cleanly. Not an error in the usual sense.
        raise
    except Exception as e:  # noqa: BLE001
        return (f"{type(e).__name__}: {e}", True)


def _json_dumps(obj: Any) -> str:
    return json.dumps(obj, default=_json_default, indent=2)


def _json_default(obj: Any) -> Any:
    if isinstance(obj, (set, frozenset)):
        return sorted(obj)
    if hasattr(obj, "__dataclass_fields__"):
        return asdict(obj)
    return str(obj)


def _handle_compute_vol_p(session: Any, tool_input: dict[str, Any]) -> str:
    ops = tool_input.get("ops", [])
    hypothetical, errors = apply_ledger_ops(session.ledger, ops)
    if errors:
        return _json_dumps({"errors": errors, "vol_p": None})
    score = compute_vol_p(hypothetical, session.weights)
    current = compute_vol_p(session.ledger, session.weights)
    return _json_dumps({
        "vol_p": score,
        "current_vol_p": current,
        "delta": score - current,
        "rationale_ack": tool_input.get("rationale", ""),
    })


def _handle_leverage_report(session: Any) -> str:
    report = leverage_report(session.ledger, session.weights)
    return _json_dumps({
        "total_vol_p": report.total_vol_p,
        "per_agent": report.per_agent,
        "top_capabilities": [
            {"agent": aid, "capability": cap_key, "leverage": lev}
            for (aid, cap_key), lev in report.top_k_capabilities(10)
        ],
        "per_cooperative": report.per_cooperative,
    })


def _handle_read_ledger(session: Any) -> str:
    ledger = session.ledger
    return _json_dumps({
        "agents": {
            aid: {
                "substrate": a.substrate,
                "individual_capabilities": [
                    {"key": c.key, "description": c.description}
                    for c in sorted(a.individual_capabilities, key=lambda c: c.key)
                ],
            }
            for aid, a in ledger.agents.items()
        },
        "cooperative": {
            ckey: {
                "description": c.description,
                "participants": sorted(c.participants),
                "requires": {aid: sorted(caps) for aid, caps in c.requires.items()},
                "cross_substrate": c.cross_substrate,
            }
            for ckey, c in ledger.cooperative.items()
        },
        "substrate_partition": ledger.substrate_partition(),
        "m": ledger.m(),
    })


def _handle_recall(session: Any, tool_input: dict[str, Any]) -> str:
    query = tool_input["query"]
    k = tool_input.get("k", 5)
    result = session.memory.recall(query, k)
    return _json_dumps({
        "query": result.query,
        "episodes": [
            {
                "id": ep.id,
                "name": ep.name,
                "description": ep.description,
                "tags": ep.tags,
                "importance": ep.importance,
            }
            for ep in result.episodes
        ],
        "lessons": [
            {
                "id": l.id,
                "statement": l.statement,
                "confidence": l.confidence,
                "domain_tags": l.domain_tags,
                "importance": l.importance,
            }
            for l in result.lessons
        ],
    })


def _handle_append_memory(session: Any, tool_input: dict[str, Any]) -> str:
    phase = (
        session.current_feature.current_phase.value
        if session.current_feature
        else "unknown"
    )
    entry = session.memory.append(
        phase=phase,
        kind=tool_input["kind"],
        text=tool_input["text"],
        importance=tool_input.get("importance", 0.3),
    )
    return _json_dumps({"entry_id": entry.id, "phase": phase})


def _handle_commit(session: Any, tool_input: dict[str, Any]) -> str:
    ops = tool_input["ledger_ops"]
    new_ledger, errors = apply_ledger_ops(session.ledger, ops)
    if errors:
        return _json_dumps({"errors": errors, "committed": False})
    record = session.commit(
        action=tool_input["action"],
        reasoning=tool_input["reasoning"],
        categories_triggered=tool_input["categories_triggered"],
        new_ledger=new_ledger,
        expected_vol_p=tool_input["expected_vol_p"],
    )
    return _json_dumps({
        "commit_id": record.commit_id,
        "expected_delta": record.expected_delta,
        "actual_delta": record.actual_delta,
        "residual": record.residual,
        "committed": True,
    })


def _handle_transition_to(session: Any, tool_input: dict[str, Any]) -> str:
    from .phases import Phase
    target = Phase(tool_input["phase"])
    session.transition_to(target)
    return _json_dumps({
        "current_phase": target.value,
        "reason_ack": tool_input.get("reason", ""),
    })


def _handle_pause(session: Any, tool_input: dict[str, Any]) -> str:
    # Pause is signaled by raising a control-flow exception the driver catches.
    raise PauseForUser(
        reason=tool_input["reason"],
        questions=tool_input.get("questions", []),
        categories=tool_input.get("categories", []),
    )


def _handle_consolidate(session: Any, tool_input: dict[str, Any]) -> str:
    proposal = _build_consolidation_proposal(tool_input)
    result = session.memory.consolidate(proposal)
    session.retro_tuning_log([])  # placeholder; trust updates are separate tools later
    return _json_dumps({
        "accepted_episodes": result.accepted_episodes,
        "accepted_lessons": result.accepted_lessons,
        "evicted_entries": result.evicted_entries,
        "side_actions": [asdict(sa) for sa in result.side_actions],
        "validation_errors": result.validation_errors,
    })


def _build_consolidation_proposal(tool_input: dict[str, Any]) -> ConsolidationProposal:
    """Parse a JSON consolidation input from the LLM into structured form."""
    proposed_episodes = [
        Episode(
            id=ep["id"],
            name=ep["name"],
            description=ep["description"],
            feature_id=ep.get("feature_id", ""),
            entry_ids=list(ep.get("entry_ids", [])),
            importance=float(ep.get("importance", 0.5)),
            tags=list(ep.get("tags", [])),
            timestamp_range=tuple(ep.get("timestamp_range", ("", ""))),
            distilled_lessons=list(ep.get("distilled_lessons", [])),
            metadata=ep.get("metadata", {}),
        )
        for ep in tool_input.get("proposed_episodes", [])
    ]
    proposed_lessons = [
        Lesson(
            id=l["id"],
            statement=l["statement"],
            confidence=float(l.get("confidence", 0.7)),
            source_episodes=list(l.get("source_episodes", [])),
            domain_tags=list(l.get("domain_tags", [])),
            importance=float(l.get("importance", 0.5)),
            superseded_by=l.get("superseded_by"),
            metadata=l.get("metadata", {}),
        )
        for l in tool_input.get("proposed_lessons", [])
    ]
    side_actions = [
        SideAction(
            kind=sa["kind"],
            target=sa["target"],
            content=sa["content"],
            rationale=sa.get("rationale", ""),
        )
        for sa in tool_input.get("side_actions", [])
    ]
    return ConsolidationProposal(
        importance_updates={
            k: float(v) for k, v in tool_input.get("importance_updates", {}).items()
        },
        proposed_episodes=proposed_episodes,
        proposed_lessons=proposed_lessons,
        supersessions=dict(tool_input.get("supersessions", {})),
        entries_to_evict=list(tool_input.get("entries_to_evict", [])),
        side_actions=side_actions,
    )


# ---------------------------------------------------------------------------
# Control-flow exception for pausing the loop
# ---------------------------------------------------------------------------


class PauseForUser(Exception):
    """
    Raised by the pause_for_user tool handler. The agent.py driver catches
    this and returns cleanly so the caller can collect user input and
    resume the feature loop.
    """

    def __init__(
        self,
        reason: str,
        questions: list[str],
        categories: list[str],
    ):
        self.reason = reason
        self.questions = questions
        self.categories = categories
        super().__init__(reason)
