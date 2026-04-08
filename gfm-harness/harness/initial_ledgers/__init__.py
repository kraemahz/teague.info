"""
Registry of initial-ledger builder functions.

An instance's config.toml references an initial ledger by name (e.g.,
`initial_ledger = "default"`). The Instance class looks up the builder
function via get_builder() and invokes it once at first-run to seed
the session's ledger. After the first run, the ledger is persisted
to session/ledger.json and the builder is never called again for that
instance — the ledger evolves through IMPLEMENT commits, not through
re-running the builder.

To add a new initial ledger:
  1. Create harness/initial_ledgers/<name>.py exporting a
     build_initial_ledger() -> CapabilityLedger function.
  2. Register it in REGISTRY below.
  3. Reference it from an instance's config.toml via
     initial_ledger = "<name>".

Keeping builders in the harness code (not per-instance) matches the
D4 decision: code stays with the harness, data lives in the instance
home dir. Multiple instances can share the same builder and still
have distinct persisted ledger state.
"""

from __future__ import annotations

from typing import Callable

from ..ledger import CapabilityLedger

from . import default


BuilderFn = Callable[[], CapabilityLedger]


REGISTRY: dict[str, BuilderFn] = {
    "default": default.build_initial_ledger,
}


def get_builder(name: str) -> BuilderFn:
    """Look up an initial-ledger builder by name."""
    if name not in REGISTRY:
        known = sorted(REGISTRY.keys())
        raise KeyError(
            f"unknown initial_ledger {name!r}; known builders: {known}"
        )
    return REGISTRY[name]


def list_builders() -> list[str]:
    """Return the sorted list of registered builder names."""
    return sorted(REGISTRY.keys())
