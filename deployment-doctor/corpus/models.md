# Model catalog

Snapshot as of 2026-06-24. Prices are US dollars per million tokens.

## Current models

| Model | ID | Context | Max output | Input | Output |
|---|---|---:|---:|---:|---:|
| Claude Fable 5 | `claude-fable-5` | 1M | 128K | $10.00 | $50.00 |
| Claude Opus 5 | `claude-opus-5` | 1M | 128K | $5.00 | $25.00 |
| Claude Sonnet 5 | `claude-sonnet-5` | 1M | 128K | $3.00 | $15.00 |
| Claude Haiku 4.5 | `claude-haiku-4-5` | 200K | 64K | $1.00 | $5.00 |

Claude Sonnet 5 has introductory pricing of $2.00 / $10.00 through 2026-08-31.

Model IDs are complete as written. **Never append a date suffix** to a current
alias — `claude-opus-5-20260101` is not a real model and returns a 404.

## Previous generation, still served

`claude-opus-4-8`, `claude-opus-4-7`, `claude-opus-4-6`, `claude-opus-4-5`,
`claude-sonnet-4-6`, `claude-sonnet-4-5`.

## Deprecated

| Model | Retires | Replace with |
|---|---|---|
| `claude-opus-4-1` | 2026-08-05 | `claude-opus-5` |
| `claude-opus-4-0` | 2026-06-15 | `claude-opus-5` |
| `claude-sonnet-4-0` | 2026-06-15 | `claude-sonnet-5` |
| `claude-3-haiku-20240307` | 2026-04-19 | `claude-haiku-4-5` |

## Retired — these return 404

| Model | Retired | Replace with |
|---|---|---|
| `claude-3-7-sonnet-20250219` | 2026-02-19 | `claude-sonnet-5` |
| `claude-3-5-haiku-20241022` | 2026-02-19 | `claude-haiku-4-5` |
| `claude-3-opus-20240229` | 2026-01-05 | `claude-opus-5` |
| `claude-3-5-sonnet-20241022` | 2025-10-28 | `claude-sonnet-5` |
| `claude-3-5-sonnet-20240620` | 2025-10-28 | `claude-sonnet-5` |
| `claude-3-sonnet-20240229` | 2025-07-21 | `claude-sonnet-5` |
| `claude-2.1`, `claude-2.0` | 2025-07-21 | `claude-sonnet-5` |

## Choosing effort

`output_config.effort` accepts `low`, `medium`, `high`, `xhigh`, `max`. Default
is `high`.

Start at `xhigh` for coding and agentic work, `high` for other work that needs
intelligence, then sweep downward — `low` and `medium` are unusually strong on
Claude Opus 5, and effort defaults carried over from an older model are rarely
the right setting.

At `xhigh` or `max`, set a large `max_tokens` — start around 64000 — so the
model has room to think and act across tool calls.

## Fast mode

`speed: "fast"` is available on Claude Opus 5 and Claude Opus 4.8 only, requires
the `fast-mode-2026-02-01` beta flag and the beta messages endpoint, and is
priced at $10 / $50 per million tokens. It is Claude API only — not available on
Amazon Bedrock, Google Vertex AI, or Microsoft Foundry.

The retired `-fast` model strings behave differently and both are traps:
`claude-opus-4-6-fast` **silently falls back** to standard Opus 4.6, so you lose
fast mode with no error at all. `claude-opus-4-7-fast` returns an API error.

## Provider prefixes

Amazon Bedrock model IDs carry an `anthropic.` prefix — `anthropic.claude-opus-5`.
Google Vertex AI and Claude Platform on AWS use the bare first-party ID.
