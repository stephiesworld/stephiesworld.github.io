# Code walkthrough

Every file, what it does, and why it's shaped that way. Read this next to the
code. Roughly in dependency order — each layer only knows about the one below.

```
knowledge.py     facts about Claude models          (no dependencies)
model.py         the types everything speaks in     (no dependencies)
extract/         source code → typed facts          (uses model.py)
checks/          typed facts → findings             (uses model.py, knowledge.py)
llm.py           code → findings, one call          (uses model.py)
agent.py         code → findings, agent loop        (uses model.py, llm.py)
report.py        findings → markdown/JSON/terminal
fix.py           findings → edits on disk
cli.py           wires it all together
```

The one rule that shapes everything: **checks never touch a syntax tree.** They
read typed facts. That's why adding a language is one new file in `extract/`
instead of edits to thirty check functions.

---

## `knowledge.py` — the part that rots

Every fact about Claude models: IDs, prices, context windows, retirement dates,
cache minimums, and which parameters return a 400 on which model.

It's a separate module for one reason: **this is the only part guaranteed to go
stale.** Model IDs and prices change on Anthropic's release cadence, not yours.
If those facts were scattered across eight check modules, the tool would be
wrong within a quarter and nobody would know which lines to update. Here,
refreshing is a diff to one file, and `KNOWLEDGE_AS_OF` gets printed in every
report so a reader can judge how much to trust it.

The core type:

```python
@dataclass(frozen=True)
class ModelInfo:
    id: str
    input_usd: float
    cache_min_tokens: int = 1024
    retires: date | None = None
    rejects_sampling_params: bool = False   # temperature/top_p/top_k -> 400
    rejects_budget_tokens: bool = False
    rejects_prefill: bool = False
    thinking_on_by_default: bool = False
    thinking_disable_max_effort: str | None = None
    ...
```

Those booleans are the trick. A check doesn't ask *"is this Opus 4.8 or newer?"*
— that would need updating every release. It asks
`if info.rejects_sampling_params`. When a new model ships, you add one row to
the table and every check that cares picks it up. **Capabilities as data, not
version comparisons in logic.**

Two methods deserve attention:

```python
def status_on(self, on: date) -> Status:
    if self.retires and on >= self.retires:
        return Status.RETIRED
    return self.status
```

Status is computed **relative to a date passed in**, never `date.today()` inside
the check. So the same model is `DEPRECATED` on 2026-07-01 and `RETIRED` on
2026-09-01, and the test suite can pin both without freezing the clock. (There's
a test that does exactly this.)

```python
def price(self, on: date) -> tuple[float, float]:
    if self.intro_until and on <= self.intro_until and self.intro_input_usd:
        return (self.intro_input_usd, self.intro_output_usd)
    return (self.input_usd, self.output_usd)
```

Same idea for introductory pricing that expires.

The odd-looking constant worth knowing about:

```python
cache_min_tokens: 512   on Opus 5 and Fable 5
                  1024  on Opus 4.8, Sonnet 5, Sonnet 4.6
                  2048  on Opus 4.7
                  4096  on Opus 4.6 and Haiku 4.5
```

**Not monotonic.** A 750-token prompt caches on Opus 5 and silently doesn't on
Opus 4.6 — no error, the marker is just accepted and ignored. That single
non-monotonic column is most of the justification for the tool existing, and
there's a test asserting both directions.

---

## `model.py` — the vocabulary

Pure data classes, no logic. This is the contract between layers.

**`Severity`** is an `IntEnum` so findings sort by it, and the comments define
the bands precisely enough to be usable:

```python
CRITICAL = 4  # The API rejects this. Requests fail today.
HIGH     = 3  # Silently wrong, silently expensive, or silently truncated.
MEDIUM   = 2  # Real cost or quality left on the table.
LOW      = 1  # Cleanup.
```

The `HIGH` definition is the one doing work. Everything in that band shares a
property — **no error is raised** — which is exactly why a human reviewer misses
it and a tool shouldn't.

**`Arg`** is the important one:

```python
@dataclass
class Arg:
    name: str
    raw: str          # the source text
    value: Any = None # the Python value, if we could work it out
    resolved: bool = False
    node: Any = None  # the AST node, for checks that inspect the expression
```

Three views of one argument, because different checks need different ones. The
cache-invalidator check needs `node` (it walks the expression looking for
`datetime.now()`). The model check needs `value`. The auto-fixer needs `raw` (to
confirm the literal is actually on that line before rewriting it).

`resolved` matters more than it looks: it separates *"we know this is wrong"*
from *"we couldn't see it."* Checks are required to stay silent on the second.

