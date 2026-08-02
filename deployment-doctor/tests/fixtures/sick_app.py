"""Deliberately broken fixture. Every defect here is one a real integration ships.

Do not "fix" this file — the test suite asserts on what's wrong with it.
"""

import json
from datetime import datetime

import anthropic

client = anthropic.Anthropic(max_retries=0)

MODEL = "claude-opus-4-8"
LEGACY_MODEL = "claude-3-opus-20240229"  # retired: 404
SYSTEM = "You are a support triage assistant. " + ("Context paragraph. " * 900)

TOOLS = [
    {
        "type": "text_editor_20250728",
        "name": "str_replace_editor",  # wrong name for this type -> 400
    },
    {
        "name": "lookup_order",
        "description": "Gets orders",  # no trigger condition, no param docs
        "input_schema": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}},
        },
    },
]


def triage(ticket: str) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=64000,  # non-streaming at this size: SDK raises ValueError
        temperature=0.2,  # rejected on current models
        top_p=0.9,  # ...and both together error on any Claude 4+
        thinking={"type": "enabled", "budget_tokens": 8000},  # removed
        system=[
            {
                "type": "text",
                "text": SYSTEM + json.dumps({"now": str(datetime.now())}),
                "cache_control": {"type": "ephemeral"},
            }
        ],
        tools=TOOLS,
        messages=[
            {"role": "user", "content": ticket},
            {"role": "assistant", "content": '{"category": "'},  # prefill -> 400
        ],
    )
    return response.content[0].text  # index 0 is a thinking block, not text


def archive_summary(doc: str) -> str:
    """Nobody has touched this path since 2024. It 404s."""
    return (
        client.messages.create(
            model=LEGACY_MODEL,
            max_tokens=1024,
            messages=[{"role": "user", "content": doc}],
        )
        .content[0]
        .text
    )


def classify(text: str) -> str:
    resp = client.messages.create(
        model="claude-opus-5",
        max_tokens=16,
        messages=[{"role": "user", "content": f"Label this: {text}"}],
    )
    return resp.content[0].text


def summarise(doc: str) -> str:
    try:
        return client.messages.create(
            model="claude-opus-4-6-fast",  # retired; silently falls back to standard
            max_tokens=1024,
            messages=[{"role": "user", "content": doc}],
            extra_headers={"anthropic-beta": "effort-2025-11-24,interleaved-thinking-2025-05-14"},
        ).content[0].text
    except Exception:  # noqa: BLE001 - untyped catch-all
        return ""
