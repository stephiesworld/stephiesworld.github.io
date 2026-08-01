"""Run the graded set against one or more models and print a comparison.

This is the procedure you would walk a customer through when they ask "can we
use a cheaper model?" — hold the prompt fixed, vary only the model, and read
the numbers. It replaces an argument with a measurement.

    python -m doctor.cli --eval
    python -m doctor.cli --eval --models claude-opus-5,claude-sonnet-5,claude-haiku-4-5

Every run costs money. The table prints the exact amount.
"""

from __future__ import annotations

import time
from pathlib import Path

from .. import knowledge, llm
from .cases import CASES, Case
from .score import CaseResult, RunResult, score_case

FIXTURES = Path(__file__).resolve().parent.parent.parent / "tests" / "fixtures"

DEFAULT_MODELS = ("claude-opus-5", "claude-sonnet-5", "claude-haiku-4-5")


def _payload(case: Case) -> str:
    """One file, line-numbered, in the same shape `llm.build_payload` produces.

    Byte-identical framing matters: the eval must exercise the real prompt, not
    a convenient approximation of it.
    """
    source = (FIXTURES / case.file).read_text(encoding="utf-8")
    numbered = "\n".join(f"{i:>5} | {line}" for i, line in enumerate(source.splitlines(), start=1))
    return (
        "Review the following 1 file(s). Line numbers are prefixed; cite them "
        f"exactly as shown.\n\n<file path={case.file!r}>\n{numbered}\n</file>"
    )


def _cost(model: str, result: llm.LLMResult, today) -> float:
    info = knowledge.lookup(model)
    if info is None:
        return 0.0
    price_in, price_out = info.price(today)
    # Cache reads bill at ~10% of the input rate; uncached input at full rate.
    return (
        result.input_tokens * price_in
        + result.cache_read_tokens * price_in * 0.1
        + result.output_tokens * price_out
    ) / 1_000_000


def run_model(model: str, *, effort: str, today) -> RunResult:
    run = RunResult(model=model, effort=effort)
    started = time.monotonic()

    for case in CASES:
        result = llm.review(_payload(case), effort=effort, model=model)
        run.input_tokens += result.input_tokens
        run.output_tokens += result.output_tokens
        run.cache_read_tokens += result.cache_read_tokens
        run.cost_usd += _cost(model, result, today)

        if result.error and not result.findings:
            scored = CaseResult(case=case.name, error=result.error)
            scored.possible = sum(e.weight for e in case.expected)
            scored.missed = [e.key for e in case.expected]
        else:
            scored = score_case(case, result.findings)
            scored.error = result.error
        run.cases.append(scored)

    run.seconds = time.monotonic() - started
    return run


def render(runs: list[RunResult]) -> str:
    out: list[str] = []
    out.append("Judgement-pass eval\n")
    possible = sum(sum(e.weight for e in c.expected) for c in CASES)
    out.append(
        f"  {len(CASES)} case(s), {possible} weighted point(s) of expected findings.\n"
        "  Recall: share of real findings caught. Traps: share of output that "
        "repeated\n  a mechanical check the rubric said to skip — lower is better.\n"
    )

    header = f"  {'model':<22} {'effort':<7} {'recall':>7} {'traps':>7} {'found':>6} {'cost':>9} {'time':>7}"
    out.append(header)
    out.append("  " + "-" * (len(header) - 2))
    for run in runs:
        out.append(
            f"  {run.model:<22} {run.effort:<7} {run.recall:>6.0%} "
            f"{run.trap_rate:>6.0%} {run.total_findings:>6} "
            f"${run.cost_usd:>8.4f} {run.seconds:>6.0f}s"
        )

    baseline = runs[0] if runs else None
    for run in runs:
        out.append(f"\n  {run.model} @ {run.effort}")
        for case in run.cases:
            if case.error:
                out.append(f"    {case.case}: error — {case.error}")
                continue
            out.append(
                f"    {case.case}: {case.recall:.0%} "
                f"({len(case.found)}/{len(case.found) + len(case.missed)} expected)"
            )
            for key in case.missed:
                out.append(f"      missed   {key}")
            for title in case.traps:
                out.append(f"      trap     {title[:70]}")
            for note in case.unscored:
                out.append(f"      unscored {note[:70]}")

    if baseline and len(runs) > 1:
        out.append("\n  Against the baseline:")
        for run in runs[1:]:
            quality = (
                (run.recall / baseline.recall) if baseline.recall else 0.0
            )
            saving = (
                (1 - run.cost_usd / baseline.cost_usd) if baseline.cost_usd else 0.0
            )
            out.append(
                f"    {run.model:<22} {quality:>6.0%} of {baseline.model}'s recall, "
                f"{saving:>4.0%} cheaper"
            )
        out.append(
            "\n  A cheaper model is the right call only if its recall clears the bar "
            "you set\n  before running this. Pick that bar first, or the number "
            "just talks you into it."
        )

    out.append(
        "\n  Unscored findings matched no expectation and no trap. Read them: they "
        "are\n  either real findings this set does not know about — add them to "
        "cases.py —\n  or padding, which is a quality signal in itself."
    )
    return "\n".join(out) + "\n"
