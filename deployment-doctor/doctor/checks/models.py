"""Model-selection checks: is the model live, is it the right tier, is it pinned."""

from __future__ import annotations

from collections.abc import Iterable

from .. import knowledge
from ..knowledge import Status
from ..model import Finding, Fix, Location, Severity
from . import Context, check

# Distinct model IDs in one file above which we call it a catalog, not a caller.
_REGISTRY_THRESHOLD = 6


@check("MODEL_RETIRED", "models", "Model ID has been retired and returns 404")
def retired_models(ctx: Context) -> Iterable[Finding]:
    for model_id, location, in_call in _all_model_uses(ctx):
        bare, provider = knowledge.strip_provider_prefix(model_id)
        replacement = knowledge.RETIRED.get(bare)
        info = knowledge.lookup(bare)
        if replacement is None and info is not None and info.status_on(ctx.today) is Status.RETIRED:
            replacement = info.successor
        if replacement is None:
            continue
        target = f"anthropic.{replacement}" if provider == "bedrock" else replacement
        live = not in_call and (location.path, model_id) in _referenced(ctx)
        # Only offer a fix where the literal actually is. When `model=MODEL`
        # points at a constant, the call site has nothing to rewrite — the edit
        # belongs at the constant, which is the separate reference finding.
        inline = model_id in _model_raw(ctx, location) if in_call else True
        yield Finding(
            id="MODEL_RETIRED",
            title=f"Retired model `{model_id}`",
            severity=Severity.CRITICAL if in_call else (Severity.HIGH if live else Severity.MEDIUM),
            location=location,
            detail=(
                f"`{model_id}` is retired — the API returns 404. "
                + (
                    "This is a live call site."
                    if in_call
                    else (
                        "This constant is referenced by a call site in the same file, so it "
                        "is live code — this is the line to edit."
                        if live
                        else "This is a bare reference, not a call site. It may be config, a "
                        "registry entry that legitimately keeps the old ID, or a fixture — "
                        "check which before changing it."
                    )
                )
            ),
            remedy=f"Replace with `{target}`.",
            fix=Fix(location.path, location.line, model_id, target, f"{model_id} -> {target}")
            if inline
            else None,
            confidence=1.0 if in_call else 0.75 if live else 0.5,
        )


def _model_raw(ctx: Context, location) -> str:
    for site in ctx.call_sites:
        arg = site.get("model")
        if arg is not None and arg.location == location:
            return arg.raw
    return ""


def _referenced(ctx: Context) -> set[tuple[str, str]]:
    return {
        (site.location.path, mid)
        for site in ctx.call_sites
        if (mid := site.model_id()) is not None
    }


@check("MODEL_DEPRECATED", "models", "Model has an announced retirement date")
def deprecated_models(ctx: Context) -> Iterable[Finding]:
    for model_id, location, in_call in _all_model_uses(ctx):
        bare, _ = knowledge.strip_provider_prefix(model_id)
        info = knowledge.lookup(bare)
        if info is None or info.status_on(ctx.today) is not Status.DEPRECATED:
            continue
        days = (info.retires - ctx.today).days if info.retires else None
        window = f" in {days} days ({info.retires})" if days is not None else ""
        yield Finding(
            id="MODEL_DEPRECATED",
            title=f"Deprecated model `{model_id}`",
            severity=Severity.HIGH if (days is not None and days < 60) else Severity.MEDIUM,
            location=location,
            detail=f"`{model_id}` retires{window}. After that, calls return 404.",
            remedy=f"Migrate to `{info.successor}` before the retirement date.",
            confidence=1.0 if in_call else 0.6,
        )


