# The agent loop, in about 40 lines

Written for the question *"if agentic workflows are chained prompts, why don't I
chain anything when I talk to Claude Code?"*

The short answer: **the chaining moved into the harness.** You still have a
chain. You just aren't writing it, because it's generic — the loop doesn't need
to know whether it's building a linter or renaming a variable.

---

## The loop

This is the whole thing. Everything else a coding agent does is tools, prompt,
and plumbing around this.

```python
messages = [{"role": "user", "content": user_request}]

while True:
    response = client.messages.create(
        model="claude-opus-5",
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        tools=TOOLS,
        messages=messages,
    )

    # 1. Record the assistant turn BEFORE running anything. The tool_use blocks
    #    live in this message; a tool_result whose tool_use is missing from the
    #    history is rejected.
    messages.append({"role": "assistant", "content": response.content})

    # 2. Claude is done talking and didn't ask for anything. Exit.
    if response.stop_reason == "end_turn":
        break

    # 3. A server-side tool hit its internal iteration limit mid-turn. Re-send
    #    to resume. Do NOT append "continue" — the API sees the pending block.
    if response.stop_reason == "pause_turn":
        continue

    # 4. Run every tool Claude asked for. One assistant turn can contain
    #    several tool_use blocks; they're independent, so run them together.
    tool_results = []
    for block in response.content:
        if block.type != "tool_use":
            continue
        try:
            output = TOOLS_BY_NAME[block.name](**block.input)
            is_error = False
        except Exception as exc:
            # Hand the error back as a result. The model recovers from a bad
            # path far more reliably than your retry logic will.
            output, is_error = f"error: {exc}", True

        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,     # must match the tool_use block
            "content": output,
            "is_error": is_error,
        })

    # 5. ALL results go back in ONE user message. Splitting them across several
    #    messages silently trains the model to stop making parallel tool calls.
    messages.append({"role": "user", "content": tool_results})
```

That's it. Twelve turns of a coding agent — read a file, run the tests, see the
failure, edit, re-run — is this loop going round twelve times. Nobody wrote
"read the file" and "run the tests" as separate prompts, because **which twelve
steps happen isn't known until they happen.**

A live version with real tools is in [`../doctor/agent.py`](../doctor/agent.py).

## The one thing to add before production

The loop above runs forever if the model keeps calling tools. Bound it:

```python
for iteration in range(MAX_ITERATIONS):
    ...
else:
    raise RuntimeError("agent did not converge")
```

An unbounded agent loop is the single most common way an agent deployment turns
into a billing incident.

---

## Why this replaces prompt chaining

Prompt chaining is a workaround for two missing primitives.

| Missing primitive | What you do instead | What replaces it |
|---|---|---|
| The model can't act | You move data between steps by hand: extract → summarize → classify, three calls, you piping strings | **Tool use.** The model acts and sees the result. |
| Step 3 can't see step 1 | You compress and hand off explicitly at each boundary | **Long context.** A 1M-token window holds the whole session. |

Take both away and the decomposition happens *at runtime, chosen by the model*
rather than *at design time, fixed by you*.

**This does not make chaining obsolete.** It relocates the decision:

| | Chained prompts (workflow) | Agentic loop |
|---|---|---|
| Who picks the next step | You, at design time | The model, at runtime |
| Shape of the work | Known in advance | Discovered while working |
| Testing | Easy — each stage is a unit | Hard — you test outcomes, not steps |
| Cost / latency | Predictable | Variable, usually higher |
| Debugging | Read the DAG | Read the transcript |
| Failure mode | Wrong DAG, silently | Wanders, loops, over-explores |

**Use a workflow when you can name the steps. Use a loop when you can't.** Most
good systems are a workflow with one or two agentic steps inside it.

This repository is deliberately both, which makes it a usable interview example:

- `doctor/checks/` — ~25 deterministic checks. No model, no tokens, perfectly
  reproducible. The steps are known: parse, walk, compare against a table.
