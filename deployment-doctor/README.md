# Deployment Doctor

Point it at a repository that calls the Claude API. Get back a prioritised
scorecard: what will break, what's silently costing money, what's untested.

```
$ deployment-doctor ../customer-repo

Deployment Doctor — customer-repo
  score 42/100 · 22 finding(s)

  🔴 app/triage.py:36  `max_tokens=64000` on a non-streaming request
      STREAMING_REQUIRED  →  Switch to `client.messages.stream(...)` and call `.get_final_message()`
  🔴 app/triage.py:37  `temperature`, `top_p` rejected by Claude Opus 4.8
      PARAM_SAMPLING_REJECTED  →  Delete the parameter. If it was there for determinism, use effort
  🔴 app/triage.py:47  `text_editor_20250728` paired with `name='str_replace_editor'`
      TOOL_EDITOR_PAIR  →  Set `name="str_replace_based_edit_tool"`.
  🟠 app/triage.py:40  System prompt contains a per-request value
      CACHE_INVALIDATOR  →  Freeze the system prompt and move the dynamic value later in `messages`
  🟡 app/triage.py:70  Claude Opus 5 on a 16-token, tool-free call
      MODEL_TIER_MISMATCH  →  Benchmark `claude-haiku-4-5`: 80% cut on input and output
```

## Why

This automates the thing an AI deployment manager does by hand every week: read
a customer's integration and say what's costing them money and what's costing
them quality. It is deliberately the shape of a deliverable you'd send a
customer, not a dashboard nobody opens.

## Quickstart

```bash
pip install -e .

deployment-doctor ../some-repo                       # deterministic checks only
deployment-doctor ../some-repo --format markdown -o report.md
deployment-doctor ../some-repo --fix --dry-run       # show mechanical fixes
deployment-doctor --list-checks                      # the catalog
```

The deterministic checks are **stdlib-only** — no install step, no API key, no
network. Add `--llm` (or `--llm-agent`) for the judgement pass, which needs
`pip install -e ".[llm]"` and either `ANTHROPIC_API_KEY` or an `ant auth login`
profile.

Exit code is 1 if anything at or above `--fail-on` (default `high`) is found, so
it drops into CI as-is.

## Architecture

```
discover files → pick extractor by suffix → source → typed facts (CallSite/Arg)
                                                          │
                              ┌───────────────────────────┴──────────┐
                              │                                      │
                    ~30 pure check functions              judgement pass
                    facts → findings                      code → findings
                    (no model, no tokens)                       │
                              │                    ┌────────────┴────────────┐
                              │              --llm: one call        --llm-agent:
                              │              (payload known         tool loop, model
                              │               up front)             picks what to read
                              └───────────────┬──────────────────────┘
                                        merge, rank, score
                                              │
                                    render report / apply fixes
```

The split is the point. **Deterministic where the shape is known, model
judgement where it isn't** — and `checks/` has a hard rule: *prove it from the
extracted facts, or stay silent*. A static check that guesses produces confident
nonsense, which is worse than no finding. Anything requiring taste (is this
prompt any good? will this tool description actually trigger?) goes to the
judgement pass.

`--llm` makes one call, because we already know which files matter.
`--llm-agent` runs a real agent loop, because the reviewer decides what to read
next — it can follow a prompt constant into another module, or open a tool's
handler to check the implementation matches the description it advertises. That
payload can't be assembled in advance, which is exactly when you need a loop.
[`docs/the-loop.md`](docs/the-loop.md) works through that distinction.

| Module | Role |
|---|---|
| `knowledge.py` | Model catalog, prices, retirement dates, breaking parameters. **The part that rots** — refreshing is a diff to one file. |
| `extract/` | Source → typed facts. One extractor per language, one interface. |
| `checks/` | ~30 pure functions over the facts. Registered by decorator. |
| `llm.py` | Judgement pass, single call. |
| `agent.py` | Judgement pass, agent loop with `grep` / `read_file` tools. |
| `report.py` | Markdown / JSON / terminal rendering, scorecard, coverage note. |
| `fix.py` | Line-scoped auto-fixes, verified before writing. |

