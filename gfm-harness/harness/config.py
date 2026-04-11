"""
TOML config file reader and writer for instances.

Python 3.11+ has `tomllib` in the standard library for reading TOML, but
not for writing. Rather than take a dependency on `tomli-w`, this module
hand-writes a TOML serializer for the small, known schema used by
instance config files. The serializer is NOT general-purpose — it
handles only the value types and nesting we actually use:

  - Strings (with basic escaping for quotes and backslashes)
  - Integers, floats, booleans
  - ISO timestamp strings (serialized as quoted strings)
  - Flat [section] tables with scalar values
  - Top-level arrays of tables [[section]] for goals

If we ever need richer TOML output, swap this for `tomli-w`. For now
the hand-written version keeps the harness zero-dep beyond anthropic.

Instance config schema:

    # ~/.gfm-harness/instances/<name>/config.toml
    [instance]
    name = "primary"
    description = "Primary research partner instance"
    created_at = "2026-04-08T20:30:00Z"

    [run]
    model = "claude-opus-4-6"
    max_iterations = 40
    max_tokens = 16000
    initial_ledger = "default"
    default_task = ""

    [paths]
    # Optional: override the default session subdirectory
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# tomllib is stdlib in Python 3.11+; this module requires 3.11+.
if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover — harness targets 3.11+ for stdlib tomllib
    raise RuntimeError(
        "harness.config requires Python 3.11+ for stdlib tomllib. "
        f"Current version: {sys.version}"
    )


DEFAULT_MODEL = "claude-opus-4-6"
DEFAULT_MAX_ITERATIONS = 500  # generous ceiling; only hit on runaway loops
DEFAULT_MAX_TOKENS = 16000
DEFAULT_INITIAL_LEDGER = "default"


@dataclass
class InstanceConfig:
    """Parsed instance configuration."""

    name: str
    description: str = ""
    created_at: str = ""
    model: str = DEFAULT_MODEL
    max_iterations: int = DEFAULT_MAX_ITERATIONS
    max_tokens: int = DEFAULT_MAX_TOKENS
    initial_ledger: str = DEFAULT_INITIAL_LEDGER
    default_task: str = ""

    @classmethod
    def default(cls, name: str, description: str = "") -> InstanceConfig:
        return cls(
            name=name,
            description=description,
            created_at=datetime.now(timezone.utc).isoformat(),
        )


@dataclass
class UserCapabilityConfig:
    """A single user capability declaration from user.toml."""

    key: str
    description: str


@dataclass
class UserConfig:
    """Parsed user-level configuration from ~/.gfm-harness/user.toml."""

    name: str = "user"
    substrate: str = "biological"
    capabilities: list[UserCapabilityConfig] = field(default_factory=list)


def _get_harness_home() -> Path:
    """Return the harness home directory (respects GFM_HARNESS_HOME env)."""
    import os
    home = os.environ.get("GFM_HARNESS_HOME")
    if home:
        return Path(home).expanduser().resolve()
    return Path.home() / ".gfm-harness"


def load_user_config(path: Path | None = None) -> UserConfig | None:
    """
    Load user-level config from user.toml.

    Looks for the file at ``path`` if given, otherwise at
    ``~/.gfm-harness/user.toml`` (or ``$GFM_HARNESS_HOME/user.toml``).
    Returns None if the file does not exist.
    """
    if path is None:
        path = _get_harness_home() / "user.toml"
    if not path.exists():
        return None

    with path.open("rb") as f:
        data = tomllib.load(f)

    user_section = data.get("user", {})
    caps_raw = user_section.get("capabilities", [])
    capabilities = [
        UserCapabilityConfig(
            key=c.get("key", ""),
            description=c.get("description", ""),
        )
        for c in caps_raw
        if c.get("key")
    ]
    return UserConfig(
        name=user_section.get("name", "user"),
        substrate=user_section.get("substrate", "biological"),
        capabilities=capabilities,
    )


def save_user_config(config: UserConfig, path: Path | None = None) -> None:
    """Write a user config to user.toml."""
    if path is None:
        path = _get_harness_home() / "user.toml"
    lines = [
        "# GFM Harness user-level config",
        "# Shared across all instances. Edit to change your capabilities.",
        "",
        "[user]",
        f"name = {_escape_string(config.name)}",
        f"substrate = {_escape_string(config.substrate)}",
        "",
    ]
    for cap in config.capabilities:
        lines.extend([
            "[[user.capabilities]]",
            f"key = {_escape_string(cap.key)}",
            f"description = {_escape_string(cap.description)}",
            "",
        ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def load_config(path: Path) -> InstanceConfig:
    """Load an instance config from a TOML file."""
    with path.open("rb") as f:
        data = tomllib.load(f)

    instance = data.get("instance", {})
    run = data.get("run", {})

    return InstanceConfig(
        name=instance.get("name", path.parent.name),
        description=instance.get("description", ""),
        created_at=instance.get("created_at", ""),
        model=run.get("model", DEFAULT_MODEL),
        max_iterations=int(run.get("max_iterations", DEFAULT_MAX_ITERATIONS)),
        max_tokens=int(run.get("max_tokens", DEFAULT_MAX_TOKENS)),
        initial_ledger=run.get("initial_ledger", DEFAULT_INITIAL_LEDGER),
        default_task=run.get("default_task", ""),
    )


def save_config(config: InstanceConfig, path: Path) -> None:
    """Write an instance config to a TOML file."""
    lines = [
        "# GFM Harness instance config",
        "# Both humans and agents can edit this file. Changes take effect",
        "# at the next `harness run` invocation for this instance.",
        "",
        "[instance]",
        f'name = {_escape_string(config.name)}',
        f'description = {_escape_string(config.description)}',
        f'created_at = {_escape_string(config.created_at)}',
        "",
        "[run]",
        f'model = {_escape_string(config.model)}',
        f"max_iterations = {config.max_iterations}",
        f"max_tokens = {config.max_tokens}",
        f'initial_ledger = {_escape_string(config.initial_ledger)}',
        f'default_task = {_escape_string(config.default_task)}',
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def _escape_string(value: str) -> str:
    """
    Escape a Python string for TOML output.

    TOML basic strings allow most characters but require escaping of:
      - backslash
      - double quote
      - control characters (newlines, tabs) — we convert to escape codes
    """
    if value is None:
        return '""'
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )
    return f'"{escaped}"'
