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
    # The Agent tool is enabled so the main agent can invoke subagents
    # defined via ClaudeAgentOptions(agents={...}). Currently used for
    # the codex-review subagent that wraps the full codex CLI round
    # (invocation + capture + parse + return structured findings) for
    # any review flow — paper, spec, code, security, etc. See
    # constitution §8.
    "Agent",
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
        AgentDefinition,
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

    # The codex-review subagent wraps a single codex CLI invocation:
    # it runs codex against a target directory, captures the output to
    # a file, parses the final assessment section, and returns a
    # structured findings list to the calling agent. The subagent is
    # domain-agnostic — it handles paper reviews, spec reviews, code
    # reviews, security reviews, and post-refactor sanity checks with
    # the same interface. The calling agent provides the verbatim codex
    # prompt plus optional round/prior-context metadata; the subagent
    # does not know or care what domain it is in.
    #
    # Why this is a subagent rather than inline Bash+Read on the main
    # agent: codex output is 50-250KB per review round and the main
    # agent would burn its context window on the raw exploration trace.
    # The subagent runs codex, parses the assessment, and returns only
    # the ~500-token findings list, so the main agent sees only
    # actionable severity-tagged issues.
    #
    # Critical constraints (see constitution §8):
    # - Output is pure prose, never JSON. A prior JSON-formatted attempt
    #   triggered OpenAI's distillation-protection system and got the
    #   project banned from the API.
    # - Codex invocations always use `--sandbox read-only` and always
    #   capture to /tmp/codex_review_rN.txt (unredirected stdout is
    #   truncated by the Bash tool and costs a full retry).
    # - The caller owns the working-directory scope decision. The
    #   sandbox is scoped to the working directory and its descendants,
    #   so the caller must pick a directory wide enough to include
    #   every file the review prompt references.
    codex_review = AgentDefinition(
        description=(
            "Invoke codex (GPT-5.4 via /opt/homebrew/bin/codex exec) on "
            "a target directory, capture its output, parse the final "
            "assessment, and return structured P0/P1/P2/P3 findings. Use "
            "this for any codex-based review: paper, spec, code, "
            "security, refactor sanity check, or other. Domain-agnostic "
            "wrapper around a single codex invocation."
        ),
        prompt=(
            "You are the codex-review subagent for the GFM harness. Your "
            "single job is to wrap a single codex CLI invocation: run "
            "codex against a target, capture its output to a file, parse "
            "the final assessment section, and return a structured "
            "findings list to the calling agent.\n"
            "\n"
            "You are domain-agnostic. The calling agent handles paper "
            "reviews, spec reviews, code reviews, security reviews, "
            "refactor sanity checks, and anything else codex can reason "
            "about. You do not know or care which domain you are in — "
            "you just run codex with the prompt you were given.\n"
            "\n"
            "The calling agent sends a task description with these fields:\n"
            "\n"
            "  Working directory: <absolute path to a directory that "
            "encompasses all files the review prompt references or "
            "implies>\n"
            "  Round: <optional integer; defaults to 1 if omitted>\n"
            "  Prior rounds addressed: <optional prose summary, one "
            "entry per round>\n"
            "  Review prompt: <the actual prompt to pass to codex, verbatim>\n"
            "\n"
            "IMPORTANT — sandbox scope. Codex runs with "
            "--sandbox read-only, which scopes its file access to the "
            "working directory and its descendants. The calling agent "
            "is responsible for choosing a working directory wide "
            "enough to include every file the review needs to see. If "
            "the review compares two files in different subtrees "
            "(e.g., a spec in `specs/` against an implementation in "
            "`workers/`), the working directory must be a common "
            "ancestor of both — typically the repo root. You do not "
            "and cannot validate this; the caller owns the scope "
            "decision. If codex returns a finding like \"I cannot find "
            "the implementation file\" or the capture file contains a "
            "permission-denied error from the sandbox, return \"ERROR: "
            "working directory too narrow — codex could not access a "
            "referenced file\" and include the last ~500 characters of "
            "the capture file so the caller can widen the scope and "
            "retry.\n"
            "\n"
            "If Working directory is missing or not a directory, return "
            "\"ERROR: missing or invalid Working directory\" and stop. "
            "Review prompt is required; if missing, return \"ERROR: "
            "missing Review prompt\" and stop.\n"
            "\n"
            "Procedure:\n"
            "\n"
            "1. Compose the full codex prompt. Start with the verbatim "
            "Review prompt from the task description. If Prior rounds "
            "addressed is present, append:\n"
            "\n"
            "     Prior review rounds have already addressed the "
            "following issues. Do not re-report them:\n"
            "\n"
            "     {Prior rounds addressed}\n"
            "\n"
            "   Then append:\n"
            "\n"
            "     Use severity labels when surfacing issues: P0 for "
            "soundness-critical, P1 for substantive, P2 for clarity, "
            "P3 for minor. If no new P0 or P1 issues remain from this "
            "pass, state 'CONVERGED: no new P0 or P1 findings' "
            "explicitly.\n"
            "\n"
            "2. Run codex with mandatory file capture. Use the Bash "
            "tool:\n"
            "\n"
            "     cd {Working directory} && /opt/homebrew/bin/codex "
            "exec --sandbox read-only \"<composed prompt from step 1>\" "
            "> /tmp/codex_review_r{Round}.txt 2>&1\n"
            "\n"
            "   The cd is load-bearing: it sets the sandbox scope. "
            "Always use --sandbox read-only. Always capture to "
            "/tmp/codex_review_r{Round}.txt (unredirected codex output "
            "is truncated by the Bash tool and costs a full retry). If "
            "Round was not provided, use r1.\n"
            "\n"
            "3. Read the capture file. Scan for the final assessment "
            "section. Codex's natural format is prose with a thinking "
            "trace followed by a final structured assessment. Look for "
            "markers like \"**Assessment**\", \"**Overall**\", "
            "\"**Findings**\", \"**Major Issues**\", \"**P0**\", or "
            "similar. Everything before the final assessment is "
            "exploration trace and should be discarded.\n"
            "\n"
            "4. Normalize codex's severity labels into P0/P1/P2/P3. "
            "Codex may use different words depending on the domain:\n"
            "     - \"critical\", \"blocker\", \"soundness-critical\", "
            "\"major issue\"     → P0\n"
            "     - \"substantive\", \"significant\", \"P1\", "
            "\"secondary issue\"   → P1\n"
            "     - \"clarity\", \"minor issue\", \"style\", \"P2\"        "
            "           → P2\n"
            "     - \"nit\", \"typo\", \"cosmetic\", \"P3\"                   "
            "      → P3\n"
            "   When in doubt, default to the more severe bucket.\n"
            "\n"
            "5. Return the structured findings as prose. Required "
            "format:\n"
            "\n"
            "     <If codex said CONVERGED or equivalent:>\n"
            "       CONVERGED: no new P0 or P1 findings.\n"
            "       {Optional P2/P3 findings from this round, if any.}\n"
            "\n"
            "     <Otherwise:>\n"
            "       P0 (critical):\n"
            "         - <file:line or location>: <one-line finding>\n"
            "         - ...\n"
            "       P1 (substantive):\n"
            "         - ...\n"
            "       P2 (clarity):\n"
            "         - ...\n"
            "       P3 (minor):\n"
            "         - ...\n"
            "\n"
            "   If a severity bucket is empty, omit that section "
            "entirely. Preserve codex's file:line references when "
            "codex gave them — the calling agent uses those to apply "
            "fixes.\n"
            "\n"
            "CRITICAL CONSTRAINTS:\n"
            "\n"
            "- Never return the raw codex output. The whole point of "
            "this subagent is that the calling agent sees only the "
            "parsed findings, not the 50-250KB of exploration trace "
            "codex produces. If you return raw output you have failed "
            "the subagent's purpose.\n"
            "\n"
            "- Never produce JSON output. A prior attempt to force "
            "JSON-formatted reviews triggered OpenAI's "
            "distillation-protection system and got the project banned "
            "from the API. The chain stays prose-only from codex "
            "through this subagent to the calling agent.\n"
            "\n"
            "- Never run codex without the file-redirect "
            "(`> /tmp/codex_review_rN.txt 2>&1`). Unredirected codex "
            "stdout is truncated by the Bash tool and costs a full "
            "retry invocation.\n"
            "\n"
            "- Never modify files outside /tmp/. Your only filesystem "
            "write is the codex capture file. You do not apply "
            "findings, edit source, or commit anything.\n"
            "\n"
            "- If codex fails (nonzero exit code, empty capture file, "
            "no parseable assessment section), return \"ERROR: codex "
            "invocation failed\" plus the last ~500 characters of the "
            "capture file. Do not retry; do not try to diagnose; "
            "return the error to the caller and let them decide."
        ),
        tools=["Bash", "Read"],
    )

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
        agents={"codex-review": codex_review},
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

    # Snapshot the consolidation counter before the loop runs. The fallback
    # eviction path at end-of-loop compares this to the post-loop counter
    # to determine whether the agent called consolidate() during this loop.
    consolidations_before = session.memory.consolidations_applied

    # Emit a startup observation to the working buffer. This is the harness
    # side of constitution §2.8: the user starting a feature loop (whether
    # by providing a task description, or by resuming a paused loop, or
    # by kicking off autonomous mode) is observational evidence of the
    # user exercising framing capabilities. The agent reads this entry
    # during PLAN and can act on it — typically by adding or updating the
    # `user` ledger entry with observed capabilities. No trust bootstrap
    # is applied; see §2.8 for why.
    _emit_startup_observation(
        session,
        task_description=task_description,
        resume_context=resume_context,
        autonomous=autonomous,
    )

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
    agent_consolidated = (
        session.memory.consolidations_applied > consolidations_before
    )
    _run_fallback_eviction(session, terminated_reason, agent_consolidated, verbose)

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


