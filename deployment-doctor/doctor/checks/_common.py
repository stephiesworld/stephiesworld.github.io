"""Shared helpers for reading structure out of a CallSite."""

from __future__ import annotations

from typing import Any

from .. import knowledge
from ..knowledge import ModelInfo
from ..model import CallSite


def model_of(site: CallSite) -> ModelInfo | None:
    model_id = site.model_id()
    if not model_id:
        return None
    bare, _ = knowledge.strip_provider_prefix(model_id)
    return knowledge.lookup(bare)


def thinking_of(site: CallSite) -> dict[str, Any] | None:
    arg = site.get("thinking")
    if arg is None or not isinstance(arg.value, dict):
        return None
    return arg.value


def effort_of(site: CallSite) -> str | None:
    arg = site.get("output_config")
    if arg and isinstance(arg.value, dict):
        effort = arg.value.get("effort")
        if isinstance(effort, str):
            return effort
        if isinstance(effort, dict):
            t = effort.get("type")
            return t if isinstance(t, str) else None
    return None


def betas_of(site: CallSite) -> list[str]:
    out: list[str] = []
    arg = site.get("betas")
    if arg and isinstance(arg.value, (list, tuple)):
        out.extend(v for v in arg.value if isinstance(v, str))
    headers = site.get("extra_headers")
    if headers and isinstance(headers.value, dict):
        raw = headers.value.get("anthropic-beta")
        if isinstance(raw, str):
            out.extend(part.strip() for part in raw.split(",") if part.strip())
    return out


def messages_of(site: CallSite) -> list[Any] | None:
    arg = site.get("messages")
    if arg and isinstance(arg.value, list):
        return arg.value
    return None


def tools_of(site: CallSite) -> list[Any] | None:
    arg = site.get("tools")
    if arg and isinstance(arg.value, list):
        return arg.value
    return None


def system_blocks(site: CallSite) -> list[Any]:
    arg = site.get("system")
    if arg is None:
        return []
    if isinstance(arg.value, list):
        return arg.value
    return [arg.value] if arg.value is not None else []


def count_cache_breakpoints(site: CallSite) -> int:
    """Count `cache_control` markers across tools, system, and messages."""
    total = 0
    for name in ("tools", "system", "messages"):
        arg = site.get(name)
        if arg is None:
            continue
        total += _count_cache_control(arg.value)
    return total


def _count_cache_control(value: Any) -> int:
    if isinstance(value, dict):
        n = 1 if "cache_control" in value else 0
        return n + sum(_count_cache_control(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        return sum(_count_cache_control(v) for v in value)
    return 0


def has_cache_control(site: CallSite) -> bool:
    if site.get("cache_control") is not None:
        return True
    return count_cache_breakpoints(site) > 0


def estimate_tokens(text: str) -> int:
    """Rough character-based estimate, only ever used to decide whether a prefix is
    *obviously* below a cache minimum. Never reported as a number — for real
    counts, callers should use `client.messages.count_tokens`, not this."""
    return max(1, len(text) // 4)


def static_system_text(site: CallSite) -> str | None:
    """Concatenate statically-known system text, or None if we can't see it."""
    blocks = system_blocks(site)
    if not blocks:
        return None
    parts: list[str] = []
    for block in blocks:
        if isinstance(block, str):
            parts.append(block)
        elif isinstance(block, dict) and isinstance(block.get("text"), str):
            parts.append(block["text"])
        else:
            return None
    return "\n".join(parts) if parts else None
