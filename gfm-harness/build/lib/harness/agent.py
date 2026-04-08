"""
LLM driver for the GFM harness.

One conversation per feature loop. The constitution + importance rubric
are loaded once into the system prompt at the start of the loop and
cached via top-level cache_control on messages.create() so subsequent
turns in the same loop pay only the cache-read cost. State that persists
between feature loops (ledger, memory, commit log, trust model) lives
on disk in the session directory, not in conversation history.

Requires the `anthropic` Python SDK. Importing this module does not
require anthropic — the SDK is only imported when run_feature_loop()
is actually invoked, so the rest of the harness remains testable in
environments where the SDK is not installed.

Default model is claude-opus-4-6 with adaptive thinking. Override via
run_feature_loop(model=..., thinking=...) if you need a different model
for a specific task.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from .loop import HarnessSession, save_trust
from .phases import Phase
from .tools import (
    PauseForUser,
    dispatch_tool_call,
    tool_schemas,
)


DEFAULT_MODEL = "claude-opus-4-6"
DEFAULT_MAX_TOKENS = 16000
DEFAULT_MAX_ITERATIONS = 40  # safety cap on the agentic loop per feature


FRAMING_PROMPT = """\
You are operating inside the GFM harness. The full text of your operating
constitution follows; read it with the attention you would give to a
coding-standards document you have to obey. The harness is a measurement
infrastructure — it computes vol_p over the capability ledger and exposes
tools for you to query, modify, and commit changes through. You are
responsible for all forward modeling and world reasoning; the harness only
measures what you give it. See Principle 2.1 in the constitution for the
full framing of this separation.

---

