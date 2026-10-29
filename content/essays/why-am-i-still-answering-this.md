---
title: "Why am I still the one answering this?"
date: "2026-10-27"
order: 2
category: "Notes"
dek: "Two and a half years with some of Amazon's biggest vendors, the same questions on repeat, and why I built Henry to answer them once, for everyone."
---

Before Amazon, I had always been on the building side. I researched customers through data, never across a table. Even when I ran my own company and did every job, I spent most of my time on R&D and partnerships.

In 2024 I wanted to sit across the table. So I spent two and a half years at Amazon working with large retail vendors, as many of them as I could get. I wanted breadth more than depth with any one company, because the industry turned out not to matter. Sponges, beans, computers, data center shelves. What mattered was who led the company, how the org actually worked, who made the decision (often three different people), what the growth plan was, where it hurt, and which strengths were going unused.

## The same questions, on repeat

Most of what vendors asked me had an answer somewhere. Public guidance, Vendor Central, an internal wiki, an SOP, or the head of someone three teams over. In a company that big, knowledge lives in endless documents and just as often in people's memory, passed peer to peer. Half the work is finding the person who can point you in the right direction.

The vendors weren't short on intelligence. They were buried in fragmented information. What they needed was synthesis: one clear answer, from the right source, applied to their business.

After I'd given the same handful of answers enough times, the question changed. It stopped being *what's the answer?* and became *why am I still the one answering this, and what would it take to build something that answers it once, for everyone?*

That's the question that turns a job into a product.

## Less of me was the point

As the repeat questions got easier to resolve, our meetings got shorter and more focused. That was the evidence it was working: less time hunting for information, more time on decisions that actually needed both of us in the room. Over time the vendors needed me less, and that was the point.

The relationship still mattered. It's how I learned what a vendor was afraid of, what their leadership valued, and which constraints were shaping a decision. No dashboard tells you that. The goal was never to take the people out. It was to stop spending people on research a machine could do.

## So I built Henry

The weekend after I left Amazon, I built [Henry](https://henry-ten.vercel.app): Helpful Expert, Navigating Retail Yield. Public data only, nothing confidential. It's the one-stop shop I kept wishing those vendors had. It handles everyday P&L tasks, maps the competitive landscape including pricing, shows where margin goes, and helps with supply chain. It also finds the root cause of a chargeback and drafts the dispute, graded by evals.

This is the kind of problem AI is good at. Take a mountain of scattered information and make it conversational, because if it's conversational, it's easier to digest. The part that took real thought was deciding what the model should never touch. In Henry, the margin math is plain code. A number a vendor carries into a pricing meeting has to be right every time.

What's left for people is the good part: judgment, growth, and the problems that genuinely need another person.

## The loop

That's the work I want to keep doing. Get close enough to a problem to understand it from the inside, notice the question that keeps coming back, and build the thing that answers it for everyone who has it.

Henry is [live](https://henry-ten.vercel.app), and the [code is public](https://github.com/stephiesworld/henry).
