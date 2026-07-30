"""Check registry.

A check is a function `(Context) -> Iterable[Finding]`. Registering is a
decorator; adding a check means adding a function, never editing a dispatch
table. Each check declares a `dimension` so the scorecard can group them.

Design rule: a check either proves a defect from the extracted facts, or it
stays quiet. Anything requiring judgement (is this prompt any good? is the tool
description precise enough?) belongs in the LLM pass, not here — deterministic
checks that guess produce confident nonsense, which is worse than silence.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from ..model import CallSite, Finding, ModelRef

DIMENSIONS = [
    "models",  # right model, live model
    "cost",  # caching, batching, tier
    "correctness",  # will this 400 or truncate
    "tools",  # tool definitions and versions
    "resilience",  # refusals, retries, errors
    "evals",  # is any of this tested
]


@dataclass
class Context:
    root: Path
    call_sites: list[CallSite] = field(default_factory=list)
    model_refs: list[ModelRef] = field(default_factory=list)
    files: list[Path] = field(default_factory=list)
    today: date = field(default_factory=date.today)

    _cache: dict[str, str | None] = field(default_factory=dict, repr=False)

    def rel(self, path: Path) -> str:
        try:
            return str(path.relative_to(self.root))
        except ValueError:
            return str(path)

    def read(self, rel_path: str) -> str | None:
        """Read a repo-relative file, cached. Returns None if unreadable — checks
        must treat that as 'no evidence', never as 'clean'."""
        if rel_path not in self._cache:
            try:
                self._cache[rel_path] = (self.root / rel_path).read_text(
                    encoding="utf-8", errors="replace"
                )
            except OSError:
                self._cache[rel_path] = None
        return self._cache[rel_path]


CheckFn = Callable[[Context], Iterable[Finding]]


@dataclass
class RegisteredCheck:
    id: str
    dimension: str
    summary: str
    fn: CheckFn


_REGISTRY: dict[str, RegisteredCheck] = {}


def check(id: str, dimension: str, summary: str):
    if dimension not in DIMENSIONS:
        raise ValueError(f"unknown dimension {dimension!r}")

    def wrap(fn: CheckFn) -> CheckFn:
        if id in _REGISTRY:
            raise ValueError(f"duplicate check id {id!r}")
        _REGISTRY[id] = RegisteredCheck(id=id, dimension=dimension, summary=summary, fn=fn)
        return fn

    return wrap


def all_checks() -> list[RegisteredCheck]:
    _load()
    return sorted(_REGISTRY.values(), key=lambda c: (DIMENSIONS.index(c.dimension), c.id))


def run(ctx: Context, only: set[str] | None = None) -> list[Finding]:
    findings: list[Finding] = []
    for registered in all_checks():
        if only and registered.id not in only and registered.dimension not in only:
            continue
        for finding in registered.fn(ctx):
            finding.check = registered.id
            findings.append(finding)
    return findings


_loaded = False


def _load() -> None:
    global _loaded
    if _loaded:
        return
    from . import caching, correctness, evals, models, resilience, tools  # noqa: F401

    _loaded = True
