"""Is any of this actually tested, and is anyone counting tokens correctly?

The single strongest predictor of a deployment that degrades quietly is the
absence of an eval. Everything else in this tool finds a specific defect; this
module asks whether the team would notice the next one on their own.
"""

from __future__ import annotations

import re
from collections.abc import Iterable

from ..model import Finding, Location, Severity
from . import Context, check

_TEST_MARKERS = ("test_", "_test.", ".test.", ".spec.", "/tests/", "\\tests\\", "/eval", "/evals")

# An eval asserts on model output. A test that mocks the client and asserts the
# request body is a unit test — useful, but it will not catch a quality
# regression from a model or prompt change.
_ASSERTION_MARKERS = (
    "content",
    "stop_reason",
    "usage",
    "parsed_output",
    "output_config",
)
_MOCK_MARKERS = ("mock", "patch", "stub", "vcr", "cassette", "responses.add", "nock")
# A file under tests/ that never asserts anything is a fixture, not a test.
_ASSERT_MARKERS = ("assert", "expect(", "should.", "chai.", "t.is(")

_TIKTOKEN = re.compile(r"\b(?:import\s+tiktoken|from\s+tiktoken|require\(['\"]gpt-tokenizer)")
_CHAR_ESTIMATE = re.compile(r"len\s*\([^)]{1,60}\)\s*(?://|/)\s*(?:3|3\.5|4)\b")


@check("EVAL_NONE", "evals", "No test asserts on model output")
def no_evals(ctx: Context) -> Iterable[Finding]:
    if not ctx.call_sites:
        return
    test_files = [p for p in ctx.files if any(m in str(p).replace("\\", "/") for m in _TEST_MARKERS)]
    scored: list[str] = []
    mocked_only: list[str] = []
    for path in test_files:
        source = ctx.read(ctx.rel(path))
        if source is None:
            continue
        if not any(m in source for m in _ASSERT_MARKERS):
            continue  # a fixture, not a test
        if not any(m in source for m in _ASSERTION_MARKERS):
            continue
        if any(m in source.lower() for m in _MOCK_MARKERS):
            mocked_only.append(ctx.rel(path))
        else:
            scored.append(ctx.rel(path))

    anchor = ctx.call_sites[0].location
    if scored:
        return
    if mocked_only:
        yield Finding(
            id="EVAL_NONE",
            title="Tests exist, but every one mocks the model",
            severity=Severity.HIGH,
            location=Location(mocked_only[0], 1),
            detail=(
                f"{len(mocked_only)} test file(s) touch the API surface, and all of them mock "
                "the client. Mocked tests verify that you built the request you meant to "
                "build — they cannot tell you the answer got worse. A prompt edit, a model "
                "bump, or an effort change will pass every one of them."
            ),
            remedy=(
                "Add a small graded set: 20–50 real inputs with expected properties (not "
                "expected strings), run against the live model, score with assertions or an "
                "LLM judge. That set is what makes every other finding in this report safe "
                "to act on — including the cheaper-model recommendation."
            ),
            confidence=0.75,
        )
        return
    yield Finding(
        id="EVAL_NONE",
        title=f"{len(ctx.call_sites)} API call site(s), no test asserting on output",
        severity=Severity.HIGH,
        location=anchor,
        detail=(
            "Nothing in this repository asserts on what the model returns. Every "
            "recommendation in this report — switch models, lower effort, shorten the "
            "prompt — is unverifiable without one, which means none of them can be taken "
            "safely."
        ),
        remedy=(
            "Build the eval set before acting on anything else here. 20–50 representative "
            "inputs, assertions on properties rather than exact strings, run in CI. It is "
            "the highest-leverage thing on this list and the only item that makes the "
            "others actionable."
        ),
    )


@check("TOKENIZER_WRONG", "evals", "OpenAI tokenizer used to estimate Claude tokens")
def wrong_tokenizer(ctx: Context) -> Iterable[Finding]:
    for path in ctx.files:
        rel = ctx.rel(path)
        source = ctx.read(rel)
        if source is None:
            continue
        match = _TIKTOKEN.search(source)
        if not match:
            continue
        line = source.count("\n", 0, match.start()) + 1
        yield Finding(
            id="TOKENIZER_WRONG",
            title="`tiktoken` used for Claude token counts",
            severity=Severity.HIGH,
            location=Location(rel, line),
            detail=(
                "`tiktoken` is OpenAI's tokenizer. It undercounts Claude tokens by roughly "
                "15–20% on prose and considerably more on code and non-English text. Any "
                "budget, cost estimate, or context-window guard built on it is wrong — and "
                "wrong in the direction that overflows."
            ),
            remedy=(
                "Use `client.messages.count_tokens(model=..., messages=...)`. Counts are "
                "model-specific, so pass the same model ID you use for inference — the "
                "current-generation tokenizer produces roughly 1×–1.35× the tokens of "
                "earlier models for the same text."
            ),
        )


@check("TOKENIZER_ESTIMATED", "evals", "Characters-divided-by-4 used as a token count")
def char_estimate(ctx: Context) -> Iterable[Finding]:
    for path in ctx.files:
        rel = ctx.rel(path)
        source = ctx.read(rel)
        if source is None:
            continue
        match = _CHAR_ESTIMATE.search(source)
        if not match:
            continue
        line = source.count("\n", 0, match.start()) + 1
        yield Finding(
            id="TOKENIZER_ESTIMATED",
            title="Character-count heuristic standing in for a token count",
            severity=Severity.LOW,
            location=Location(rel, line),
            detail=(
                "`len(text) // 4` is fine for a rough guard and dangerous as a budget. It "
                "drifts most on exactly the inputs that matter: code, JSON, and non-English "
                "text."
            ),
            remedy="Call `count_tokens` where the number drives a decision; keep the "
            "heuristic only where being wrong is free.",
            confidence=0.6,
        )
