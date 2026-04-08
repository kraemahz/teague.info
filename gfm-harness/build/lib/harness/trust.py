"""
Commit-level trust tracking.

Each IMPLEMENT-phase commit records an expected Δvol_p (what the agent
predicted would happen when it constructed a hypothetical ledger before
acting) alongside the actual Δvol_p (measured after the action completed
and the LLM updated the ledger to reflect observations).

The residual — actual minus expected — is a calibration signal on the
agent's own predictive accuracy. Large sustained residuals indicate
the agent's world model is drifting from reality; RETRO uses this to
decide whether to update the constitution's reasoning heuristics.

This is structurally the same as Paper 3's risk-trust update machinery,
applied reflexively to the agent's own ledger-state predictions rather
than to other agents' risk claims.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class CommitRecord:
    """
    A single IMPLEMENT-phase commit with its expected/actual residual.
    """

    commit_id: str
    timestamp: str
    action: str                       # one-line description of what was done
    reasoning: str                    # why the agent chose this action
    categories_triggered: list[str]   # decision categories the action fell into
    pre_vol_p: float                  # measured before the action
    expected_post_vol_p: float        # agent's prediction (from hypothetical ledger)
    actual_post_vol_p: float          # measured after the action
    expected_delta: float = 0.0
    actual_delta: float = 0.0
    residual: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.expected_delta = self.expected_post_vol_p - self.pre_vol_p
        self.actual_delta = self.actual_post_vol_p - self.pre_vol_p
        self.residual = self.actual_delta - self.expected_delta


@dataclass
class CommitLog:
    """
    Append-only log of commits. Backed by a JSON-Lines file so the user
    can inspect the trajectory directly without running the harness.
    """

    path: Path
    records: list[CommitRecord] = field(default_factory=list)

    @classmethod
    def load(cls, path: Path) -> "CommitLog":
        log = cls(path=path)
        if path.exists():
            for line in path.read_text().splitlines():
                if not line.strip():
                    continue
                data = json.loads(line)
                # drop derived fields so __post_init__ recomputes them consistently
                for key in ("expected_delta", "actual_delta", "residual"):
                    data.pop(key, None)
                log.records.append(CommitRecord(**data))
        return log

    def append(self, record: CommitRecord) -> None:
        self.records.append(record)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a") as f:
            f.write(json.dumps(asdict(record)) + "\n")

    def mean_residual(self, n: int | None = None) -> float:
        """Mean residual over the last n commits (or all if n is None)."""
        target = self.records[-n:] if n else self.records
        if not target:
            return 0.0
        return sum(r.residual for r in target) / len(target)

    def prediction_bias(self, n: int | None = None) -> str:
        """
        Classify the agent's predictive bias over recent commits.
        RETRO uses this to decide whether to warn the LLM that its
        world model is systematically over- or under-estimating vol_p.
        """
        mean = self.mean_residual(n)
        if abs(mean) < 0.5:
            return "calibrated"
        if mean > 0:
            return "under-predicting (actions are more productive than expected)"
        return "over-predicting (actions are less productive than expected)"