@check("MODEL_UNKNOWN", "models", "Model ID is not in the catalog — likely a typo")
def unknown_models(ctx: Context) -> Iterable[Finding]:
    for model_id, location, in_call in _all_model_uses(ctx):
        bare, _ = knowledge.strip_provider_prefix(model_id)
        if knowledge.is_known(bare):
            continue
        # Dated suffix on a live alias is the classic slip: `claude-opus-5` is
        # complete as-is, and appending a date produces a 404.
        stem = _strip_date(bare)
        hint = (
            f" Did you mean `{stem}`? Current aliases carry no date suffix."
            if stem != bare and knowledge.is_known(stem)
            else ""
        )
        yield Finding(
            id="MODEL_UNKNOWN",
            title=f"Unrecognised model ID `{model_id}`",
            severity=Severity.HIGH if in_call else Severity.LOW,
            location=location,
            detail=(
                f"`{model_id}` is not in the model catalog (as of {knowledge.KNOWLEDGE_AS_OF})."
                f"{hint} Either it is a typo, or this tool's catalog is stale."
            ),
            remedy="Verify against the Models API (`GET /v1/models`) and refresh `knowledge.py`.",
            confidence=0.7 if in_call else 0.4,
        )


@check("MODEL_FAST_SUFFIX", "models", "`-fast` model string — retired, and one of them fails silently")
def fast_suffix(ctx: Context) -> Iterable[Finding]:
    for model_id, location, in_call in _all_model_uses(ctx):
        bare, _ = knowledge.strip_provider_prefix(model_id)
        entry = knowledge.FAST_SUFFIX_MODELS.get(bare)
        if entry is None:
            continue
        mode, target = entry
        if mode == "silent-fallback":
            detail = (
                f"`{bare}` is retired and the API **silently falls back** to standard "
                "Opus 4.6. No error is raised — the caller just stops getting fast-mode "
                "speed and never finds out."
            )
            severity = Severity.HIGH
        else:
            detail = f"`{bare}` is retired and returns an API error."
            severity = Severity.CRITICAL
        yield Finding(
            id="MODEL_FAST_SUFFIX",
            title=f"Retired fast-mode model string `{bare}`",
            severity=severity if in_call else Severity.MEDIUM,
            location=location,
            detail=detail,
            remedy=(
                f"Move to `{target}` and request fast mode the supported way: "
                f'`client.beta.messages.create(model="{target}", speed="fast", '
                'betas=["fast-mode-2026-02-01"], ...)`. Note fast mode is Claude API only '
                "(not Bedrock/Vertex/Foundry) and is priced at $10/$50 per MTok."
            ),
        )


@check("MODEL_DATED_PIN", "models", "Pinned to a dated snapshot where an alias exists")
def dated_pin(ctx: Context) -> Iterable[Finding]:
    for model_id, location, in_call in _all_model_uses(ctx):
        if not in_call:
            continue
        bare, _ = knowledge.strip_provider_prefix(model_id)
        alias = knowledge.canonical(bare)
        if alias is None:
            continue
        yield Finding(
            id="MODEL_DATED_PIN",
            title=f"Dated snapshot pin `{bare}`",
            severity=Severity.LOW,
            location=location,
            detail=f"`{bare}` pins a dated snapshot of `{alias}`.",
            remedy=(
                f"Use the alias `{alias}` unless the pin is deliberate. Deliberate pins are "
                "fine — but they need an owner and a review date, or they become the reason "
                "an integration is three generations behind."
            ),
            confidence=0.8,
        )