**`Fix`** carries `old` and `new` text plus a line, not a diff. `fix.py`
re-verifies `old` is still on that line before writing — so if the file changed
since analysis, the fix is skipped rather than applied to whatever's there now.

---

## `extract/` — source to facts

### `extract/__init__.py`

A `Protocol` and a lookup by file suffix. Twelve lines. Adding Go means writing
`extract/go.py` and adding it to the list; no check changes.

### `extract/python.py`

Two passes over the AST.

**Pass 1 — module-level constants.** Real code almost never inlines the model
ID; it's `MODEL = "claude-opus-5"` at the top and `model=MODEL` at the call. Without
this pass the tool sees nothing useful in a real repo.

The `_AMBIGUOUS` sentinel is the interesting bit:

```python
if target.id in self.consts and self.consts[target.id] != value:
    self.consts[target.id] = _AMBIGUOUS   # assigned twice, differently
```

If a name is assigned two different values, we **refuse to resolve it** rather
than pick one. A wrong resolution produces a confident finding about code that
doesn't exist, which is the worst output this tool can produce. There's a test
for it.

**Pass 2 — call sites.** Walk for `ast.Call` nodes whose attribute chain ends in
`create`/`stream`/`parse`/`count_tokens`/`tool_runner` *and* contains `messages`
or `batches`. That two-part condition avoids matching every `.create()` in the
codebase.

**`safe_eval` — the part I got wrong first.** The original used
`ast.literal_eval`, which is all-or-nothing. Real code writes:

```python
messages=[{"role": "user", "content": ticket}]   # `ticket` is a parameter
```

`literal_eval` fails on the whole list because one leaf is a variable — so the
prefill check, the tool checks, and everything else structural went blind. The
fixture run caught it.

`safe_eval` resolves **element-wise**, substituting an `UNRESOLVED` sentinel for
leaves it can't see:

```python
[{"role": "user", "content": UNRESOLVED}]
```

The dict resolves, `content` is marked unknown, and the prefill check can still
read `role`. It also handles `"a" + B` and `"x " * 900`, because prompts are
routinely built that way. There's a size guard so `"x" * 10**9` in a constant
can't blow up the analyser.

**Pass 3 — bare model IDs.** Any `claude-*` string *not* on a call-site line:
constants, config, registries, fixtures. Reported separately and never
auto-fixed, because a registry that legitimately *serves* an old model should
keep the ID — only the caller needs changing, and the tool can't tell which
you have.

### `extract/javascript.py`

Heuristic on purpose. A real TS parser (tree-sitter, or the TypeScript compiler)
would be more accurate but trades a stdlib-only tool for a build step.

It brace-matches the request object — skipping strings and comments, which is
the part naive regex gets wrong — and reads top-level literal keys. That covers
`model`, `max_tokens`, `temperature`, `stream`, `betas`.

It cannot see identifiers, spreads, or imported constants. That limitation is
stated in the module docstring, in the README, and **in every report's coverage
section**, because silently under-reporting on half a codebase is how a tool
gets trusted when it shouldn't be.

---

## `checks/` — facts to findings

### `checks/__init__.py`

A decorator registry:

```python
@check("MODEL_RETIRED", "models", "Model ID has been retired and returns 404")
def retired_models(ctx: Context) -> Iterable[Finding]:
    ...
```

Adding a check is adding a function. There's no dispatch table to edit, so two
people can add checks without conflicting. `--list-checks` reads the registry,
so the catalog can't drift from the code.

`Context` carries call sites, model refs, the file list, a cached `read()`, and
**`today`** — injected, never `date.today()` inside a check. That's what makes
the date-relative deprecation test possible.

The docstring states the rule the whole package follows:

> A check either proves a defect from the extracted facts, or it stays quiet.
> Anything requiring judgement belongs in the LLM pass — deterministic checks
> that guess produce confident nonsense, which is worse than silence.

### `checks/_common.py`

Readers: `model_of(site)`, `thinking_of(site)`, `effort_of(site)`,
`betas_of(site)`, `count_cache_breakpoints(site)`. Shared so a change in how
`betas` can be spelled (`betas=[...]` vs `extra_headers={"anthropic-beta": ...}`)
is fixed once.

`estimate_tokens` is `len(text) // 4` and its docstring says never to report the
number — it's only used to decide whether a prefix is *obviously* below a cache
minimum. The tool that flags you for estimating tokens badly shouldn't do it
either.

### `checks/models.py`

Retired, deprecated, unknown, `-fast` strings, dated pins, tier mismatch.

`MODEL_FAST_SUFFIX` distinguishes two failure modes, because they need different
urgency: `claude-opus-4-7-fast` errors (you find out immediately);
`claude-opus-4-6-fast` **silently falls back** to standard Opus 4.6 — no error,
you just stop getting fast mode and never learn. The second is more dangerous,
so it gets the louder writeup.

