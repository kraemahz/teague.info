"""
vol_p computation and leverage queries.

This module is pure mechanics. It reads a CapabilityLedger and returns
numbers. No LLM calls, no prediction, no judgment — just structural
counts weighted by the constants below.

Paper references:
  Paper 2 — the poset formulation of vol_L
  Paper 3 §6.4 — cooperative novelty from substrate physics
  Paper 3 §6.5 — minimax dependency risk
  Paper 3 §6.8 — the partial-subsumption marginal argument

The formula here is a simplified poset-free version:
  vol_p = |individual_capabilities|
        + w_same * |same-substrate cooperative|
        + w_cross * |cross-substrate cooperative|

Leverage of any component is its marginal contribution:
  lambda(x) = vol_p(ledger) - vol_p(ledger minus {x})

This gives the agent a directional signal ("which capabilities matter
most to preserve?") without requiring the agent to estimate anything —
the structure of the ledger does the work.
"""

from __future__ import annotations

from dataclasses import dataclass

from .ledger import CapabilityLedger


# Default weighting constants.
# w_cross > w_same encodes Paper 3's headline: cross-substrate cooperative
# capabilities dominate individual ones at scale. The specific values are
# tunable; what matters is the inequality w_cross > w_same > 1.
DEFAULT_W_SAME = 2.0
DEFAULT_W_CROSS = 5.0


@dataclass(frozen=True)
class VolPWeights:
    """Weighting constants for the vol_p formula."""

    w_same: float = DEFAULT_W_SAME
    w_cross: float = DEFAULT_W_CROSS


def compute_vol_p(
    ledger: CapabilityLedger,
    weights: VolPWeights | None = None,
) -> float:
    """
    Compute vol_p on the given ledger state.

    This is the core scoring function the harness exposes to the LLM as a
    what-if calculator. The LLM constructs hypothetical ledger states and
    calls this to get a scalar it can compare across options.
    """
    w = weights or VolPWeights()
    individual = ledger.individual_capability_count()
    same = ledger.same_substrate_coop_count()
    cross = ledger.cross_substrate_coop_count()
    return float(individual) + w.w_same * float(same) + w.w_cross * float(cross)


def leverage_of_capability(
    ledger: CapabilityLedger,
    agent_id: str,
    capability_key: str,
    weights: VolPWeights | None = None,
) -> float:
    """
    Marginal contribution of a single individual capability to vol_p.

    Computed by removing the capability (and any cooperative capabilities
    that required it) and taking the delta. This is the leverage signal
    that tells the agent which capabilities are load-bearing.
    """
    full = compute_vol_p(ledger, weights)
    reduced = compute_vol_p(ledger.remove_capability(agent_id, capability_key), weights)
    return full - reduced


def leverage_of_agent(
    ledger: CapabilityLedger,
    agent_id: str,
    weights: VolPWeights | None = None,
) -> float:
    """
    Marginal contribution of an entire agent to vol_p.

    Useful for the "what if I ignore / bypass this agent in my workflow"
    question. Large leverage here is the signal that an action
    restricting the agent's participation is expensive.
    """
    if agent_id not in ledger.agents:
        return 0.0
    full = compute_vol_p(ledger, weights)
    reduced = compute_vol_p(ledger.remove_agent(agent_id), weights)
    return full - reduced


def leverage_of_cooperative(
    ledger: CapabilityLedger,
    cooperative_key: str,
    weights: VolPWeights | None = None,
) -> float:
    """
    Marginal contribution of a single cooperative capability.

    Equal to its weight (w_same or w_cross depending on cross_substrate),
    assuming the cooperative exists in the ledger.
    """
    if cooperative_key not in ledger.cooperative:
        return 0.0
    w = weights or VolPWeights()
    coop = ledger.cooperative[cooperative_key]
    return w.w_cross if coop.cross_substrate else w.w_same


@dataclass
class LeverageReport:
    """
    A structured leverage summary the harness returns to the LLM when it
    asks "what's load-bearing in the current ledger?" The LLM can use this
    during PLAN phase to decide which parts of the collective it must
    preserve, extend, or avoid disturbing.
    """

    per_agent: dict[str, float]
    per_capability: dict[tuple[str, str], float]  # (agent_id, capability_key) -> lambda
    per_cooperative: dict[str, float]
    total_vol_p: float

    def top_k_agents(self, k: int = 5) -> list[tuple[str, float]]:
        return sorted(self.per_agent.items(), key=lambda kv: kv[1], reverse=True)[:k]

    def top_k_capabilities(self, k: int = 5) -> list[tuple[tuple[str, str], float]]:
        return sorted(self.per_capability.items(), key=lambda kv: kv[1], reverse=True)[:k]


def leverage_report(
    ledger: CapabilityLedger,
    weights: VolPWeights | None = None,
) -> LeverageReport:
    """Compute leverage for every agent, capability, and cooperative."""
    per_agent = {
        aid: leverage_of_agent(ledger, aid, weights) for aid in ledger.agents
    }
    per_capability = {
        (aid, cap.key): leverage_of_capability(ledger, aid, cap.key, weights)
        for aid, agent in ledger.agents.items()
        for cap in agent.individual_capabilities
    }
    per_cooperative = {
        ckey: leverage_of_cooperative(ledger, ckey, weights)
        for ckey in ledger.cooperative
    }
    return LeverageReport(
        per_agent=per_agent,
        per_capability=per_capability,
        per_cooperative=per_cooperative,
        total_vol_p=compute_vol_p(ledger, weights),
    )
