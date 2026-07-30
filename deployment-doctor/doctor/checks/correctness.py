"""Will this request 400, truncate, or silently do the wrong thing?

Everything here is provable from the request shape plus the model's documented
surface. No judgement calls.
"""

from __future__ import annotations

from collections.abc import Iterable

from .. import knowledge
from ..model import Finding, Severity
from . import Context, check
from ._common import (
    betas_of,
    effort_of,
    messages_of,
    model_of,
    thinking_of,
)


@check("PARAM_SAMPLING_REJECTED", "correctness", "temperature/top_p/top_k return 400 on current models")
def sampling_params(ctx: Context) -> Iterable[Finding]:
    for site in ctx.call_sites:
        info = model_of(site)
        present = [p for p in knowledge.SAMPLING_PARAMS if site.get(p) is not None]
        if not present:
            continue
        if info is not None and info.rejects_sampling_params:
            names = ", ".join(f"`{p}`" for p in present)
            arg = site.get(present[0])
            yield Finding(
                id="PARAM_SAMPLING_REJECTED",
                title=f"{names} rejected by {info.display}",
                severity=Severity.CRITICAL,
                location=arg.location if arg else site.location,
                detail=(
                    f"{info.display} removed the sampling parameters. Sending {names} "
                    "returns a 400 — this request fails every time."
                ),
                remedy=(
                    "Delete the parameter. If it was there for determinism, use "
                    "`output_config={'effort': 'low'}` and a tighter prompt (note "
                    "`temperature=0` never guaranteed identical outputs anyway). If it was "
                    "there for creative variance, steer with the prompt instead — for "
                    "design work, have the model propose N directions and pick one."
                ),
            )
        elif len(present) > 1 and {"temperature", "top_p"} <= set(present):
            arg = site.get("temperature")
            yield Finding(
                id="PARAM_SAMPLING_REJECTED",
                title="`temperature` and `top_p` set together",
                severity=Severity.CRITICAL,
                location=arg.location if arg else site.location,
                detail="Passing both errors on every Claude 4+ model.",
                remedy="Keep one. Delete the other.",
            )


@check("PARAM_BUDGET_TOKENS", "correctness", "thinking.budget_tokens is removed on current models")
def budget_tokens(ctx: Context) -> Iterable[Finding]:
    for site in ctx.call_sites:
        thinking = thinking_of(site)
        if not thinking or "budget_tokens" not in thinking:
            continue
        info = model_of(site)
        arg = site.get("thinking")
        loc = arg.location if arg else site.location
        if info is not None and info.rejects_budget_tokens:
            yield Finding(
                id="PARAM_BUDGET_TOKENS",
                title=f"`budget_tokens` rejected by {info.display}",
                severity=Severity.CRITICAL,
                location=loc,
                detail=(
                    "Manual extended thinking is removed. "
                    f"`thinking={{'type': 'enabled', 'budget_tokens': ...}}` returns a 400 on "
                    f"{info.display}."
                ),
                remedy=(
                    "Use `thinking={'type': 'adaptive'}` and control depth with "
                    "`output_config={'effort': ...}`. There is no 1:1 token mapping — "
                    "start at `high` (`xhigh` for coding/agentic) and sweep down."
                ),
                # Deliberately not auto-fixed: picking the replacement effort level is a
                # cost/quality decision, not a mechanical substitution.
            )
        else:
            yield Finding(
                id="PARAM_BUDGET_TOKENS",
                title="`budget_tokens` is deprecated",
                severity=Severity.MEDIUM,
                location=loc,
                detail="Fixed thinking budgets are deprecated and removed on newer models.",
                remedy="Move to `thinking={'type': 'adaptive'}` + `output_config.effort` now, "
                "so the next model bump is a one-line change.",
            )


@check("PARAM_PREFILL", "correctness", "Trailing assistant turn returns 400 on current models")
def prefill(ctx: Context) -> Iterable[Finding]:
    for site in ctx.call_sites:
        messages = messages_of(site)
        if not messages:
            continue
        last = messages[-1]
        if not (isinstance(last, dict) and last.get("role") == "assistant"):
            continue
        info = model_of(site)
        if info is None or not info.rejects_prefill:
            continue
        arg = site.get("messages")
        yield Finding(
            id="PARAM_PREFILL",
            title=f"Assistant prefill rejected by {info.display}",
            severity=Severity.CRITICAL,
            location=arg.location if arg else site.location,
            detail=(
                "The conversation ends on an assistant turn. Prefilling the final "
                f"assistant message returns a 400 on {info.display}."
            ),
            remedy=(
                "Pick the replacement that matches what the prefill was doing: forcing a "
                "JSON shape -> `output_config.format` with a schema; forcing a label -> a "
                "tool with an enum; skipping a preamble -> a system-prompt instruction "
                "(\"Respond directly, no preamble\"); continuing an interrupted response -> "
                "move the continuation into the user turn."
            ),
        )


@check("PARAM_OUTPUT_FORMAT", "correctness", "`output_format` is superseded by `output_config.format`")
def output_format(ctx: Context) -> Iterable[Finding]:
    for site in ctx.call_sites:
        if site.get("output_format") is None:
            continue
        # `.parse()` accepts `output_format` as an SDK convenience — not a defect.
        if site.method.endswith(".parse"):
            continue
        arg = site.get("output_format")
        yield Finding(
            id="PARAM_OUTPUT_FORMAT",
            title="Deprecated `output_format` parameter",
            severity=Severity.MEDIUM,
            location=arg.location if arg else site.location,
            detail="The top-level `output_format` parameter is deprecated API-wide.",
            remedy="Move the schema under `output_config={'format': {...}}`.",
        )


