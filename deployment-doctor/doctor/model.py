"""Core data model: what the extractors produce and what the checks emit."""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any


class Severity(enum.IntEnum):
    """Ordering matters — findings are ranked by this."""

    CRITICAL = 4  # The API rejects this. Requests fail today (or on the next SDK bump).
    HIGH = 3  # Works, but silently wrong, silently expensive, or silently truncated.
    MEDIUM = 2  # Real cost or quality left on the table.
    LOW = 1  # Cleanup. Stale headers, dead parameters.
    INFO = 0  # Observation, no action implied.

    @property
    def label(self) -> str:
        return self.name.title()


@dataclass(frozen=True, order=True)
class Location:
    path: str  # repo-relative
    line: int
    col: int = 0

    def __str__(self) -> str:
        return f"{self.path}:{self.line}"


@dataclass
class Arg:
    """One argument at a call site.

    `value` is populated only when we could resolve it statically — a literal, or a
    module-level constant we traced. `node` keeps the language-native AST node so
    checks can inspect the expression itself (e.g. looking for `datetime.now()`
    inside a system prompt).
    """

    name: str
    raw: str
    location: Location
    value: Any = None
    resolved: bool = False
    node: Any = None

    def as_str(self) -> str | None:
        return self.value if isinstance(self.value, str) else None

    def as_int(self) -> int | None:
        return self.value if isinstance(self.value, int) and not isinstance(self.value, bool) else None


@dataclass
class CallSite:
    """A single call into the Messages API surface."""

    location: Location
    method: str  # "messages.create", "messages.stream", "beta.messages.create", ...
    args: dict[str, Arg] = field(default_factory=dict)
    language: str = "python"
    source: str = ""  # raw source slice, handed to the LLM pass

    @property
    def streaming(self) -> bool:
        if self.method.endswith(".stream"):
            return True
        stream = self.args.get("stream")
        return bool(stream and stream.value is True)

    @property
    def beta(self) -> bool:
        return self.method.startswith("beta.")

    def get(self, name: str) -> Arg | None:
        return self.args.get(name)

    def model_id(self) -> str | None:
        arg = self.args.get("model")
        return arg.as_str() if arg else None


@dataclass
class ModelRef:
    """A model-ID string found outside a call site — a constant, a config value, a
    registry entry. Worth flagging when retired, but never auto-fixed: it might be
    a definer rather than a caller (see README, "Buckets")."""

    location: Location
    model_id: str
    context: str


@dataclass
class Fix:
    """A mechanical, line-scoped edit. Only emitted when we're confident enough to
    apply it without a human reading the surrounding code."""

    path: str
    line: int
    old: str
    new: str
    description: str


@dataclass
class Finding:
    id: str  # stable slug, e.g. "MODEL_RETIRED"
    title: str
    severity: Severity
    location: Location
    detail: str
    remedy: str
    check: str = ""
    fix: Fix | None = None
    # Estimated $/million-input-tokens saved or over-spent. Signed: negative means
    # the current code is cheaper. Populated by cost-relevant checks only.
    cost_signal: str | None = None
    confidence: float = 1.0

    def sort_key(self) -> tuple:
        return (-int(self.severity), self.location.path, self.location.line, self.id)


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    call_sites: list[CallSite] = field(default_factory=list)
    model_refs: list[ModelRef] = field(default_factory=list)
    files_scanned: int = 0
    skipped: list[str] = field(default_factory=list)
    llm_ran: bool = False
    llm_error: str | None = None
    llm_note: str | None = None

    def add(self, finding: Finding) -> None:
        self.findings.append(finding)

    def sorted_findings(self) -> list[Finding]:
        return sorted(self.findings, key=lambda f: f.sort_key())

    def by_severity(self) -> dict[Severity, int]:
        counts = {s: 0 for s in Severity}
        for f in self.findings:
            counts[f.severity] += 1
        return counts
