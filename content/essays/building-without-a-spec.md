---
title: "Building without a finished spec"
date: "2026-07-11"
order: 5
category: "Building with AI"
---

I didn't build [Cherry](https://cherry-topaz.vercel.app) from a product requirements document or a finished spec. I had a problem I couldn't stop thinking about — companies drown in customer feedback — and a blank Claude Code session. I began with the problem, used the model to explore possible structures, and iterated until the specification emerged from the work. I started with conversation because I didn't know what to build yet.

## The spec emerged through building

The clean story of software goes: think first, specify second, implement third. Some work happens that way. Zero-to-one work mostly doesn't, because when the problem is new, building the solution is how you learn what the problem contains.

Cherry began as "collect and summarize customer feedback." That framing collapsed within days. The model could summarize well enough; I just had no way of knowing whether to trust it. It could hand me five beautifully written themes, each with a persuasive explanation, and the fluency told me nothing about whether those themes were real, representative, distinct, or worth acting on. Every product question that ended up mattering came out of that gap. Should severity and reach be one score? (No — a problem can be devastating for a small group without being widespread.) And what happens after an issue is identified — because a feedback system that produces a beautiful dashboard nobody owns is a museum of customer frustration.

None of that was in my head on day one. It emerged through a loop: I'd bring an unfinished thought, Claude would propose an approach, I'd probe it, and somewhere in the probing I'd discover I had been asking the wrong question. Revise, implement a piece, watch what happened, find the next question. The specification exists now, and it came out of the building.

## Judgment moves up the stack

There's a recurring anxiety about AI-assisted creation: if the model generated much of the code, who really built the product? I understand the question, but I think it defines "building" too narrowly.

Someone still has to decide which problem is worth solving, which user the system serves, what output is misleading, which tradeoffs are acceptable, where a human must remain involved, what "good" means, and when the thing is finished enough to put in front of someone. If anything, the model makes those decisions more important, because when implementation gets fast, it gets much easier to build the wrong thing well. A feature can feel inevitable simply because it was easy to generate. The discipline I've had to develop is asking, over and over, whether this is real functionality or product theater.

## Propose and decide

Working this way often felt like working with a cofounder — someone I could bring a half-formed thought at any hour, who could hold the entire evolving system in context while we examined one tiny decision. The word overreaches, though, because a cofounder owns outcomes. Claude doesn't wake up worried we chose the wrong customer, and it can't take responsibility for what ships. Thought partner is more accurate. It proposed, and I decided.

The work is mine because I made the judgment calls and took responsibility for the result. I chose the problem, kept asking the questions, rejected the ideas that felt impressive but hollow, and answered for what shipped.

## Why I work this way

Arriving with a finished spec would have meant the model happily building my first idea, the summarization framing, which sounded plausible and wasn't enough. Starting with the problem instead keeps me honest about what I don't know yet, and it keeps me open to better questions and better ways of working while the discernment stays my job.

It has made me faster, and more curious. The unfinished space between an important problem and a product worth making is the most interesting place I've ever worked, and I think deciding what's worth making should stay a human job.

*How this philosophy shows up inside the product itself is its own essay: [why the human stays in the loop](/writing/why-the-human-stays-in-the-loop).*
