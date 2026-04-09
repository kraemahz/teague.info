"""
LLM driver for the GFM harness, built on the Claude Agent SDK.

One conversation per feature loop. The constitution + importance rubric
are loaded once into the system_prompt at the start of the loop; the
Agent SDK handles caching of the stable prefix internally. The harness's
9 measurement tools are exposed via an in-process MCP server, and the
SDK's built-in tools (Read, Write, Edit, Bash, Glob, Grep) are
available alongside them under the `allowed_tools` allowlist.

State that persists between feature loops (ledger, memory, commit log,
trust model, goals) lives on disk in the instance directory, not in
conversation history. The `Instance` class owns the persistence.

Requires the `claude-agent-sdk` Python SDK. Importing this module does
not require the SDK at module load time — the SDK is imported lazily
inside run_feature_loop() so the rest of the harness remains testable
in environments where the SDK is not installed.

Default model is claude-opus-4-6 with adaptive thinking. Override via
run_feature_loop(model=..., thinking=...) if needed.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from .loop import HarnessSession, save_trust
from .phases import Phase
from .tools import (
    PauseForUser,
    build_harness_mcp_server,
    mcp_tool_names,
)


DEFAULT_MODEL = "claude-opus-4-6"
# Generous default ceiling. The intent is "only hit by an obvious problem"
# (infinite loop, runaway recursion) rather than "force the agent to budget
# tightly." When running against a logged-in Claude Code session there is
# no per-token cost, so the only thing 500 turns buys us over 40 is
# "RETRO actually runs and the loop ends naturally via end_turn." Per-task
# overrides via CLI flag are a Phase 2 concern.
DEFAULT_MAX_TURNS = 500


# Built-in Agent SDK tools the harness enables by default. The
# research instance's current task (memory consolidation review and
# eventual implementation) needs Read/Glob/Grep for investigation and
# Edit/Write/Bash for actual fixes. AskUserQuestion and Agent (subagent)
# are deliberately OFF for v1 — AskUserQuestion overlaps with our
# pause_for_user and the subagent review loop from constitution §3.1 is
# deferred to Phase 2 of the SDK migration.
DEFAULT_BUILTIN_TOOLS = [
    "Read",
    "Edit",
    "Write",
    "Glob",
    "Grep",
    "Bash",
]


# Default permission mode. acceptEdits means Read/Write/Edit are
# auto-accepted, Bash still prompts, dangerous ops prompt. This gives
# the research agent room to investigate code and make edits, while
# keeping the harness's own trust gates as the primary pause mechanism.
# Future: map trust categories onto per-tool permission modes via
# can_use_tool callback (Phase 2 migration work).
DEFAULT_PERMISSION_MODE = "acceptEdits"


FRAMING_PROMPT = """\
You are operating inside the GFM harness. The full text of your operating
constitution follows; read it with the attention you would give to a
coding-standards document you have to obey. The harness is a measurement
infrastructure — it computes vol_p over the capability ledger and exposes
tools for you to query, modify, and commit changes through. You are
responsible for all forward modeling and world reasoning; the harness only
measures what you give it. See Principle 2.1 in the constitution for the
full framing of this separation.

In addition to the harness's measurement tools
(mcp__gfm-harness__compute_vol_p, leverage_report, read_ledger, recall,
append_memory, commit, transition_to, pause_for_user, consolidate), you
also have access to Claude Code's built-in tools: Read, Edit, Write,
Glob, Grep, Bash. Use them when the task genuinely requires file I/O
or shell access — for example, to read source code during the PLAN
phase, or to edit files during IMPLEMENT. Do not use them as
shortcuts around the harness's measurement flow: all material changes
should still go through the harness's `commit` tool with accurate
ledger_ops and an expected vol_p.

---