"""


@dataclass
class FeatureLoopResult:
    """Returned when a feature loop terminates."""

    feature_id: str
    terminated_reason: str        # "end_turn" | "paused" | "max_iterations" | "error"
    pause: PauseForUser | None = None
    iterations: int = 0
    final_phase: str = ""
    messages: list[dict[str, Any]] = field(default_factory=list)
    usage_total: dict[str, int] = field(default_factory=dict)


def _build_system_prompt(constitution_path: Path) -> str:
    """
    Construct the system prompt: framing + constitution + importance rubric.
    Loaded once at the start of a feature loop.
    """
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
    task_description: str,
    resume_context: str | None = None,
) -> str:
    """
    The first user message of the feature loop. Includes the task and
    enough current state for the model to orient itself.
    """
    lines = [
        f"# Feature loop: {task_description}",
        "",
        f"Current phase: **{session.current_feature.current_phase.value if session.current_feature else 'plan'}**",
        "",
        "## Current ledger summary",
        f"- Agents: {list(session.ledger.agents.keys())}",
        f"- Cooperative capabilities: {list(session.ledger.cooperative.keys())}",
        f"- Substrate partition (m={session.ledger.m()}): {session.ledger.substrate_partition()}",
        "",
        "## Trust state",
        f"Pause threshold: {session.trust.pause_threshold}",
        f"Categories with non-zero trust: {[k for k, v in session.trust.category_trust.items() if v > 0]}",
        "",
    ]

    # Include recent memory tail so the model has continuity.
    recent_memory = session.memory.tail(10)
    if recent_memory:
        lines.append("## Recent memory (last 10 working-buffer entries)")
        lines.append(session.memory.as_narrative(recent_memory))
        lines.append("")

    if resume_context:
        lines.append("## User response to prior pause")
        lines.append(resume_context)
        lines.append("")

    lines.append(
        "Begin the feature loop in the PLAN phase. Call tools as needed; "
        "use transition_to() when you are ready to move between phases; "
        "call pause_for_user() if you need direction."
    )
    return "\n".join(lines)


def run_feature_loop(
    session: HarnessSession,
    task_description: str,
    constitution_path: Path,
    resume_context: str | None = None,
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    max_iterations: int = DEFAULT_MAX_ITERATIONS,
    verbose: bool = True,
) -> FeatureLoopResult:
    """
    Run a single feature loop end-to-end against a live LLM.

    The harness manages phase state on disk; this function orchestrates
    one conversation with the model, walking the phase machine until the
    loop completes (`stop_reason == "end_turn"`), pauses for user input
    (`PauseForUser` exception from a tool handler), or hits the iteration
    cap.

    Returns a FeatureLoopResult describing how the loop terminated and
    what happened. Trust state is saved to disk automatically at the end
    of the loop so subsequent calls see the updated trust.
    """
    # Lazy import — harness must remain importable without anthropic.
    try:
        import anthropic  # type: ignore
    except ImportError as e:
        raise RuntimeError(
            "run_feature_loop requires the `anthropic` package. "
            "Install with: pip install anthropic"
        ) from e

    client = anthropic.Anthropic()

    # Begin a feature loop in PLAN phase if one isn't already active.
    if session.current_feature is None:
        session.begin_feature(task_description)

    system_prompt = _build_system_prompt(constitution_path)
    tools = tool_schemas()

    user_message = _build_initial_user_message(session, task_description, resume_context)
    messages: list[dict[str, Any]] = [{"role": "user", "content": user_message}]

    iterations = 0
    usage_total = {"input_tokens": 0, "output_tokens": 0, "cache_read_input_tokens": 0}
    pause: PauseForUser | None = None
    terminated_reason = "max_iterations"

    while iterations < max_iterations:
        iterations += 1

        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            # Top-level cache_control auto-caches the largest cacheable block
            # (the system prompt) so subsequent turns pay only the cache-read cost.
            cache_control={"type": "ephemeral"},
            thinking={"type": "adaptive"},
            tools=tools,
            messages=messages,
        )

        # Track token usage. Use getattr for robustness across SDK versions.
        usage = response.usage
        usage_total["input_tokens"] += getattr(usage, "input_tokens", 0) or 0
        usage_total["output_tokens"] += getattr(usage, "output_tokens", 0) or 0
        cache_read = getattr(usage, "cache_read_input_tokens", 0) or 0
        usage_total["cache_read_input_tokens"] += cache_read

        if verbose:
            _print_turn_summary(iterations, response, cache_read)

        # Append the assistant message to the conversation in full — tool_use
        # blocks and any thinking blocks must be preserved for the next turn.
        messages.append({"role": "assistant", "content": response.content})

        stop_reason = response.stop_reason

        if stop_reason == "end_turn":
            terminated_reason = "end_turn"
            break

        if stop_reason == "pause_turn":
            # Server-side tool iteration limit hit; re-send to resume.
            continue

        # Execute any tool calls and collect results for the next turn.
        tool_use_blocks = [b for b in response.content if getattr(b, "type", None) == "tool_use"]
        if not tool_use_blocks:
            # No tool calls and not end_turn — unusual, treat as termination.
            terminated_reason = f"unexpected_stop:{stop_reason}"
            break

        tool_results = []
        caught_pause: PauseForUser | None = None

        for block in tool_use_blocks:
            tool_name = block.name
            tool_input = block.input
            try:
                result_text, is_error = dispatch_tool_call(session, tool_name, tool_input)
            except PauseForUser as exc:
                # The pause tool raises this as a control-flow signal.
                caught_pause = exc
                result_text = json.dumps({
                    "paused": True,
                    "reason": exc.reason,
                    "questions": exc.questions,
                    "categories": exc.categories,
                })
                is_error = False

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result_text,
                "is_error": is_error,
            })

            if caught_pause is not None:
                break  # stop executing further tool calls; we're pausing

        messages.append({"role": "user", "content": tool_results})

        if caught_pause is not None:
            pause = caught_pause
            terminated_reason = "paused"
            break

    # Persist trust state regardless of how we terminated.
    save_trust(session)

    return FeatureLoopResult(
        feature_id=session.current_feature.feature_id if session.current_feature else "",
        terminated_reason=terminated_reason,
        pause=pause,
        iterations=iterations,
        final_phase=(
            session.current_feature.current_phase.value
            if session.current_feature else ""
        ),
        messages=messages,
        usage_total=usage_total,
    )


def _print_turn_summary(iteration: int, response: Any, cache_read: int) -> None:
    """Diagnostic print so the user can see the feature loop advancing."""
    stop = getattr(response, "stop_reason", "?")
    content = getattr(response, "content", [])
    tool_calls = [getattr(b, "name", "?") for b in content if getattr(b, "type", None) == "tool_use"]
    text_parts = [getattr(b, "text", "") for b in content if getattr(b, "type", None) == "text"]
    preview = " ".join(text_parts)[:200].replace("\n", " ")
    cache_marker = f" [cache_read={cache_read}]" if cache_read else ""
    print(f"  [turn {iteration}]{cache_marker} stop={stop} tools={tool_calls}")
    if preview:
        print(f"    text: {preview}{'...' if len(' '.join(text_parts)) > 200 else ''}")
