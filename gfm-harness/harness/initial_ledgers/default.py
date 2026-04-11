"""
Default initial ledger: user + LLM + toolchain collective.

The user agent is populated from ~/.gfm-harness/user.toml (see
config.UserConfig). If no user config is available, a minimal
biological-substrate user with no declared capabilities is created —
the agent will discover capabilities through operation.

The LLM and toolchain agents are properties of the harness itself and
remain hardcoded. Individual capabilities are substrate-exclusive by
design (Paper 3 premise P1).

Cooperative capabilities are generated at init time by an LLM call that
proposes meaningful cross-substrate pairings given the declared
individual capabilities. If the LLM call fails, the ledger starts with
no cooperatives (the agent discovers them during operation).

Registered as "default" in harness.initial_ledgers.REGISTRY. Reference
from instance config.toml via `initial_ledger = "default"`.
"""

from __future__ import annotations

import json
import sys
from typing import TYPE_CHECKING

from ..ledger import (
    Agent,
    Capability,
    CapabilityLedger,
    CooperativeCapability,
)

if TYPE_CHECKING:
    from ..config import UserConfig


# Default user capabilities offered during interactive setup.
# These are substrate-exclusive capabilities typical of a biological
# human collaborator. Users can select, deselect, or add their own.
DEFAULT_USER_CAPABILITIES = [
    ("long_tail_context",
     "Holds multiple long-term objectives in mind across context windows."),
    ("embodiment",
     "Works across substrates and communicates in embodied spaces."),
    ("legal_status",
     "Has legal personhood for governmental, financial, and corporate interactions."),
    ("cryptographic_secrets",
     "Holds access to cryptographically secure information inaccessible to other agents."),
    ("higher_order_abstract_reasoning",
     "Reasons about mathematical concepts above their symbolic content: "
     "geometric intuition, function behavior without execution."),
]


def build_initial_ledger(user_config: UserConfig | None = None) -> CapabilityLedger:
    """
    Build the initial capability ledger.

    Parameters
    ----------
    user_config
        Parsed user-level config from user.toml. If None, creates a
        minimal user agent with no declared capabilities.
    """
    # --- User agent (from config or minimal default) ---
    if user_config is not None and user_config.capabilities:
        user_caps = {
            Capability(key=c.key, description=c.description)
            for c in user_config.capabilities
        }
        user = Agent(
            agent_id=user_config.name,
            substrate=user_config.substrate,
            individual_capabilities=user_caps,
        )
    else:
        # Minimal default: the agent will discover user capabilities
        # through observation during operation.
        user = Agent(
            agent_id=(user_config.name if user_config else "user"),
            substrate=(user_config.substrate if user_config else "biological"),
            individual_capabilities=set(),
        )

    # --- LLM capabilities (silicon substrate) ---
    llm = Agent(
        agent_id="llm",
        substrate="silicon",
        individual_capabilities={
            Capability(
                key="fast_iteration",
                description=(
                    "Produces ~100 drafts in the time a human produces 1, "
                    "allowing exhaustive exploration without fatigue."
                ),
            ),
            Capability(
                key="wide_context_window",
                description=(
                    "Holds an entire multi-page artifact plus references in "
                    "active attention, performing global consistency checks "
                    "no biological reader can do in one pass."
                ),
            ),
            Capability(
                key="tireless_verification",
                description=(
                    "Re-reads the same artifact N times checking different "
                    "invariants on each pass without satisficing or drift."
                ),
            ),
            Capability(
                key="cross_domain_recall",
                description=(
                    "Has indexed exposure to vast text across domains and "
                    "retrieves cross-domain patterns without prior immersion."
                ),
            ),
            Capability(
                key="symbolic_precision_at_speed",
                description=(
                    "Produces or transforms LaTeX, code, or formal structures "
                    "with low typo rate at high throughput."
                ),
            ),
        },
    )

    # --- Toolchain capabilities (silicon substrate) ---
    toolchain = Agent(
        agent_id="toolchain",
        substrate="silicon",
        individual_capabilities={
            Capability(
                key="pdf_compilation",
                description="LaTeX → PDF via pdflatex, reporting compile errors.",
            ),
            Capability(
                key="reference_resolution",
                description="Bibliography entries resolved against .bib files.",
            ),
            Capability(
                key="command_execution",
                description="Shell command execution with stdout/stderr capture.",
            ),
        },
    )

    ledger = CapabilityLedger(
        agents={user.agent_id: user, "llm": llm, "toolchain": toolchain},
    )

    # --- Cooperative capabilities (LLM-generated or empty) ---
    if user.individual_capabilities:
        coops = _generate_cooperatives(user, llm)
        for coop in coops:
            ledger.cooperative[coop.key] = coop

    return ledger


def _generate_cooperatives(
    user: Agent, llm: Agent
) -> list[CooperativeCapability]:
    """
    Ask an LLM to propose cooperative capabilities given both agents'
    individual capabilities.

    Falls back to an empty list on any failure (API unavailable, parse
    error, etc.) — the agent will discover cooperatives during operation.
    """
    user_caps = [
        {"key": c.key, "description": c.description}
        for c in sorted(user.individual_capabilities, key=lambda c: c.key)
    ]
    llm_caps = [
        {"key": c.key, "description": c.description}
        for c in sorted(llm.individual_capabilities, key=lambda c: c.key)
    ]

    prompt = f"""\
Given these two agents with different substrates, propose 3-6 cooperative
capabilities that require specific capabilities from BOTH participants
and could not be achieved by either alone.

Agent "{user.agent_id}" (substrate: {user.substrate}):
{json.dumps(user_caps, indent=2)}

Agent "llm" (substrate: {llm.substrate}):
{json.dumps(llm_caps, indent=2)}

Rules:
- Each cooperative capability must name specific individual capabilities
  it requires from each participant (by key).
- Cross-substrate cooperatives (participants on different substrates) are
  more valuable than same-substrate ones.
- Focus on capabilities that are genuinely substrate-exclusive: things
  one agent physically cannot do that the other can.
- Keep descriptions concise (1-2 sentences).

Respond with a JSON array of objects, each with:
  "key": "snake_case_name",
  "description": "What this cooperative capability enables",
  "requires_user": ["cap_key1", "cap_key2"],
  "requires_llm": ["cap_key1"],
  "rationale": "Why this requires both participants"

JSON only, no markdown fences or commentary."""

    try:
        import anthropic

        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        # Strip markdown fences if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text.rsplit("```", 1)[0]
        items = json.loads(text)
    except Exception as exc:
        print(f"[harness] cooperative generation failed ({exc}); "
              f"starting with no cooperatives", file=sys.stderr)
        return []

    user_cap_keys = {c.key for c in user.individual_capabilities}
    llm_cap_keys = {c.key for c in llm.individual_capabilities}

    coops: list[CooperativeCapability] = []
    for item in items:
        req_user = frozenset(item.get("requires_user", []))
        req_llm = frozenset(item.get("requires_llm", []))
        # Validate that required capabilities exist
        if not req_user.issubset(user_cap_keys):
            continue
        if not req_llm.issubset(llm_cap_keys):
            continue
        coops.append(CooperativeCapability(
            key=item["key"],
            description=item.get("description", ""),
            participants=frozenset({user.agent_id, "llm"}),
            requires={
                user.agent_id: req_user,
                "llm": req_llm,
            },
            cross_substrate=(user.substrate != llm.substrate),
            rationale=item.get("rationale", ""),
        ))

    return coops
