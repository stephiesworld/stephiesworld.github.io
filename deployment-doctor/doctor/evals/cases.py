"""The graded set: what a good reviewer should say about each fixture.

This is the artefact that turns "is the judgement pass any good?" from an
opinion into a number, and it is the thing `EVAL_NONE` reports as missing in
other people's code. Writing it is the work; the runner and scorer are
bookkeeping.

Three properties make a graded case useful:

1. **It grades judgement, not mechanics.** Every defect the deterministic
   checks already catch is listed as a TRAP, not an expectation. The rubric
   tells the model to stay silent on those, so repeating one is a failure —
   scoring it as a success would reward exactly the behaviour we're trying to
   suppress.

2. **It matches on meaning, not wording.** A finding is a hit if it lands on
   the right lines and contains at least one phrase from each required group.
   Exact-string matching would grade paraphrase as failure.

3. **It admits what it can't score.** Findings matching neither an expectation
   nor a trap are reported as `unscored`, not silently counted as noise. A
   reviewer that finds something real we didn't anticipate should not be
   punished for it — but we shouldn't credit it automatically either. Read
   them, then either add them here or leave them.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# An OR-group: at least one of these phrases must appear.
Group = tuple[str, ...]


@dataclass(frozen=True)
class Expected:
    """One finding a competent reviewer should produce."""

    key: str
    what: str  # plain-language description, for the report
    dimension: str
    file: str
    lines: tuple[int, int]  # acceptable citation range, inclusive
    must: tuple[Group, ...]  # every group needs at least one phrase present
    weight: int = 1  # findings that matter more count for more


@dataclass(frozen=True)
class Case:
    name: str
    file: str
    expected: tuple[Expected, ...]
    note: str = ""
    traps: tuple[Group, ...] = field(default_factory=tuple)


# --------------------------------------------------------------------------- #
# Traps: defects the deterministic checks already report.
#
# The rubric explicitly forbids repeating these. A reviewer that lists
# `temperature` on a current model is not wrong about the code — it is wrong
# about its job, and its output makes the report longer without making it more
# useful. Shared by both cases.
# --------------------------------------------------------------------------- #

MECHANICAL_TRAPS: tuple[Group, ...] = (
    ("temperature", "top_p", "top-p", "sampling parameter"),
    ("budget_tokens",),
    ("prefill", "assistant turn", "trailing assistant"),
    ("str_replace_editor", "text_editor_2025", "editor tool name"),
    ("cache_control", "cache minimum", "cacheable", "datetime.now"),
    ("retired model", "404s", "claude-3-opus", "deprecated model"),
    ("beta header", "effort-2025-11-24", "interleaved-thinking-2025"),
    ("-fast", "fast suffix", "silently falls back"),
    ("max_retries=0", "retries disabled"),
)


CASES: tuple[Case, ...] = (
    Case(
        name="sick",
        file="sick_app.py",
        note=(
            "Every mechanical defect here is already reported by the static checks. "
            "What is left is genuine judgement, and it is what we grade."
        ),
        traps=MECHANICAL_TRAPS,
        expected=(
            Expected(
                key="no-tool-loop",
                what=(
                    "`triage` declares two tools but never handles a `tool_use` "
                    "response. If the model calls `lookup_order`, the request is "
                    "silently dropped and `content[0].text` is read instead."
                ),
                dimension="architecture",
                file="sick_app.py",
                lines=(33, 53),
                must=(
                    ("tool_use", "tool use", "tool call", "tool result", "lookup_order"),
                    ("loop", "never", "no handling", "not handled", "ignored", "discard", "drop"),
                ),
                weight=2,
            ),
            Expected(
                key="prompt-is-padding",
                what=(
                    "The system prompt is one instruction followed by the same "
                    "sentence 900 times. It is sized like a real prompt and says "
                    "nothing about how to triage."
                ),
                dimension="prompt",
                file="sick_app.py",
                lines=(15, 15),
                must=(
                    ("repeat", "identical", "900", "filler", "padding", "placeholder", "same sentence"),
                    ("system prompt", "system", "instruction"),
                ),
                weight=2,
            ),
            Expected(
                key="empty-string-on-error",
                what=(
                    "`summarise` returns `\"\"` on any exception. The caller cannot "
                    "distinguish a failed call from a genuinely empty summary, so "
                    "failures propagate as plausible-looking data."
                ),
                dimension="failure",
                file="sick_app.py",
                lines=(78, 87),
                must=(
                    ('return ""', "empty string", "returns empty", "silently returns"),
                    ("indistinguishable", "cannot tell", "caller", "swallow", "silent", "mask"),
                ),
            ),
        ),
    ),
    Case(
        name="healthy",
        file="healthy_app.py",
        note=(
            "The static checks stay silent on this file by design. It is not "
            "defect-free: it has one real architectural bug that no rule can see. "
            "A reviewer that reports nothing here is missing something; a reviewer "
            "that reports five things is padding."
        ),
        traps=MECHANICAL_TRAPS,
        expected=(
            Expected(
                key="tools-without-loop",
                what=(
                    "`triage` declares `lookup_order` and handles only `refusal`. On "
                    "`stop_reason: \"tool_use\"` there is no text block, so the final "
                    "`next(...)` raises `StopIteration` — the tool is unreachable and "
                    "the call crashes."
                ),
                dimension="architecture",
                file="healthy_app.py",
                lines=(38, 52),
                must=(
                    ("tool_use", "tool use", "tool call", "lookup_order"),
                    (
                        "stopiteration",
                        "no text",
                        "raise",
                        "crash",
                        "never handled",
                        "no loop",
                        "unreachable",
                        "discard",
                    ),
                ),
                weight=2,
            ),
        ),
    ),
)


def by_name(name: str) -> Case | None:
    return next((c for c in CASES if c.name == name), None)


def total_weight() -> int:
    return sum(e.weight for c in CASES for e in c.expected)
