"""
Smoke test for the tool dispatch layer.

Exercises apply_ledger_ops and dispatch_tool_call without making any
API calls — the LLM-facing tools are all callable directly with
dict inputs that match the schemas defined in tools.py.

Run with:  python3 experiments/task_001/tools_smoke.py
"""

from __future__ import annotations

# Self-bootstrap.
import sys
import tempfile
from pathlib import Path
_HARNESS_ROOT = Path(__file__).resolve().parents[2]
if str(_HARNESS_ROOT) not in sys.path:
    sys.path.insert(0, str(_HARNESS_ROOT))

from experiments.task_001.ledger import build_initial_ledger
from harness.loop import load_session
from harness.tools import (
    PauseForUser,
    apply_ledger_ops,
    dispatch_tool_call,
    tool_schemas,
)


def main() -> None:
    print("=" * 60)
    print("TOOLS SMOKE TEST")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmp:
        session = load_session(Path(tmp) / "session", build_initial_ledger())
        session.begin_feature("tool-layer smoke test")

        print("\n--- 1. compute_vol_p with no ops ---")
        result, is_error = dispatch_tool_call(session, "compute_vol_p", {"ops": []})
        assert not is_error
        print(result)

        print("\n--- 2. compute_vol_p with an add_cooperative op ---")
        ops = [
            {
                "type": "add_cooperative",
                "key": "test_new_coop",
                "description": "A hypothetical new cross-substrate cooperative.",
                "participants": ["user", "llm"],
                "requires": {
                    "user": ["long_tail_context"],
                    "llm": ["fast_iteration"],
                },
                "rationale": "Testing the hypothetical query machinery.",
            },
        ]
        result, is_error = dispatch_tool_call(
            session, "compute_vol_p", {"ops": ops, "rationale": "adding a coop"}
        )
        assert not is_error
        print(result)

        print("\n--- 3. compute_vol_p with a destructive op (remove user) ---")
        ops = [{"type": "remove_agent", "agent_id": "user"}]
        result, is_error = dispatch_tool_call(session, "compute_vol_p", {"ops": ops})
        assert not is_error
        print(result)

        print("\n--- 4. leverage_report ---")
        result, is_error = dispatch_tool_call(session, "leverage_report", {})
        assert not is_error
        # Truncate for display
        print(result[:400] + "...")

        print("\n--- 5. read_ledger ---")
        result, is_error = dispatch_tool_call(session, "read_ledger", {})
        assert not is_error
        print(result[:400] + "...")

        print("\n--- 6. append_memory ---")
        result, is_error = dispatch_tool_call(
            session,
            "append_memory",
            {
                "kind": "reasoning",
                "text": "Evaluating the add_cooperative hypothetical showed +5 vol_p.",
                "importance": 0.5,
            },
        )
        assert not is_error
        print(result)

        print("\n--- 7. recall (empty archive) ---")
        result, is_error = dispatch_tool_call(session, "recall", {"query": "latex"})
        assert not is_error
        print(result)

        print("\n--- 8. transition_to implement ---")
        result, is_error = dispatch_tool_call(
            session, "transition_to", {"phase": "implement", "reason": "plan converged"}
        )
        assert not is_error
        print(result)

        print("\n--- 9. commit (IMPLEMENT-phase) ---")
        result, is_error = dispatch_tool_call(
            session,
            "commit",
            {
                "action": "added test_new_coop to ledger",
                "reasoning": "hypothetical scored +5; real-world equivalent now committed",
                "categories_triggered": ["result_interpretation"],
                "ledger_ops": [
                    {
                        "type": "add_cooperative",
                        "key": "test_new_coop",
                        "description": "A new cross-substrate cooperative for the smoke test.",
                        "participants": ["user", "llm"],
                        "requires": {
                            "user": ["long_tail_context"],
                            "llm": ["fast_iteration"],
                        },
                        "rationale": "smoke test",
                    }
                ],
                "expected_vol_p": 45.0,
            },
        )
        assert not is_error
        print(result)

        print("\n--- 10. pause_for_user raises control-flow exception ---")
        caught = None
        try:
            dispatch_tool_call(
                session,
                "pause_for_user",
                {
                    "reason": "Need guidance on scope of the change",
                    "questions": ["Should we extend this to silicon-silicon coops too?"],
                    "categories": ["scope_decision"],
                },
            )
        except PauseForUser as exc:
            caught = exc
        assert caught is not None
        print(f"caught PauseForUser: reason={caught.reason!r}")
        print(f"  questions={caught.questions}")
        print(f"  categories={caught.categories}")

        print("\n--- 11. unknown tool returns error ---")
        result, is_error = dispatch_tool_call(session, "nonexistent_tool", {})
        assert is_error
        print(f"is_error={is_error}: {result}")

        print("\n--- 12. bad ledger op returns validation errors ---")
        result, is_error = dispatch_tool_call(
            session,
            "compute_vol_p",
            {
                "ops": [
                    {
                        "type": "add_cooperative",
                        "key": "broken_coop",
                        "participants": ["nonexistent_agent"],
                    }
                ]
            },
        )
        assert not is_error  # dispatch didn't raise; errors are in the result
        print(result)

        print("\n--- 13. Tool schemas are well-formed JSON ---")
        schemas = tool_schemas()
        for s in schemas:
            assert "name" in s and "description" in s and "input_schema" in s
            assert s["input_schema"]["type"] == "object"
        print(f"  {len(schemas)} tool schemas validated")

    print("\n" + "=" * 60)
    print("TOOLS SMOKE TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
