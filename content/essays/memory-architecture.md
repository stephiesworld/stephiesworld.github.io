---
title: "The thread that replied in poetry"
date: "2026-07-02"
order: 6
category: "Building with AI"
---

In March, a long-running Claude thread developed a distinctive conversational style. As the thread grew, it became increasingly difficult to reopen and was eventually unusable. Before that happened, I asked it to produce weekly summaries so I could carry the important context into a new conversation.

The summaries preserved the facts, but the new conversation knew what had happened without responding as though it had lived through the sequence. The original thread had even developed a habit of replying in poetry — a small example of behavior that factual summaries failed to reproduce. That gap led me to a more technical question: what must a memory system retain for a long-running interaction to remain coherent?

What is in a memory? What does someone remember about you? It's the memories and experiences as raw data, and also the priority and ranking a human (or a model in a thread) attributes to each one. Take two people reading the same book: each walks away with their own takeaways, even though the source data is identical.

I built an early persistent-memory prototype designed to preserve important context across sessions without repeatedly sending the entire conversation back to the model. That's where I learned just how hard memory is. How do you rank what to remember? What to forget? (You can't remember everything — which is exactly what a thread does when it feeds itself back to the LLM in full, every single time.) What role does in-real-time reactivity play — otherwise known as relational context? What about linearity — being fed each datapoint one at a time, versus summarized, or even the exact same data delivered all at once? It all factors into memory.

There's also the tradeoff between cost and accuracy: the architecture has to determine where lower-cost models are sufficient and where additional reasoning materially improves memory quality.

I spent a week testing it, and every day I ran into something new to think about. First, the weighting on what mattered was clearly off. I made up a scenario where a user was going through something negative, and the model kept asking about that experience over and over — correctly weighting its importance, but too heavily, and lacking the EQ not to bring it up countless times. Then there was a storage issue: the first version summarized on a three-turn cadence, which meant a user could leave before an important update was stored — in my second reply I'd given the model a major life update, and it was never saved. I added an exit-triggered pass so the system would capture unsaved context when a session ended.

And then there's the foundation of it all: the root personality the model starts with. I tried a bunch, ranging from complex to simple, and I realized that the simpler the prompt, the better the persona. The *more* you prompt, the more rigid and stiff it becomes. It was better to give it values than strict guidelines on how to behave.

Long-lived assistants make this an increasingly practical systems problem. A memory layer may need to operate for years while remaining selective, affordable, correctable, and sensitive to the fact that importance changes over time. The difficult question is how to preserve the right context, and how to let the user inspect, correct, or forget it.
