"""A clean fixture. The tests assert the analyser stays quiet on this one —
a linter that can't be satisfied gets turned off."""

import anthropic

client = anthropic.Anthropic()

MODEL = "claude-opus-5"

# Frozen. No timestamps, no per-user interpolation, nothing that changes the
# cached prefix between requests.
SYSTEM = "You are a support triage assistant.\n" + ("Policy paragraph. " * 900)

TOOLS = [
    {
        "name": "lookup_order",
        "description": (
            "Look up an order by ID. Call this whenever the user references an order, "
            "asks about delivery status, or mentions a tracking number — do not answer "
            "from the conversation history alone."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "Order ID, format ORD-00000000.",
                }
            },
            "required": ["order_id"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]


def triage(ticket: str) -> str:
    with client.messages.stream(
        model=MODEL,
        max_tokens=64000,
        thinking={"type": "adaptive"},
        output_config={"effort": "high"},
        system=[{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
        tools=TOOLS,
        messages=[{"role": "user", "content": ticket}],
    ) as stream:
        response = stream.get_final_message()

    if response.stop_reason == "refusal":
        raise RuntimeError("declined")
    return next(b.text for b in response.content if b.type == "text")
