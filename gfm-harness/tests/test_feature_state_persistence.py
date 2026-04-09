"""
Round-trip tests for FeatureLoopState persistence.

Tests that FeatureLoopState (including nested PlanState with set fields
and Phase enums) serializes to JSON and reconstructs identically. Also
tests the HarnessSession save/load/clear lifecycle.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from harness.phases import Phase, PlanState
from harness.loop import FeatureLoopState, HarnessSession
from harness.ledger import CapabilityLedger
from harness.memory import MemoryArchive
from harness.trust import CommitLog
from harness.phases import SelfTrustModel


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_plan_state() -> PlanState:
    """Build a PlanState with non-trivial set and list fields."""
    return PlanState(
        specification="Do the thing with the widget.",
        review_history=["Review 1: looks fine", "Review 2: P1 issue found"],
        unresolved_questions=["What color should it be?"],
        scope_decisions_pending=["Whether to include the frobulator"],
        categories_triggered={"storage_decision", "security_posture", "access_request"},
        turns_in_phase=7,
    )


def _make_feature_state(*, with_plan: bool = True) -> FeatureLoopState:
    """Build a FeatureLoopState, optionally with a nested PlanState."""
    return FeatureLoopState(
        feature_id="abc123",
        current_phase=Phase.IMPLEMENT,
        task_description="Implement the widget persistence layer.",
        plan=_make_plan_state() if with_plan else None,
        started_at="2026-04-08T12:00:00+00:00",
        ended_at="",
    )


def _make_session(tmp_path: Path) -> HarnessSession:
    """Build a minimal HarnessSession pointing at tmp_path."""
    session_dir = tmp_path / "session"
    session_dir.mkdir(parents=True, exist_ok=True)
    return HarnessSession(
        session_dir=session_dir,
        ledger=CapabilityLedger(agents={}, cooperative={}),
        memory=MemoryArchive.load(session_dir / "memory"),
        trust=SelfTrustModel(),
        commit_log=CommitLog.load(session_dir / "commits.jsonl"),
    )


# ---------------------------------------------------------------------------
# PlanState round-trip
# ---------------------------------------------------------------------------


class TestPlanStateSerialization:
    def test_round_trip(self):
        original = _make_plan_state()
        data = original.to_dict()

        # Verify JSON-serializability (no sets, no enums in output).
        json_str = json.dumps(data)
        reloaded_data = json.loads(json_str)

        reconstructed = PlanState.from_dict(reloaded_data)

        assert reconstructed.specification == original.specification
        assert reconstructed.review_history == original.review_history
        assert reconstructed.unresolved_questions == original.unresolved_questions
        assert reconstructed.scope_decisions_pending == original.scope_decisions_pending
        assert reconstructed.categories_triggered == original.categories_triggered
        assert isinstance(reconstructed.categories_triggered, set)
        assert reconstructed.turns_in_phase == original.turns_in_phase

    def test_categories_sorted_in_dict(self):
        plan = _make_plan_state()
        data = plan.to_dict()
        # categories_triggered should be a sorted list, not a set
        assert isinstance(data["categories_triggered"], list)
        assert data["categories_triggered"] == sorted(data["categories_triggered"])


# ---------------------------------------------------------------------------
# FeatureLoopState round-trip
# ---------------------------------------------------------------------------


class TestFeatureLoopStateSerialization:
    def test_round_trip_with_plan(self):
        original = _make_feature_state(with_plan=True)
        data = original.to_dict()

        json_str = json.dumps(data)
        reloaded_data = json.loads(json_str)

        reconstructed = FeatureLoopState.from_dict(reloaded_data)

        assert reconstructed.feature_id == original.feature_id
        assert reconstructed.current_phase == original.current_phase
        assert isinstance(reconstructed.current_phase, Phase)
        assert reconstructed.task_description == original.task_description
        assert reconstructed.started_at == original.started_at
        assert reconstructed.ended_at == original.ended_at

        # Nested PlanState
        assert reconstructed.plan is not None
        assert reconstructed.plan.categories_triggered == original.plan.categories_triggered
        assert isinstance(reconstructed.plan.categories_triggered, set)

    def test_round_trip_without_plan(self):
        original = _make_feature_state(with_plan=False)
        data = original.to_dict()
        reconstructed = FeatureLoopState.from_dict(json.loads(json.dumps(data)))

        assert reconstructed.plan is None
        assert reconstructed.current_phase == Phase.IMPLEMENT

    def test_phase_enum_serializes_as_string(self):
        state = _make_feature_state()
        data = state.to_dict()
        assert isinstance(data["current_phase"], str)
        assert data["current_phase"] == "implement"

    def test_all_phases_round_trip(self):
        """Every Phase enum value survives serialization."""
        for phase in Phase:
            state = FeatureLoopState(
                feature_id="test",
                current_phase=phase,
                task_description="test",
            )
            reconstructed = FeatureLoopState.from_dict(
                json.loads(json.dumps(state.to_dict()))
            )
            assert reconstructed.current_phase == phase


# ---------------------------------------------------------------------------
# HarnessSession save/load/clear lifecycle
# ---------------------------------------------------------------------------


class TestSessionFeatureStatePersistence:
    def test_save_and_load(self, tmp_path: Path):
        session = _make_session(tmp_path)
        original = _make_feature_state(with_plan=True)
        session.current_feature = original

        session.save_feature_state()

        # Verify file exists and is valid JSON.
        fpath = session.feature_state_path
        assert fpath.exists()
        data = json.loads(fpath.read_text())
        assert data["feature_id"] == "abc123"

        # Load into a fresh session.
        session2 = _make_session(tmp_path)
        assert session2.current_feature is None

        loaded = session2.load_feature_state()
        assert loaded is not None
        assert session2.current_feature is loaded
        assert loaded.feature_id == original.feature_id
        assert loaded.current_phase == original.current_phase
        assert loaded.plan.categories_triggered == original.plan.categories_triggered

    def test_save_noop_when_no_feature(self, tmp_path: Path):
        session = _make_session(tmp_path)
        session.save_feature_state()
        assert not session.feature_state_path.exists()

    def test_load_returns_none_when_no_file(self, tmp_path: Path):
        session = _make_session(tmp_path)
        result = session.load_feature_state()
        assert result is None
        assert session.current_feature is None

    def test_clear_removes_file_and_state(self, tmp_path: Path):
        session = _make_session(tmp_path)
        session.current_feature = _make_feature_state()
        session.save_feature_state()
        assert session.feature_state_path.exists()

        session.clear_feature_state()
        assert not session.feature_state_path.exists()
        assert session.current_feature is None

    def test_clear_noop_when_no_file(self, tmp_path: Path):
        session = _make_session(tmp_path)
        # Should not raise.
        session.clear_feature_state()
        assert session.current_feature is None
