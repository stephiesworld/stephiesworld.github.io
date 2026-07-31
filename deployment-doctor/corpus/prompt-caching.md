# Prompt caching

## What caching does

The API is stateless. Every request re-sends the whole prompt, so a long system
prompt that never changes is paid for on every single call.

Caching removes that cost. Mark a stable section, and on later requests that
section bills at roughly 10% of the normal input price instead of 100%.

## The prefix rule

Caching is a **prefix match**. The cached section must be byte-for-byte
identical to the previous request, and any change invalidates everything after
the change point.

Render order is `tools` → `system` → `messages`. Stable content must physically
come first; volatile content goes after the last breakpoint.

## Minimum cacheable prefix

A prompt shorter than the model's minimum is **not cached at all**. No error is
raised — the marker is accepted and silently ignored, so the request costs full
price while appearing to be cached.

| Model | Minimum |
|---|---:|
| Claude Opus 5, Claude Fable 5, Claude Mythos 5 | 512 tokens |
| Claude Opus 4.8, Claude Sonnet 5, Claude Sonnet 4.6, Claude Sonnet 4.5 | 1024 tokens |
| Claude Opus 4.7 | 2048 tokens |
| Claude Opus 4.6, Claude Opus 4.5, Claude Haiku 4.5 | 4096 tokens |

These minimums are **not monotonic across generations**. A 750-token prompt
caches on Claude Opus 5 and silently does not cache on Claude Opus 4.6, so a
prompt that worked can stop caching after what looks like an upgrade.

## Silent invalidators

These make the prefix unique on every request, so nothing is ever cached:

- `datetime.now()`, `date.today()`, or any timestamp in the system prompt
- A UUID or request ID early in the content
- `json.dumps()` without `sort_keys=True` — key order can vary between runs
- An f-string interpolating a user ID or session value into the system prompt
- Conditional system sections, where each combination of flags is a distinct prefix

## Verifying it works

Read `usage.cache_read_input_tokens` on the response. If it stays at zero across
repeated requests with the same prefix, something is invalidating the cache. The
total prompt size is `input_tokens + cache_creation_input_tokens +
cache_read_input_tokens` — `input_tokens` alone is only the uncached remainder.

## Breakpoints

At most **4** `cache_control` markers per request; more returns a 400. Place them
at genuine stability boundaries: the end of tools+system, the end of a shared
prefix, and the most recent conversation turn.

## Economics

Cache reads cost about 0.1x normal input price. Cache writes cost 1.25x for the
5-minute TTL and 2x for the 1-hour TTL. With the 5-minute TTL, two requests
break even. With the 1-hour TTL you need at least three.

## Changing things mid-conversation

Editing the top-level system prompt invalidates the whole conversation's cache.
On Claude Opus 5, Claude Opus 4.8, Claude Fable 5 and Claude Mythos 5 you can
instead append a `{"role": "system"}` message to `messages`, which adds operator
instructions without touching the cached prefix.

Switching models also invalidates the cache — caches are per-model. Adding or
removing tools invalidates everything, because tools render at position 0.
