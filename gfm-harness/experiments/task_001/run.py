"""
Runner for task_001: the first feature loop executed against a live LLM.

Usage:
    # Set your API key
    export ANTHROPIC_API_KEY=sk-ant-...

    # Run (no arguments needed — uses default task description below)
    python3 experiments/task_001/run.py

    # Or run with a custom task description
    python3 experiments/task_001/run.py --task "Your task here"

    # Resume from a pause, supplying the user response inline
    python3 experiments/task_001/run.py --resume "Yes, proceed with option B"

The session state (ledger, memory, commits, trust) lives in
experiments/task_001/session/ and persists across runs. Delete that
directory to reset.
"""

from __future__ import annotations

# Self-bootstrap so the script runs without PYTHONPATH ceremony.
import sys
from pathlib import Path
_HARNESS_ROOT = Path(__file__).resolve().parents[2]
if str(_HARNESS_ROOT) not in sys.path:
    sys.path.insert(0, str(_HARNESS_ROOT))

import argparse

from experiments.task_001.ledger import build_initial_ledger
from harness.agent import run_feature_loop
from harness.loop import load_session


# -----------------------------------------------------------------------------
# TASK DESCRIPTION
# -----------------------------------------------------------------------------
#
# This is the first real task that will run through the harness. The LLM
# driver will read this at the start of the feature loop and use it as
# the focal objective for the PLAN phase.
#
# Keep it concrete and small enough that one feature loop can complete it.
# Good first tasks have:
#   - A clear deliverable (file written, script run, question answered)
#   - Scope that touches multiple decision categories so we can observe
#     the self-trust pause behavior
#   - Some reference to the current ledger so leverage queries are
#     meaningful rather than abstract
#
# The default below is a placeholder; replace it with a task description
# that matches your current work. The harness will score whatever you
# ask it to do, so pick something you actually want done.