@check("MODEL_TIER_MISMATCH", "cost", "Top-tier model on a call shaped like a cheap task")
def tier_mismatch(ctx: Context) -> Iterable[Finding]:
    """Deliberately conservative. A tiny `max_tokens` with no tools and no thinking
    is the one shape where over-tiering is provable from the request alone —
    classification and extraction. Everything subtler is the LLM pass's job."""
    for site in ctx.call_sites:
        model_id = site.model_id()
        if not model_id:
            continue
        info = knowledge.lookup(knowledge.strip_provider_prefix(model_id)[0])
        if info is None or info.tier not in ("opus", "fable"):
            continue
        max_tokens = site.get("max_tokens")
        n = max_tokens.as_int() if max_tokens else None
        if n is None or n > 512:
            continue
        if site.get("tools") or site.get("thinking"):
            continue
        cheaper = knowledge.lookup("claude-haiku-4-5")
        assert cheaper is not None
        cur_in, cur_out = info.price(ctx.today)
        new_in, new_out = cheaper.price(ctx.today)
        yield Finding(
            id="MODEL_TIER_MISMATCH",
            title=f"{info.display} on a {n}-token, tool-free call",
            severity=Severity.MEDIUM,
            location=site.location,
            detail=(
                f"`max_tokens={n}` with no tools and no thinking is the shape of a "
                f"classification or extraction call. {info.display} costs "
                f"${cur_in:.2f}/${cur_out:.2f} per MTok; {cheaper.display} costs "
                f"${new_in:.2f}/${new_out:.2f}."
            ),
            remedy=(
                f"Benchmark `{cheaper.id}` on this route. If accuracy holds, that is a "
                f"{(1 - new_in / cur_in) * 100:.0f}% cut on input and "
                f"{(1 - new_out / cur_out) * 100:.0f}% on output. "
                "Never downgrade without an eval — see EVAL_NONE."
            ),
            cost_signal=f"${cur_in:.2f}/MTok in -> ${new_in:.2f}/MTok in",
            confidence=0.55,
        )


@check("MODEL_REGISTRY", "models", "File looks like a model catalog, not a caller")
def registry_detected(ctx: Context) -> Iterable[Finding]:
    """One accurate summary beats twenty wrong alarms.

    A file listing many distinct model IDs is a *definer* — a registry, a routing
    table, a pricing catalog, a migration map. Those legitimately keep retired
    IDs: the model is still being served to someone, or the entry is the thing
    that knows it isn't. Reporting each one as a defect buries the real findings
    and teaches the reader to skim.
    """
    for path, model_ids in sorted(_registry_files(ctx).items()):
        stale = sorted(
            m
            for m in model_ids
            if m in knowledge.RETIRED
            or ((info := knowledge.lookup(m)) is not None and info.status_on(ctx.today) is not Status.CURRENT)
        )
        if not stale:
            continue
        line = min(
            (ref.location.line for ref in ctx.model_refs if ref.location.path == path),
            default=1,
        )
        yield Finding(
            id="MODEL_REGISTRY",
            title=f"`{path}` looks like a model catalog ({len(model_ids)} distinct IDs)",
            severity=Severity.INFO,
            location=Location(path, line),
            detail=(
                f"{len(stale)} of the entries reference retired or deprecated models: "
                + ", ".join(f"`{m}`" for m in stale[:8])
                + ("…" if len(stale) > 8 else "")
                + ". Per-entry findings are suppressed for this file — a registry that "
                "*serves* an old model is supposed to keep the ID."
            ),
            remedy=(
                "Confirm each stale entry is intentional. Registries usually need the old "
                "row kept and a new one added alongside — never a blind replace, which "
                "would de-register a model that is still in production."
            ),
            confidence=0.7,
        )


def _registry_files(ctx: Context) -> dict[str, set[str]]:
    """Files whose bare model-ID references cross the catalog threshold."""
    by_file: dict[str, set[str]] = {}
    for ref in ctx.model_refs:
        by_file.setdefault(ref.location.path, set()).add(ref.model_id)
    return {p: ids for p, ids in by_file.items() if len(ids) >= _REGISTRY_THRESHOLD}


def _strip_date(model_id: str) -> str:
    parts = model_id.rsplit("-", 1)
    if len(parts) == 2 and parts[1].isdigit() and len(parts[1]) == 8:
        return parts[0]
    return model_id


def _all_model_uses(ctx: Context) -> Iterable[tuple[str, Location, bool]]:
    for site in ctx.call_sites:
        model_id = site.model_id()
        if model_id:
            arg = site.get("model")
            yield model_id, (arg.location if arg else site.location), True
    registries = _registry_files(ctx)
    for ref in ctx.model_refs:
        # Suppressed in favour of one MODEL_REGISTRY summary per catalog file.
        if ref.location.path in registries:
            continue
        yield ref.model_id, ref.location, False
