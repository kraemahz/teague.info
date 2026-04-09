"""
Instance: a persistent named agent with its own identity and state.

An instance lives in a directory under the instance root (default:
~/.gfm-harness/instances/<name>/) and holds everything that makes one
agent distinct from another:

  - config.toml      — instance metadata, model, run limits
  - goals.toml       — standing objectives the agent gravitates toward
  - session/         — runtime state, persistent across invocations
      ledger.json    — current capability ledger (evolves via IMPLEMENT)
      memory/        — working buffer + episodes + lessons
        working_buffer.jsonl
        episodes.jsonl
        lessons.jsonl
      commits.jsonl  — IMPLEMENT-phase action log
      trust.json     — self-trust model state
      feature_loops.jsonl — log of completed feature loops (future)

This is the orchestration layer on top of the lower-level primitives
(CapabilityLedger, MemoryArchive, CommitLog, SelfTrustModel). The
Instance knows how to bootstrap from a builder the first time, persist
all state to disk, and reload itself on subsequent invocations.

Design decisions encoded here (from the 2026-04-08 instance-architecture
discussion):

  D1: config.toml uses TOML (Python 3.11+ tomllib)
  D2: goals.toml uses TOML [[goal]] array-of-tables
  D3: instance root is ~/.gfm-harness/instances/ by default; the
      GFM_HARNESS_HOME environment variable overrides
  D4: initial ledger builders live in harness/initial_ledgers/ as
      Python code; instances reference them by name in config.toml
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from .config import InstanceConfig, load_config, save_config
from .goals import GoalSet, default_goals, load_goals, save_goals
from .initial_ledgers import get_builder, list_builders
from .ledger import CapabilityLedger
from .ledger_persistence import load_ledger, save_ledger
from .loop import HarnessSession
from .memory import MemoryArchive
from .phases import SelfTrustModel
from .trust import CommitLog

if TYPE_CHECKING:
    from .phases import FeatureLoopState  # noqa: F401


DEFAULT_HOME = Path.home() / ".gfm-harness"
HOME_ENV_VAR = "GFM_HARNESS_HOME"


def get_instance_root() -> Path:
    """
    Resolve the instance root directory.

    Default: ~/.gfm-harness/instances/
    Override: set GFM_HARNESS_HOME to any directory; instances live at
              $GFM_HARNESS_HOME/instances/
    """
    home = os.environ.get(HOME_ENV_VAR)
    if home:
        return Path(home).expanduser().resolve() / "instances"
    return DEFAULT_HOME / "instances"


def instance_path(name: str) -> Path:
    """Return the directory path for a named instance (may not exist yet)."""
    return get_instance_root() / name


def list_instances() -> list[str]:
    """List the names of all instances currently on disk."""
    root = get_instance_root()
    if not root.exists():
        return []
    return sorted(
        p.name for p in root.iterdir()
        if p.is_dir() and not p.name.startswith(".")
    )


@dataclass
class Instance:
    """
    A persistent named agent.

    Instance is an orchestration object: it owns the path to its
    on-disk state and provides a HarnessSession view into that state
    for the agent loop to operate on. Instances are created via
    Instance.create() and loaded via Instance.load().
    """

    name: str
    path: Path
    config: InstanceConfig
    goal_set: GoalSet
    session: HarnessSession

    # ---- path helpers -----------------------------------------------------

    @property
    def config_path(self) -> Path:
        return self.path / "config.toml"

    @property
    def goals_path(self) -> Path:
        return self.path / "goals.toml"

    @property
    def session_dir(self) -> Path:
        return self.path / "session"

    @property
    def ledger_path(self) -> Path:
        return self.session_dir / "ledger.json"

    # ---- persistence ------------------------------------------------------

    @classmethod
    def create(
        cls,
        name: str,
        description: str = "",
        initial_ledger: str = "default",
        goal_set: GoalSet | None = None,
    ) -> Instance:
        """
        Create a new instance on disk. Fails if an instance with this
        name already exists. Writes template config.toml, goals.toml,
        and an empty session/ directory. The initial ledger is built
        by running the named builder from harness.initial_ledgers and
        saved to session/ledger.json.
        """
        path = instance_path(name)
        if path.exists():
            raise FileExistsError(
                f"instance {name!r} already exists at {path}"
            )

        # Validate the initial_ledger key before touching the filesystem.
        if initial_ledger not in list_builders():
            raise KeyError(
                f"unknown initial_ledger {initial_ledger!r}; "
                f"known: {list_builders()}"
            )

        path.mkdir(parents=True, exist_ok=False)

        # Build config.
        config = InstanceConfig.default(name=name, description=description)
        config.initial_ledger = initial_ledger
        save_config(config, path / "config.toml")

        # Build goals: use supplied set, else fall back to the default starter.
        goals = goal_set if goal_set is not None else default_goals()
        save_goals(goals, path / "goals.toml")

        # Build the initial ledger and save.
        builder = get_builder(initial_ledger)
        ledger = builder()
        (path / "session").mkdir(parents=True, exist_ok=True)
        save_ledger(ledger, path / "session" / "ledger.json")

        return cls.load(name)

    @classmethod
    def load(cls, name: str) -> Instance:
        """
        Load an existing instance from disk. Raises FileNotFoundError
        if the instance does not exist.
        """
        path = instance_path(name)
        if not path.exists():
            raise FileNotFoundError(
                f"instance {name!r} does not exist at {path}. "
                f"Use Instance.create({name!r}) to create it."
            )

        config_path = path / "config.toml"
        goals_path = path / "goals.toml"
        session_dir = path / "session"
        session_dir.mkdir(parents=True, exist_ok=True)
        ledger_path = session_dir / "ledger.json"

        config = load_config(config_path) if config_path.exists() else InstanceConfig.default(name)
        goal_set = load_goals(goals_path) if goals_path.exists() else default_goals()

        # Load the ledger from disk, or bootstrap from the named builder
        # if this is the first run (no ledger.json exists yet).
        ledger = load_ledger(ledger_path)
        if ledger is None:
            builder = get_builder(config.initial_ledger)
            ledger = builder()
            save_ledger(ledger, ledger_path)

        # Load session primitives from the session directory.
        memory = MemoryArchive.load(session_dir / "memory")
        commit_log = CommitLog.load(session_dir / "commits.jsonl")
        trust = SelfTrustModel.load(session_dir / "trust.json")

        session = HarnessSession(
            session_dir=session_dir,
            ledger=ledger,
            memory=memory,
            trust=trust,
            commit_log=commit_log,
        )

        # Restore any active feature loop from a prior session.
        session.load_feature_state()

        return cls(
            name=name,
            path=path,
            config=config,
            goal_set=goal_set,
            session=session,
        )

    def save(self) -> None:
        """
        Persist everything that might have changed: config, goals,
        ledger, trust, feature state. Memory archive and commit log
        are already append-only to disk, so they don't need an explicit
        flush here. Call at the end of every feature loop.
        """
        save_config(self.config, self.config_path)
        save_goals(self.goal_set, self.goals_path)
        save_ledger(self.session.ledger, self.ledger_path)
        self.session.trust.save(self.session_dir / "trust.json")
        self.session.save_feature_state()

    # ---- goal management --------------------------------------------------

    def add_goal(
        self,
        id: str,
        statement: str,
        priority: str = "medium",
        added_by: str = "agent",
        notes: str = "",
    ) -> None:
        """Add a new goal and persist. Called by the propose_goal tool."""
        self.goal_set.add(
            id=id,
            statement=statement,
            priority=priority,
            added_by=added_by,
            notes=notes,
        )
        save_goals(self.goal_set, self.goals_path)

    def complete_goal(self, goal_id: str) -> None:
        """Mark a goal completed and persist."""
        self.goal_set.complete(goal_id)
        save_goals(self.goal_set, self.goals_path)

    # ---- status summary ---------------------------------------------------

    def status_summary(self) -> dict:
        """Return a dict summarizing the instance's current state."""
        from .vol_p import compute_vol_p

        return {
            "name": self.name,
            "path": str(self.path),
            "description": self.config.description,
            "model": self.config.model,
            "initial_ledger": self.config.initial_ledger,
            "vol_p": compute_vol_p(self.session.ledger),
            "agents": list(self.session.ledger.agents.keys()),
            "substrate_count": self.session.ledger.m(),
            "goals_active": len(self.goal_set.active()),
            "goals_total": len(self.goal_set.goals),
            "memory_working_buffer": len(self.session.memory.working_buffer),
            "memory_episodes": len(self.session.memory.episodes),
            "memory_lessons": len(self.session.memory.lessons),
            "commits": len(self.session.commit_log.records),
            "trust_nonzero_categories": sorted([
                k for k, v in self.session.trust.category_trust.items() if v > 0
            ]),
        }
