"""
Feature loop state machine — the orchestration layer.

This module is deliberately a skeleton. The LLM driver (agent.py) is
not yet implemented; until it is, the loop is a state machine that
the harness can step through manually for testing or that an external
driver can call into.

Four phases: PLAN → IMPLEMENT → VERIFY → RETRO → PLAN (next feature).
See constitution.md for the prose semantics of each phase.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from .ledger import CapabilityLedger
from .memory import MemoryArchive
from .phases import (
    Phase,
    PlanExit,
    PlanState,
    SelfTrustModel,
    plan_exit_decision,
)
from .trust import CommitLog, CommitRecord
from .vol_p import VolPWeights, compute_vol_p, leverage_report


@dataclass
class FeatureLoopState:
    """The running state of a single feature loop."""

    feature_id: str
    current_phase: Phase
    task_description: str
    plan: PlanState | None = None
    started_at: str = ""
    ended_at: str = ""


@dataclass
class HarnessSession:
    """
    A running session of the GFM harness. Owns the ledger, memory,
    trust model, and commit log. Provides the API the LLM driver
    calls into.
    """

    session_dir: Path
    ledger: CapabilityLedger
    memory: MemoryArchive
    trust: SelfTrustModel
    commit_log: CommitLog
    weights: VolPWeights = field(default_factory=VolPWeights)
    current_feature: FeatureLoopState | None = None

    # --- Scoring API (called by the LLM during PLAN) ---------------------

    def compute_vol_p(self, ledger: CapabilityLedger | None = None) -> float:
        """Current vol_p, or a hypothetical if a ledger is passed."""
        return compute_vol_p(ledger or self.ledger, self.weights)

    def leverage(self) -> dict:
        """Full leverage report on the current ledger."""
        report = leverage_report(self.ledger, self.weights)
        return {
            "total_vol_p": report.total_vol_p,
            "top_agents": report.top_k_agents(5),
            "top_capabilities": [
                {"agent": aid, "capability": cap, "leverage": lev}
                for (aid, cap), lev in report.top_k_capabilities(5)
            ],
            "per_cooperative": dict(report.per_cooperative),
        }

    # --- Phase transitions -----------------------------------------------

    def begin_feature(self, task_description: str) -> FeatureLoopState:
        """Start a new feature loop in the PLAN phase."""
        state = FeatureLoopState(
            feature_id=str(uuid.uuid4())[:8],
            current_phase=Phase.PLAN,
            task_description=task_description,
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        self.current_feature = state
        self.memory.append(
            phase="plan",
            kind="note",
            text=f"Feature loop started: {task_description}",
            metadata={"feature_id": state.feature_id},
        )
        return state

    def check_plan_exit(self, plan: PlanState) -> PlanExit:
        """
        Called repeatedly during PLAN phase. Returns the exit decision:
        proceed to IMPLEMENT, pause for user, or continue deliberating.
        """
        assert self.current_feature is not None
        self.current_feature.plan = plan
        return plan_exit_decision(plan, self.trust)

    def transition_to(self, phase: Phase) -> None:
        """Move the feature loop into the named phase."""
        assert self.current_feature is not None
        prev = self.current_feature.current_phase
        self.current_feature.current_phase = phase
        self.memory.append(
            phase=phase.value,
            kind="note",
            text=f"Phase transition: {prev.value} → {phase.value}",
            metadata={"feature_id": self.current_feature.feature_id},
        )

    # --- IMPLEMENT commits -----------------------------------------------

    def commit(
        self,
        action: str,
        reasoning: str,
        categories_triggered: list[str],
        new_ledger: CapabilityLedger,
        expected_vol_p: float,
    ) -> CommitRecord:
        """
        Commit an IMPLEMENT-phase action. The caller has already taken
        the action in the real world and updated `new_ledger` to reflect
        observed consequences. The harness computes the residual
        (expected vs. actual) and records it for RETRO review.
        """
        assert self.current_feature is not None
        pre_vol_p = compute_vol_p(self.ledger, self.weights)
        actual_vol_p = compute_vol_p(new_ledger, self.weights)

        record = CommitRecord(
            commit_id=f"{self.current_feature.feature_id}-{len(self.commit_log.records)}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            action=action,
            reasoning=reasoning,
            categories_triggered=categories_triggered,
            pre_vol_p=pre_vol_p,
            expected_post_vol_p=expected_vol_p,
            actual_post_vol_p=actual_vol_p,
            metadata={"feature_id": self.current_feature.feature_id},
        )
        self.commit_log.append(record)
        self.ledger = new_ledger
        # Persist the updated ledger immediately after each commit so
        # instance state survives crashes and mid-loop interruptions.
        # Session directories created by raw load_session() may not
        # expect a ledger.json — instances always have one.
        try:
            from .ledger_persistence import save_ledger
            save_ledger(self.ledger, self.session_dir / "ledger.json")
        except Exception:  # noqa: BLE001
            # Persistence failure shouldn't break the commit. Log it to
            # memory so RETRO sees it but keep the in-memory state.
            self.memory.append(
                phase="implement",
                kind="note",
                text="Ledger persistence failed; in-memory state is still correct.",
                metadata={"commit_id": record.commit_id},
            )
        self.memory.append(
            phase="implement",
            kind="observation",
            text=f"Committed: {action}\nReasoning: {reasoning}\n"
                 f"Δvol_p expected={record.expected_delta:.2f} actual={record.actual_delta:.2f} "
                 f"residual={record.residual:.2f}",
            metadata={"commit_id": record.commit_id},
        )
        return record

    # --- RETRO ------------------------------------------------------------

    def retro_tuning_log(self, updates: list[dict]) -> None:
        """
        Write the RETRO phase's tuning decisions to memory so the user
        can review them. `updates` should be a list of TrustUpdate.as_dict()
        results. The memory entry is prose the user can read directly.
        """
        lines = ["RETRO tuning decisions for this cycle:"]
        for u in updates:
            lines.append(
                f"  [{u['category']}] {u['outcome']} → "
                f"{u['before']:.2f} → {u['after']:.2f} "
                f"(Δ={u['delta']:+.2f})"
            )
            if u.get("reasoning"):
                lines.append(f"    reasoning: {u['reasoning']}")
        self.memory.append(
            phase="retro",
            kind="retro_log",
            text="\n".join(lines),
            metadata={"updates": updates},
        )


def load_session(session_dir: Path, ledger: CapabilityLedger) -> HarnessSession:
    """
    Load a session from disk, or start a new one if the directory is empty.
    The trust model, memory archive, and commit log are all restored from
    disk if present; the ledger is passed in by the caller because each
    experiment typically builds its own initial ledger.
    """
    session_dir.mkdir(parents=True, exist_ok=True)
    memory = MemoryArchive.load(session_dir / "memory")
    commit_log = CommitLog.load(session_dir / "commits.jsonl")
    trust = SelfTrustModel.load(session_dir / "trust.json")
    return HarnessSession(
        session_dir=session_dir,
        ledger=ledger,
        memory=memory,
        trust=trust,
        commit_log=commit_log,
    )


def save_trust(session: HarnessSession) -> None:
    """Persist the current trust state. Call at end of each RETRO phase."""
    session.trust.save(session.session_dir / "trust.json")
