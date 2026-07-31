# RAG, in plain language

Written for someone who keeps hearing "RAG" and wants to know when they'd
actually need one.

---

## What it is

**Search your documents. Paste the results into the prompt. Ask the question.**

That's it. "Retrieval-augmented generation" = retrieve, then generate.

There is no magic in the middle. If you've ever pasted a page from a manual into
a chat before asking about it, you've done RAG by hand. A RAG system just does
the pasting for you.

## Try it

```bash
python -m doctor.cli --search "why is my prompt not caching" -k 3
```

```
29 chunk(s) indexed from corpus/ · query: "why is my prompt not caching"

Top 3 of 3 requested:

1. [ 5.46] prompt-caching.md:20 (Prompt caching › Minimum cacheable prefix)
        matched: caching, not, prompt
2. [ 4.19] prompt-caching.md:3 (Prompt caching › What caching does)
        matched: caching, prompt
3. [ 3.37] prompt-caching.md:47 (Prompt caching › Verifying it works)
        matched: caching, prompt
```

Add `--show` to see the full text of each result — that text is exactly what
would get pasted into the prompt.

## The only question that matters

**Does the knowledge fit in the prompt?**

If yes: stop. Put it in the prompt and cache it. You don't need retrieval, and
building it anyway means maintaining a search system that makes your answers
worse.

That's the actual situation in this tool. `knowledge.py` — every model ID,
price, and retirement date — is a few hundred lines. It fits. So the analyser
does not use this package at all.

You need retrieval when one of these is true:

- **Too big to fit.** Millions of documents, a whole wiki, years of tickets.
- **Changes constantly.** Today's prices, this morning's incident log.
- **Per-user or permissioned.** You can't put every customer's data in one
  prompt; you fetch only what *this* person is allowed to see.
- **You need citations.** Easier when you know which passages you injected.
- **Cost.** Re-sending 500,000 tokens on every question is real money.

## The four rungs

You've seen three of these already if you've read the rest of this repo:

| Approach | Use when | Where it appears |
|---|---|---|
| Put it in the prompt | Fits, and always relevant | The rubric in `llm.py` |
| Load on demand | Fits, but only sometimes relevant | Skills — one line resident, full text loaded when needed |
| Give the model a search tool | Too big; model picks what to read | `agent.py` — `grep` + `read_file` |
| **RAG** | Too big; *you* pick before the call | This package |

The difference between the last two is who decides. That's the whole
distinction, and it's worth being able to say out loud.

## Two ways to search

### Keyword (`keyword.py`) — start here

Ranks documents by shared words, with two sensible adjustments: rare words count
for more than common ones, and repeating a word helps with diminishing returns.

This is BM25, the algorithm search engines used for decades. It is unfashionable
and it is very often correct, because **for technical docs the words in the
question are the words in the document.** No API key, no network, no cost.

### Meaning-based (`embedding.py`) — only when you can prove you need it

Turns each passage into a list of numbers representing what it's *about*, and
returns the passages whose numbers point in a similar direction to the question.
Because it compares meaning rather than spelling, "how do I cancel" can find a
page titled "ending your subscription."

Costs one API call per passage to build, plus one per question, plus storage.

**Do not start here.** "We used embeddings because that's what RAG means" is how
teams end up maintaining a vector database that performs worse than `grep`.

## Where keyword search actually breaks

Not hypothetical — this is real output from the corpus in this repo:

```
$ python -m doctor.cli --search "my bill went up after upgrading" -k 3

1. [ 3.82] breaking-changes.md (Beta headers that went GA)
        matched: went
2. [ 3.71] prompt-caching.md (The prefix rule)
        matched: after
```

The question is really about the cache-minimum trap — a prompt that cached on
one model silently stops caching on another. The corpus contains the answer.

Keyword search matched on **"went"** and **"after"**. Filler words. It returned
unrelated sections with confident-looking scores.

**That is the case that justifies embeddings**, and it's the only honest way to
decide: find real questions where the cheap method fails, then upgrade. There's
a test pinning this exact failure (`test_paraphrased_question_retrieves_junk`),
so it can't quietly change.

## "What should k be?"

`k` is just **how many results to take**. The problem is you pick it *before* you
know how much the question needs.

- Too small → the answer is missing, and the model answers confidently anyway.
- Too large → the good result drowns in noise, and you pay for the extra.

**How to actually decide:** write down ~20 real questions where you know the
right answer. Run them at k=3, 5, 10, 20. Check two things — did the right
passage show up at all, and how much junk came with it. Pick the smallest k
where accuracy stops improving.

Rough starting points:

| Question shape | k |
|---|---|
| One specific fact | 3–5 |
| Compare or summarize across sources | 10–20 |
| You don't know in advance | Don't pick — see below |

**Two ways to stop guessing:**

1. **Over-fetch, then filter.** Grab 20, run a cheap pass that discards the
   irrelevant ones, keep what survives. `overfetch_and_filter()` in
   `embedding.py` does this — the judge is injected, so you can start with a
   plain rule and upgrade to a small model call later.
2. **Let the model search.** Give it search as a tool. It searches, reads, and
   searches again if that wasn't enough. `k` stops being a number you pick.

**The best answer to "what k?" is usually "don't have a k."**

## The mistake that ruins most RAG systems

Chunking. Chopping documents into equal-sized blocks is the fast thing to write
and it quietly poisons everything downstream, because a passage stripped of its
context can be retrieved for a question it has nothing to do with.

> The minimum is 4096 tokens.

Which model? The heading said, and the heading is gone. Retrieval returns this
for a question about a completely different model, and the answer reads as
authoritative.

`corpus.py` splits on **headings**, and every chunk carries the trail of headings
above it. Long sections split further but keep the same trail, with a little
overlap so a fact sitting on the seam survives whole in at least one piece.

```
[prompt-caching.md · Prompt caching › Minimum cacheable prefix]
A prompt shorter than the model's minimum is not cached at all...
```

Now the passage can't be misread, and the model can cite where it came from.

## When retrieval is the wrong tool entirely

If your data is **structured** — customers, orders, prices, dates — query it.
Write SQL. Don't embed a database and hope similarity search reconstructs a
`WHERE` clause. Vector search is for unstructured text, and reaching for it
because it's the fashionable option is how you get a system that can't answer
"how many orders shipped last Tuesday."

## Debugging: it's almost always retrieval

When a RAG system gives a bad answer, the instinct is to blame the model or
rewrite the prompt. Usually the model answered correctly using bad source
material.

**Check what was retrieved first.** That's why every result here prints its
score and which words matched, and why `--show` prints the full passage. If the
right passage isn't in the results, no amount of prompting fixes it.

## What to say in an interview

> "First I'd check whether the knowledge fits in context — if it does, RAG is
> premature. If it doesn't, I'd ask whether one search can answer the question
> or whether it needs several. Single-hop over a static corpus, classic RAG is
> fine and cheaper. Multi-hop or exploratory, I'd give the model a search tool
> and let it iterate. And if the data is structured, I'd query it directly
> rather than embedding it."

That's stronger than describing a vector pipeline, because it shows you know
when *not* to build one.
