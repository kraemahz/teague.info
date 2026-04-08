"""
Phase model and self-trust.

The feature loop has four phases: PLAN, IMPLEMENT, VERIFY, RETRO.
Phase transitions are checkpoints; the harness commits to the ledger
only during IMPLEMENT. This module holds the state machine definitions
and the SelfTrustModel that determines when PLAN phase should exit by
pausing for user direction vs. proceeding to IMPLEMENT autonomously.

See constitution.md for the prose description of phase semantics.
See RETRO_LOG format at the bottom of this file — RETRO produces a
reviewable log of its tuning decisions so the user can inspect the
self-trust updates before the agent is trusted to self-modify.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Phase(Enum):
    PLAN = "plan"
    IMPLEMENT = "implement"
    VERIFY = "verify"
    RETRO = "retro"


class PauseOutcome(Enum):
    """How RETRO classifies a past pause's user response."""

    PRODUCTIVE = "productive"      # User contributed substantive direction
    UNNECESSARY = "unnecessary"    # User just approved ("yes", "go ahead")
    INTERRUPT = "interrupt"        # User broke in mid-action (recorded via record_interrupt)


# Default tuning constants for SelfTrustModel.
# The asymmetric deltas bias toward caution: interrupts hit harder than
# unnecessary pauses reward, so the agent needs repeated confirmation
# before it stops pausing in a category, but a single interrupt brings
# pausing back immediately.
PRODUCTIVE_DELTA = -0.02   # productive pause: slight downward pressure (keep pausing here)
UNNECESSARY_DELTA = +0.08  # unnecessary pause: stronger upward pressure (stop pausing here)
INTERRUPT_DELTA = -0.25    # interrupt: strong downward pressure (start pausing here again)
DEFAULT_PAUSE_THRESHOLD = 0.7


# Initial decision categories.
# These are drawn from empirical failure modes in Teague's manual workflow
# with LLM agents, not from abstract reasoning about decision types.
# Each one names a specific behavior that has historically gone wrong.
#
# All start at 0.0 (always pause) per the "start low, climb through
# calibration" philosophy. Categories climb out of 0.0 as the RETRO
# phase accumulates unnecessary-pause signals.
#
# Floors override this for categories where the agent should always ask
# regardless of feedback history. security_posture is the only floored
# category in v1 — Teague explicitly opted for "always ask" on security.
INITIAL_CATEGORIES: dict[str, float] = {
    "storage_decision":       0.0,  # where data lives — paths, databases, cloud targets
    "security_posture":       0.0,  # auth, permissions, credential exposure, public/private
    "deep_filesystem_trawl":  0.0,  # broad grep/find across unfamiliar territory
    "access_request":         0.0,  # the agent needs something only the user can sign in for
    "infrastructure_failure": 0.0,  # tests/services down; should the agent ask to restart?
    "result_interpretation":  0.0,  # is the output actually correct, or just "close enough"?
    "visual_inspection":      0.0,  # does the rendered thing actually look right?
    "execution_environment":  0.0,  # resource cost, local vs cloud, available infrastructure
}

INITIAL_FLOORS: dict[str, float] = {
    # security_posture has a floor of the pause threshold itself, which means
    # the trust value cannot climb above the pause threshold and the category
    # effectively always triggers a pause. This is the "always ask" floor.
    # Other categories have no floor in v1 — Teague wants to observe RETRO's
    # tuning behavior before committing to let the agent stop asking.
    "security_posture": DEFAULT_PAUSE_THRESHOLD,
}


