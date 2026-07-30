"""Prompt-caching checks.

Caching is where the money is, and where the failures are silent: an
invalidator in the prefix costs full price forever and raises no error. The one
invariant everything below tests against — caching is a *prefix match*, so any
byte change anywhere in the prefix invalidates everything after it.
"""

from __future__ import annotations

from collections.abc import Iterable

from .. import knowledge
from ..extract.python import contains_fstring, walk_calls
from ..model import Finding, Severity
from . import Context, check
from ._common import (
    count_cache_breakpoints,
    estimate_tokens,
    has_cache_control,
    model_of,
    static_system_text,
)

# Below this we don't bother suggesting caching — the write premium wouldn't pay
# back before the entry expires.
_WORTH_CACHING = 2048


@check("CACHE_ABSENT", "cost", "Large reusable prefix with no cache_control")
def cache_absent(ctx: Context) -> Iterable[Finding]:
    for site in ctx.call_sites:
        if has_cache_control(site):
            continue
        text = static_system_text(site)
        if text is None:
            continue
        tokens = estimate_tokens(text)
        info = model_of(site)
        if tokens < _WORTH_CACHING:
            continue
        if info and tokens < info.cache_min_tokens:
            continue

        price_note = ""
        if info:
            in_usd, _ = info.price(ctx.today)
            per_1k = tokens * 1000 / 1_000_000 * in_usd
            saved = per_1k * 0.9
            price_note = (
                f" At {info.display} input pricing, re-sending this prefix across 1,000 "
                f"requests costs about ${per_1k:.2f}; cached, roughly ${per_1k - saved:.2f}."
            )
        yield Finding(
            id="CACHE_ABSENT",
            title=f"~{tokens:,}-token system prompt is re-sent uncached",
            severity=Severity.HIGH if tokens > 8000 else Severity.MEDIUM,
            location=(site.get("system").location if site.get("system") else site.location),
            detail=(
                f"The system prompt is statically known and roughly {tokens:,} tokens, but "
                "no `cache_control` appears on this request. Every call pays full input "
                f"price for the same bytes.{price_note}"
            ),
            remedy=(
                "Add `cache_control={'type': 'ephemeral'}` at the top level (auto-places on "
                "the last cacheable block), or mark the last system block explicitly for "
                "fine-grained control. Then verify with "
                "`response.usage.cache_read_input_tokens` — if it stays at 0 across "
                "identical-prefix requests, an invalidator is at work."
            ),
            cost_signal="~90% off the cached prefix from the second request on",
            confidence=0.8,
        )


@check("CACHE_BELOW_MINIMUM", "cost", "Prefix is below the model's minimum cacheable size")
def cache_below_minimum(ctx: Context) -> Iterable[Finding]:
    """The nastiest silent failure in the set: below the minimum, the marker is
    accepted, no error is raised, and nothing is ever cached. The minimum is also
    *not* monotonic across generations — 512 on Opus 5, 4096 on Opus 4.6."""
    for site in ctx.call_sites:
        if not has_cache_control(site):
            continue
        info = model_of(site)
        text = static_system_text(site)
        if info is None or text is None:
            continue
        tokens = estimate_tokens(text)
        if tokens >= info.cache_min_tokens * 0.8:  # margin for our rough estimate
            continue
        better = min(
            (m for m in knowledge.MODELS.values() if m.cache_min_tokens <= tokens),
            key=lambda m: m.cache_min_tokens,
            default=None,
        )
        hint = (
            f" (`{better.id}` caches from {better.cache_min_tokens} tokens)"
            if better and better.id != info.id
            else ""
        )
        yield Finding(
            id="CACHE_BELOW_MINIMUM",
            title=f"Cached prefix (~{tokens:,} tok) is under {info.display}'s {info.cache_min_tokens} minimum",
            severity=Severity.HIGH,
            location=(site.get("system").location if site.get("system") else site.location),
            detail=(
                f"`cache_control` is set, but the prefix looks like ~{tokens:,} tokens and "
                f"{info.display} does not cache below {info.cache_min_tokens}. The marker is "
                "accepted silently and nothing is cached — you pay the full price and "
                f"believe you aren't.{hint}"
            ),
            remedy=(
                "Confirm with `client.messages.count_tokens` (not a character estimate — "
                "this tool's is deliberately crude). Then either grow the shared prefix past "
                "the minimum, move to a model with a lower minimum, or drop the marker so "
                "the code stops implying a saving it isn't getting."
            ),
            confidence=0.6,
        )