The fix-placement logic is subtle and worth reading:

```python
inline = model_id in _model_raw(ctx, location) if in_call else True
```

When the call says `model=LEGACY_MODEL`, there's no literal on that line to
rewrite. So the **call site** gets the CRITICAL finding (that's where the
breakage is) with no fix, and the **constant** gets a finding with the fix
attached (that's where the edit goes). Offering a fix the patcher can't apply is
a promise you break.

`MODEL_TIER_MISMATCH` is deliberately narrow: it only fires on
`max_tokens <= 512` with no tools and no thinking, which is unambiguously a
classification call. Every subtler over-tiering judgement is left to the LLM
pass. Its confidence is 0.55 and the remedy ends *"never downgrade without an
eval"* — a cost recommendation you can't verify is a trap.

### `checks/correctness.py`

The 400s: sampling parameters, `budget_tokens`, prefill, `output_format`,
disabled thinking above `high` effort, large `max_tokens` without streaming,
stale beta headers.

Two worth calling out.

**`PARAM_OUTPUT_FORMAT` has a carve-out.** `output_format` is deprecated on
`create()` but is a legitimate SDK convenience on `.parse()`. Flagging the
correct usage would train users to ignore the tool. There's a test pinning both
directions.

**`THINKING_DEFAULT_ON` is the subtlest check in the tool.** On Opus 5 and
Sonnet 5, omitting `thinking` runs adaptive thinking — the previous generation
ran without it. `max_tokens` caps thinking *plus* response text together. So a
budget sized around the answer alone now truncates mid-response, with no error.
Nothing in the diff looks wrong; the model string changed and the answer got cut
off. That's a HIGH: it's silent.

### `checks/caching.py`

`CACHE_BELOW_MINIMUM` is the check that most justifies the project. It's also
where model-specificity pays off — same code, different model, different
verdict, and a test asserts both.

`CACHE_INVALIDATOR` is the one that uses `Arg.node`, walking the system-prompt
expression for `datetime.now()`, `uuid4()`, `random`, or an f-string. It's a
prefix match: one changed byte invalidates everything after it, so a timestamp
in a system prompt is a permanent, silent, 10× cost bug.

Note the severity is conditional:

```python
severity=Severity.HIGH if has_cache_control(site) else Severity.MEDIUM
```

An invalidator with caching on is actively costing money now. Without caching
it's only blocking you from turning caching on later. Different urgency, so
different band.

### `checks/tools.py`

`TOOL_EDITOR_PAIR` is the highest-value check per line of code. The `type` and
`name` fields of the text-editor tool are a matched pair; bumping the version
and leaving `name` alone is a 400, and it's the single most common migration
slip. Eight lines, CRITICAL, zero false positives.

`TOOL_DESCRIPTION_THIN` only flags what's *provable* — missing, or under 25
characters. Whether a description is any **good** is the LLM pass's job. That
line is drawn deliberately and is the same line drawn everywhere else.

### `checks/resilience.py`

`REFUSAL_UNHANDLED` had a bug the fixture run caught: it originally checked
whether *any* file in the repo mentioned `stop_reason`, so one well-written
module suppressed the finding for every badly-written one next to it. Now it
groups by file. **Repo-level checks are usually per-file checks in disguise.**

The finding text explains *why* it matters rather than citing a rule: a refusal
is a successful HTTP 200 with an empty `content` array, so `content[0].text`
raises `IndexError`. That's the difference between a finding someone acts on and
one they dismiss.

### `checks/evals.py`

`EVAL_NONE` is HIGH, and the wording is doing deliberate work:

> Every recommendation in this report — switch models, lower effort, shorten the
> prompt — is unverifiable without one, which means none of them can be taken
> safely.

It grades three states: no tests, tests that **only mock** the model (they
verify you built the request you meant to build — they cannot tell you the
answer got worse), and real evals.

This check also had a bug the fixture run caught: it treated anything under
`tests/` as a test, so the fixture files counted as evals and suppressed the
finding. Fixed by requiring an actual assertion keyword. **A file under `tests/`
that never asserts is a fixture, not a test.**

---

## `llm.py` — judgement, one call

Everything above is deterministic. This handles what no rule can decide.

The request deliberately uses every feature the checks look for, so the tool is
its own first patient: current model ID, adaptive thinking, prompt caching,
structured outputs, streaming, refusal handling, server-side fallbacks.

**`RUBRIC` is a module-level constant** — and there's a comment saying why:

```python
# Kept as a module-level constant on purpose: this is the cached prefix. Any
# per-run value interpolated in here would invalidate the cache on every call —
# the exact defect CACHE_INVALIDATOR reports.
```

The prompt's most important instruction is negative:

> DO NOT REPORT ANY OF THE ABOVE. Repeating a mechanical finding is worse than
> silence: it makes the report longer without making it more useful, and it
> trains the reader to skim.

Without it you get a duplicate of the static analysis in worse prose. It also
explicitly authorises an empty answer — *"An empty list is a valid and
respectable answer"* — because otherwise a model asked to review will find
something.

The response handling checks `stop_reason` **before** touching `content`, which
is precisely what `REFUSAL_UNHANDLED` flags in other people's code.

`review()` never raises. A judgement-pass failure degrades the report to the
deterministic findings; it doesn't fail the run.

---

## `agent.py` — judgement, as a loop

`llm.py` assembles the payload up front because we know what the reviewer needs.
This is what you build when you don't.

The reviewer gets `grep` and `read_file` and decides for itself: it sees
`handle_tool_call(...)` referenced in the file it's reading and goes to read the
handler, to check whether a tool's implementation matches the description it
advertises. **You cannot assemble that payload in advance**, because which file
matters depends on what the model finds. That's the whole difference between a
workflow and an agent.

Written as a hand-rolled loop rather than the SDK's tool runner because the loop
is the thing worth reading. In production, use `client.beta.messages.tool_runner`.

Five things the loop gets right, each of which is a real bug if you get it
wrong:

1. **Append the assistant turn before running tools.** The `tool_use` blocks
   live in that message; a `tool_result` whose `tool_use` is missing from the
   history is rejected.
2. **`pause_turn` continues without injecting a message.** The API sees the
   pending block and resumes itself. Adding "please continue" corrupts the turn.
3. **All results go back in ONE user message.** Splitting them silently trains
   the model to stop making parallel tool calls.
4. **Tool errors are returned, not raised.** `is_error: true` and the message
   text. The model recovers from a bad path far more reliably than your retry
   logic will.
5. **The loop is bounded.** `MAX_ITERATIONS = 14`. An unbounded agent loop is
   how an agent deployment becomes a billing incident.

`submit_findings` is a **tool**, not a structured-output constraint. Forcing a
JSON schema on the response would conflict with tool calling; making the verdict
itself a tool gives a clean termination signal — the loop ends when it's called.

Context management is real, not decorative:

```python
context_management={"edits": [{"type": "clear_tool_uses_20250919"}]}
```

Without it, turn 12 re-sends every file read on turn 2 and input tokens grow
quadratically.

**`Workspace` treats every model-supplied path as untrusted input.** It resolves
and confirms the result is still inside the root *and* in the scanned file set,
so a prompt injection in a reviewed file can't turn `read_file` into an
arbitrary-file-read primitive. Tests cover `../`, absolute paths, and in-root
files that aren't in scope.

---

## `report.py`, `fix.py`, `cli.py`

**`report.py`** renders markdown / JSON / terminal. Scoring starts each dimension
at 100 and subtracts by severity (critical 40, high 20, medium 8, low 2) — crude
but monotonic and explainable, which is what a scorecard needs.

`_coverage()` is the part I'd defend hardest. It states what *wasn't* analysed:
how many model IDs couldn't be resolved, that JS/TS was read heuristically, that
runtime behaviour isn't covered. Its docstring:

> A report that hides its blind spots reads as a clean bill of health, which is
> worse than no report.

**`fix.py`** applies only mechanical substitutions — model IDs and tool version
strings. It re-verifies the expected text is still on the line before writing,
and applies edits in **descending line order** so earlier edits don't shift later
ones. Anything needing a judgement call (*which* effort level replaces this
`budget_tokens`?) is reported and left alone.

**`cli.py`** wires it together. `--fail-on high` by default, so it drops into CI
as-is: exit 1 when something at or above that severity is found.

---

## Testing

42 tests, no network. The interesting ones:

- **`test_ambiguous_constant_is_not_resolved`** — pins the refusal to guess.
- **`test_deprecated_status_is_date_relative`** — same code, two dates, two
  verdicts. Possible only because `today` is injected.
- **`test_cache_below_minimum_is_model_specific`** — same prompt, two models,
  opposite results.
- **`test_healthy_fixture_has_no_critical_or_high_findings`** — the false-positive
  guard. A linter that can't be satisfied gets turned off.
- **`test_retired_model_via_constant_reports_at_call_site_but_fixes_at_the_constant`**
  — pins the fix-placement contract.

`tests/test_agent.py` drives the loop with a **stub client**, so it runs offline
and deterministically. That's also the answer to *"how do you test an agent?"*:
you don't assert on the model's choices. You assert the harness around them is
correct — results paired to their `tool_use` blocks, errors handed back rather
than raised, the sandbox holding, the loop terminating.