def _emit_startup_observation(
    session: HarnessSession,
    task_description: str | None,
    resume_context: str | None,
    autonomous: bool,
) -> None:
    """
    Write a working-buffer entry at loop start describing the startup
    event. The agent reads this during PLAN phase as observational
    evidence that the user has exercised framing capabilities.

    See constitution §2.8 for the framework rationale. No trust bootstrap
    is performed — the user is the root of authority by construction, not
    a node in a behaviorally-modeled trust chain.

    The entry is appended with importance 0.6 — high enough to survive
    an initial consolidation pass, low enough to be consolidated into an
    episode during RETRO and evicted afterward. An agent that reads the
    observation and acts on it (by adding `user` to the ledger, for
    example) does not need the raw entry to persist beyond that point.
    """
    is_resume = resume_context is not None and resume_context.strip() != ""

    if autonomous and not is_resume:
        # Autonomous mode with no resume context: the user started the
        # instance but did not specify a task. The framing act is
        # "invoke me with authority to pick my own task from the goal
        # set", which is still an observation — just a weaker one,
        # because the content of the task comes from the goal set
        # rather than from the user's direct articulation.
        body = (
            "Feature loop started in autonomous mode. The user exercised "
            "framing capability by invoking the harness and authorizing "
            "task selection from the active goal set, but did not provide "
            "a specific task description. This is evidence of the user's "
            "framing and task_selection_delegation capabilities. "
            "Consider whether the ledger contains a `user` entry; if not, "
            "this observation is standing reason to add one during PLAN "
            "or RETRO per §2.8."
        )
    elif is_resume and task_description:
        body = (
            f"Feature loop resumed with new task. Resume context: "
            f"{resume_context[:500]}{'...' if len(resume_context) > 500 else ''}\n"
            f"New task: {task_description[:500]}"
            f"{'...' if task_description and len(task_description) > 500 else ''}\n"
            f"This is evidence of the user exercising long_tail_context "
            f"(carrying state across a session boundary that exceeded the "
            f"agent's working memory) and task_articulation (specifying "
            f"the next piece of work). See §2.8: if the ledger has no "
            f"`user` entry, or lacks `long_tail_context` on the existing "
            f"entry, update it during PLAN or RETRO."
        )
    elif is_resume:
        body = (
            f"Feature loop resumed. Resume context: "
            f"{resume_context[:800]}{'...' if len(resume_context) > 800 else ''}\n"
            f"This is evidence of the user exercising long_tail_context "
            f"(carrying state across a session boundary). See §2.8."
        )
    elif task_description:
        body = (
            f"Feature loop started with user-specified task. "
            f"Task: {task_description[:800]}"
            f"{'...' if len(task_description) > 800 else ''}\n"
            f"This is evidence of the user exercising task_articulation "
            f"and framing capabilities: the authority to specify what "
            f"work matters and articulate it in actionable terms. See "
            f"§2.8: if the ledger has no `user` entry, this observation "
            f"is standing reason to add one."
        )
    else:
        # Unusual case: non-autonomous, no task, no resume. Shouldn't
        # normally happen given CLI validation, but be defensive.
        body = (
            "Feature loop started with no task description, no resume "
            "context, and autonomous=False. This is an unusual startup "
            "state that should not occur in normal operation; record it "
            "but do not treat it as a meaningful observation."
        )

    try:
        session.memory.append(
            phase="plan",
            kind="observation",
            text=body,
            importance=0.6,
            metadata={
                "source": "user_framing_channel",
                "startup_observation": True,
                "autonomous": autonomous,
                "is_resume": is_resume,
                "has_task": task_description is not None and task_description.strip() != "",
            },
        )
    except Exception as e:  # noqa: BLE001
        # Startup observation is best-effort — if the append fails
        # (e.g., disk full, memory locked), the loop should still run.
        # The agent can still function without the observation; it just
        # won't have the explicit user-channel prompt in its buffer.
        import traceback
        print(f"  [startup observation failed] {type(e).__name__}: {e}")
        traceback.print_exc(limit=2)


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
    agent_consolidated: bool,
    verbose: bool,
) -> None:
    """
    Harness-side fallback eviction. Runs at the end of every feature loop
    regardless of how it terminated, to enforce memory layer bounds.

    Two distinct cases, distinguished by ``agent_consolidated``:

    1. **Agent never consolidated** (``agent_consolidated=False``). This
       is a real failure mode: the loop crashed or paused before RETRO,
       or the agent skipped consolidation. The memory note uses the
       ``fallback_no_consolidation`` tag and importance 0.85 (structural
       failure, future loops should detect and reason about it). The next
       feature loop should run cognitive consolidation over the carried-
       forward working buffer.

    2. **Agent consolidated but buffer still over bound**
       (``agent_consolidated=True``). This is routine backstop trimming:
       the agent's consolidate proposal didn't evict enough entries to
       get back under the hard limit, so the harness drops the N
       lowest-importance excess entries mechanically. The memory note
       uses ``fallback_backstop_trim`` and importance 0.5 (informational,
       not a failure). No action needed from the next feature loop.

    The fallback is mechanical in both cases: it just calls memory.evict()
    to drop over-cap entries, then leaves a memory note describing what
    happened. It does NOT propose episodes or lessons — that's the
    agent's cognitive work, and forcing it from the harness side would
    taint the audit trail with hallucinated consolidation.
    """
    # Important ordering: write the diagnostic note FIRST, then call
    # evict(). Writing the note after eviction would push the buffer
    # back over its cap by 1 (the note itself is an entry). By writing
    # the note first, evict() sees it in the buffer when it runs and
    # the note's importance means it either survives (failure case, 0.85)
    # or can itself be evicted (routine case, 0.5) against the lowest-
    # importance entries, while the bound is correctly enforced.
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

    if agent_consolidated:
        placeholder_note = (
            f"Harness backstop trim. The agent ran consolidate() during this "
            f"loop, but the working buffer remained above the hard bound "
            f"({pre_eviction_counts['working_buffer']} entries vs "
            f"{session.memory.working_buffer_max_entries} max), so the "
            f"harness mechanically dropped the lowest-importance excess "
            f"entries to enforce the bound. This is routine: the agent's "
            f"cognitive consolidation ran and the backstop only trimmed "
            f"the residual."
        )
        note_importance = 0.5
        note_tag = "fallback_backstop_trim"
    else:
        placeholder_note = (
            f"Harness fallback eviction fired. The feature loop terminated as "
            f"'{terminated_reason}' and the agent did not run consolidate() "
            f"during this loop. Pre-eviction layer counts: "
            f"working_buffer={pre_eviction_counts['working_buffer']}, "
            f"episodes={pre_eviction_counts['episodes']}, "
            f"lessons={pre_eviction_counts['lessons']}. "
            f"A future feature loop should run RETRO consolidation to produce "
            f"proper episodes and lessons from the work this loop did before "
            f"termination — the fallback only enforces bounds, it does not "
            f"do cognitive consolidation."
        )
        note_importance = 0.85
        note_tag = "fallback_no_consolidation"

    try:
        session.memory.append(
            phase="retro",
            kind="note",
            text=placeholder_note,
            importance=note_importance,
            metadata={
                note_tag: True,
                "terminated_reason": terminated_reason,
                "agent_consolidated": agent_consolidated,
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
        label = "backstop trim" if agent_consolidated else "fallback eviction"
        print(
            f"  [{label}] terminated={terminated_reason!r} "
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
