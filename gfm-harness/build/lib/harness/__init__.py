"""
GFM Harness — a measurement infrastructure for LLM agents operating
under Goal-Frontier Maximization.

See README.md for the architectural overview and constitution.md for
the prose description of the phase model and decision categories.
"""

from .config import (
    DEFAULT_INITIAL_LEDGER,
    DEFAULT_MAX_ITERATIONS,
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODEL,
    InstanceConfig,
    load_config,
    save_config,
)
from .goals import Goal, GoalSet, default_goals, load_goals, save_goals
from .initial_ledgers import REGISTRY as INITIAL_LEDGER_REGISTRY
from .initial_ledgers import get_builder, list_builders
from .instance import (
    DEFAULT_HOME,
    HOME_ENV_VAR,
    Instance,
    get_instance_root,
    instance_path,
    list_instances,
)
from .ledger import Agent, Capability, CapabilityLedger, CooperativeCapability
from .ledger_persistence import (
    dict_to_ledger,
    ledger_to_dict,
    load_ledger,
    save_ledger,
)
from .memory import (
    IMPORTANCE_RUBRIC,
    ConsolidationProposal,
    ConsolidationResult,
    Episode,
    EvictionReport,
    Lesson,
    MemoryArchive,
    MemoryEntry,
    RecallResult,
    SideAction,
)
from .phases import (
    INITIAL_CATEGORIES,
    INITIAL_FLOORS,
    PauseOutcome,
    Phase,
    PlanExit,
    PlanState,
    SelfTrustModel,
    TrustUpdate,
    plan_exit_decision,
)
from .tools import (
    PauseForUser,
    apply_ledger_ops,
    dispatch_tool_call,
    tool_schemas,
)
from .trust import CommitLog, CommitRecord
from .vol_p import (
    VolPWeights,
    compute_vol_p,
    leverage_of_agent,
    leverage_of_capability,
    leverage_of_cooperative,
    leverage_report,
)
from .loop import FeatureLoopState, HarnessSession, load_session, save_trust

__all__ = [
    "DEFAULT_INITIAL_LEDGER",
    "DEFAULT_MAX_ITERATIONS",
    "DEFAULT_MAX_TOKENS",
    "DEFAULT_MODEL",
    "DEFAULT_HOME",
    "HOME_ENV_VAR",
    "INITIAL_LEDGER_REGISTRY",
    "Goal",
    "GoalSet",
    "Instance",
    "InstanceConfig",
    "default_goals",
    "dict_to_ledger",
    "get_builder",
    "get_instance_root",
    "instance_path",
    "ledger_to_dict",
    "list_builders",
    "list_instances",
    "load_config",
    "load_goals",
    "load_ledger",
    "save_config",
    "save_goals",
    "save_ledger",
    "Agent",
    "Capability",
    "CapabilityLedger",
    "CooperativeCapability",
    "IMPORTANCE_RUBRIC",
    "ConsolidationProposal",
    "ConsolidationResult",
    "Episode",
    "EvictionReport",
    "Lesson",
    "MemoryArchive",
    "MemoryEntry",
    "RecallResult",
    "SideAction",
    "INITIAL_CATEGORIES",
    "INITIAL_FLOORS",
    "PauseOutcome",
    "Phase",
    "PlanExit",
    "PlanState",
    "SelfTrustModel",
    "TrustUpdate",
    "plan_exit_decision",
    "CommitLog",
    "CommitRecord",
    "VolPWeights",
    "compute_vol_p",
    "leverage_of_agent",
    "leverage_of_capability",
    "leverage_of_cooperative",
    "leverage_report",
    "FeatureLoopState",
    "HarnessSession",
    "load_session",
    "save_trust",
    "PauseForUser",
    "apply_ledger_ops",
    "dispatch_tool_call",
    "tool_schemas",
]
