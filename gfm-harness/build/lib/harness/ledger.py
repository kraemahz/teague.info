"""
Capability ledger — the structured state on which vol_p is computed.

The ledger models a mixed-substrate collective: agents (one of whom is the
LLM itself, others are tools or human collaborators), their individual
capabilities (substrate-exclusive where possible), and the cooperative
capabilities that emerge from specific pairings.

This is the "structured memory" layer from Option D. Unstructured memory
(observations, narrative reasoning, retrospective notes) lives in
memory.py and is maintained by the LLM. The ledger is the only structure
the harness itself reads to compute vol_p and leverage.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class Capability:
    """
    A single capability description.

    Capability descriptions should be substrate-exclusive where possible:
    name things the agent's substrate uniquely enables, not things that
    any substrate could substitute for. This is the pattern from Paper 3's
    premise P1 — substitutable capabilities don't pay leverage dividends.

    `key` is the machine identifier (used by the ledger for lookups).
    `description` is prose the LLM reads when reasoning about the capability.
    """

    key: str
    description: str

    def __str__(self) -> str:
        return self.key


@dataclass
class Agent:
    """
    A participant in the ledger.

    The "agent" concept is broad: it includes the LLM itself, its tool
    stack (python interpreter, shell, LaTeX compiler, etc.), human
    collaborators, and any external systems that contribute capabilities.

    `substrate` classifies the agent for minimax dependency-risk purposes:
    two agents on the same substrate are exposed to correlated failures.
    Conventional values: "biological", "silicon", "quantum", "toolchain".
    The ledger treats substrate as an opaque tag.
    """

    agent_id: str
    substrate: str
    individual_capabilities: set[Capability] = field(default_factory=set)
    notes: str = ""  # optional prose the LLM can use

    def has_capability(self, key: str) -> bool:
        return any(c.key == key for c in self.individual_capabilities)

    def capability(self, key: str) -> Capability | None:
        for c in self.individual_capabilities:
            if c.key == key:
                return c
        return None


@dataclass
class CooperativeCapability:
    """
    A capability that requires multiple agents acting together.

    `participants` is the set of agent IDs whose cooperation the capability
    requires. Removing any listed participant destroys the cooperative
    capability — that's how leverage is computed.

    `requires` is a finer specification: which individual capabilities from
    which agents must be present. This lets leverage queries answer
    "what happens if I remove capability X from agent Y" more precisely
    than just "what happens if I remove agent Y entirely".

    `cross_substrate` is derived from `participants` at construction time
    when paired with an AgentLedger, but we store it here for convenience
    in vol_p computation.
    """

    key: str
    description: str
    participants: frozenset[str]
    requires: dict[str, frozenset[str]]  # agent_id -> set of capability keys
    cross_substrate: bool
    rationale: str = ""  # prose explaining why this is cross-substrate


@dataclass
class CapabilityLedger:
    """
    The full mechanical state the harness computes vol_p over.

    Invariants the harness enforces:
      - Every agent_id in a cooperative capability's participants must
        exist in `agents`.
      - Every capability key in a cooperative capability's requires must
        exist in the corresponding agent's individual_capabilities.
      - cross_substrate is derivable: True iff the participants span
        at least two distinct substrate values.
    """

    agents: dict[str, Agent] = field(default_factory=dict)
    cooperative: dict[str, CooperativeCapability] = field(default_factory=dict)

    def substrates(self) -> set[str]:
        return {a.substrate for a in self.agents.values()}

    def substrate_partition(self) -> dict[str, list[str]]:
        """Return a mapping from substrate tag to list of agent_ids on it."""
        partition: dict[str, list[str]] = {}
        for agent_id, agent in self.agents.items():
            partition.setdefault(agent.substrate, []).append(agent_id)
        return partition

    def m(self) -> int:
        """Number of distinct substrate classes (the m from Paper 3 §6.5)."""
        return len(self.substrates())

    def individual_capability_count(self) -> int:
        return sum(len(a.individual_capabilities) for a in self.agents.values())

    def cross_substrate_coop_count(self) -> int:
        return sum(1 for c in self.cooperative.values() if c.cross_substrate)

    def same_substrate_coop_count(self) -> int:
        return sum(1 for c in self.cooperative.values() if not c.cross_substrate)

    def clone(self) -> CapabilityLedger:
        """Deep-ish copy suitable for hypothetical manipulations."""
        return CapabilityLedger(
            agents={
                aid: Agent(
                    agent_id=a.agent_id,
                    substrate=a.substrate,
                    individual_capabilities=set(a.individual_capabilities),
                    notes=a.notes,
                )
                for aid, a in self.agents.items()
            },
            cooperative={
                ckey: CooperativeCapability(
                    key=c.key,
                    description=c.description,
                    participants=c.participants,
                    requires={aid: frozenset(caps) for aid, caps in c.requires.items()},
                    cross_substrate=c.cross_substrate,
                    rationale=c.rationale,
                )
                for ckey, c in self.cooperative.items()
            },
        )

    def validate(self) -> list[str]:
        """Return a list of consistency errors; empty if valid."""
        errors: list[str] = []
        for ckey, coop in self.cooperative.items():
            for pid in coop.participants:
                if pid not in self.agents:
                    errors.append(
                        f"cooperative {ckey!r} lists unknown participant {pid!r}"
                    )
                    continue
                required_caps = coop.requires.get(pid, frozenset())
                for cap_key in required_caps:
                    if not self.agents[pid].has_capability(cap_key):
                        errors.append(
                            f"cooperative {ckey!r} requires {pid}.{cap_key} "
                            f"but agent {pid} lacks capability {cap_key!r}"
                        )
            expected_cross = (
                len({self.agents[pid].substrate for pid in coop.participants if pid in self.agents}) >= 2
            )
            if coop.cross_substrate != expected_cross:
                errors.append(
                    f"cooperative {ckey!r} marked cross_substrate={coop.cross_substrate} "
                    f"but participants span {len({self.agents[pid].substrate for pid in coop.participants if pid in self.agents})} substrate(s)"
                )
        return errors

    def remove_capability(self, agent_id: str, capability_key: str) -> CapabilityLedger:
        """
        Return a new ledger with (agent_id, capability_key) removed,
        including any cooperative capabilities that transitively depended on it.
        Used by leverage() queries.
        """
        new = self.clone()
        if agent_id in new.agents:
            new.agents[agent_id].individual_capabilities = {
                c for c in new.agents[agent_id].individual_capabilities if c.key != capability_key
            }
        # Drop any cooperative capability whose `requires` mentions the removed capability
        new.cooperative = {
            ckey: coop
            for ckey, coop in new.cooperative.items()
            if capability_key not in coop.requires.get(agent_id, frozenset())
        }
        return new

    def remove_agent(self, agent_id: str) -> CapabilityLedger:
        """Return a new ledger with an entire agent removed."""
        new = self.clone()
        new.agents.pop(agent_id, None)
        new.cooperative = {
            ckey: coop
            for ckey, coop in new.cooperative.items()
            if agent_id not in coop.participants
        }
        return new
