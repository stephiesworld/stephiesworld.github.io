---
title: "The cheap, fast way to make a million decisions"
date: "2026-10-01"
order: 11
category: "AI & the enterprise"
---

Most of the AI work inside a company is small decisions made over and over: which team gets this ticket, is this invoice a duplicate, is this lead worth a call. Jev, a new model from TypeSafe, is built only for those decisions, and it makes them much faster and cheaper than an LLM.

## What Jev is

Jev reads a piece of text and answers a set of multiple-choice questions about it, with how confident it is in each answer.

You write the questions ahead of time. For a support email, they might be: Is this urgent? (yes / no) Which team? (billing / tech / sales) Churn risk? (low / medium / high). Jev reads the email and returns every answer at once, like "urgent: yes, 91%."

It can't write, chat, or explain itself. It's still a trained language model, so it understands messy, casual writing the way an LLM does. It just answers in checkboxes instead of sentences.

## How it fits

![Jev sorts every message and hands off only what needs more](../images/writing/jev-flow.svg)

Jev sits at the front and makes the quick call on everything that comes in. Confident answers trigger an action right away, an LLM only gets involved when something needs to be written, and a person only sees the cases Jev is unsure about.

## Customer-facing use cases

These are places where a customer is waiting, so speed matters as much as cost.

| Use case | What Jev decides | Why speed or cost matters |
| --- | --- | --- |
| Support ticket routing | Urgency, team, product area, churn risk | Every ticket gets sorted the second it arrives |
| Chatbot and agent routing | Which tool or workflow a message needs next | The bot can answer fast and only call a big model when it has to |
| Fraud and risk checks | Whether an order, signup, or message looks suspicious | Has to happen during checkout without slowing it down |
| Content moderation | Whether a post, review, or listing breaks specific rules | Runs on every post, so cost per check adds up fast |
| Lead qualification | Fit, intent, budget range from a form or first email | Hot leads get routed to sales right away |
| Search and recommendations | Which results or products match what someone asked for | Scoring hundreds of options per search is only practical if each check is cheap |

The pattern is the same in each: Jev makes the call instantly, and a person or a larger model only steps in when Jev isn't sure.

## Internal use cases

Inside a company, nobody is waiting on a reply, so the win here is mostly cost and volume. These are jobs people do by hand today, or skip because there's too much to get through.

| Use case | What Jev decides | Who it helps |
| --- | --- | --- |
| Invoice and expense review | Category, duplicate or not, needs approval or not | Finance |
| Contract review | Whether a contract has certain clauses, like auto-renewal or a liability cap | Legal |
| Resume screening | Whether an application meets a fixed list of must-haves | Recruiting |
| Account health | Whether a customer's notes, emails, or usage point to risk or expansion | Customer success |
| Inbox and request triage | Which team or person an internal request belongs to | Operations, IT, HR |
| Data cleanup | Whether records match, are duplicates, or are missing key details | Data and ops teams |
| Grading AI outputs | Whether another model's answer is accurate, on-brand, or safe | Teams running AI products |

The last one is worth calling out. Companies that use LLMs need to check thousands of their outputs. Jev is cheap enough to check every one of them instead of a small sample.

## Cost and speed

Jev is cheaper and faster because it skips the two most expensive things an LLM does. It doesn't write its answer one piece at a time, and it doesn't think out loud before answering. It reads the input once and answers every question in a single pass.

Here's a rough example: a company sorting 1 million support tickets a month, about 1,000 tokens each, so 1 billion tokens of input.

|  | Jev | LLMs |
| --- | --- | --- |
| Price per million input tokens | $0.042 | about $0.20–$10 |
| Input cost for 1 billion tokens | $42 | about $200–$10,000 |
| Output and reasoning tokens | Free | Charged on top |
| Time per answer | 70–500 milliseconds | Seconds, up to minutes for reasoning models |

These prices and times come from TypeSafe's launch post. Their own tests put Jev at about 190x faster and 440x cheaper than frontier models, and they say real results will likely be lower than that.

## Where it doesn't fit

- **Anything that needs writing.** Replies, summaries, and reports still need an LLM.
- **High-stakes calls.** Jev's accuracy is mid-tier. On TypeSafe's benchmark it agrees with two large models about 68% of the time. It's best for screening and sorting, with people reviewing the unsure cases.
- **Long documents.** Input caps at about 32,000 tokens, so a long contract goes in by section.
- **Unproven claims.** The speed and cost numbers are self-reported, and independent testing is still thin.

## How to start

Pick one high-volume decision your team already makes by hand, like ticket routing. Run Jev on a few hundred past examples and compare its answers with what people decided. If it holds up, set a confidence cutoff: above it, Jev acts on its own, and below it, a person reviews.

Jev is available through TypeSafe's API, Vercel AI Gateway, and Cloudflare Workers AI. Open-source versions like open-alternative-jev also exist for teams that want to run it on their own servers.

## Sources

- [TypeSafe: Introducing System One models and Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- [Awesome Jev (community list, access options)](https://github.com/kraayenjon/awesome-jev/wiki)
- [open-alternative-jev on GitHub](https://github.com/ikermoel/open-alternative-jev)