- `doctor/llm.py` — one model call. Still not a loop, because we already know
  which files matter, so the payload can be assembled up front.
- `doctor/agent.py` — a real loop, because the reviewer decides what to read
  next. It can follow a prompt constant into another module, or read a tool's
  handler to check the implementation matches the description it advertises.
  You cannot assemble *that* payload in advance.

The tell for which one you need: **can you write down the list of steps before
you start?** If yes, a loop is an expensive way to get a worse-tested version of
a workflow.

---

## #4 — Context management

The API is stateless. Every call re-sends the entire conversation. Turn 20
re-sends turns 1–19, including that 4,000-line file read on turn 3 that stopped
mattering on turn 5.

Two consequences: input tokens grow **quadratically** over a session, and
eventually the window fills. Three mechanisms, all used by real harnesses:

**Prompt caching.** The unchanged prefix bills at roughly 10%. Caching is a
*prefix match*, so ordering is the whole game: `tools` → `system` → `messages`.
Put stable content first, volatile content after the last breakpoint. One
changed byte anywhere in the prefix invalidates everything after it — which is
why a `datetime.now()` in a system prompt is a silent, permanent cost bug, and
why `agent.py` keeps its system prompt as a module-level constant.

**Context editing.** Delete stale tool results outright. In `agent.py`:

```python
context_management={"edits": [{"type": "clear_tool_uses_20250919"}]}
```

**Compaction.** Summarize old history server-side when you approach the window.
Distinct from editing: editing *deletes*, compaction *summarizes*.

Rule of thumb: editing for tool-heavy loops (most of the bulk is stale tool
output), compaction for long conversations (the history itself matters).

---

## #5 — Progressive disclosure

You have far more instructions than you want resident in context, and most are
irrelevant to any given task.

So you keep a **one-line description** of each chunk in the system prompt, and
load the full text only when a task turns out to need it. That's what a *skill*
is: a folder with a `SKILL.md`, whose description sits in context permanently
and whose body is read on demand.

This is not hypothetical for this repository. Building it went:

1. One line about a Claude-API reference skill sat in the system prompt.
2. The task — "write checks about model IDs, pricing, and which parameters
   return a 400" — matched it.
3. The harness loaded roughly 40,000 tokens of API reference.
4. Every model ID, price, cache minimum, and retirement date in
   [`../doctor/knowledge.py`](../doctor/knowledge.py) came from that document.

Which is the honest reason `knowledge.py` is a separate module with a
`KNOWLEDGE_AS_OF` date at the top: those facts are the part that rots, and a
tool that hardcodes them across eight check modules is wrong within a quarter.

Progressive disclosure is also the answer to "won't a huge tool library blow up
my context?" — tool search defers tool definitions the same way, loading schemas
only when a request looks relevant. Note it *appends* rather than swapping, so
the cached prefix survives; swapping the tool list mid-conversation would
invalidate everything, because tools render at position 0.

---

## What to say in the interview

If asked to design an agentic system, the strong answer isn't "use an agent."
It's:

1. **Name the tier.** Single call → workflow → agent. Justify picking the
   simplest one that works, because each step up costs latency, money, and
   testability.
2. **Show the loop.** It's ~40 lines and most people can't write it. Knowing
   that `tool_result` goes back in one user message, and that the assistant turn
   is appended before tools run, signals you've built one rather than read about
   one.
3. **Bound it.** Max iterations, and a token budget. Unbounded loops are how
   agent deployments become billing incidents.
4. **Say how you'd test it.** This is where most answers collapse. You cannot
   unit-test a loop that chooses its own steps — you test *outcomes* against a
   graded set, not steps. Which is why `EVAL_NONE` is a HIGH-severity finding in
   this tool: without an eval, every other recommendation it makes is
   unverifiable.
5. **Name the failure modes.** Wanders, over-explores, loops, over-verifies,
   silently truncates on `max_tokens`, treats a refusal as a successful empty
   response.