Full file-by-file explanation: [`docs/walkthrough.md`](docs/walkthrough.md).

## What it checks

30 checks across six dimensions. `--list-checks` prints the current catalog.

**Models** — retired IDs (404s), deprecation windows computed against today,
hallucinated or typo'd IDs, dated snapshots pinned where an alias exists,
retired `-fast` strings (one of which *silently* falls back and costs you fast
mode with no error).

**Cost** — large prefixes re-sent uncached, `cache_control` set below the
model's minimum cacheable size (accepted silently, caches nothing), per-request
values inside the cached prefix, non-deterministic serialization, top-tier
models on classification-shaped calls.

**Correctness** — everything that returns a 400 on current models: sampling
parameters, `budget_tokens`, assistant prefill, disabled thinking above `high`
effort, more than four cache breakpoints. Plus the silent ones: adaptive
thinking now defaulting *on* and truncating a `max_tokens` sized for the answer
alone, and large `max_tokens` without streaming.

**Tools** — stale version strings, the `text_editor` `type`/`name` pair (the
most common migration slip), descriptions with no trigger condition,
undocumented parameters, custom tools shadowing Anthropic-defined names, MCP
servers declared without a matching toolset.

**Resilience** — `stop_reason: refusal` never checked (a refusal is a 200 with
an empty `content` array, not an exception), `content[0]` indexed without a type
check, catch-all exception handling that can't distinguish retryable from
permanent, disabled retries.

**Evals** — no test asserting on model output, or tests that mock the model
exclusively. Plus `tiktoken` used to count Claude tokens, which undercounts by
15–20% on prose and far more on code.

## Cache-minimum example

The check that most justifies the tool existing:

```python
system=[{"type": "text", "text": PROMPT_750_TOKENS,
         "cache_control": {"type": "ephemeral"}}]
```

Fine on Opus 5 (512-token minimum). On Opus 4.6 (4096) it is accepted, raises no
error, and caches nothing — you pay full price believing you don't. The minimum
is **not monotonic across generations**, so this survives an "upgrade."

## What it does not do

Stated plainly, and repeated in every report's coverage section, because a
report that hides its blind spots reads as a clean bill of health:

- **No runtime behaviour.** No real token counts, no real cache hit rates, no
  output quality. Those need the live API and an eval set.
- **JS/TS is read heuristically, not parsed.** Identifiers, spreads, and
  imported constants are invisible. Absence of findings there is absence of
  evidence.
- **Model IDs from config, env vars, or a database are invisible.** Python
  module-level constants are traced; a database lookup isn't.
- **Bare model-ID strings are reported but never auto-fixed.** A registry that
  legitimately *serves* an old model should keep the ID; only the caller needs
  changing. The tool can't tell which you have, so it says so instead of
  guessing.
- **The catalog goes stale.** `knowledge.py` carries a `KNOWLEDGE_AS_OF` date
  and every report prints it. Unknown IDs are reported as *either* a typo *or* a
  stale catalog, because from inside the tool those are indistinguishable.

## Development

```bash
pip install -e ".[dev]"
pytest                        # 42 tests, no network
python -m doctor.cli tests/fixtures --fail-on never
```

`tests/fixtures/sick_app.py` is a deliberately broken integration; every defect
in it is one that ships in real code. `healthy_app.py` is the control — the
suite asserts the analyser stays quiet on it, because a linter that can't be
satisfied gets turned off.

Adding a check is one function:

```python
@check("MY_CHECK", "cost", "One-line summary for --list-checks")
def my_check(ctx: Context) -> Iterable[Finding]:
    for site in ctx.call_sites:
        ...
        yield Finding(id="MY_CHECK", ...)
```

## Roadmap

- Real TS parsing (tree-sitter) to close the largest coverage gap
- `--fix` emitting a branch and a PR rather than editing in place
- Cost model driven by real usage data instead of static request shape
- Go / Java / Ruby extractors behind the same interface
