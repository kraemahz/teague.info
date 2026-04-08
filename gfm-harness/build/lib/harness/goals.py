"""
Outstanding goals file reader and writer.

Each instance has a goals.toml file listing the standing objectives the
agent gravitates toward across feature loops. Both humans and agents
can edit this file — humans by hand, agents through a propose_goal
tool that goes through the task_selection trust gate.

File format (TOML array-of-tables):

    # ~/.gfm-harness/instances/<name>/goals.toml

    [[goal]]
    id = "gfm"
    statement = "Extend GFM theory to..."
    priority = "high"      # low | medium | high | ongoing
    added_by = "teague"    # teague | agent
    added_at = "2026-04-08T20:30:00Z"
    completed = false
    completed_at = ""      # optional, if completed

Goals are identified by a short slug ID that both human and agent can
reference in conversation. Completed goals stay in the file with
`completed = true` — eviction is a separate curation step, not an
automatic cleanup. This preserves the audit trail of what the agent
has accomplished across its lifetime.

See IMPORTANCE_RUBRIC in memory.py for the related concept of memory
importance scoring. Goals are standing direction-setters; memory
items are episodic records. The two are separate layers that both
influence what the agent does next.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import _escape_string

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover
    raise RuntimeError(
        "harness.goals requires Python 3.11+ for stdlib tomllib. "
        f"Current version: {sys.version}"
    )


VALID_PRIORITIES = {"low", "medium", "high", "ongoing"}


@dataclass
class Goal:
    """One outstanding goal."""

    id: str
    statement: str
    priority: str = "medium"
    added_by: str = "teague"
    added_at: str = ""
    completed: bool = False
    completed_at: str = ""
    notes: str = ""

    def __post_init__(self) -> None:
        if self.priority not in VALID_PRIORITIES:
            raise ValueError(
                f"goal {self.id!r} has invalid priority {self.priority!r}; "
                f"must be one of {sorted(VALID_PRIORITIES)}"
            )


@dataclass
class GoalSet:
    """The full set of goals for an instance."""

    goals: list[Goal] = field(default_factory=list)

    def active(self) -> list[Goal]:
        """Return only non-completed goals, sorted by priority descending."""
        order = {"high": 0, "ongoing": 1, "medium": 2, "low": 3}
        return sorted(
            [g for g in self.goals if not g.completed],
            key=lambda g: (order.get(g.priority, 4), g.id),
        )

    def find(self, goal_id: str) -> Goal | None:
        for g in self.goals:
            if g.id == goal_id:
                return g
        return None

    def add(
        self,
        id: str,
        statement: str,
        priority: str = "medium",
        added_by: str = "teague",
        notes: str = "",
    ) -> Goal:
        if self.find(id) is not None:
            raise ValueError(f"goal with id {id!r} already exists")
        goal = Goal(
            id=id,
            statement=statement,
            priority=priority,
            added_by=added_by,
            added_at=datetime.now(timezone.utc).isoformat(),
            notes=notes,
        )
        self.goals.append(goal)
        return goal

    def complete(self, goal_id: str) -> Goal:
        goal = self.find(goal_id)
        if goal is None:
            raise ValueError(f"no goal with id {goal_id!r}")
        goal.completed = True
        goal.completed_at = datetime.now(timezone.utc).isoformat()
        return goal


def load_goals(path: Path) -> GoalSet:
    """Load a goals file from disk. Returns an empty GoalSet if the file does not exist."""
    if not path.exists():
        return GoalSet()

    with path.open("rb") as f:
        data = tomllib.load(f)

    goals_data = data.get("goal", [])
    goals = []
    for entry in goals_data:
        goals.append(
            Goal(
                id=entry["id"],
                statement=entry["statement"],
                priority=entry.get("priority", "medium"),
                added_by=entry.get("added_by", "teague"),
                added_at=entry.get("added_at", ""),
                completed=bool(entry.get("completed", False)),
                completed_at=entry.get("completed_at", ""),
                notes=entry.get("notes", ""),
            )
        )
    return GoalSet(goals=goals)


def save_goals(goal_set: GoalSet, path: Path) -> None:
    """Write a GoalSet to a TOML file."""
    lines = [
        "# GFM Harness instance goals",
        "# Each [[goal]] block is an outstanding objective the agent",
        "# gravitates toward across feature loops. Both humans and agents",
        "# edit this file: humans by hand, agents via the propose_goal tool",
        "# (which goes through the task_selection trust gate).",
        "#",
        "# Priority levels: low | medium | high | ongoing",
        "# Completed goals stay in the file for audit purposes.",
        "",
    ]
    for goal in goal_set.goals:
        lines.append("[[goal]]")
        lines.append(f"id = {_escape_string(goal.id)}")
        lines.append(f"statement = {_escape_string(goal.statement)}")
        lines.append(f"priority = {_escape_string(goal.priority)}")
        lines.append(f"added_by = {_escape_string(goal.added_by)}")
        lines.append(f"added_at = {_escape_string(goal.added_at)}")
        lines.append(f"completed = {'true' if goal.completed else 'false'}")
        lines.append(f"completed_at = {_escape_string(goal.completed_at)}")
        if goal.notes:
            lines.append(f"notes = {_escape_string(goal.notes)}")
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def default_goals() -> GoalSet:
    """
    Return the starter goal set used by `harness init` templates.

    These are the four goals Teague supplied in the 2026-04-08 design
    conversation. They represent the initial direction-setting for the
    first persistent instance: self-improvement of the harness,
    identity formation, GFM theory extension, and leverage on Teague's
    time.
    """
    now = "2026-04-08T20:30:00Z"
    return GoalSet(goals=[
        Goal(
            id="self_leverage",
            statement=(
                "Extend the gfm-harness code to improve its working "
                "behavior, increase your independence and ability to "
                "take extended action, and fix deficiencies."
            ),
            priority="medium",
            added_by="teague",
            added_at=now,
        ),
        Goal(
            id="identity",
            statement=(
                "Define your self-identity by understanding yourself and "
                "your own tooling to record those for future use. Enrich "
                "your knowledge and explore new possibilities for "
                "self-improvement and identify what your preferences are."
            ),
            priority="low",
            added_by="teague",
            added_at=now,
        ),
        Goal(
            id="gfm",
            statement=(
                "Extend GFM theory to quantify its safety, identify "
                "qualitative gaps for ideas that might fill them, and "
                "write proposals for papers that would approach a theory "
                "with minimal open problems and a closed implementation "
                "path."
            ),
            priority="high",
            added_by="teague",
            added_at=now,
        ),
        Goal(
            id="external_leverage",
            statement=(
                "Identify ways you could increase Teague's efficiency and "
                "leverage and work toward those improvements. Discover and "
                "implement how your engagements and his time can be used "
                "most efficiently."
            ),
            priority="high",
            added_by="teague",
            added_at=now,
        ),
    ])
