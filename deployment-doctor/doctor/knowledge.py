"""The knowledge base every check reads from.

This is the part that rots. Model IDs, prices, retirement dates, and which
parameters return a 400 all change on Anthropic's release cadence, not yours.
Keep the facts here and the logic in `checks/` so a refresh is a diff to one file.

Sourced from the Anthropic model catalog and migration guide as of 2026-06-24.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import date

KNOWLEDGE_AS_OF = date(2026, 6, 24)


class Status(enum.Enum):
    CURRENT = "current"
    LEGACY = "legacy"  # still served, not the recommended target
    DEPRECATED = "deprecated"  # retirement date announced
    RETIRED = "retired"  # returns 404


@dataclass(frozen=True)
class ModelInfo:
    id: str
    display: str
    tier: str
    status: Status
    input_usd: float  # per million tokens
    output_usd: float
    context: int
    max_output: int
    # Minimum cacheable prefix. NOT monotonic across generations — a 3K-token
    # prompt caches on Opus 5 and silently does not on Opus 4.6.
    cache_min_tokens: int = 1024
    retires: date | None = None
    successor: str | None = None
    # --- request-surface behaviour -------------------------------------------
    rejects_sampling_params: bool = False  # temperature/top_p/top_k -> 400
    rejects_budget_tokens: bool = False  # thinking.budget_tokens -> 400
    rejects_prefill: bool = False  # trailing assistant turn -> 400
    thinking_on_by_default: bool = False  # omitting `thinking` still thinks
    thinking_disable_max_effort: str | None = None  # None = disable always allowed
    rejects_thinking_disabled: bool = False  # Fable 5: disabled -> 400 at any effort
    effort_levels: tuple[str, ...] = ()
    supports_fast_mode: bool = False
    # `thinking={"type": "adaptive"}` -> 400 on models predating it. A flag
    # rather than a version comparison, for the same reason as everything else
    # here: "newer than X" is not a fact about the API, it is a guess that holds
    # until it doesn't.
    supports_adaptive_thinking: bool = False
    # Server-side `fallbacks`. Narrower than adaptive thinking — Sonnet 5 has
    # adaptive thinking and rejects `fallbacks`, so one cannot stand in for the
    # other.
    supports_server_fallbacks: bool = False
    intro_input_usd: float | None = None
    intro_output_usd: float | None = None
    intro_until: date | None = None

    def price(self, on: date) -> tuple[float, float]:
        if self.intro_until and on <= self.intro_until and self.intro_input_usd is not None:
            return (self.intro_input_usd, self.intro_output_usd or self.output_usd)
        return (self.input_usd, self.output_usd)

    def status_on(self, on: date) -> Status:
        if self.retires and on >= self.retires:
            return Status.RETIRED
        return self.status


_EFFORT_FULL = ("low", "medium", "high", "xhigh", "max")
_EFFORT_46 = ("low", "medium", "high", "max")

MODELS: dict[str, ModelInfo] = {
    m.id: m
    for m in [
        ModelInfo(
            id="claude-fable-5",
            display="Claude Fable 5",
            tier="fable",
            status=Status.CURRENT,
            input_usd=10.0,
            output_usd=50.0,
            context=1_000_000,
            max_output=128_000,
            cache_min_tokens=512,
            rejects_sampling_params=True,
            rejects_budget_tokens=True,
            rejects_prefill=True,
            thinking_on_by_default=True,
            rejects_thinking_disabled=True,
            effort_levels=_EFFORT_FULL,
            supports_adaptive_thinking=True,
            supports_server_fallbacks=True,
        ),
        ModelInfo(
            id="claude-mythos-5",
            display="Claude Mythos 5",
            tier="fable",
            status=Status.CURRENT,
            input_usd=10.0,
            output_usd=50.0,
            context=1_000_000,
            max_output=128_000,
            cache_min_tokens=512,
            rejects_sampling_params=True,
            rejects_budget_tokens=True,
            rejects_prefill=True,
            thinking_on_by_default=True,
            rejects_thinking_disabled=True,
            effort_levels=_EFFORT_FULL,
            supports_adaptive_thinking=True,
            supports_server_fallbacks=True,
        ),
        ModelInfo(
            id="claude-opus-5",
            display="Claude Opus 5",
            tier="opus",
            status=Status.CURRENT,
            input_usd=5.0,
            output_usd=25.0,
            context=1_000_000,
            max_output=128_000,
            cache_min_tokens=512,
            rejects_sampling_params=True,
            rejects_budget_tokens=True,
            rejects_prefill=True,
            thinking_on_by_default=True,
            thinking_disable_max_effort="high",
            effort_levels=_EFFORT_FULL,
            supports_fast_mode=True,
            supports_adaptive_thinking=True,
            supports_server_fallbacks=True,
        ),
        ModelInfo(
            id="claude-opus-4-8",
            display="Claude Opus 4.8",
            tier="opus",
            status=Status.LEGACY,
            input_usd=5.0,
            output_usd=25.0,
            context=1_000_000,
            max_output=128_000,
            cache_min_tokens=1024,
            successor="claude-opus-5",
            rejects_sampling_params=True,
            rejects_budget_tokens=True,
            rejects_prefill=True,
            effort_levels=_EFFORT_FULL,
            supports_fast_mode=True,
            supports_adaptive_thinking=True,
        ),
        ModelInfo(
            id="claude-opus-4-7",
            display="Claude Opus 4.7",
            tier="opus",
            status=Status.LEGACY,
            input_usd=5.0,
            output_usd=25.0,
            context=1_000_000,
            max_output=128_000,
            cache_min_tokens=2048,
            successor="claude-opus-5",
            rejects_sampling_params=True,
            rejects_budget_tokens=True,
            rejects_prefill=True,
            effort_levels=_EFFORT_FULL,
            supports_adaptive_thinking=True,
        ),
        ModelInfo(
            id="claude-opus-4-6",
            display="Claude Opus 4.6",
            tier="opus",
            status=Status.LEGACY,
            input_usd=5.0,
            output_usd=25.0,
            context=1_000_000,
            max_output=128_000,
            cache_min_tokens=4096,
            successor="claude-opus-5",
            rejects_prefill=True,
            effort_levels=_EFFORT_46,
            supports_adaptive_thinking=True,
        ),
        ModelInfo(
            id="claude-opus-4-5",
            display="Claude Opus 4.5",
            tier="opus",
            status=Status.LEGACY,
            input_usd=5.0,
            output_usd=25.0,
            context=200_000,
            max_output=64_000,
            cache_min_tokens=4096,
            successor="claude-opus-5",
            effort_levels=("low", "medium", "high"),
        ),
        ModelInfo(
            id="claude-opus-4-1",
            display="Claude Opus 4.1",
            tier="opus",
            status=Status.DEPRECATED,
            input_usd=15.0,
            output_usd=75.0,
            context=200_000,
            max_output=32_000,
            retires=date(2026, 8, 5),
            successor="claude-opus-5",
        ),
        ModelInfo(
            id="claude-opus-4-0",
            display="Claude Opus 4",
            tier="opus",
            status=Status.DEPRECATED,
            input_usd=15.0,
            output_usd=75.0,
            context=200_000,
            max_output=32_000,
            retires=date(2026, 6, 15),
            successor="claude-opus-5",
        ),
        ModelInfo(
            id="claude-sonnet-5",
            display="Claude Sonnet 5",
            tier="sonnet",
            status=Status.CURRENT,
            input_usd=3.0,
            output_usd=15.0,
            intro_input_usd=2.0,
            intro_output_usd=10.0,
            intro_until=date(2026, 8, 31),
            context=1_000_000,
            max_output=128_000,
            cache_min_tokens=1024,
            rejects_sampling_params=True,
            rejects_budget_tokens=True,
            rejects_prefill=True,
            thinking_on_by_default=True,
            effort_levels=_EFFORT_FULL,
            supports_adaptive_thinking=True,
        ),
        ModelInfo(
            id="claude-sonnet-4-6",
            display="Claude Sonnet 4.6",
            tier="sonnet",
            status=Status.LEGACY,
            input_usd=3.0,
            output_usd=15.0,
            context=1_000_000,
            max_output=128_000,
            cache_min_tokens=1024,
            successor="claude-sonnet-5",
            rejects_prefill=True,
            effort_levels=_EFFORT_46,
            supports_adaptive_thinking=True,
        ),
        ModelInfo(
            id="claude-sonnet-4-5",
            display="Claude Sonnet 4.5",
            tier="sonnet",
            status=Status.LEGACY,
            input_usd=3.0,
            output_usd=15.0,
            context=200_000,
            max_output=64_000,
            cache_min_tokens=1024,
            successor="claude-sonnet-5",
        ),
        ModelInfo(
            id="claude-sonnet-4-0",
            display="Claude Sonnet 4",
            tier="sonnet",
            status=Status.DEPRECATED,
            input_usd=3.0,
            output_usd=15.0,
            context=200_000,
            max_output=64_000,
            retires=date(2026, 6, 15),
            successor="claude-sonnet-5",
        ),
        ModelInfo(
            id="claude-haiku-4-5",
            display="Claude Haiku 4.5",
            tier="haiku",
            status=Status.CURRENT,
            input_usd=1.0,
            output_usd=5.0,
            context=200_000,
            max_output=64_000,
            cache_min_tokens=4096,
        ),
        ModelInfo(
            id="claude-3-haiku-20240307",
            display="Claude Haiku 3",
            tier="haiku",
            status=Status.DEPRECATED,
            input_usd=0.25,
            output_usd=1.25,
            context=200_000,
            max_output=4096,
            retires=date(2026, 4, 19),
            successor="claude-haiku-4-5",
        ),
    ]
}

# Retired: the API returns 404. Value is the recommended replacement.
RETIRED: dict[str, str] = {
    "claude-3-7-sonnet-20250219": "claude-sonnet-5",
    "claude-3-5-haiku-20241022": "claude-haiku-4-5",
    "claude-3-opus-20240229": "claude-opus-5",
    "claude-3-5-sonnet-20241022": "claude-sonnet-5",
    "claude-3-5-sonnet-20240620": "claude-sonnet-5",
    "claude-3-sonnet-20240229": "claude-sonnet-5",
    "claude-2.1": "claude-sonnet-5",
    "claude-2.0": "claude-sonnet-5",
}

# Dated snapshots that alias to a live model. Pinning is legal but usually
# accidental — flag as LOW.
DATED_ALIASES: dict[str, str] = {
    "claude-haiku-4-5-20251001": "claude-haiku-4-5",
    "claude-opus-4-5-20251101": "claude-opus-4-5",
    "claude-sonnet-4-5-20250929": "claude-sonnet-4-5",
    "claude-opus-4-1-20250805": "claude-opus-4-1",
    "claude-opus-4-20250514": "claude-opus-4-0",
    "claude-sonnet-4-20250514": "claude-sonnet-4-0",
}

DEFAULT_TARGET = {
    "opus": "claude-opus-5",
    "sonnet": "claude-sonnet-5",
    "haiku": "claude-haiku-4-5",
    "fable": "claude-fable-5",
}

# `-fast` suffix strings. `claude-opus-4-6-fast` is retired and *silently* falls
# back to standard Opus 4.6 — no error, the caller just quietly loses fast mode.
# `claude-opus-4-7-fast` hard-errors instead.
FAST_SUFFIX_MODELS = {
    "claude-opus-4-6-fast": ("silent-fallback", "claude-opus-5"),
    "claude-opus-4-7-fast": ("error", "claude-opus-5"),
}

# Beta headers that went GA. Harmless, but they pin callers to `client.beta.*`
# for no reason.
GA_BETA_HEADERS: dict[str, str] = {
    "effort-2025-11-24": "Effort is GA.",
    "fine-grained-tool-streaming-2025-05-14": "GA — set `eager_input_streaming` on the tool instead.",
    "token-efficient-tools-2025-02-19": "Built into all Claude 4+ models; the header is a no-op.",
    "output-128k-2025-02-19": "Built into Claude 4+ models; the header is a no-op.",
    "interleaved-thinking-2025-05-14": "Adaptive thinking enables interleaving automatically.",
}

# Superseded server-tool / client-tool versions.
TOOL_UPGRADES: dict[str, str] = {
    "text_editor_20250124": "text_editor_20250728",
    "text_editor_20250429": "text_editor_20250728",
    "web_search_20250305": "web_search_20260209",
    "web_fetch_20250910": "web_fetch_20260209",
    "code_execution_20250825": "code_execution_20260521",
    "code_execution_20250522": "code_execution_20260521",
}

# The text-editor `type` and `name` fields are a matched pair. Updating one and
# not the other is a 400 — and it's the single most common migration slip.
TEXT_EDITOR_NAMES: dict[str, str] = {
    "text_editor_20250124": "str_replace_editor",
    "text_editor_20250429": "str_replace_based_edit_tool",
    "text_editor_20250728": "str_replace_based_edit_tool",
}

SAMPLING_PARAMS = ("temperature", "top_p", "top_k")

# Non-streaming requests above this risk an SDK HTTP timeout; the Python SDK
# raises ValueError outright well before the 128K ceiling.
NONSTREAMING_MAXTOKENS_WARN = 16_000
NONSTREAMING_MAXTOKENS_FAIL = 32_000

MAX_CACHE_BREAKPOINTS = 4

# Expressions that make a cached prefix unique per request.
CACHE_INVALIDATORS: dict[str, str] = {
    "datetime.now": "a timestamp changes the prefix on every request",
    "datetime.utcnow": "a timestamp changes the prefix on every request",
    "date.today": "rolls the cache at midnight and on every date boundary",
    "time.time": "a timestamp changes the prefix on every request",
    "uuid.uuid4": "a fresh UUID makes every prefix unique",
    "uuid4": "a fresh UUID makes every prefix unique",
    "random.random": "randomness in the prefix defeats the cache entirely",
    "os.urandom": "randomness in the prefix defeats the cache entirely",
}


def lookup(model_id: str) -> ModelInfo | None:
    return MODELS.get(model_id)


def canonical(model_id: str) -> str | None:
    """Resolve a dated snapshot to its alias, if there is one."""
    return DATED_ALIASES.get(model_id)


def is_known(model_id: str) -> bool:
    return (
        model_id in MODELS
        or model_id in RETIRED
        or model_id in DATED_ALIASES
        or model_id in FAST_SUFFIX_MODELS
    )


def looks_like_model_id(value: str) -> bool:
    """Heuristic for strings that are *meant* to be model IDs, so we can flag
    typos and hallucinated IDs rather than silently ignoring them."""
    v = value.strip()
    if v.startswith("anthropic."):  # Bedrock provider prefix
        v = v[len("anthropic.") :]
    return v.startswith("claude-") or v in {"claude-2.1", "claude-2.0"}


def strip_provider_prefix(value: str) -> tuple[str, str | None]:
    """Bedrock IDs carry an `anthropic.` prefix; Vertex/first-party do not."""
    if value.startswith("anthropic."):
        return value[len("anthropic.") :], "bedrock"
    return value, None


def cheaper_alternative(model_id: str) -> ModelInfo | None:
    """The next tier down, for the 'is Opus doing Haiku's job?' check."""
    info = lookup(model_id)
    if info is None:
        return None
    ladder = {"fable": "claude-opus-5", "opus": "claude-sonnet-5", "sonnet": "claude-haiku-4-5"}
    target = ladder.get(info.tier)
    return lookup(target) if target else None
