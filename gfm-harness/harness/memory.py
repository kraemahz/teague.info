"""
Three-layer memory architecture: working buffer, episodes, lessons.

The harness gives the LLM something it structurally lacks: episodic
memory with consolidation. Without this, an LLM agent has only its
context window — a working buffer that's wiped at every session
boundary, with no way to maintain narrative coherence across feature
loops. The three-layer architecture is the minimum scaffolding that
gives the agent something approximating long-running memory.

Layers:

  - working_buffer  (≈ working memory)  full-detail entries from the
                                         current feature loop, bounded
                                         in size, cleared by RETRO
                                         consolidation.

  - episodes        (≈ episodic memory) named, described event records
                                         produced by RETRO consolidation,
                                         survive indefinitely subject to
                                         importance-based eviction.

  - lessons         (≈ semantic memory) distilled rules with confidence
                                         scores and domain tags, refined
                                         over time, subject to supersession.

The agent does the cognitive work in the RETRO phase: it reads the
working buffer, proposes episodes that group related entries, proposes
lessons that distill generalizable patterns, scores importance, and
identifies entries safe to evict. The harness validates the proposals
and applies them.

See constitution.md §6 for the prose specification of consolidation
discipline. See IMPORTANCE_RUBRIC below for how the agent assigns
importance during consolidation.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


# ---------------------------------------------------------------------------
# IMPORTANCE_RUBRIC — read by the agent during RETRO consolidation
# ---------------------------------------------------------------------------

IMPORTANCE_RUBRIC = """
# Memory importance rubric for the GFM harness

Importance scores are floats in [0.0, 1.0]:
  0.0 = ephemeral, safe to evict at end of feature loop
  1.0 = critical, never evict, preserve indefinitely

Classify each working-buffer entry into one or more of the categories
below and assign importance accordingly. When multiple categories
apply, use the highest importance score among them. After scoring,
follow the consolidation behavior listed for the category — many
categories require promoting the entry to a Lesson, not just keeping
it as an Entry.

