"""
Default initial ledger: user + LLM + toolchain collective.

This populates the harness with the collective derived from the
original design discussion. Individual capabilities are
substrate-exclusive by design (Paper 3 premise P1) — only things one
substrate uniquely enables are listed. Substitutable capabilities
("knows Python", "is intelligent") are deliberately omitted.

Cooperative capabilities derive mechanically from pairings of
substrate-exclusive individual capabilities: each cooperative entry
names which individual capabilities from which agents it requires,
and is cross-substrate by construction if its participants span
distinct substrates.

Registered as "default" in harness.initial_ledgers.REGISTRY. Reference
from instance config.toml via `initial_ledger = "default"`.
"""

from __future__ import annotations

from ..ledger import (
    Agent,
    Capability,
    CapabilityLedger,
    CooperativeCapability,
)


def build_initial_ledger() -> CapabilityLedger:
    # --- User capabilities (biological substrate) ------------------------
    user = Agent(
        agent_id="user",
        substrate="biological",
        individual_capabilities={
            Capability(
                key="long_tail_context",
                description=(
                    "The user holds multiple long-term objectives in mind and "
                    "works toward them over time horizons exceeding any "
                    "available context window."
                ),
            ),
            Capability(
                key="embodiment",
                description=(
                    "The user works across substrates and communicates with "
                    "other agents in embodied spaces."
                ),
            ),
            Capability(
                key="legal_status",
                description=(
                    "The user has legal personhood and can interact with "
                    "governmental, financial, and corporate structures "
                    "requiring it."
                ),
            ),
            Capability(
                key="cryptographic_secrets",
                description=(
                    "The user holds the knowledge of access to cryptographically "
                    "secure information otherwise inaccessible to other agents."
                ),
            ),
            Capability(
                key="higher_order_abstract_reasoning",
                description=(
                    "The user reasons about mathematical concepts at an "
                    "abstraction level above their symbolic content: "
                    "envisioning geometric shapes, intuitively assessing "
                    "function behavior without execution."
                ),
            ),
        },
    )

    # --- LLM capabilities (silicon substrate) ----------------------------
    llm = Agent(
        agent_id="llm",
        substrate="silicon",
        individual_capabilities={
            Capability(
                key="fast_iteration",
                description=(
                    "The LLM can produce ~100 drafts of a passage in the time "
                    "a human produces 1, allowing exhaustive exploration of "
                    "phrasings, structures, or alternatives without fatigue."
                ),
            ),
            Capability(
                key="wide_context_window",
                description=(
                    "The LLM can hold an entire multi-page artifact plus "
                    "its references in active attention simultaneously, "
                    "performing global consistency checks no biological "
                    "reader can do in one pass."
                ),
            ),
            Capability(
                key="tireless_verification",
                description=(
                    "The LLM can re-read the same artifact N times checking "
                    "different invariants on each pass without satisficing "
                    "or attention drift."
                ),
            ),
            Capability(
                key="cross_domain_recall",
                description=(
                    "The LLM has indexed exposure to vast amounts of text "
                    "across domains and retrieves cross-domain patterns "
                    "without prior topical immersion."
                ),
            ),
            Capability(
                key="symbolic_precision_at_speed",
                description=(
                    "The LLM produces or transforms LaTeX, code, or formal "
                    "structures with low typo rate at high throughput, "
                    "freed from the attentional cost biological writers pay "
                    "per token."
                ),
            ),
        },
    )

    # --- Toolchain capabilities (silicon substrate, shared with llm) -----
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
        agents={"user": user, "llm": llm, "toolchain": toolchain},
    )

    # --- Cooperative capabilities ----------------------------------------
    coops = [
        CooperativeCapability(
            key="sustained_research_collaboration",
            description=(
                "Multi-session research arcs where the user holds the "
                "long-term objective across context resets and the LLM "
                "holds within-session detail across the entire artifact."
            ),
            participants=frozenset({"user", "llm"}),
            requires={
                "user": frozenset({"long_tail_context"}),
                "llm": frozenset({"wide_context_window", "tireless_verification"}),
            },
            cross_substrate=True,
            rationale=(
                "User's multi-session memory and LLM's per-session global "
                "reading are each substrate-exclusive. Neither alone "
                "sustains the arc."
            ),
        ),
        CooperativeCapability(
            key="intuition_to_formalism_pipeline",
            description=(
                "User supplies pre-symbolic intuition about argument "
                "correctness; LLM converts validated intuitions into "
                "precise formal text without typos."
            ),
            participants=frozenset({"user", "llm"}),
            requires={
                "user": frozenset({"higher_order_abstract_reasoning"}),
                "llm": frozenset({"symbolic_precision_at_speed"}),
            },
            cross_substrate=True,
            rationale=(
                "Pre-symbolic intuition is biologically grounded; "
                "low-typo high-speed formal manipulation is silicon-grounded."
            ),
        ),
        CooperativeCapability(
            key="embodied_briefing",
            description=(
                "User attends meetings, signs documents, engages "
                "counterparties in person; LLM produces briefing materials "
                "in advance and rapid iterations after."
            ),
            participants=frozenset({"user", "llm"}),
            requires={
                "user": frozenset({"embodiment", "legal_status"}),
                "llm": frozenset({"cross_domain_recall", "fast_iteration"}),
            },
            cross_substrate=True,
            rationale=(
                "Embodied presence and legal personhood are substrate-exclusive "
                "bottlenecks the LLM cannot route around."
            ),
        ),
        CooperativeCapability(
            key="authenticated_automation",
            description=(
                "User holds credentials and legal authority for actions in "
                "financial, governmental, and corporate systems; LLM "
                "performs the work those credentials authorize at speed."
            ),
            participants=frozenset({"user", "llm"}),
            requires={
                "user": frozenset({"cryptographic_secrets", "legal_status"}),
                "llm": frozenset({"tireless_verification", "fast_iteration"}),
            },
            cross_substrate=True,
            rationale=(
                "Credential gates and legal authority are substrate-exclusive "
                "by construction."
            ),
        ),
        CooperativeCapability(
            key="argument_stress_testing",
            description=(
                "Adversarial review of an argument combining the LLM's "
                "global consistency check with the user's pre-symbolic "
                "taste for when conclusions outrun their math."
            ),
            participants=frozenset({"user", "llm"}),
            requires={
                "user": frozenset({"higher_order_abstract_reasoning", "long_tail_context"}),
                "llm": frozenset({"wide_context_window", "tireless_verification", "fast_iteration"}),
            },
            cross_substrate=True,
            rationale=(
                "Each substrate catches classes of errors the other misses."
            ),
        ),
        CooperativeCapability(
            key="compile_verification",
            description=(
                "LLM edits LaTeX source; toolchain compiles and reports "
                "errors; LLM corrects."
            ),
            participants=frozenset({"llm", "toolchain"}),
            requires={
                "llm": frozenset({"symbolic_precision_at_speed", "tireless_verification"}),
                "toolchain": frozenset({"pdf_compilation", "reference_resolution"}),
            },
            cross_substrate=False,  # both silicon
            rationale=(
                "Same-substrate cooperative: verifies LaTeX via compile loop."
            ),
        ),
    ]
    for coop in coops:
        ledger.cooperative[coop.key] = coop

    return ledger