"""


@dataclass
class FeatureLoopResult:
    """Returned when a feature loop terminates."""

    feature_id: str
    terminated_reason: str        # "end_turn" | "paused" | "max_turns" | "error"
    pause: PauseForUser | None = None
    turns_observed: int = 0
    final_phase: str = ""
    usage_total: dict[str, int] = field(default_factory=dict)
    last_result_message: Any = None  # sdk.ResultMessage if present


def _build_system_prompt(constitution_path: Path) -> str:
    """Construct the system prompt: framing + constitution + importance rubric."""
    from .memory import IMPORTANCE_RUBRIC

    constitution_text = constitution_path.read_text()
    return (
        FRAMING_PROMPT
        + constitution_text
        + "\n\n---\n\n# Importance Rubric (read this during RETRO consolidation)\n\n"
        + IMPORTANCE_RUBRIC
    )


def _build_initial_user_message(
    session: HarnessSession,
    task_description: str | None,
    resume_context: str | None = None,
    goal_set: Any = None,
    autonomous: bool = False,
) -> str:
    """
    The first user message of the feature loop.

    Two modes:
      - Task-harness mode (autonomous=False, task_description required):
        the user supplies a concrete task; the feature loop starts in
        PLAN phase with the task as the focal objective.
      - Autonomous mode (autonomous=True, task_description optional):
        no task is supplied; the feature loop starts in SELECT phase,
        and the agent proposes its own task from goals + ledger +
        leverage before pausing for user approval.
    """
    current_phase = (
        session.current_feature.current_phase.value
        if session.current_feature else ("select" if autonomous else "plan")
    )

    if autonomous:
        header = "# Autonomous feature loop: propose a task"
    else:
        header = f"# Feature loop: {task_description}"

    lines = [
        header,
        "",
        f"Current phase: **{current_phase}**",
        "",
    ]

    # In autonomous mode, surface the active goal list so SELECT has
    # something to gravitate toward. In task-harness mode the goals are
    # still relevant context but the task itself is the focal objective.
    if goal_set is not None:
        active = goal_set.active() if hasattr(goal_set, "active") else []
        if active:
            lines.append("## Your active goals (priority-ordered)")
            for goal in active:
                lines.append(f"- **[{goal.priority}] {goal.id}**: {goal.statement}")
            lines.append("")

    lines.extend([
        "## Current ledger summary",
        f"- Agents: {list(session.ledger.agents.keys())}",
        f"- Cooperative capabilities: {list(session.ledger.cooperative.keys())}",
        f"- Substrate partition (m={session.ledger.m()}): {session.ledger.substrate_partition()}",
        "",
        "## Trust state",
        f"Pause threshold: {session.trust.pause_threshold}",
        f"Categories with non-zero trust: {[k for k, v in session.trust.category_trust.items() if v > 0]}",
        "",
    ])

    recent_memory = session.memory.tail(10)
    if recent_memory:
        lines.append("## Recent memory (last 10 working-buffer entries)")
        lines.append(session.memory.as_narrative(recent_memory))
        lines.append("")

    if resume_context:
        lines.append("## User response to prior pause")
        lines.append(resume_context)
        lines.append("")

    # The terminal instruction differs by mode.
    if autonomous:
        lines.append(
            "You are in the **SELECT** phase. Your job in SELECT is to "
            "propose the next task for this feature loop, grounded in "
            "your active goals and the current ledger state. Specifically:\n"
            "\n"
            "  1. Orient using mcp__gfm-harness__read_ledger, "
            "     mcp__gfm-harness__leverage_report, and "
            "     mcp__gfm-harness__recall (query for prior work relevant "
            "     to any of the active goals).\n"
            "  2. Reason about which goal(s) to gravitate toward this loop "
            "     and what the highest-leverage concrete task would be "
            "     under current conditions.\n"
            "  3. Draft a proposed task: a clear deliverable, a terminal "
            "     condition, and the category(ies) of decision the task "
            "     falls into. Record it via mcp__gfm-harness__append_memory "
            "     with kind='reasoning' and importance=0.6.\n"
            "  4. Call mcp__gfm-harness__pause_for_user with "
            "     categories=['task_selection'], including the proposed "
            "     task verbatim in the `reason` field so the user can "
            "     approve or redirect it.\n"
            "\n"
            "Do NOT transition out of SELECT or begin executing the "
            "proposed task in this session. The pause is the end of the "
            "SELECT phase for this session; the user will either approve "
            "(and you resume in PLAN on the next run) or redirect (and "
            "you re-propose with their feedback)."
        )
    else:
        lines.append(
            "Begin the feature loop in the PLAN phase. Call tools as "
            "needed; use mcp__gfm-harness__transition_to when you are "
            "ready to move between phases; call "
            "mcp__gfm-harness__pause_for_user if you need direction from "
            "the user."
        )
    return "\n".join(lines)


async def _run_feature_loop_async(
    session: HarnessSession,
    task_description: str | None,
    constitution_path: Path,
    resume_context: str | None,
    model: str,
    max_turns: int,
    builtin_tools: list[str],
    permission_mode: str,
    cwd: str | Path | None,
    verbose: bool,
    goal_set: Any = None,
    autonomous: bool = False,
) -> FeatureLoopResult:
    """Async implementation; run_feature_loop() wraps this in asyncio.run()."""
    from claude_agent_sdk import (
        AssistantMessage,
        ClaudeAgentOptions,
        ResultMessage,
        SystemMessage,
        TextBlock,
        ThinkingBlock,
        ThinkingConfigAdaptive,
        ToolUseBlock,
        UserMessage,
        query,
    )

    # Begin a feature loop if one isn't already active. Autonomous mode
    # starts in SELECT phase; task-harness mode starts in PLAN.
    if session.current_feature is None:
        if autonomous:
            state = session.begin_feature(
                task_description or "(autonomous: task to be proposed in SELECT)"
            )
            # Override the default PLAN starting phase so the agent's
            # initial message matches the phase machine state.
            state.current_phase = Phase.SELECT
        else:
            if task_description is None:
                raise ValueError(
                    "task_description is required in non-autonomous mode; "
                    "pass autonomous=True to have the agent propose a task."
                )
            session.begin_feature(task_description)

    # Reset any stale pause marker from a previous loop.
    session._pending_pause = None

    system_prompt = _build_system_prompt(constitution_path)
    harness_server = build_harness_mcp_server(session)

    allowed_tools = list(builtin_tools) + mcp_tool_names()

    # pause_for_user is a notification mechanism, not a hard control-flow
    # stop. When the agent fires it, session._pending_pause is set and the
    # CLI surfaces the question at end-of-loop — but the agent is free to
    # keep working on orthogonal parts of its current phase or to wrap up
    # cleanly via end_turn. A legitimate free agent should be able to
    # parallelize: "I need input on X" does not imply "everything else
    # must stop" — the parallelism is a feature, not a bug. See
    # constitution §3.1 (SELECT) and §4.9 (task_selection).

    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
        allowed_tools=allowed_tools,
        mcp_servers={"gfm-harness": harness_server},
        permission_mode=permission_mode,
        model=model,
        # ThinkingConfigAdaptive is a TypedDict; the "type" field is required
        # and must be explicitly provided or the subprocess CLI transport
        # throws KeyError when serializing.
        thinking=ThinkingConfigAdaptive(type="adaptive"),
        max_turns=max_turns,
        cwd=cwd,
    )

    initial_message = _build_initial_user_message(
        session,
        task_description,
        resume_context=resume_context,
        goal_set=goal_set,
        autonomous=autonomous,
    )

    usage_total = {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0,
    }
    turns_observed = 0
    last_result: Any = None
    terminated_reason = "end_turn"

    try:
        async for message in query(prompt=initial_message, options=options):
            if isinstance(message, AssistantMessage):
                turns_observed += 1
                if verbose:
                    _print_assistant_turn(turns_observed, message)
                # Log assistant text and tool calls into session memory
                # as notes — gives RETRO a trace of what the agent did.
                _log_assistant_message(session, message)
            elif isinstance(message, UserMessage):
                # Tool results come back as UserMessages in the SDK stream.
                # They're the SDK's internal bookkeeping; we don't need to
                # log them because the tool handlers already logged the
                # relevant content to the working buffer.
                pass
            elif isinstance(message, SystemMessage):
                # SessionStart, notifications, etc. — ignore for v1.
                pass
            elif isinstance(message, ResultMessage):
                last_result = message
                terminated_reason = getattr(message, "stop_reason", "end_turn") or "end_turn"
                _accumulate_usage(usage_total, message)
                if verbose:
                    _print_result_summary(message)
                break
    except Exception as e:
        # Unexpected errors terminate the loop but still let us persist state.
        # Full traceback is shown under verbose to aid debugging; callers
        # running in scripted contexts get a compact error string.
        if verbose:
            import traceback
            print(f"  [error] {type(e).__name__}: {e}")
            traceback.print_exc(limit=5)
        terminated_reason = f"error:{type(e).__name__}"

    # Did the agent signal a pause at any point?
    pause = session._pending_pause
    if pause is not None:
        terminated_reason = "paused"

    # Fallback memory bounds enforcement. The agent's normal RETRO
    # consolidate() also calls evict() (post the round-3 fix), but if the
    # loop terminated without reaching RETRO — for example because it hit
    # max_turns mid-VERIFY, or crashed in IMPLEMENT, or was paused early
    # in PLAN — the working buffer can be left over its capacity bound.
    # This is harm reduction: the harness enforces the bound mechanically
    # so the next loop starts in a clean state. It does NOT do any
    # cognitive consolidation work (proposing episodes/lessons) — that's
    # the agent's job, and a future feature loop can do it.
    _run_fallback_eviction(session, terminated_reason, verbose)

    # Persist trust state regardless of how we terminated.
    save_trust(session)

    return FeatureLoopResult(
        feature_id=session.current_feature.feature_id if session.current_feature else "",
        terminated_reason=terminated_reason,
        pause=pause,
        turns_observed=turns_observed,
        final_phase=(
            session.current_feature.current_phase.value
            if session.current_feature else ""
        ),
        usage_total=usage_total,
        last_result_message=last_result,
    )


def run_feature_loop(
    session: HarnessSession,
    task_description: str | None,
    constitution_path: Path,
    resume_context: str | None = None,
    model: str = DEFAULT_MODEL,
    max_turns: int = DEFAULT_MAX_TURNS,
    builtin_tools: list[str] | None = None,
    permission_mode: str = DEFAULT_PERMISSION_MODE,
    cwd: str | Path | None = None,
    verbose: bool = True,
    goal_set: Any = None,
    autonomous: bool = False,
) -> FeatureLoopResult:
    """
    Run a single feature loop end-to-end against a live LLM via the
    Claude Agent SDK.

    Two modes:
      - Task-harness mode (default): pass a task_description. The loop
        starts in PLAN and works toward the task.
      - Autonomous mode (autonomous=True): task_description may be None.
        Pass goal_set (typically instance.goal_set) so the agent can
        read the active goals when proposing a task. The loop starts
        in SELECT phase; the agent proposes a task and pauses for
        user approval via the task_selection category.

    This is a synchronous wrapper around the async SDK driver. If the
    caller is already in an async context, use _run_feature_loop_async
    directly instead (it's a private coroutine that does the actual work).
    """
    # Lazy import — harness must remain importable without the SDK.
    try:
        import claude_agent_sdk  # noqa: F401
    except ImportError as e:
        raise RuntimeError(
            "run_feature_loop requires the `claude-agent-sdk` package. "
            "Install with: pip install claude-agent-sdk"
        ) from e

    return asyncio.run(
        _run_feature_loop_async(
            session=session,
            task_description=task_description,
            constitution_path=constitution_path,
            resume_context=resume_context,
            model=model,
            max_turns=max_turns,
            builtin_tools=builtin_tools if builtin_tools is not None else list(DEFAULT_BUILTIN_TOOLS),
            permission_mode=permission_mode,
            cwd=cwd,
            verbose=verbose,
            goal_set=goal_set,
            autonomous=autonomous,
        )
    )


# ---------------------------------------------------------------------------
# Diagnostics and message logging
# ---------------------------------------------------------------------------


def _log_assistant_message(session: HarnessSession, message: Any) -> None:
    """Record the assistant's text and tool calls to the working buffer."""
    from claude_agent_sdk import TextBlock, ThinkingBlock, ToolUseBlock

    text_parts: list[str] = []
    tool_calls: list[str] = []
    for block in getattr(message, "content", []):
        if isinstance(block, TextBlock):
            text_parts.append(block.text)
        elif isinstance(block, ToolUseBlock):
            tool_calls.append(block.name)
        elif isinstance(block, ThinkingBlock):
            # Thinking blocks are internal reasoning; don't log them to
            # the working buffer (they'd dominate the trace). RETRO can
            # see them via the commit log if we add that later.
            pass

    text = "\n".join(text_parts).strip()
    if text or tool_calls:
        session.memory.append(
            phase=(
                session.current_feature.current_phase.value
                if session.current_feature else "plan"
            ),
            kind="action" if tool_calls else "reasoning",
            text=(text if text else "(tool call only)"),
            importance=0.3,
            metadata={
                "source": "assistant",
                "tool_calls": tool_calls,
            },
        )


def _accumulate_usage(total: dict[str, int], result_message: Any) -> None:
    """
    Pull usage fields off a ResultMessage and add to the running total.
    ResultMessage.usage is a plain dict (dict[str, Any]) in the Agent SDK,
    not an attribute-bearing object — use .get() not getattr.
    """
    usage = getattr(result_message, "usage", None)
    if not isinstance(usage, dict):
        return
    for key in (
        "input_tokens",
        "output_tokens",
        "cache_read_input_tokens",
        "cache_creation_input_tokens",
    ):
        value = usage.get(key, 0) or 0
        if key in total:
            total[key] += value
        else:
            total[key] = value
    # Also capture total_cost_usd if present — useful for per-loop budgeting.
    total_cost = getattr(result_message, "total_cost_usd", None)
    if total_cost is not None:
        total["total_cost_usd"] = total_cost


def _run_fallback_eviction(
    session: HarnessSession,
    terminated_reason: str,
    verbose: bool,
) -> None:
    """
    Harness-side fallback eviction. Runs at the end of every feature loop
    regardless of how it terminated, to enforce memory layer bounds even
    when the agent's normal RETRO did not run.

    The fallback is mechanical: it just calls memory.evict() to drop
    over-cap entries, then leaves a memory note describing what happened.
    It does NOT propose episodes or lessons — that's the agent's
    cognitive work, and forcing it from the harness side would taint the
    audit trail with hallucinated consolidation.

    Note level on the fallback memory entry uses importance 0.85 because
    "the harness fell back to bounds enforcement" is the same shape as
    the rubric's "loss of function" category — a structural failure of
    the normal flow that future feature loops should be able to detect
    and reason about.
    """
    # Important ordering: write the diagnostic note FIRST, then call
    # evict(). Writing the note after eviction would push the buffer
    # back over its cap by 1 (the note itself is an entry). By writing
    # the note first, evict() sees it in the buffer when it runs and
    # the note's high importance (0.85) means it survives against the
    # lowest-importance entries, while the bound is correctly enforced.
    needs_check = (
        len(session.memory.working_buffer) > session.memory.working_buffer_max_entries
        or len(session.memory.episodes) > session.memory.episodes_max_count
        or len(session.memory.lessons) > session.memory.lessons_max_count
    )

    if not needs_check:
        return  # No bound violations; nothing for the fallback to do.

    pre_eviction_counts = {
        "working_buffer": len(session.memory.working_buffer),
        "episodes": len(session.memory.episodes),
        "lessons": len(session.memory.lessons),
    }

    placeholder_note = (
        f"Harness fallback eviction fired. The feature loop terminated as "
        f"'{terminated_reason}' before normal RETRO consolidation could "
        f"enforce memory bounds. Pre-eviction layer counts: "
        f"working_buffer={pre_eviction_counts['working_buffer']}, "
        f"episodes={pre_eviction_counts['episodes']}, "
        f"lessons={pre_eviction_counts['lessons']}. "
        f"A future feature loop should run RETRO consolidation to produce "
        f"proper episodes and lessons from the work this loop did before "
        f"termination — the fallback only enforces bounds, it does not "
        f"do cognitive consolidation."
    )

    try:
        session.memory.append(
            phase="retro",
            kind="note",
            text=placeholder_note,
            importance=0.85,
            metadata={
                "fallback_eviction": True,
                "terminated_reason": terminated_reason,
                "pre_eviction_counts": pre_eviction_counts,
            },
        )
    except Exception as e:  # noqa: BLE001
        if verbose:
            print(f"  [fallback eviction note failed] {type(e).__name__}: {e}")

    try:
        report = session.memory.evict()
    except Exception as e:  # noqa: BLE001
        if verbose:
            print(f"  [fallback eviction failed] {type(e).__name__}: {e}")
        return

    if verbose:
        print(
            f"  [fallback eviction] terminated={terminated_reason!r} "
            f"evicted entries={len(report.evicted_entries)} "
            f"episodes={len(report.evicted_episodes)} "
            f"lessons={len(report.evicted_lessons)}"
        )


def _print_assistant_turn(turn: int, message: Any) -> None:
    """Per-turn diagnostic summary."""
    from claude_agent_sdk import TextBlock, ToolUseBlock

    content = getattr(message, "content", [])
    tool_calls = [getattr(b, "name", "?") for b in content if isinstance(b, ToolUseBlock)]
    text_parts = [getattr(b, "text", "") for b in content if isinstance(b, TextBlock)]
    preview = " ".join(text_parts)[:200].replace("\n", " ")
    print(f"  [turn {turn}] tools={tool_calls}")
    if preview:
        print(f"    text: {preview}{'...' if len(' '.join(text_parts)) > 200 else ''}")


def _print_result_summary(result_message: Any) -> None:
    """Diagnostic summary printed when the stream ends."""
    usage = getattr(result_message, "usage", None)
    stop = getattr(result_message, "stop_reason", "?")
    num_turns = getattr(result_message, "num_turns", "?")
    cost = getattr(result_message, "total_cost_usd", None)
    print(f"  [stream end] stop_reason={stop} num_turns={num_turns}")
    if isinstance(usage, dict) and usage:
        in_tokens = usage.get("input_tokens", 0) or 0
        out_tokens = usage.get("output_tokens", 0) or 0
        cache_read = usage.get("cache_read_input_tokens", 0) or 0
        cache_write = usage.get("cache_creation_input_tokens", 0) or 0
        print(
            f"    usage: input={in_tokens} output={out_tokens} "
            f"cache_read={cache_read} cache_write={cache_write}"
        )
    if cost is not None:
        print(f"    total_cost_usd: {cost:.4f}")