@dataclass
class SelfTrustModel:
    """
    Per-category trust levels that determine pause frequency.

    Higher trust → pause less. Lower trust → pause more. Updated in the
    RETRO phase from classified pause outcomes and from user interrupts.

    Starts conservative (all categories pause by default) and tunes
    upward as the agent demonstrates it can be trusted in each category.

    Floors cap how high a category's trust can climb. A floor at or above
    `pause_threshold` means the category will always pause regardless of
    feedback history — this is the "always ask" setting.
    """

    category_trust: dict[str, float] = field(
        default_factory=lambda: dict(INITIAL_CATEGORIES)
    )
    category_floors: dict[str, float] = field(
        default_factory=lambda: dict(INITIAL_FLOORS)
    )
    pause_threshold: float = DEFAULT_PAUSE_THRESHOLD
    productive_delta: float = PRODUCTIVE_DELTA
    unnecessary_delta: float = UNNECESSARY_DELTA
    interrupt_delta: float = INTERRUPT_DELTA

    def should_pause(self, category: str) -> bool:
        """
        Query during PLAN phase exit to decide PLAN → IMPLEMENT vs
        PLAN → user-direction. Returns True if the current trust level
        in this category is below the pause threshold.

        If the category is floored at or above the pause threshold,
        should_pause always returns True regardless of learned trust.
        """
        floor = self.category_floors.get(category, 0.0)
        if floor >= self.pause_threshold:
            return True  # always-ask floor
        trust = self.category_trust.get(category, 0.0)
        return trust < self.pause_threshold

    def record_pause_outcome(
        self,
        category: str,
        outcome: PauseOutcome,
        reasoning: str = "",
    ) -> "TrustUpdate":
        """
        Called during RETRO after classifying each past pause's user
        response. Returns a TrustUpdate record describing what changed
        and why, which gets appended to the RETRO log for user review.
        """
        if outcome == PauseOutcome.INTERRUPT:
            # Interrupts come through record_interrupt() normally, but handle
            # defensively in case RETRO classifies a "pause" retroactively
            # as an interrupt.
            return self.record_interrupt(category, reasoning)

        before = self.category_trust.get(category, 0.0)
        delta = (
            self.productive_delta
            if outcome == PauseOutcome.PRODUCTIVE
            else self.unnecessary_delta
        )
        floor = self.category_floors.get(category, 0.0)
        # Floor caps the lower bound on trust; pause_threshold caps the upper
        # bound for floored categories.
        proposed = before + delta
        if floor >= self.pause_threshold:
            # Floored at always-ask: don't let trust climb.
            proposed = min(proposed, self.pause_threshold - 0.01)
        after = max(0.0, min(1.0, proposed))
        self.category_trust[category] = after

        return TrustUpdate(
            category=category,
            outcome=outcome,
            delta=after - before,
            before=before,
            after=after,
            reasoning=reasoning,
        )

    def record_interrupt(
        self,
        category: str,
        reasoning: str = "",
    ) -> "TrustUpdate":
        """
        Called when the user interrupts the agent mid-action. Applies
        interrupt_delta to the category and returns the update record.
        """
        before = self.category_trust.get(category, 0.0)
        after = max(0.0, before + self.interrupt_delta)
        self.category_trust[category] = after
        return TrustUpdate(
            category=category,
            outcome=PauseOutcome.INTERRUPT,
            delta=after - before,
            before=before,
            after=after,
            reasoning=reasoning,
        )

    def snapshot(self) -> dict[str, Any]:
        """Return a serializable snapshot of the current trust state."""
        return {
            "category_trust": dict(self.category_trust),
            "category_floors": dict(self.category_floors),
            "pause_threshold": self.pause_threshold,
            "deltas": {
                "productive": self.productive_delta,
                "unnecessary": self.unnecessary_delta,
                "interrupt": self.interrupt_delta,
            },
        }

    def save(self, path) -> None:
        """Persist the trust state to a JSON file."""
        import json
        from pathlib import Path

        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(self.snapshot(), indent=2))

    @classmethod
    def load(cls, path) -> "SelfTrustModel":
        """
        Load trust state from a JSON file, or return a fresh default
        instance if the file does not exist. Floor overrides from
        INITIAL_FLOORS are always applied after loading, so a category
        added to INITIAL_FLOORS in a new release takes effect even if
        the saved file predates it.
        """
        import json
        from pathlib import Path

        p = Path(path)
        if not p.exists():
            return cls()

        data = json.loads(p.read_text())
        deltas = data.get("deltas", {})
        model = cls(
            category_trust=dict(data.get("category_trust", INITIAL_CATEGORIES)),
            category_floors=dict(data.get("category_floors", INITIAL_FLOORS)),
            pause_threshold=data.get("pause_threshold", DEFAULT_PAUSE_THRESHOLD),
            productive_delta=deltas.get("productive", PRODUCTIVE_DELTA),
            unnecessary_delta=deltas.get("unnecessary", UNNECESSARY_DELTA),
            interrupt_delta=deltas.get("interrupt", INTERRUPT_DELTA),
        )
        # Re-apply floors from INITIAL_FLOORS in case new floored categories
        # were added after this snapshot was saved.
        for cat, floor in INITIAL_FLOORS.items():
            if cat not in model.category_floors:
                model.category_floors[cat] = floor
        return model


@dataclass
class TrustUpdate:
    """
    A single trust update event, emitted by RETRO for user review.
    Appended to retro_log in the trajectory store.
    """

    category: str
    outcome: PauseOutcome
    delta: float
    before: float
    after: float
    reasoning: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "outcome": self.outcome.value,
            "delta": self.delta,
            "before": self.before,
            "after": self.after,
            "reasoning": self.reasoning,
        }


# --- Phase transition guards ---------------------------------------------


@dataclass
class PlanState:
    """
    Snapshot of what the agent has produced during the PLAN phase.
    Used by the transition logic to decide whether to proceed to
    IMPLEMENT or pause for user direction.
    """

    specification: str
    review_history: list[str]
    unresolved_questions: list[str]
    scope_decisions_pending: list[str]
    categories_triggered: set[str]  # categories the planned action falls into
    turns_in_phase: int


def plan_exit_decision(
    plan: PlanState,
    trust: SelfTrustModel,
) -> "PlanExit":
    """
    Decide how the PLAN phase should exit. Three outcomes:

    1. PROCEED — plan has converged (no P1 claims surfaced in latest
       review iteration, no unresolved questions, no trust pauses
       triggered) → transition to IMPLEMENT.
    2. PAUSE_FOR_USER — something requires user direction (unresolved
       questions, or one of the triggered categories has should_pause
       returning True).
    3. CONTINUE_DELIBERATING — the plan isn't converged yet; keep running
       the review loop.
    """
    # Convergence check: review has stopped surfacing P1 claims.
    latest_review = plan.review_history[-1] if plan.review_history else ""
    has_p1_claims = "P1" in latest_review or "p1" in latest_review
    if has_p1_claims:
        return PlanExit(
            kind="continue",
            reason="review still surfacing P1 claims",
            pause_categories=[],
        )

    # Unresolved questions always force a pause.
    if plan.unresolved_questions:
        return PlanExit(
            kind="pause",
            reason=f"unresolved questions: {plan.unresolved_questions}",
            pause_categories=[],
        )

    # Trust-gated categories: any category the action triggers where the
    # agent's trust is below threshold (or floored) forces a pause.
    pause_categories = [
        cat for cat in plan.categories_triggered if trust.should_pause(cat)
    ]
    if pause_categories:
        return PlanExit(
            kind="pause",
            reason=f"trust-gated pause on categories: {pause_categories}",
            pause_categories=pause_categories,
        )

    return PlanExit(
        kind="proceed",
        reason="plan converged, no pause categories triggered",
        pause_categories=[],
    )


@dataclass
class PlanExit:
    """Result of plan_exit_decision."""

    kind: str  # "proceed" | "pause" | "continue"
    reason: str
    pause_categories: list[str]
