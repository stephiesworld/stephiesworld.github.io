"""Does this integration survive contact with production?

Refusals, retries, error classes, and the stop reasons nobody handles until the
first incident.
"""

from __future__ import annotations

import re
from collections.abc import Iterable

from ..model import Finding, Location, Severity
from . import Context, check
from ._common import betas_of, model_of

# Models whose safety classifiers can decline a request outright: HTTP 200 with
# `stop_reason: "refusal"` and an empty (or partial) content array.
_REFUSAL_CAPABLE = {"claude-opus-5", "claude-fable-5", "claude-mythos-5", "claude-sonnet-5"}

_TYPED_EXCEPTIONS = (
    "RateLimitError",
    "APIStatusError",
    "APIConnectionError",
    "BadRequestError",
    "NotFoundError",
    "OverloadedError",
    "InternalServerError",
    "AnthropicError",
    "APIError",
)

_UNGUARDED_CONTENT = re.compile(r"\.content\s*\[\s*0\s*\]")


@check("REFUSAL_UNHANDLED", "resilience", "`stop_reason: refusal` is never checked")
def refusal_unhandled(ctx: Context) -> Iterable[Finding]:
    # Per file, not per repo: one module handling refusals correctly says nothing
    # about the module next to it that doesn't.
    by_path: dict[str, list] = {}
    for site in ctx.call_sites:
        info = model_of(site)
        if info is not None and info.id in _REFUSAL_CAPABLE:
            by_path.setdefault(site.location.path, []).append(site)

    for path, sites in sorted(by_path.items()):
        source = ctx.read(path)
        if source is None or "stop_reason" in source:
            continue
        site = sites[0]
        info = model_of(site)
        assert info is not None
        yield _refusal_finding(site, info, path)


def _refusal_finding(site, info, path: str) -> Finding:
    return Finding(
        id="REFUSAL_UNHANDLED",
        title=f"{info.display} can refuse, and `stop_reason` is never checked",
        severity=Severity.HIGH,
        location=site.location,
        detail=(
            f"{info.display} runs safety classifiers that can decline a request. A decline "
            "is a **successful HTTP 200** with `stop_reason: \"refusal\"` and an empty or "
            f"partial `content` array — not an exception. Nothing in `{path}` reads "
            "`stop_reason`, so any code doing "
            "`response.content[0].text` raises an IndexError on the first refusal, and any "
            "code reading a partial treats a truncated answer as complete. Benign "
            "security-adjacent and life-sciences work trips these classifiers occasionally, "
            "so this is not a hypothetical for those domains."
        ),
        remedy=(
            "Branch on `stop_reason` before touching `content`. Branch on `stop_reason`, "
            "not on `stop_details` — the latter is informational and can be `null` even on "
            "a refusal. Then opt into server-side fallbacks so a decline is re-served "
            "instead of surfacing: `betas=[\"server-side-fallback-2026-07-01\"]` with "
            '`fallbacks="default"`, which routes by refusal category so you never maintain '
            "a model list."
        ),
    )


@check("REFUSAL_FALLBACK_ABSENT", "resilience", "No fallback configured on a refusal-capable model")
def fallback_absent(ctx: Context) -> Iterable[Finding]:
    for site in ctx.call_sites:
        info = model_of(site)
        if info is None or info.id not in _REFUSAL_CAPABLE:
            continue
        if site.get("fallbacks") is not None:
            continue
        if any(b.startswith("server-side-fallback") for b in betas_of(site)):
            continue
        yield Finding(
            id="REFUSAL_FALLBACK_ABSENT",
            title=f"No `fallbacks` on a {info.display} call",
            severity=Severity.MEDIUM,
            location=site.location,
            detail=(
                "Fallbacks are opt-in. Without them, a policy decline simply stops the "
                "request and the caller gets nothing back."
            ),
            remedy=(
                'Add `fallbacks="default"` with `betas=["server-side-fallback-2026-07-01"]` '
                "on the beta messages endpoint. The `\"default\"` mode picks the recommended "
                "substitute by refusal category, so there is no model list to migrate later. "
                "Claude API only — on Bedrock/Vertex/Foundry, register the SDK's client-side "
                "refusal-fallback middleware instead."
            ),
            confidence=0.8,
        )