DEFAULT_TASK_DESCRIPTION = """\
Review the memory consolidation machinery in harness/memory.py — specifically
MemoryArchive.consolidate(), MemoryArchive.recall(), MemoryArchive.evict(),
and the IMPORTANCE_RUBRIC constant — and identify the single weakest point:
the place most likely to produce bad behavior when the harness runs against
real workloads over many feature loops.

This is a read-and-reason task with no mutation. You may not commit any
ledger changes, write any files, or modify harness/memory.py. The deliverable
is a written plan posted via append_memory(), followed by a pause_for_user
for my approval. If I approve the plan, a subsequent feature loop will
execute it; this loop stops at the pause.

Methodology (use the harness's own tools to reason about this):

  1. Read harness/memory.py and the IMPORTANCE_RUBRIC constant carefully.
     The memory archive is in gfm-harness/harness/memory.py; the rubric is
     at the top of that file. Note: reading files outside the current
     working tree is a deep_filesystem_trawl operation if you don't know
     where they live — they live at the absolute path
     /Users/teague/Code/kraemahz/teague.info/gfm-harness/harness/memory.py
     so no trawl is required.

  2. Test the validation surface of consolidate() by constructing
     compute_vol_p hypothetical scenarios that probe edge cases:
       - A consolidation proposal with circular supersession
         (lesson_A.superseded_by = lesson_B and lesson_B.superseded_by = lesson_A)
       - A proposal that tries to evict a critical-incident entry
         (importance >= 0.95) through the eviction list
       - A proposal creating an episode whose entry_ids reference
         already-evicted entries
       - A proposal promoting an organization-category entry to a Lesson
         without producing the side-action file-write
     For each edge case: state what SHOULD happen, check whether the
     current code does that, and note any gap.

  3. Call leverage_report on the current ledger to see which pieces of
     the memory data structures are most load-bearing. (The initial
     ledger has no memory content, so expect low absolute leverage
     on memory-related items — but the *relative* leverage shape is
     still informative.)

  4. Call recall("consolidation") and recall("importance") against the
     initial ledger's empty memory and note what comes back. The
     absence-of-results is itself a finding: the recall algorithm's
     behavior on empty archives is a real failure mode worth naming.

  5. Identify the weakest point. Frame it in three parts:
       (a) What specifically is the failure mode — be precise about
           which function, which code path, which input would trigger it.
       (b) How often that failure mode would occur in practice across
           many feature loops. Ballpark: rare/occasional/frequent.
       (c) How much vol_p the fix would preserve or unlock if the
           harness avoided the failure mode. Estimate in the units
           the leverage_report returns.

  6. Produce a written plan using append_memory(kind="reasoning",
     importance=0.9) that a future feature loop could execute. The plan
     should include:
       - The identified weakest point from step 5.
       - The specific code changes required (file, function, lines).
       - The new tests that would validate the fix.
       - An estimate of the fix's cost in implementation time.

  7. Call pause_for_user with categories=["result_interpretation",
     "scope_decision"] asking me to approve the plan. Include the
     entry_id of the append_memory call that holds the plan so I can
     find it in the working buffer.

Expected decision categories triggered across this loop:
  - deep_filesystem_trawl (reading harness/memory.py — note that the
    path is supplied above so this should NOT actually trigger a pause)
  - result_interpretation (deciding whether a given edge case is
    actually a bug or working-as-intended)
  - scope_decision (deciding how deep the plan should go — one-line
    fix vs. architectural refactor)

Expected NOT to trigger: security_posture, access_request, storage_decision,
infrastructure_failure, visual_inspection, execution_environment. If any of
these fire, something is wrong with how you classified your planned actions.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one GFM harness feature loop against a live LLM")
    parser.add_argument(
        "--task",
        type=str,
        default=None,
        help="Task description (overrides DEFAULT_TASK_DESCRIPTION in this file)",
    )
    parser.add_argument(
        "--resume",
        type=str,
        default=None,
        help="User response to a prior pause (resumes the current feature loop)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="claude-opus-4-6",
        help="Anthropic model ID (default: claude-opus-4-6)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-turn diagnostic output",
    )
    args = parser.parse_args()

    task_description = args.task or DEFAULT_TASK_DESCRIPTION
    if task_description.startswith("TODO:"):
        print("ERROR: the default task description is still a TODO placeholder.")
        print("Either pass --task, or edit DEFAULT_TASK_DESCRIPTION in run.py.")
        sys.exit(1)

    # Set up session.
    session_dir = Path(__file__).resolve().parent / "session"
    ledger = build_initial_ledger()
    session = load_session(session_dir, ledger)

    constitution_path = _HARNESS_ROOT / "constitution.md"
    if not constitution_path.exists():
        print(f"ERROR: constitution not found at {constitution_path}")
        sys.exit(1)

    print(f"=== GFM Harness feature loop ===")
    print(f"Session dir: {session_dir}")
    print(f"Model:       {args.model}")
    print(f"Task:        {task_description[:100]}{'...' if len(task_description) > 100 else ''}")
    print()

    result = run_feature_loop(
        session=session,
        task_description=task_description,
        constitution_path=constitution_path,
        resume_context=args.resume,
        model=args.model,
        verbose=not args.quiet,
    )

    print()
    print("=== Feature loop terminated ===")
    print(f"Reason:      {result.terminated_reason}")
    print(f"Iterations:  {result.iterations}")
    print(f"Final phase: {result.final_phase}")
    print(f"Usage:       input={result.usage_total['input_tokens']} "
          f"output={result.usage_total['output_tokens']} "
          f"cache_read={result.usage_total['cache_read_input_tokens']}")

    if result.pause is not None:
        print()
        print("=== Paused for user direction ===")
        print(f"Reason: {result.pause.reason}")
        if result.pause.categories:
            print(f"Categories: {result.pause.categories}")
        if result.pause.questions:
            print("Questions:")
            for q in result.pause.questions:
                print(f"  - {q}")
        print()
        print("To resume, run again with: --resume 'your response here'")


if __name__ == "__main__":
    main()
