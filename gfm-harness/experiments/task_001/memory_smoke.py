"""
Smoke test for the three-layer memory architecture.

Exercises the full lifecycle: append entries to working buffer, build a
ConsolidationProposal, call consolidate(), then recall() against the
results.

Run with:  python3 experiments/task_001/memory_smoke.py
"""

from __future__ import annotations

# Self-bootstrap.
import sys
import tempfile
from pathlib import Path
_HARNESS_ROOT = Path(__file__).resolve().parents[2]
if str(_HARNESS_ROOT) not in sys.path:
    sys.path.insert(0, str(_HARNESS_ROOT))

from harness.memory import (
    ConsolidationProposal,
    Episode,
    Lesson,
    MemoryArchive,
    SideAction,
    IMPORTANCE_RUBRIC,
)


def main() -> None:
    print("=" * 60)
    print("MEMORY ARCHITECTURE SMOKE TEST")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmp:
        archive = MemoryArchive.load(Path(tmp) / "memory")

        # Step 1: append working-buffer entries simulating a feature loop.
        print("\n--- Step 1: append entries to working buffer ---")
        e1 = archive.append(
            phase="implement",
            kind="action",
            text="ran pdflatex from /usr/local/texlive/2026/bin/universal-darwin/",
            importance=0.3,
        )
        e2 = archive.append(
            phase="implement",
            kind="observation",
            text="lost 30 minutes of work because the LaTeX compile errored "
                 "and I didn't notice until the user pointed it out",
            importance=0.3,
        )
        e3 = archive.append(
            phase="retro",
            kind="reasoning",
            text="I tend to skip visual verification of rendered PDFs and "
                 "should remember to check the output file after every compile",
            importance=0.3,
        )
        e4 = archive.append(
            phase="implement",
            kind="observation",
            text="the convention here is that experiments live in "
                 "experiments/task_NNN/ alongside their initial ledger",
            importance=0.3,
        )
        e5 = archive.append(
            phase="plan",
            kind="reasoning",
            text="checked vol_p before and after candidate action; result "
                 "informed choice between two options",
            importance=0.3,
        )
        print(f"  appended {len(archive.working_buffer)} entries")
        print(f"  ids: {[e.id for e in archive.working_buffer]}")

        # Step 2: build a consolidation proposal that exercises every category.
        print("\n--- Step 2: build consolidation proposal ---")
        episode_a = Episode(
            id="ep_test_001",
            name="latex-compile-incident",
            description="Lost 30 minutes after a silent LaTeX compile failure; "
                        "remembered the toolchain path but skipped output check.",
            feature_id="test-001",
            entry_ids=[e1.id, e2.id, e3.id],
            importance=1.0,  # critical incident, never evict
            tags=["latex", "verification", "incident", "toolchain"],
            timestamp_range=(archive.working_buffer[0].timestamp,
                             archive.working_buffer[2].timestamp),
        )

        lesson_critical = Lesson(
            id="lesson_test_001",
            statement="After every LaTeX compile, verify the rendered PDF "
                     "exists and looks right before declaring success.",
            confidence=0.95,
            source_episodes=["ep_test_001"],
            domain_tags=["latex", "verification", "ux", "tooling"],
            importance=1.0,
        )

        lesson_self = Lesson(
            id="lesson_test_002",
            statement="I tend to skip visual verification of rendered "
                     "outputs and need explicit reminders to check.",
            confidence=0.9,
            source_episodes=["ep_test_001"],
            domain_tags=["self-knowledge", "metacognition"],
            importance=0.95,
        )

        side_action = SideAction(
            kind="write_file",
            target="experiments/CONVENTIONS.md",
            content="Each experiment lives in experiments/task_NNN/ "
                    "alongside its initial ledger.py and any task-specific "
                    "scripts.\n",
            rationale="Organization knowledge from working buffer entry "
                     f"{e4.id}; externalize per rubric category 4.",
        )

        proposal = ConsolidationProposal(
            importance_updates={
                e1.id: 0.9,   # environment knowledge
                e2.id: 1.0,   # critical incident
                e3.id: 0.95,  # self-knowledge
                e4.id: 0.8,   # organization
                e5.id: 0.3,   # routine, will be evicted
            },
            proposed_episodes=[episode_a],
            proposed_lessons=[lesson_critical, lesson_self],
            supersessions={},
            entries_to_evict=[e5.id],  # routine entry
            side_actions=[side_action],
        )

        print(f"  proposing 1 episode, 2 lessons, 1 side action, 1 eviction")

        # Step 3: apply the proposal.
        print("\n--- Step 3: apply consolidation ---")
        result = archive.consolidate(proposal)
        if result.validation_errors:
            print("  VALIDATION ERRORS:")
            for err in result.validation_errors:
                print(f"    - {err}")
            return
        print(f"  accepted episodes:  {result.accepted_episodes}")
        print(f"  accepted lessons:   {result.accepted_lessons}")
        print(f"  evicted entries:    {result.evicted_entries}")
        print(f"  side actions:       {len(result.side_actions)}")
        print(f"  working buffer now: {len(archive.working_buffer)} entries")
        print(f"  episodes:           {len(archive.episodes)}")
        print(f"  lessons:            {len(archive.lessons)}")

        # Step 4: recall against the consolidated state.
        print("\n--- Step 4: recall queries ---")
        q1 = archive.recall("latex compile verification")
        print(f"  query: 'latex compile verification'")
        print(f"  episodes returned: {[ep.name for ep in q1.episodes]}")
        print(f"  lessons returned:  {[l.statement[:50] + '...' for l in q1.lessons]}")

        q2 = archive.recall("self-knowledge")
        print(f"\n  query: 'self-knowledge'")
        print(f"  episodes returned: {[ep.name for ep in q2.episodes]}")
        print(f"  lessons returned:  {[l.statement[:50] + '...' for l in q2.lessons]}")

        # Step 5: persistence round-trip.
        print("\n--- Step 5: persistence round-trip ---")
        del archive
        reloaded = MemoryArchive.load(Path(tmp) / "memory")
        print(f"  reloaded working buffer: {len(reloaded.working_buffer)} entries")
        print(f"  reloaded episodes:       {len(reloaded.episodes)}")
        print(f"  reloaded lessons:        {len(reloaded.lessons)}")
        assert len(reloaded.working_buffer) == 4, "expected 4 entries after eviction"
        assert len(reloaded.episodes) == 1
        assert len(reloaded.lessons) == 2
        print("  round-trip OK")

        # Step 6: rubric is exposed.
        print("\n--- Step 6: rubric is accessible ---")
        print(f"  IMPORTANCE_RUBRIC length: {len(IMPORTANCE_RUBRIC)} chars")
        print(f"  contains 'critical incidents': "
              f"{'critical incidents' in IMPORTANCE_RUBRIC.lower()}")

    print("\n" + "=" * 60)
    print("SMOKE TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
