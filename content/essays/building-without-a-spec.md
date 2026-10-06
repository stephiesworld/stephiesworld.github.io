---
title: "Building without a finished spec"
date: "2026-07-11"
order: 5
category: "Notes"
dek: "I built Cherry without a spec. The spec came out of the building, and the judgment calls stayed mine."
---

I didn't build [Cherry](https://cherry-topaz.vercel.app) from a requirements document or a finished spec. I had a problem I couldn't stop thinking about, companies drowning in customer feedback, and a blank Claude Code session. I started with the problem, used the model to explore possible structures, and kept going until the spec emerged from the work. I started with conversation because I didn't know yet what to build.

## The spec came out of the building

The clean story of software goes: think first, specify second, build third. Some work happens that way. New work mostly doesn't, because when the problem is new, building is how you learn what the problem contains.

Cherry started as "collect and summarize customer feedback." That framing fell apart within days. The model could summarize well enough. I just had no way to know whether to trust it. It could hand me five well-written themes, each with a persuasive explanation, and the polish told me nothing about whether those themes were real, representative, distinct, or worth acting on.

Every product question that ended up mattering came out of that gap. Should severity and reach be one score? (No. A problem can be devastating for a small group without being widespread.) What happens after an issue is identified? A feedback system that produces a beautiful dashboard nobody owns is a museum of customer frustration.

None of that was in my head on day one. It came out of a loop: I'd bring an unfinished thought, Claude would propose an approach, I'd push on it, and somewhere in the pushing I'd realize I'd been asking the wrong question. Revise, build a piece, watch what happened, find the next question. The spec exists now, and it came out of the building.

## Judgment moves up the stack

There's a common worry about building with AI: if the model wrote much of the code, who really built the product? I understand the question, but I think it defines "building" too narrowly.

Someone still has to decide which problem is worth solving, which user the system serves, what output would mislead, which tradeoffs are acceptable, where a person has to stay involved, what "good" means, and when it's ready to put in front of someone. If anything, the model makes those decisions more important. When building gets fast, it gets much easier to build the wrong thing well. A feature can feel inevitable just because it was easy to generate. The discipline I've had to develop is asking, over and over, whether something is real functionality or product theater.

## It proposed, I decided

Working this way often felt like working with a cofounder: someone I could bring a half-formed thought to at any hour, who could hold the whole evolving system in mind while we looked at one small decision. But the word overreaches, because a cofounder owns outcomes. Claude doesn't wake up worried we picked the wrong customer, and it can't take responsibility for what ships. Thought partner is more accurate. It proposed, and I decided.

The work is mine because I made the judgment calls and answered for the result. I chose the problem, kept asking questions, rejected ideas that sounded impressive but were hollow, and stood behind what shipped.

## Why I work this way

If I'd arrived with a finished spec, the model would have happily built my first idea, the summarization framing, which sounded plausible and wasn't enough. Starting with the problem keeps me honest about what I don't know yet. It keeps me open to better questions, while the judgment stays my job.

It has made me faster, and more curious. The unfinished space between an important problem and a product worth making is the most interesting place I've worked, and I think deciding what's worth making should stay a human job.

*How this shows up inside the product itself is its own essay: [an opinion with edit access](/writing/why-the-human-stays-in-the-loop).*
