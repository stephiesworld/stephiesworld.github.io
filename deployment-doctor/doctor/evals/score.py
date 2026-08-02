"""Scoring: match model output against the graded set.

Deliberately deterministic — no model grades another model here. Two reasons.
A model-as-judge costs money on every run, which discourages running it, and
an eval you avoid running is worse than no eval. And it introduces a second
source of variance, so a score drop no longer tells you whether the reviewer
regressed or the judge did.

Keyword matching is cruder than a judge and will occasionally miss a correct
finding phrased unusually. That failure mode is visible — it shows up in
`unscored`, where you can read it and fix the case — which is the trade we
want. A judge's failures are invisible.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .cases import Case, Expected, Group

LINE_SLACK = 8  # a reviewer citing a function may land anywhere inside it


def _haystack(finding) -> str:
    return f"{finding.title} {finding.detail} {finding.remedy}".lower()


def _groups_match(text: str, groups: tuple[Group, ...]) -> bool:
    """Every group needs at least one phrase present."""
    return all(any(phrase.lower() in text for phrase in group) for group in groups)


def _any_group_matches(text: str, groups: tuple[Group, ...]) -> bool:
    return any(any(phrase.lower() in text for phrase in group) for group in groups)


def _locates(finding, expected: Expected) -> bool:
    if not finding.location.path.endswith(expected.file):
        return False
    low, high = expected.lines
    return low - LINE_SLACK <= finding.location.line <= high + LINE_SLACK


@dataclass
class CaseResult:
    case: str
    found: list[str] = field(default_factory=list)
    missed: list[str] = field(default_factory=list)
    traps: list[str] = field(default_factory=list)  # titles of trap-hitting findings
    unscored: list[str] = field(default_factory=list)
    total_findings: int = 0
    earned: int = 0
    possible: int = 0
    error: str | None = None

    @property
    def recall(self) -> float:
        return self.earned / self.possible if self.possible else 0.0


def score_case(case: Case, findings: list) -> CaseResult:
    """Match one case's findings. Each expectation is claimed at most once."""
    result = CaseResult(case=case.name, total_findings=len(findings))
    result.possible = sum(e.weight for e in case.expected)

    unclaimed = list(case.expected)
    for finding in findings:
        text = _haystack(finding)

        hit = next(
            (e for e in unclaimed if _locates(finding, e) and _groups_match(text, e.must)),
            None,
        )
        if hit is not None:
            unclaimed.remove(hit)
            result.found.append(hit.key)
            result.earned += hit.weight
            continue

        # Not an expectation. Is it something the rubric told it to skip?
        if _any_group_matches(text, case.traps):
            result.traps.append(finding.title)
            continue

        result.unscored.append(f"{finding.location} — {finding.title}")

    result.missed = [e.key for e in unclaimed]
    return result


@dataclass
class RunResult:
    """One model+effort configuration across the whole graded set."""

    model: str
    effort: str
    cases: list[CaseResult] = field(default_factory=list)
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cost_usd: float = 0.0
    seconds: float = 0.0

    @property
    def recall(self) -> float:
        possible = sum(c.possible for c in self.cases)
        return sum(c.earned for c in self.cases) / possible if possible else 0.0

    @property
    def total_findings(self) -> int:
        return sum(c.total_findings for c in self.cases)

    @property
    def trap_rate(self) -> float:
        """Share of output that repeated a mechanical finding. Lower is better."""
        traps = sum(len(c.traps) for c in self.cases)
        return traps / self.total_findings if self.total_findings else 0.0

    @property
    def unscored(self) -> int:
        return sum(len(c.unscored) for c in self.cases)

    @property
    def errors(self) -> list[str]:
        return [c.error for c in self.cases if c.error]

    def to_dict(self) -> dict:
        return {
            "model": self.model,
            "effort": self.effort,
            "recall": round(self.recall, 4),
            "trap_rate": round(self.trap_rate, 4),
            "total_findings": self.total_findings,
            "unscored": self.unscored,
            "cost_usd": round(self.cost_usd, 6),
            "seconds": round(self.seconds, 1),
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cache_read_tokens": self.cache_read_tokens,
            "cases": [
                {
                    "case": c.case,
                    "recall": round(c.recall, 4),
                    "found": c.found,
                    "missed": c.missed,
                    "traps": c.traps,
                    "unscored": c.unscored,
                    "total_findings": c.total_findings,
                    "error": c.error,
                }
                for c in self.cases
            ],
        }
