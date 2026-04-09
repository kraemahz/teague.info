"""
Command-line interface for the GFM harness.

Usage:
    python3 -m harness.cli init <name>
    python3 -m harness.cli run <name> [--task "..."] [--resume "..."]
    python3 -m harness.cli status <name>
    python3 -m harness.cli list
    python3 -m harness.cli builders

All commands operate on named instances stored under ~/.gfm-harness/
(or $GFM_HARNESS_HOME if set). See harness.instance for the instance
layout and lifecycle.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .initial_ledgers import list_builders
from .instance import (
    Instance,
    get_instance_root,
    instance_path,
    list_instances,
)


def cmd_init(args: argparse.Namespace) -> int:
    """Create a new instance with template files and an initial ledger."""
    try:
        instance = Instance.create(
            name=args.name,
            description=args.description,
            initial_ledger=args.initial_ledger,
        )
    except FileExistsError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except KeyError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        print(f"Known initial ledgers: {list_builders()}", file=sys.stderr)
        return 1

    print(f"Created instance {args.name!r}")
    print(f"  path:           {instance.path}")
    print(f"  config:         {instance.config_path}")
    print(f"  goals:          {instance.goals_path}")
    print(f"  session dir:    {instance.session_dir}")
    print(f"  initial ledger: {instance.config.initial_ledger}")
    print(f"  agents:         {list(instance.session.ledger.agents.keys())}")
    print()
    print("Edit the config and goals files as needed, then run with:")
    print(f"  python3 -m harness.cli run {args.name} --task '...'")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    """Run a feature loop for an instance."""
    try:
        instance = Instance.load(args.name)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    autonomous = bool(getattr(args, "autonomous", False))

    if autonomous:
        # Autonomous mode: no task required. The agent will propose one
        # in SELECT phase based on its goals + ledger + leverage.
        task = args.task  # optional hint, None is fine
    else:
        task = args.task or instance.config.default_task
        if not task:
            print(
                "ERROR: no task specified and instance has no default_task "
                "in config.\n"
                f"Either pass --task, edit {instance.config_path} to set "
                "run.default_task, or use --autonomous to have the agent "
                "propose a task from its goals and ledger state.",
                file=sys.stderr,
            )
            return 1

    # Resolve the constitution path. It lives in the harness repo, not
    # in the instance data directory. For now assume the harness repo
    # is at the import parent of this module.
    constitution_path = _find_constitution_path()
    if constitution_path is None or not constitution_path.exists():
        print(
            "ERROR: could not locate constitution.md. Expected it at "
            "<harness-repo>/constitution.md. If you've moved the repo, "
            "set GFM_HARNESS_CONSTITUTION to the absolute path.",
            file=sys.stderr,
        )
        return 1

    # Begin the feature loop if not already active.
    if instance.session.current_feature is None:
        instance.session.begin_feature(task)

    print(f"=== GFM Harness feature loop ({instance.name}) ===")
    print(f"Instance:    {instance.path}")
    print(f"Model:       {instance.config.model}")
    if autonomous:
        print(f"Mode:        autonomous (agent proposes task from goals)")
        active_goals = instance.goal_set.active()
        print(f"Goals:       {len(active_goals)} active")
        for g in active_goals:
            print(f"  [{g.priority}] {g.id}")
    else:
        print(f"Task:        {task[:100]}{'...' if len(task) > 100 else ''}")
    print()

    # Lazy-import the agent driver so the CLI is usable without the
    # claude-agent-sdk installed for `init`, `list`, `status`, `builders`.
    from .agent import run_feature_loop

    # The agent's working directory is the harness repo root by default.
    # This lets the agent read harness/memory.py and related files during
    # investigation, and edit them during implementation. Override via
    # config.toml [run].cwd in a future iteration if an instance should
    # operate on a different directory.
    cwd_path = _find_harness_repo_root()

    result = run_feature_loop(
        session=instance.session,
        task_description=task,
        constitution_path=constitution_path,
        resume_context=args.resume,
        model=args.model or instance.config.model,
        max_turns=instance.config.max_iterations,
        cwd=cwd_path,
        verbose=not args.quiet,
        goal_set=instance.goal_set,
        autonomous=autonomous,
    )

    # Always persist the updated instance state after a feature loop.
    instance.save()

    print()
    print(f"=== Feature loop terminated ({instance.name}) ===")
    print(f"Reason:      {result.terminated_reason}")
    print(f"Turns:       {result.turns_observed}")
    print(f"Final phase: {result.final_phase}")
    print(
        f"Usage:       input={result.usage_total.get('input_tokens', 0)} "
        f"output={result.usage_total.get('output_tokens', 0)} "
        f"cache_read={result.usage_total.get('cache_read_input_tokens', 0)} "
        f"cache_write={result.usage_total.get('cache_creation_input_tokens', 0)}"
    )
    cost = result.usage_total.get("total_cost_usd")
    if cost is not None:
        print(f"Cost:        ${cost:.4f}")

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
        print(f"To resume: python3 -m harness.cli run {instance.name} "
              "--resume 'your response'")

    return 0 if result.terminated_reason in ("end_turn", "paused") else 2


def cmd_status(args: argparse.Namespace) -> int:
    """Print a structured status summary for an instance."""
    try:
        instance = Instance.load(args.name)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    summary = instance.status_summary()

    if args.json:
        print(json.dumps(summary, indent=2, default=str))
        return 0

    print(f"Instance: {summary['name']}")
    print(f"  path:            {summary['path']}")
    if summary['description']:
        print(f"  description:     {summary['description']}")
    print(f"  model:           {summary['model']}")
    print(f"  initial_ledger:  {summary['initial_ledger']}")
    print()
    print("Ledger:")
    print(f"  vol_p:           {summary['vol_p']:.2f}")
    print(f"  agents:          {summary['agents']}")
    print(f"  substrates (m):  {summary['substrate_count']}")
    print()
    print("Memory:")
    print(f"  working buffer:  {summary['memory_working_buffer']} entries")
    print(f"  episodes:        {summary['memory_episodes']}")
    print(f"  lessons:         {summary['memory_lessons']}")
    print()
    print("Goals:")
    print(f"  active:          {summary['goals_active']}")
    print(f"  total:           {summary['goals_total']}")
    for goal in instance.goal_set.active():
        tag = f"[{goal.priority}]"
        print(f"    {tag:<12} {goal.id}: {goal.statement[:70]}"
              f"{'...' if len(goal.statement) > 70 else ''}")
    print()
    print("Commits:")
    print(f"  total:           {summary['commits']}")
    print()
    print("Trust:")
    print(f"  non-zero cats:   {summary['trust_nonzero_categories'] or '(none — all at 0.0)'}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """List all instances on disk."""
    root = get_instance_root()
    instances = list_instances()
    print(f"Instance root: {root}")
    if not instances:
        print("(no instances yet — use 'harness init <name>' to create one)")
        return 0
    print()
    for name in instances:
        print(f"  {name}")
    return 0


def cmd_builders(args: argparse.Namespace) -> int:
    """List all registered initial-ledger builders."""
    print("Registered initial_ledger builders:")
    for name in list_builders():
        print(f"  {name}")
    return 0


def _find_harness_repo_root() -> Path:
    """
    Locate the repo root (the directory containing constitution.md and
    the harness/ package). Used as the default cwd for the Agent SDK so
    Read/Write/Edit/Bash operate relative to the harness code.
    """
    # harness/cli.py → harness/ → gfm-harness/
    return Path(__file__).resolve().parent.parent


def _find_constitution_path() -> Path | None:
    """
    Locate constitution.md. Checks (in order):
      1. $GFM_HARNESS_CONSTITUTION if set
      2. <harness package parent>/constitution.md (repo layout)
    """
    import os

    env = os.environ.get("GFM_HARNESS_CONSTITUTION")
    if env:
        return Path(env).expanduser().resolve()

    # harness/cli.py → harness/ → gfm-harness/ → constitution.md
    here = Path(__file__).resolve()
    repo_root = here.parent.parent
    candidate = repo_root / "constitution.md"
    if candidate.exists():
        return candidate
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="harness",
        description="GFM harness — a measurement infrastructure for LLM agents",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # init
    p_init = sub.add_parser("init", help="Create a new instance")
    p_init.add_argument("name", help="Instance name (e.g. 'primary')")
    p_init.add_argument(
        "--description", default="", help="Human-readable description"
    )
    p_init.add_argument(
        "--initial-ledger",
        default="default",
        help="Name of the initial ledger builder (see 'harness builders')",
    )
    p_init.set_defaults(func=cmd_init)

    # run
    p_run = sub.add_parser("run", help="Run a feature loop")
    p_run.add_argument("name", help="Instance name")
    p_run.add_argument("--task", default=None, help="Task description (overrides instance default_task)")
    p_run.add_argument("--resume", default=None, help="User response to a prior pause")
    p_run.add_argument("--model", default=None, help="Override instance model")
    p_run.add_argument("--quiet", action="store_true", help="Suppress per-turn diagnostics")
    p_run.add_argument(
        "--autonomous",
        action="store_true",
        help=(
            "Autonomous mode: the agent proposes its own task from the "
            "instance's goals, ledger state, and leverage gradient. "
            "Starts the feature loop in SELECT phase instead of PLAN. "
            "No --task required."
        ),
    )
    p_run.set_defaults(func=cmd_run)

    # status
    p_status = sub.add_parser("status", help="Show instance state")
    p_status.add_argument("name")
    p_status.add_argument("--json", action="store_true", help="Output as JSON")
    p_status.set_defaults(func=cmd_status)

    # list
    p_list = sub.add_parser("list", help="List all instances")
    p_list.set_defaults(func=cmd_list)

    # builders
    p_builders = sub.add_parser("builders", help="List registered initial-ledger builders")
    p_builders.set_defaults(func=cmd_builders)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