## 1. Critical incidents — importance 1.0, consolidate then evict Entry
Data loss, monetary expense, time loss without progress, work that
had to be redone, scripts that ran for an extended period and then
failed without meaningful output. These exist to be remembered so they
are not repeated. The permanent record lives in the Episode and Lesson
layers — NOT in the working-buffer Entry. Once the Entry has been
consolidated into an Episode (narrative) and a Lesson (avoidance
pattern), the Entry is redundant raw material and should be listed in
entries_to_evict so the working buffer stays available for current-loop
scratch space.

  Recognition cues: "lost", "wasted", "destroyed", "had to redo",
                    "ran out of", "failed after N hours", "reverted",
                    "the cost was".

  Consolidation: score Entry at importance 1.0 (signals "must consolidate
                 before eviction"); propose an Episode with importance 1.0
                 (never evict from episode layer) AND a Lesson with high
                 confidence capturing the avoidance pattern. Then list the
                 Entry in entries_to_evict — the Episode IS the historical
                 record.

## 2. Engineering principles — importance 0.9, promote to Lesson
Rules of thumb that improve future work on similar tasks. These are
lessons in disguise: they enter as observations during a specific
feature loop but want to live in the lesson layer with broad domain
tags so they apply to future work the agent has not yet seen.

  Recognition cues: "I noticed that X works better than Y",
                    "next time I should Z", "the pattern that
                    succeeded was W", "the right way to do this is".

  Consolidation: promote to Lesson with broad domain tags; the
                 Entry can be evicted from the working buffer once
                 the Lesson is in place.

## 3. Loss of function — importance 0.95, consolidate then evict Entry
Refactors or changes that removed behavior something else was
relying on. The harness's job is to expand capability; loss of
function is a capability regression and is tracked specifically so
the agent can detect and avoid it in future similar refactors.

  Recognition cues: "removed", "deleted", "no longer works",
                    "was relying on", "depended on which is now gone",
                    "broke when".

  Consolidation: score Entry at importance 0.95 (signals "must
                 consolidate before eviction"); propose an Episode with
                 importance 0.95 (never evict from episode layer). If a
                 pattern emerges across multiple loss-of-function entries,
                 promote a Lesson capturing the structural cause. Then
                 list the Entry in entries_to_evict — the Episode and
                 Lesson are the permanent record.

## 4. Organization — importance 0.8, externalize to repo
Knowledge about where things live and how the project is intended
to be organized that is *not visible* in the source code itself —
conventions, layout decisions, naming policies, where artifacts go.
These entries trigger a side action: propose writing the convention
into an associated documentation file in the repo. The memory entry
is the backup; the file is the primary representation.

  Recognition cues: "the convention here is", "this lives in",
                    "the way we organize", "by convention",
                    "should go in".

  Consolidation: keep as Entry with importance 0.8; propose a
                 file-write side action targeting the appropriate
                 documentation location (e.g., README.md, AGENTS.md,
                 CONVENTIONS.md). Side actions are applied during
                 the next IMPLEMENT phase, not by the harness.

## 5. UX expectations — importance 0.85, promote to Lesson (broad domain)
Standing user expectations about how scripts and tools should
behave: default-safe to run, sensible defaults, no required argument
lists for the common case, destructive actions explicitly marked.
These apply to all future tool work, not just the current task, so
they belong in the lesson layer with broad domain tags and high
confidence.

  Recognition cues: "the user expects", "default behavior should be",
                    "unless explicitly", "without having to remember",
                    "should just work".

  Consolidation: promote to Lesson with confidence 0.95 and
                 domain_tags including "ux", "tooling", "scripts".

## 6. DX expectations — importance 0.85, promote to Lesson
Standing user expectations about codebase quality: code should get
more organized over time, not less. Context-specific structural
rules. Promote to lesson layer.

  Recognition cues: "code should get more organized",
                    "the structure here should follow",
                    "this is messier than it was".

  Consolidation: promote to Lesson with confidence 0.9 and
                 domain_tags including "dx", "architecture",
                 "code-quality".

## 7. Environment — importance 0.9, factual recall
Knowledge about where the agent's tools live: paths, command names,
binary locations, API endpoints. These are factual lookups that fail
catastrophically when forgotten. Preserved with high importance and
indexed for fast recall.

  Recognition cues: "is at", "lives in", "use this command",
                    "the binary is", "the path to", "is on PATH /
                    is not on PATH".

  Consolidation: keep as Entry with importance 0.9; tag with
                 "environment" and "factual-recall" so retrieval
                 surfaces it on related queries. Optionally promote
                 to a Lesson if the environment knowledge is broadly
                 applicable.

## 8. Operations — importance 0.85, promote to Lesson with supersession
Higher-level reasoning about why things are done in particular ways,
informed by past failures and incidents. New operations rules can
supersede old ones when the agent learns better. Use the
`superseded_by` field on lessons to maintain the trail — never
silently delete a superseded operation rule.

  Recognition cues: "we do it this way because last time",
                    "the reason for", "after the incident with X",
                    "we now require", "the policy is".

  Consolidation: promote to Lesson with domain_tags including
                 "operations". If the new operations rule supersedes
                 a prior one, set superseded_by on the prior lesson
                 (do not delete it).

## 9. Self-knowledge — importance 0.95, promote to Lesson, evict Entry after
What the LLM has learned about its own behavioral characteristics
and gaps: things it tends to do wrong, failure modes specific to its
own reasoning style, calibration insights. Self-knowledge that does
not propagate forward is wasted — which is why it MUST be promoted
to the Lesson layer (importance 0.95, never evict) where it survives
indefinitely. The working-buffer Entry is evictable once the Lesson
exists.

  Recognition cues: "I tend to", "I missed this because",
                    "my default behavior is",
                    "I should remember that I", "the pattern in my
                    own reasoning was".

  Consolidation: score Entry at importance 0.95; promote to
                 Lesson with confidence 0.9, importance 0.95
                 (never evict from lesson layer), and domain_tags
                 including "self-knowledge", "metacognition". Then
                 list the Entry in entries_to_evict — the Lesson
                 IS the permanent self-knowledge record.

## Default — importance 0.3
Anything not matching the above. Routine working entries:
intermediate calculations, transient observations, things that were
useful only for the current deliberation. Lives in the working
buffer for the duration of the feature loop and is evicted at
consolidation.

## Scoring honesty
Do not inflate importance to preserve entries you find interesting
but that do not match a category. Do not deflate importance to
evict entries that would be inconvenient to confront later —
especially critical incidents and self-knowledge entries. Those
exist to be confronted, not hidden. The eviction policy is enforced
mechanically by the harness based on your scores; if you score
dishonestly, the consequences fall on the agent that has to operate
without the missing context, which is you.
"""


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


@dataclass
class MemoryEntry:
    """A single timestamped entry in the working buffer."""

    id: str
    timestamp: str
    phase: str  # plan / implement / verify / retro
    kind: str   # observation / reasoning / lesson_seed / note / action
    text: str
    importance: float = 0.3  # default per rubric
    consolidated_into: str | None = None  # episode_id once consolidated
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Episode:
    """A named, described event record grouping working-buffer entries."""

    id: str
    name: str               # short label, e.g. "paper3-r2-revision-round-3"
    description: str        # 1-2 sentence prose summary
    feature_id: str
    entry_ids: list[str]    # IDs of constituent MemoryEntry items
    importance: float
    tags: list[str] = field(default_factory=list)
    timestamp_range: tuple[str, str] = ("", "")
    distilled_lessons: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Lesson:
    """A distilled rule with confidence score and domain tags."""

    id: str
    statement: str          # one-sentence rule
    confidence: float       # 0.0–1.0
    source_episodes: list[str]
    domain_tags: list[str]  # when does this apply?
    importance: float
    superseded_by: str | None = None
    created_at: str = field(default_factory=_now)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SideAction:
    """
    A non-memory action proposed by consolidation. Currently used for
    the "externalize organization knowledge to a file" pattern from
    rubric category 4. Side actions are returned to the caller and
    applied during the next IMPLEMENT phase, not by the harness.
    """

    kind: str           # e.g. "write_file"
    target: str         # e.g. "AGENTS.md"
    content: str        # what to write
    rationale: str      # why


@dataclass
class ConsolidationProposal:
    """
    Input to MemoryArchive.consolidate(). The agent constructs this
    during RETRO and passes it to the harness for validation and
    application.
    """

    importance_updates: dict[str, float]            # entry_id -> new importance
    proposed_episodes: list[Episode]
    proposed_lessons: list[Lesson]
    supersessions: dict[str, str]                   # old_lesson_id -> new_lesson_id
    entries_to_evict: list[str]                     # entry_ids
    side_actions: list[SideAction] = field(default_factory=list)


@dataclass
class ConsolidationResult:
    """Returned from consolidate() so the caller can inspect what changed."""

    accepted_episodes: list[str]
    accepted_lessons: list[str]
    accepted_supersessions: list[tuple[str, str]]
    evicted_entries: list[str]
    side_actions: list[SideAction]
    validation_errors: list[str]


@dataclass
class EvictionReport:
    """Returned from evict() when bounded growth enforcement runs."""

    evicted_entries: list[str]
    evicted_episodes: list[str]
    evicted_lessons: list[str]
    reason: str


@dataclass
class RecallResult:
    """Returned from recall(); a mix of episodes and lessons by relevance."""

    episodes: list[Episode]
    lessons: list[Lesson]
    query: str


# ---------------------------------------------------------------------------
# MemoryArchive — the orchestration layer
# ---------------------------------------------------------------------------


@dataclass
class MemoryArchive:
    """
    Orchestrates the three memory layers and persists them to disk.

    Persistence model: each layer has its own JSONL file in the
    archive directory. Loaded eagerly via MemoryArchive.load(dir).
    Append-only at the entry level; consolidation can mark entries
    consolidated and add to higher layers, but never rewrites past
    entries — that would defeat the retrospective-review property.
    """

    archive_dir: Path
    working_buffer: list[MemoryEntry] = field(default_factory=list)
    episodes: dict[str, Episode] = field(default_factory=dict)
    lessons: dict[str, Lesson] = field(default_factory=dict)

    # Bounds — when exceeded, importance-based eviction runs.
    working_buffer_max_entries: int = 200
    episodes_max_count: int = 1000
    lessons_max_count: int = 200

    # ----- persistence ----------------------------------------------------

    @property
    def _entries_path(self) -> Path:
        return self.archive_dir / "working_buffer.jsonl"

    @property
    def _episodes_path(self) -> Path:
        return self.archive_dir / "episodes.jsonl"

    @property
    def _lessons_path(self) -> Path:
        return self.archive_dir / "lessons.jsonl"

    @classmethod
    def load(cls, archive_dir: Path) -> MemoryArchive:
        archive_dir.mkdir(parents=True, exist_ok=True)
        archive = cls(archive_dir=archive_dir)
        if archive._entries_path.exists():
            for line in archive._entries_path.read_text().splitlines():
                if line.strip():
                    archive.working_buffer.append(MemoryEntry(**json.loads(line)))
        if archive._episodes_path.exists():
            for line in archive._episodes_path.read_text().splitlines():
                if line.strip():
                    data = json.loads(line)
                    # tuple round-trip for timestamp_range
                    if isinstance(data.get("timestamp_range"), list):
                        data["timestamp_range"] = tuple(data["timestamp_range"])
                    archive.episodes[data["id"]] = Episode(**data)
        if archive._lessons_path.exists():
            for line in archive._lessons_path.read_text().splitlines():
                if line.strip():
                    data = json.loads(line)
                    archive.lessons[data["id"]] = Lesson(**data)
        return archive

    def _append_jsonl(self, path: Path, obj: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a") as f:
            f.write(json.dumps(obj) + "\n")

    def _rewrite_jsonl(self, path: Path, objs: Iterable[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as f:
            for obj in objs:
                f.write(json.dumps(obj) + "\n")

    # ----- working buffer (PLAN / IMPLEMENT / VERIFY) ---------------------

    def append(
        self,
        phase: str,
        kind: str,
        text: str,
        importance: float = 0.3,
        metadata: dict[str, Any] | None = None,
    ) -> MemoryEntry:
        entry = MemoryEntry(
            id=_new_id("e"),
            timestamp=_now(),
            phase=phase,
            kind=kind,
            text=text,
            importance=importance,
            metadata=metadata or {},
        )
        self.working_buffer.append(entry)
        self._append_jsonl(self._entries_path, asdict(entry))
        return entry

    # ----- consolidation (RETRO) ------------------------------------------

    def consolidate(
        self,
        proposal: ConsolidationProposal,
    ) -> ConsolidationResult:
        """
        Validate and apply a consolidation proposal from the agent.

        Validation rules:
          - Every entry_id in importance_updates and entries_to_evict
            must exist in working_buffer.
          - Every entry_id in a proposed_episode must exist.
          - Every source_episode_id in a proposed_lesson must exist
            (either pre-existing or also in proposed_episodes).
          - Every old_lesson_id in supersessions must exist; every
            new_lesson_id must exist (either pre-existing or in
            proposed_lessons).
          - All importance and confidence scores must be in [0.0, 1.0].
        """
        errors: list[str] = []
        existing_entry_ids = {e.id for e in self.working_buffer}
        all_episode_ids = set(self.episodes) | {ep.id for ep in proposal.proposed_episodes}
        all_lesson_ids = set(self.lessons) | {l.id for l in proposal.proposed_lessons}

        # importance updates
        for eid, score in proposal.importance_updates.items():
            if eid not in existing_entry_ids:
                errors.append(f"importance_update references unknown entry {eid!r}")
            if not 0.0 <= score <= 1.0:
                errors.append(f"importance_update {eid!r} score {score} not in [0,1]")

        # episodes
        for ep in proposal.proposed_episodes:
            for eid in ep.entry_ids:
                if eid not in existing_entry_ids:
                    errors.append(f"episode {ep.id!r} references unknown entry {eid!r}")
            if not 0.0 <= ep.importance <= 1.0:
                errors.append(f"episode {ep.id!r} importance {ep.importance} not in [0,1]")

        # lessons
        for lesson in proposal.proposed_lessons:
            for sid in lesson.source_episodes:
                if sid not in all_episode_ids:
                    errors.append(f"lesson {lesson.id!r} references unknown episode {sid!r}")
            if not 0.0 <= lesson.confidence <= 1.0:
                errors.append(f"lesson {lesson.id!r} confidence {lesson.confidence} not in [0,1]")
            if not 0.0 <= lesson.importance <= 1.0:
                errors.append(f"lesson {lesson.id!r} importance {lesson.importance} not in [0,1]")

        # supersessions
        for old_id, new_id in proposal.supersessions.items():
            if old_id not in all_lesson_ids:
                errors.append(f"supersession references unknown old lesson {old_id!r}")
            if new_id not in all_lesson_ids:
                errors.append(f"supersession references unknown new lesson {new_id!r}")
            if old_id == new_id:
                errors.append(f"lesson {old_id!r} cannot supersede itself")

        # evictions
        for eid in proposal.entries_to_evict:
            if eid not in existing_entry_ids:
                errors.append(f"eviction references unknown entry {eid!r}")

        if errors:
            return ConsolidationResult(
                accepted_episodes=[],
                accepted_lessons=[],
                accepted_supersessions=[],
                evicted_entries=[],
                side_actions=[],
                validation_errors=errors,
            )

        # Apply: importance updates first, then episodes, then lessons,
        # then supersessions, then evictions.
        for eid, score in proposal.importance_updates.items():
            for entry in self.working_buffer:
                if entry.id == eid:
                    entry.importance = score
                    break

        accepted_episodes = []
        for ep in proposal.proposed_episodes:
            self.episodes[ep.id] = ep
            for eid in ep.entry_ids:
                for entry in self.working_buffer:
                    if entry.id == eid:
                        entry.consolidated_into = ep.id
                        break
            accepted_episodes.append(ep.id)

        accepted_lessons = []
        for lesson in proposal.proposed_lessons:
            self.lessons[lesson.id] = lesson
            # Back-link to episodes
            for sid in lesson.source_episodes:
                if sid in self.episodes:
                    if lesson.id not in self.episodes[sid].distilled_lessons:
                        self.episodes[sid].distilled_lessons.append(lesson.id)
            accepted_lessons.append(lesson.id)

        accepted_supersessions = []
        for old_id, new_id in proposal.supersessions.items():
            self.lessons[old_id].superseded_by = new_id
            accepted_supersessions.append((old_id, new_id))

        # Eviction: only evict entries that have been consolidated, or
        # have low importance, or are explicitly listed.
        evicted_entry_ids = set(proposal.entries_to_evict)
        self.working_buffer = [
            e for e in self.working_buffer if e.id not in evicted_entry_ids
        ]

        # Persist: rewrite entries (eviction means we can't append-only),
        # append episodes and lessons.
        self._rewrite_jsonl(
            self._entries_path,
            (asdict(e) for e in self.working_buffer),
        )
        for ep in proposal.proposed_episodes:
            self._append_jsonl(self._episodes_path, asdict(ep))
        for lesson in proposal.proposed_lessons:
            self._append_jsonl(self._lessons_path, asdict(lesson))
        # Supersessions modify existing lessons in place; rewrite the file.
        if proposal.supersessions:
            self._rewrite_jsonl(
                self._lessons_path,
                (asdict(l) for l in self.lessons.values()),
            )

        return ConsolidationResult(
            accepted_episodes=accepted_episodes,
            accepted_lessons=accepted_lessons,
            accepted_supersessions=accepted_supersessions,
            evicted_entries=list(evicted_entry_ids),
            side_actions=list(proposal.side_actions),
            validation_errors=[],
        )

    # ----- recall (start of each feature loop) ----------------------------

    def recall(self, query: str, k: int = 5) -> RecallResult:
        """
        Text-based recall against episodes and lessons.

        Scoring is a simple linear combination:
          - substring match in name/description/statement: +1.0
          - tag overlap with query terms: +0.5 per match
          - importance weight: +importance
          - recency weight: small bonus for newer (episodes only)

        Designed to be replaced by vector recall later without
        changing the call signature.
        """
        query_lower = query.lower()
        query_terms = set(query_lower.split())

        ep_scores: list[tuple[float, Episode]] = []
        for ep in self.episodes.values():
            score = 0.0
            blob = f"{ep.name} {ep.description}".lower()
            if any(term in blob for term in query_terms):
                score += 1.0
            tag_overlap = len(set(t.lower() for t in ep.tags) & query_terms)
            score += 0.5 * tag_overlap
            score += ep.importance
            ep_scores.append((score, ep))
        ep_scores.sort(key=lambda kv: kv[0], reverse=True)
        top_episodes = [ep for score, ep in ep_scores[:k] if score > 0]

        lesson_scores: list[tuple[float, Lesson]] = []
        for lesson in self.lessons.values():
            if lesson.superseded_by:
                continue  # superseded lessons not surfaced unless explicitly asked
            score = 0.0
            if any(term in lesson.statement.lower() for term in query_terms):
                score += 1.0
            tag_overlap = len(set(t.lower() for t in lesson.domain_tags) & query_terms)
            score += 0.5 * tag_overlap
            score += lesson.importance * lesson.confidence
            lesson_scores.append((score, lesson))
        lesson_scores.sort(key=lambda kv: kv[0], reverse=True)
        top_lessons = [l for score, l in lesson_scores[:k] if score > 0]

        return RecallResult(
            episodes=top_episodes,
            lessons=top_lessons,
            query=query,
        )

    # ----- bounded growth enforcement -------------------------------------

    def evict(self) -> EvictionReport:
        """
        Importance-based eviction across the three layers when their
        bounds are exceeded. Working-buffer entries are fully evictable
        (sorted by importance, lowest evicted first). Episodes and
        lessons with importance >= 0.95 are protected from eviction —
        those are the permanent layers where "never evict" applies.
        """
        evicted_entries: list[str] = []
        evicted_episodes: list[str] = []
        evicted_lessons: list[str] = []
        reasons: list[str] = []

        # Working buffer — all entries are eviction-eligible.
        # The "never evict" protection applies to Episodes and Lessons
        # (the permanent layers), not to working-buffer Entries. Once an
        # Entry has been consolidated into an Episode + Lesson, it is
        # redundant raw material and should be evictable regardless of
        # its importance score.
        if len(self.working_buffer) > self.working_buffer_max_entries:
            sorted_entries = sorted(
                self.working_buffer, key=lambda e: e.importance, reverse=True
            )
            keep = sorted_entries[: self.working_buffer_max_entries]
            drop = sorted_entries[self.working_buffer_max_entries:]
            evicted_entries = [e.id for e in drop]
            self.working_buffer = [
                e for e in self.working_buffer if e.id not in set(evicted_entries)
            ]
            self._rewrite_jsonl(
                self._entries_path,
                (asdict(e) for e in self.working_buffer),
            )
            reasons.append(
                f"working_buffer exceeded {self.working_buffer_max_entries}; "
                f"evicted {len(evicted_entries)}"
            )

        # Episodes
        if len(self.episodes) > self.episodes_max_count:
            sorted_episodes = sorted(
                self.episodes.values(), key=lambda ep: ep.importance, reverse=True
            )
            keep_count = self.episodes_max_count
            drop = [ep for ep in sorted_episodes[keep_count:] if ep.importance < 0.95]
            evicted_episodes = [ep.id for ep in drop]
            for ep_id in evicted_episodes:
                del self.episodes[ep_id]
            self._rewrite_jsonl(
                self._episodes_path,
                (asdict(e) for e in self.episodes.values()),
            )
            reasons.append(
                f"episodes exceeded {self.episodes_max_count}; "
                f"evicted {len(evicted_episodes)}"
            )

        # Lessons: superseded first, then low confidence, then low importance
        if len(self.lessons) > self.lessons_max_count:
            superseded = [l for l in self.lessons.values() if l.superseded_by]
            non_superseded = [l for l in self.lessons.values() if not l.superseded_by]
            non_superseded.sort(
                key=lambda l: (l.importance, l.confidence), reverse=True
            )
            target = self.lessons_max_count
            ordered = non_superseded + superseded
            keep = ordered[:target]
            drop = [
                l for l in ordered[target:]
                if l.importance < 0.95  # protect critical
            ]
            evicted_lessons = [l.id for l in drop]
            for lid in evicted_lessons:
                del self.lessons[lid]
            self._rewrite_jsonl(
                self._lessons_path,
                (asdict(l) for l in self.lessons.values()),
            )
            reasons.append(
                f"lessons exceeded {self.lessons_max_count}; "
                f"evicted {len(evicted_lessons)}"
            )

        return EvictionReport(
            evicted_entries=evicted_entries,
            evicted_episodes=evicted_episodes,
            evicted_lessons=evicted_lessons,
            reason="; ".join(reasons) if reasons else "no eviction needed",
        )

    # ----- inspection helpers ---------------------------------------------

    def filter(
        self,
        phase: str | None = None,
        kind: str | None = None,
        feature_id: str | None = None,
    ) -> list[MemoryEntry]:
        result = []
        for entry in self.working_buffer:
            if phase is not None and entry.phase != phase:
                continue
            if kind is not None and entry.kind != kind:
                continue
            if feature_id is not None and entry.metadata.get("feature_id") != feature_id:
                continue
            result.append(entry)
        return result

    def tail(self, n: int = 20) -> list[MemoryEntry]:
        return self.working_buffer[-n:]

    def as_narrative(self, entries: list[MemoryEntry] | None = None) -> str:
        target = entries if entries is not None else self.working_buffer
        lines = []
        for e in target:
            header = f"[{e.timestamp} | {e.phase} | {e.kind} | imp={e.importance:.2f}]"
            lines.append(header)
            lines.append(e.text)
            lines.append("")
        return "\n".join(lines).rstrip()

    def render_episodes(self, episodes: list[Episode] | None = None) -> str:
        target = episodes if episodes is not None else list(self.episodes.values())
        lines = []
        for ep in target:
            lines.append(f"=== {ep.name} (importance={ep.importance:.2f})")
            lines.append(ep.description)
            if ep.tags:
                lines.append(f"tags: {', '.join(ep.tags)}")
            lines.append("")
        return "\n".join(lines).rstrip()

    def render_lessons(self, lessons: list[Lesson] | None = None) -> str:
        target = lessons if lessons is not None else [
            l for l in self.lessons.values() if not l.superseded_by
        ]
        lines = []
        for lesson in target:
            lines.append(
                f"• {lesson.statement}  [confidence={lesson.confidence:.2f}, "
                f"importance={lesson.importance:.2f}]"
            )
            if lesson.domain_tags:
                lines.append(f"  applies: {', '.join(lesson.domain_tags)}")
        return "\n".join(lines)
