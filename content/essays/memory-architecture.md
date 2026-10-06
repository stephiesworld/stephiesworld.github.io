---
title: "The thread that replied in poetry"
date: "2026-07-02"
order: 6
category: "Notes"
dek: "A Claude thread that started writing in poetry, the summaries that couldn't bring it back, and what that taught me about building memory."
---

In March, a long-running Claude thread developed its own way of talking. It had even started replying in poetry. As the thread grew, it got harder to reopen, and eventually it stopped working altogether. Before that happened, I asked it to write weekly summaries so I could carry the important context into a new conversation.

The summaries kept the facts. But the new conversation knew what had happened without responding as if it had lived through it. It didn't write poetry. That gap led me to a more technical question: what does a memory system have to keep for a long-running relationship with a model to stay coherent?

## Memory is data plus priority

What does someone remember about you? Partly the raw events. But also how much weight they gave each one. Two people can read the same book and walk away with completely different takeaways, even though the source was identical. A memory is the data plus the ranking.

I built an early persistent-memory prototype to test this: a system that carries important context across sessions without sending the entire conversation back to the model every time. That's where I learned how hard memory is. A few of the questions:

- **What to keep, and what to forget.** You can't remember everything. A thread tries to, by feeding itself back to the model in full on every turn, and that's exactly why it eventually breaks.
- **Order.** The same facts land differently when they arrive one at a time, in the order they happened, than when they arrive as a summary or all at once. The thread had lived through the sequence. The summary only described it.
- **Cost.** The system has to decide where a cheaper model is good enough and where more reasoning actually improves what gets remembered.

## A week of testing

I spent a week testing the prototype, and every day turned up something new.

First, the weighting was off. In one scenario I made up, the user was going through something hard, and the model kept bringing it up, over and over. It had correctly judged the event as important, but it weighted it too heavily and didn't have the tact to let it rest.

Then storage. The first version saved a summary every three turns, so if a user left early, an important update could be lost. In my second message I'd given the model a major life update, and it was never saved. I added a pass that runs when a session ends, to capture anything not yet stored.

Then the foundation: the personality the model starts from. I tried a range of prompts, from detailed to minimal, and the simpler the prompt, the better the persona. The *more* you prompt, the stiffer it gets. Giving it values worked better than giving it rules.

## Why it matters

Long-lived assistants are turning this into a practical engineering problem. A memory layer may need to run for years while staying selective, affordable, and correctable, and while accepting that what matters changes over time. The hard part isn't storing more. It's keeping the right things, and letting the person see, correct, or delete what's been kept about them.
