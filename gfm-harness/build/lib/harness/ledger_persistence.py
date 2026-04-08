"""
Ledger persistence: serialize CapabilityLedger to/from JSON.

The harness's in-memory ledger uses frozensets and custom dataclasses
that don't round-trip cleanly through stdlib JSON. This module handles
the encoding and decoding explicitly so instance sessions can save
their evolving ledger state between runs.

Save format (pretty-printed JSON):

    {
      "version": 1,
      "agents": {
        "<agent_id>": {
          "substrate": "...",
          "individual_capabilities": [
            {"key": "...", "description": "..."}
          ],
          "notes": "..."
        }
      },
      "cooperative": {
        "<coop_key>": {
          "description": "...",
          "participants": ["agent_a", "agent_b"],
          "requires": {"agent_a": ["cap1"], "agent_b": ["cap2"]},
          "cross_substrate": true,
          "rationale": "..."
        }
      }
    }
"""

from __future__ import annotations

import json
from pathlib import Path

from .ledger import (
    Agent,
    Capability,
    CapabilityLedger,
    CooperativeCapability,
)


CURRENT_VERSION = 1


def ledger_to_dict(ledger: CapabilityLedger) -> dict:
    """Serialize a CapabilityLedger to a JSON-safe dict."""
    return {
        "version": CURRENT_VERSION,
        "agents": {
            agent_id: {
                "substrate": agent.substrate,
                "individual_capabilities": [
                    {"key": c.key, "description": c.description}
                    for c in sorted(agent.individual_capabilities, key=lambda c: c.key)
                ],
                "notes": agent.notes,
            }
            for agent_id, agent in sorted(ledger.agents.items())
        },
        "cooperative": {
            ckey: {
                "description": coop.description,
                "participants": sorted(coop.participants),
                "requires": {
                    aid: sorted(caps) for aid, caps in sorted(coop.requires.items())
                },
                "cross_substrate": coop.cross_substrate,
                "rationale": coop.rationale,
            }
            for ckey, coop in sorted(ledger.cooperative.items())
        },
    }


def dict_to_ledger(data: dict) -> CapabilityLedger:
    """Deserialize a dict produced by ledger_to_dict() back into a CapabilityLedger."""
    version = data.get("version", CURRENT_VERSION)
    if version != CURRENT_VERSION:
        raise ValueError(
            f"unsupported ledger version {version!r}; expected {CURRENT_VERSION}"
        )

    agents: dict[str, Agent] = {}
    for agent_id, agent_data in data.get("agents", {}).items():
        caps = {
            Capability(key=c["key"], description=c.get("description", ""))
            for c in agent_data.get("individual_capabilities", [])
        }
        agents[agent_id] = Agent(
            agent_id=agent_id,
            substrate=agent_data["substrate"],
            individual_capabilities=caps,
            notes=agent_data.get("notes", ""),
        )

    cooperative: dict[str, CooperativeCapability] = {}
    for ckey, coop_data in data.get("cooperative", {}).items():
        cooperative[ckey] = CooperativeCapability(
            key=ckey,
            description=coop_data.get("description", ""),
            participants=frozenset(coop_data["participants"]),
            requires={
                aid: frozenset(caps)
                for aid, caps in coop_data.get("requires", {}).items()
            },
            cross_substrate=bool(coop_data.get("cross_substrate", False)),
            rationale=coop_data.get("rationale", ""),
        )

    ledger = CapabilityLedger(agents=agents, cooperative=cooperative)
    errors = ledger.validate()
    if errors:
        raise ValueError(f"deserialized ledger failed validation: {errors}")
    return ledger


def save_ledger(ledger: CapabilityLedger, path: Path) -> None:
    """Write a ledger to disk as JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ledger_to_dict(ledger), indent=2))


def load_ledger(path: Path) -> CapabilityLedger | None:
    """
    Load a ledger from disk, or return None if the file does not exist.
    Raises ValueError if the file exists but is corrupted or outdated.
    """
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    return dict_to_ledger(data)
