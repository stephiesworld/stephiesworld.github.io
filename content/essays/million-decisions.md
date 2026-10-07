---
title: "The cheap, fast way to make a million decisions"
date: "2026-10-01"
order: 11
category: "Field guides"
dek: "Most AI work inside a company is small decisions made over and over. Splitting deciding from writing, with a cheap classifier at the front, changes the math."
---

When I was a customer success manager, most of my decisions were small. Which team owns this? Is it the same issue as last week? Is it urgent? None took long. There were just a lot of them.

Most AI work inside a company looks like that. And a lot of companies send every one of those decisions to their most expensive model, then pay for it to write a paragraph explaining what was really a checkbox.

## Split deciding from writing

In my own builds, I split the work by what each part is good at. In [Henry](https://henry-ten.vercel.app), the model handles language and plain code does the math. The same idea applies here: deciding and writing are different jobs, and they don't need the same tool.

A new kind of model makes that split cheap. TypeSafe's Jev only makes decisions. You give it a piece of text and a set of multiple-choice questions (Urgent? Which team? Churn risk?), and it answers all of them at once, each with a confidence, like "urgent: yes, 91%." It can't write or chat. It just answers in checkboxes.

![Jev sorts every message and hands off only what needs more](../images/writing/jev-flow.svg)

The classifier sorts everything that comes in. Confident answers trigger an action right away. A larger model is only called when something needs writing, and a person only sees the cases it isn't sure about.

## Why it matters

By TypeSafe's own numbers, sorting a million support tickets a month would cost about $42 in input with Jev, against roughly $200 to $10,000 with general-purpose models, with answers in under a second. They say real-world results will likely be lower, so treat those as numbers to test, not facts.

The point holds either way. A task worth automating happens a million times, so the cost of each decision is what decides whether automating it makes sense.

## Where I'd use it, and where I wouldn't

It fits decisions with a fixed set of answers, made at high volume: routing tickets, flagging at-risk accounts, catching duplicate invoices, cleaning up records, and grading other models' outputs, so you can check every one instead of a sample.

It doesn't fit anything that needs writing, high-stakes calls (on TypeSafe's own benchmark it agrees with large models about 68% of the time), or long documents.

## How I'd test it

Pick one decision your team already makes by hand. Run the classifier on a few hundred past cases and compare its answers with what people decided. Check how often it's right when it says it's confident. If that holds up, let it act above a confidence cutoff and send everything below to a person.

## Sources

- [TypeSafe: Introducing System One models and Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- [Awesome Jev (community list, access options)](https://github.com/kraayenjon/awesome-jev/wiki)
- [open-alternative-jev on GitHub](https://github.com/ikermoel/open-alternative-jev)