@check("THINKING_DISABLED_EFFORT", "correctness", "Disabled thinking above `high` effort is a 400")
def thinking_disabled_effort(ctx: Context) -> Iterable[Finding]:
    order = ["low", "medium", "high", "xhigh", "max"]
    for site in ctx.call_sites:
        thinking = thinking_of(site)
        info = model_of(site)
        if info is None or not thinking or thinking.get("type") != "disabled":
            continue
        arg = site.get("thinking")
        loc = arg.location if arg else site.location

        if info.rejects_thinking_disabled:
            yield Finding(
                id="THINKING_DISABLED_EFFORT",
                title=f"`thinking: disabled` rejected by {info.display}",
                severity=Severity.CRITICAL,
                location=loc,
                detail=f"Thinking is always on for {info.display}; an explicit "
                "`{'type': 'disabled'}` returns a 400 at any effort.",
                remedy="Omit the `thinking` parameter entirely.",
            )
            continue

        cap = info.thinking_disable_max_effort
        effort = effort_of(site)
        if cap and effort and effort in order and order.index(effort) > order.index(cap):
            yield Finding(
                id="THINKING_DISABLED_EFFORT",
                title=f"`thinking: disabled` + `effort: {effort}` is a 400",
                severity=Severity.CRITICAL,
                location=loc,
                detail=(
                    f"{info.display} allows disabled thinking only at effort `{cap}` or "
                    f"lower. Paired with `{effort}`, the request is rejected. This is "
                    "validated per request, so a route that raises effort later fails even "
                    "if earlier calls in the same conversation succeeded."
                ),
                remedy=(
                    f"Enable thinking, or drop effort to `{cap}` or below. Given how strong "
                    f"{info.display} is at `low`/`medium`, a latency-sensitive route is "
                    "usually better served by `medium` with thinking on than by disabling it."
                ),
            )


@check("THINKING_DEFAULT_ON", "correctness", "Thinking now defaults on — max_tokens may truncate")
def thinking_default_on(ctx: Context) -> Iterable[Finding]:
    """The silent one. On Opus 5 and Sonnet 5, omitting `thinking` runs adaptive,
    where the previous generation ran thinking-off. `max_tokens` caps thinking +
    response together, so a budget sized around the answer now truncates it."""
    for site in ctx.call_sites:
        info = model_of(site)
        if info is None or not info.thinking_on_by_default:
            continue
        if thinking_of(site) is not None or site.get("thinking") is not None:
            continue
        max_tokens = site.get("max_tokens")
        n = max_tokens.as_int() if max_tokens else None
        if n is None or n > 8192:
            continue
        yield Finding(
            id="THINKING_DEFAULT_ON",
            title=f"No `thinking` set on {info.display} with `max_tokens={n}`",
            severity=Severity.HIGH,
            location=(max_tokens.location if max_tokens else site.location),
            detail=(
                f"On {info.display}, omitting `thinking` runs **adaptive thinking** — the "
                "previous generation ran without it. `max_tokens` is a hard cap on thinking "
                f"plus response text, so {n} tokens sized around the answer alone can now "
                "truncate mid-response. There is no error; the reply is just cut off."
            ),
            remedy=(
                f"Raise `max_tokens` to leave thinking headroom, or set "
                f"`thinking={{'type': 'disabled'}}` explicitly at effort "
                f"`{info.thinking_disable_max_effort or 'high'}` or below to keep the old "
                "behaviour. Check `stop_reason == 'max_tokens'` in production either way."
            ),
            confidence=0.75,
        )


@check("STREAMING_REQUIRED", "correctness", "Large max_tokens without streaming will time out")
def streaming_required(ctx: Context) -> Iterable[Finding]:
    for site in ctx.call_sites:
        if site.streaming:
            continue
        max_tokens = site.get("max_tokens")
        n = max_tokens.as_int() if max_tokens else None
        if n is None or n <= knowledge.NONSTREAMING_MAXTOKENS_WARN:
            continue
        fails = n >= knowledge.NONSTREAMING_MAXTOKENS_FAIL
        yield Finding(
            id="STREAMING_REQUIRED",
            title=f"`max_tokens={n}` on a non-streaming request",
            severity=Severity.CRITICAL if fails else Severity.HIGH,
            location=max_tokens.location if max_tokens else site.location,
            detail=(
                f"Non-streaming requests above ~{knowledge.NONSTREAMING_MAXTOKENS_WARN} "
                "risk an SDK HTTP timeout on a long generation. "
                + (
                    "At this size the Python SDK refuses the request outright with a "
                    "`ValueError` rather than letting the connection drop."
                    if fails
                    else "Idle connections drop before the response lands."
                )
            ),
            remedy=(
                "Switch to `client.messages.stream(...)` and call `.get_final_message()` "
                "if you don't need per-event handling — you keep the same return value and "
                "gain timeout protection."
            ),
        )


@check("BETA_HEADER_STALE", "correctness", "Beta header went GA — it pins you to client.beta.* for nothing")
def stale_betas(ctx: Context) -> Iterable[Finding]:
    for site in ctx.call_sites:
        stale = [b for b in betas_of(site) if b in knowledge.GA_BETA_HEADERS]
        if not stale:
            continue
        arg = site.get("betas") or site.get("extra_headers")
        reasons = "; ".join(f"`{b}` — {knowledge.GA_BETA_HEADERS[b]}" for b in stale)
        yield Finding(
            id="BETA_HEADER_STALE",
            title=f"{len(stale)} GA beta header{'s' if len(stale) > 1 else ''} still set",
            severity=Severity.LOW,
            location=arg.location if arg else site.location,
            detail=reasons,
            remedy=(
                "Remove them. Once the last beta is gone, move the call from "
                "`client.beta.messages.create(...)` back to `client.messages.create(...)` "
                "and off the beta type surface."
            ),
        )
