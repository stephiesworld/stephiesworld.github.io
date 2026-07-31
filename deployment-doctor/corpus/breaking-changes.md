# Breaking changes and silent behaviour changes

## Parameters that return a 400 on current models

### Sampling parameters

`temperature`, `top_p`, and `top_k` are removed on Claude Opus 5, Claude Fable 5,
Claude Opus 4.8, and Claude Opus 4.7. Sending any of them returns a 400. On
Claude Sonnet 5, non-default values are rejected.

If the parameter was there for determinism, use `output_config: {"effort": "low"}`
with a tighter prompt — note that `temperature=0` never guaranteed identical
outputs anyway. If it was there for creative variance, steer with the prompt
instead.

On any Claude 4+ model, passing both `temperature` and `top_p` together errors.

### Extended thinking budgets

`thinking: {"type": "enabled", "budget_tokens": N}` is removed on Claude Opus 5,
Claude Fable 5, Claude Opus 4.8, and Claude Opus 4.7, and deprecated on Claude
Opus 4.6 and Claude Sonnet 4.6.

Use `thinking: {"type": "adaptive"}` and control depth with
`output_config.effort`. There is no one-to-one token mapping between a budget
and an effort level.

### Assistant prefill

Ending the `messages` array on an assistant turn returns a 400 on Claude Opus 5,
Claude Fable 5, Claude Sonnet 5, and the entire 4.6/4.7/4.8 family.

Replacements depend on what the prefill was doing: forcing a JSON shape becomes
`output_config.format` with a schema; forcing a label becomes a tool with an
enum; skipping a preamble becomes a system-prompt instruction; continuing an
interrupted response moves into the user turn.

### Disabled thinking above high effort

On Claude Opus 5, `thinking: {"type": "disabled"}` is accepted only at effort
`high` or lower. Pairing it with `xhigh` or `max` returns a 400. This is
validated per request, so a later call that raises effort fails even if earlier
calls in the same conversation succeeded.

On Claude Fable 5, an explicit `{"type": "disabled"}` returns a 400 at any effort
level — omit the `thinking` parameter entirely instead.

### Tool version pairs

The text editor tool's `type` and `name` fields are a matched pair. Changing one
without the other returns a 400.

| Type | Required name |
|---|---|
| `text_editor_20250124` | `str_replace_editor` |
| `text_editor_20250429` | `str_replace_based_edit_tool` |
| `text_editor_20250728` | `str_replace_based_edit_tool` |

### MCP configuration

`mcp_servers` and `tools` are two halves of one configuration. Every declared
server must be referenced by exactly one `{"type": "mcp_toolset",
"mcp_server_name": ...}` entry, or the request is rejected.

### Tool search

At least one tool must be non-deferred, and the tool-search tool itself must
never carry `defer_loading: true`. Deferring everything returns a 400.

## Silent changes — no error, different behaviour

### Thinking now defaults on

On Claude Opus 5 and Claude Sonnet 5, omitting the `thinking` parameter runs
**adaptive thinking**. The previous generation ran without it.

`max_tokens` is a hard cap on thinking *plus* response text, so a budget sized
around the answer alone can now truncate mid-response. There is no error — the
reply is simply cut off. Check `stop_reason == "max_tokens"` in production.

### Thinking content is omitted by default

`thinking.display` defaults to `"omitted"` on Claude Opus 5, Claude Fable 5,
Claude Opus 4.8 and 4.7, and Claude Sonnet 5. Thinking blocks still appear in the
response, but their text is empty. Set `display: "summarized"` to get readable
reasoning. To a streaming UI, the default looks like a long pause before output.

### Refusals are not errors

Claude Opus 5, Claude Fable 5, Claude Mythos 5, and Claude Sonnet 5 run safety
classifiers that can decline a request. A decline is a **successful HTTP 200**
with `stop_reason: "refusal"` and an empty or partial `content` array — not an
exception.

Code doing `response.content[0].text` raises an `IndexError` on the first
refusal. Branch on `stop_reason` before reading `content`. Branch on
`stop_reason`, not `stop_details`, which is informational and can be `null` even
on a refusal.

Server-side fallbacks re-serve a declined request automatically. Use
`fallbacks: "default"` with the `server-side-fallback-2026-07-01` beta, which
routes by refusal category so there is no model list to maintain.

### Tokenizer changes

Claude Sonnet 5 produces roughly 30% more tokens than Claude Sonnet 4.6 for the
same text. Per-token pricing is unchanged, so equivalent requests cost more.
Re-run `count_tokens` against the new model rather than reusing old counts.

Never use `tiktoken` for Claude — it is OpenAI's tokenizer and undercounts by
15–20% on prose and considerably more on code.

## Beta headers that went GA

Remove these; they are no-ops that pin you to the beta client for nothing:
`effort-2025-11-24`, `fine-grained-tool-streaming-2025-05-14`,
`token-efficient-tools-2025-02-19`, `output-128k-2025-02-19`, and
`interleaved-thinking-2025-05-14` once you are on adaptive thinking.

## Streaming requirement

Non-streaming requests above roughly 16,000 `max_tokens` risk an HTTP timeout on
a long generation. Well before the 128K ceiling, the Python SDK refuses the
request outright with a `ValueError`. Use `client.messages.stream(...)` and
`.get_final_message()`.