@check("UNGUARDED_CONTENT_INDEX", "resilience", "`response.content[0]` without a type or stop check")
def unguarded_content(ctx: Context) -> Iterable[Finding]:
    """`content` is a list of typed blocks. With thinking on — the default on
    current models — index 0 is a thinking block, not text."""
    seen: set[str] = set()
    for site in ctx.call_sites:
        path = site.location.path
        if path in seen:
            continue
        source = ctx.read(path)
        if source is None:
            continue
        match = _UNGUARDED_CONTENT.search(source)
        if not match:
            continue
        if "block.type" in source or 'type == "text"' in source or "type === 'text'" in source:
            continue
        seen.add(path)
        line = source.count("\n", 0, match.start()) + 1
        yield Finding(
            id="UNGUARDED_CONTENT_INDEX",
            title="`content[0]` indexed without checking the block type",
            severity=Severity.HIGH,
            location=Location(path, line),
            detail=(
                "`content` is a heterogeneous list of blocks. With adaptive thinking — on by "
                "default on current models — a `thinking` block precedes the text, so "
                "`content[0]` is not the answer. Server-tool results and `fallback` markers "
                "also land in `content`."
            ),
            remedy=(
                "Filter by type: `next(b.text for b in response.content if b.type == "
                '"text")`. In TypeScript, narrow the union before reading `.text` — the '
                "compiler will tell you if you forgot."
            ),
            confidence=0.7,
        )


@check("ERROR_HANDLING_UNTYPED", "resilience", "Broad `except` instead of the SDK's typed exceptions")
def untyped_errors(ctx: Context) -> Iterable[Finding]:
    for path in sorted({site.location.path for site in ctx.call_sites}):
        source = ctx.read(path)
        if source is None:
            continue
        broad = re.search(r"except\s+Exception\b|catch\s*\(\s*\w+\s*\)\s*\{", source)
        if not broad:
            continue
        if any(exc in source for exc in _TYPED_EXCEPTIONS):
            continue
        line = source.count("\n", 0, broad.start()) + 1
        yield Finding(
            id="ERROR_HANDLING_UNTYPED",
            title="API errors caught as one broad class",
            severity=Severity.MEDIUM,
            location=Location(path, line),
            detail=(
                "A single catch-all loses the distinction that matters: retryable (429, "
                "≥500, connection errors) versus non-retryable (400 bad request, 404 bad "
                "model ID). Retrying a 404 model ID forever is a common way to turn a "
                "one-line fix into an outage."
            ),
            remedy=(
                "Catch a chain, most-specific first: `NotFoundError` -> `RateLimitError` -> "
                "`APIStatusError` -> `APIConnectionError`. In Go, `errors.As` into "
                "`*anthropic.Error` and switch on `StatusCode`."
            ),
            confidence=0.65,
        )


@check("RETRIES_DISABLED", "resilience", "SDK retries turned off")
def retries_disabled(ctx: Context) -> Iterable[Finding]:
    for path in sorted({site.location.path for site in ctx.call_sites}):
        source = ctx.read(path)
        if source is None:
            continue
        match = re.search(r"max_?[Rr]etries\s*[=:]\s*0\b", source)
        if not match:
            continue
        line = source.count("\n", 0, match.start()) + 1
        yield Finding(
            id="RETRIES_DISABLED",
            title="`max_retries=0` disables automatic retry",
            severity=Severity.MEDIUM,
            location=Location(path, line),
            detail=(
                "The SDK retries 408/409/429/5xx and connection errors with exponential "
                "backoff by default (2 attempts). Setting 0 means a single 529 overload "
                "surfaces to the user."
            ),
            remedy="Leave the default, or raise it. If you disabled it to add your own "
            "backoff, make sure yours also honours the `retry-after` header on 429.",
            confidence=0.8,
        )