@check("CACHE_INVALIDATOR", "cost", "Per-request value inside the cached prefix")
def cache_invalidator(ctx: Context) -> Iterable[Finding]:
    for site in ctx.call_sites:
        arg = site.get("system")
        if arg is None or arg.node is None:
            continue
        hits: list[str] = []
        for dotted in walk_calls(arg.node):
            tail = dotted.split(".", 1)[-1] if "." in dotted else dotted
            for pattern, why in knowledge.CACHE_INVALIDATORS.items():
                if dotted.endswith(pattern) or tail == pattern.split(".")[-1] and pattern in dotted:
                    hits.append(f"`{dotted}()` — {why}")
                    break
        if not hits and contains_fstring(arg.node) and has_cache_control(site):
            hits.append(
                "an f-string interpolates into the system prompt — if any substituted "
                "value varies per request or per user, the prefix never repeats"
            )
        if not hits:
            continue
        yield Finding(
            id="CACHE_INVALIDATOR",
            title="System prompt contains a per-request value",
            severity=Severity.HIGH if has_cache_control(site) else Severity.MEDIUM,
            location=arg.location,
            detail=(
                "Caching is a prefix match — one changed byte invalidates everything after "
                "it. Found: " + "; ".join(hits) + "."
            ),
            remedy=(
                "Freeze the system prompt and move the dynamic value later in `messages`, "
                "after the last breakpoint. On Opus 5 / Opus 4.8 / Fable 5 you can append a "
                "`{'role': 'system', ...}` message mid-conversation instead of editing the "
                "top-level system prompt — same operator authority, cached prefix intact."
            ),
            confidence=0.85 if has_cache_control(site) else 0.5,
        )


@check("CACHE_UNSORTED_JSON", "cost", "Non-deterministic serialization in the prefix")
def unsorted_json(ctx: Context) -> Iterable[Finding]:
    for site in ctx.call_sites:
        for name in ("system", "tools"):
            arg = site.get(name)
            if arg is None or arg.node is None:
                continue
            dotted = list(walk_calls(arg.node))
            if not any(d.endswith("json.dumps") or d.endswith("dumps") for d in dotted):
                continue
            if "sort_keys" in arg.raw:
                continue
            yield Finding(
                id="CACHE_UNSORTED_JSON",
                title=f"`json.dumps` without `sort_keys` in `{name}`",
                severity=Severity.MEDIUM,
                location=arg.location,
                detail=(
                    "Dict ordering is stable within a process but not across code paths, "
                    "versions, or hosts. Any reordering changes the prefix bytes and "
                    "silently drops the cache hit rate with no error."
                ),
                remedy="Pass `sort_keys=True`, and sort tool lists by name while you're there.",
                confidence=0.6,
            )


@check("CACHE_TOO_MANY_BREAKPOINTS", "correctness", "More than 4 cache_control markers is a 400")
def too_many_breakpoints(ctx: Context) -> Iterable[Finding]:
    for site in ctx.call_sites:
        count = count_cache_breakpoints(site)
        if count <= knowledge.MAX_CACHE_BREAKPOINTS:
            continue
        yield Finding(
            id="CACHE_TOO_MANY_BREAKPOINTS",
            title=f"{count} cache breakpoints (max {knowledge.MAX_CACHE_BREAKPOINTS})",
            severity=Severity.CRITICAL,
            location=site.location,
            detail=f"A request accepts at most {knowledge.MAX_CACHE_BREAKPOINTS} "
            "`cache_control` markers.",
            remedy=(
                "Keep markers at genuine stability boundaries: end of tools+system, end of "
                "the shared prefix, and the most recent conversation turn. Extra markers "
                "inside a stable span buy nothing."
            ),
        )
