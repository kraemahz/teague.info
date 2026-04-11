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


def _ensure_user_config() -> "UserConfig | None":
    """
    Load user.toml, or interactively create it if it doesn't exist.

    Returns the loaded/created UserConfig, or None if the user declines
    interactive setup (in which case a minimal default is used).
    """
    from .config import (
        UserCapabilityConfig,
        UserConfig,
        load_user_config,
        save_user_config,
    )
    from .initial_ledgers.default import DEFAULT_USER_CAPABILITIES

    config = load_user_config()
    if config is not None:
        return config

    # No user.toml found — offer interactive setup.
    print("No user configuration found (~/.gfm-harness/user.toml).")
    print("Let's set up your user profile for the harness.\n")

    import getpass
    default_name = getpass.getuser()
    name = input(f"  Your name [{default_name}]: ").strip() or default_name
    substrate = input("  Substrate [biological]: ").strip() or "biological"

    print("\n  Default capabilities (select with y/n):")
    selected: list[UserCapabilityConfig] = []
    for key, desc in DEFAULT_USER_CAPABILITIES:
        answer = input(f"    {key}: {desc}\n    Include? [Y/n]: ").strip().lower()
        if answer in ("", "y", "yes"):
            selected.append(UserCapabilityConfig(key=key, description=desc))

    # Offer to add custom capabilities.
    print("\n  Add custom capabilities (empty key to finish):")
    while True:
        key = input("    Capability key: ").strip()
        if not key:
            break
        desc = input("    Description: ").strip()
        selected.append(UserCapabilityConfig(key=key, description=desc))

    config = UserConfig(name=name, substrate=substrate, capabilities=selected)
    save_user_config(config)
    print(f"\n  Saved to ~/.gfm-harness/user.toml ({len(selected)} capabilities)")
    return config


def cmd_init(args: argparse.Namespace) -> int:
    """Create a new instance with template files and an initial ledger."""
    # Ensure user config exists (interactive setup on first run).
    user_config = _ensure_user_config()

    try:
        instance = Instance.create(
            name=args.name,
            description=args.description,
            initial_ledger=args.initial_ledger,
            user_config=user_config,
        )
    except FileExistsError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except KeyError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        print(f"Known initial ledgers: {list_builders()}", file=sys.stderr)
        return 1

    print(f"\nCreated instance {args.name!r}")
    print(f"  path:           {instance.path}")
    print(f"  config:         {instance.config_path}")
    print(f"  goals:          {instance.goals_path}")
    print(f"  session dir:    {instance.session_dir}")
    print(f"  initial ledger: {instance.config.initial_ledger}")
    print(f"  agents:         {list(instance.session.ledger.agents.keys())}")
    coops = list(instance.session.ledger.cooperative.keys())
    if coops:
        print(f"  cooperatives:   {coops}")
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

    # --reset: clear saved feature state and exit without running a loop.
    if getattr(args, "reset", False):
        saved = instance.session.current_feature
        if saved is not None:
            print(f"Clearing saved feature state (was: phase={saved.current_phase.value}, "
                  f"task={saved.task_description[:80]})")
            instance.session.clear_feature_state()
        else:
            print("No saved feature state to clear.")
        return 0

    autonomous = bool(getattr(args, "autonomous", False))
    saved_state = instance.session.current_feature  # loaded by Instance.load()

    # --- Resolve task and handle saved-state precedence ---
    #
    # Precedence semantics (per user spec):
    #   --resume "..." (no --task) → load saved state, error if none
    #   --task "..."              → replace saved state (log the old one)
    #   --autonomous              → replace saved state (log the old one)
    #   (none of the above)       → resume saved if present, else need --task

    if args.resume and not args.task:
        # Resume mode: continue from saved feature state. --resume takes
        # precedence over --autonomous when both are passed, because the
        # intent is "continue the saved loop with this feedback" not
        # "start a fresh autonomous loop."
        if saved_state is None:
            print(
                "ERROR: --resume was given but no saved feature state exists.\n"
                "Use --task to start a new feature loop instead.",
                file=sys.stderr,
            )
            return 1
        task = saved_state.task_description
        # If the saved state was produced by an autonomous SELECT
        # (task_description is None), inherit that mode for the resume.
        # This preserves the original loop's prompt framing and phase
        # machine starting point. An explicit --autonomous flag reinforces
        # the inference; its absence doesn't override.
        if task is None:
            autonomous = True
        print(f"Resuming saved feature (phase={saved_state.current_phase.value})")
    elif args.task or autonomous:
        # New task or autonomous mode: replace any saved state.
        if saved_state is not None:
            # Log the replaced state to memory so it's recoverable via recall.
            # task_description can be None for saved states produced by a
            # prior autonomous SELECT — handle that explicitly rather than
            # slicing a None value.
            task_preview = (
                saved_state.task_description[:200]
                if saved_state.task_description
                else "(autonomous, no task supplied)"
            )
            instance.session.memory.append(
                phase=saved_state.current_phase.value,
                kind="note",
                text=(
                    f"Replaced saved feature state (feature_id={saved_state.feature_id}, "
                    f"phase={saved_state.current_phase.value}, "
                    f"task={task_preview}) "
                    f"with {'--autonomous' if autonomous else '--task'} invocation."
                ),
                importance=0.5,
            )
            instance.session.clear_feature_state()
            print(f"Replaced saved feature state (was: phase={saved_state.current_phase.value})")

        if autonomous:
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
    else:
        # No flags: resume saved state if present, else require --task.
        if saved_state is not None:
            task = saved_state.task_description
            print(f"Resuming saved feature (phase={saved_state.current_phase.value})")
        else:
            task = instance.config.default_task
            if not task:
                print(
                    "ERROR: no task specified, no saved feature state, and "
                    "instance has no default_task in config.\n"
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

    # Begin the feature loop if not already active (i.e., no saved state
    # was loaded, or saved state was cleared by --task/--autonomous).
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

    # The agent's working directory is the parent of the harness repo
    # by default. This lets the agent read/write harness code AND papers
    # AND docs all under one cwd, so work products land in their natural
    # location instead of being scoped down to gfm-harness/. Per-instance
    # cwd override is a Phase 2 concern.
    cwd_path = _find_default_cwd()

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


def _find_default_cwd() -> Path:
    """
    Default cwd for the Agent SDK's Read/Write/Edit/Bash tools.

    Currently returns the parent of the harness repo so the agent can
    write to docs/, papers/, and the harness's own files all under one
    cwd. The previous default was the harness repo root, which scoped
    the agent's filesystem reach too narrowly — work products like the
    GFM safety gap analysis ended up under gfm-harness/docs/ when they
    really belonged at the parent repo's docs/ level.

    This is a hard-coded default for v1; per-instance config.toml
    override is a Phase 2 concern. When the harness eventually moves
    to its own repo, this default will need to change.
    """
    # harness/cli.py → harness/ → gfm-harness/ → project root
    return Path(__file__).resolve().parent.parent.parent


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
    p_run.add_argument(
        "--reset",
        action="store_true",
        help=(
            "Clear any saved feature state without starting a new loop. "
            "Use when a paused loop is stuck and you want to abandon it "
            "cleanly rather than overwrite by starting a new task."
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
