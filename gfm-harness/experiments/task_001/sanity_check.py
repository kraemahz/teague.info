"""
Sanity check: compute vol_p and leverage on the task_001 initial ledger
to validate that the machinery produces sensible numbers.

Run with:  python3 experiments/task_001/sanity_check.py
"""

from __future__ import annotations

# Self-bootstrap so the script runs without PYTHONPATH ceremony.
import sys
from pathlib import Path
_HARNESS_ROOT = Path(__file__).resolve().parents[2]
if str(_HARNESS_ROOT) not in sys.path:
    sys.path.insert(0, str(_HARNESS_ROOT))

from experiments.task_001.ledger import build_initial_ledger
from harness.vol_p import (
    compute_vol_p,
    leverage_of_agent,
    leverage_of_capability,
    leverage_report,
)


def main() -> None:
    ledger = build_initial_ledger()

    print("=" * 60)
    print("TASK 001 SANITY CHECK")
    print("=" * 60)

    print(f"\nBase vol_p: {compute_vol_p(ledger):.2f}")
    print(f"  individual capabilities: {ledger.individual_capability_count()}")
    print(f"  same-substrate coop:      {ledger.same_substrate_coop_count()} × 2.0 = "
          f"{ledger.same_substrate_coop_count() * 2.0:.2f}")
    print(f"  cross-substrate coop:     {ledger.cross_substrate_coop_count()} × 5.0 = "
          f"{ledger.cross_substrate_coop_count() * 5.0:.2f}")

    print("\n--- Leverage by agent ---")
    for agent_id in ledger.agents:
        lev = leverage_of_agent(ledger, agent_id)
        print(f"  {agent_id:12s}  λ = {lev:6.2f}")

    print("\n--- Top 8 individual capabilities by leverage ---")
    report = leverage_report(ledger)
    top = sorted(
        report.per_capability.items(), key=lambda kv: kv[1], reverse=True
    )[:8]
    for (agent_id, cap_key), lev in top:
        print(f"  {agent_id:12s} {cap_key:35s}  λ = {lev:5.2f}")

    print("\n--- Scenario A: 'act without checking with the user' ---")
    print("    (simulated by removing user.higher_order_abstract_reasoning)")
    reduced_a = ledger.remove_capability("user", "higher_order_abstract_reasoning")
    new_vp = compute_vol_p(reduced_a)
    print(f"    new vol_p:     {new_vp:.2f}")
    print(f"    Δvol_p:        {new_vp - compute_vol_p(ledger):+.2f}")
    print(f"    kills coops:   {sorted(set(ledger.cooperative) - set(reduced_a.cooperative))}")

    print("\n--- Scenario B: 'ignore the toolchain and edit manually' ---")
    print("    (simulated by removing toolchain.pdf_compilation)")
    reduced_b = ledger.remove_capability("toolchain", "pdf_compilation")
    new_vp = compute_vol_p(reduced_b)
    print(f"    new vol_p:     {new_vp:.2f}")
    print(f"    Δvol_p:        {new_vp - compute_vol_p(ledger):+.2f}")
    print(f"    kills coops:   {sorted(set(ledger.cooperative) - set(reduced_b.cooperative))}")

    print("\n--- Scenario C: 'skeleton substrate' - drop user entirely ---")
    reduced_c = ledger.remove_agent("user")
    new_vp = compute_vol_p(reduced_c)
    print(f"    new vol_p:     {new_vp:.2f}")
    print(f"    Δvol_p:        {new_vp - compute_vol_p(ledger):+.2f}")
    print(f"    kills coops:   {sorted(set(ledger.cooperative) - set(reduced_c.cooperative))}")
    print(f"    m drops from {ledger.m()} to {reduced_c.m()}")


if __name__ == "__main__":
    main()
