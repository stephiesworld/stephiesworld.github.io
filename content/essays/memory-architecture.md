---
title: "The thread that replied in poetry"
date: "2026-07-02"
order: 4
category: "Notes"
dek: "A Claude thread that started writing in poetry, the summaries that couldn't bring it back, and what that taught me about building memory."
---

In March, a long-running Claude thread started replying in poetry. As the thread grew, it got harder to open, and eventually it stopped working. Before it did, I had it write weekly summaries so I could carry the context into a new conversation.

The new conversation knew everything that had happened. It just didn't sound like it had been there. It didn't write poetry.

That's when I realized a memory is more than the facts. Two people can read the same book and remember completely different things, because each one decided what mattered. A memory is the data plus the ranking.

So I built a small memory prototype and tested it for a week. Three things went wrong, and each one taught me something:

- **It remembered too hard.** In one test, the user was going through something difficult, and the model kept bringing it up. It was right that it mattered. It just didn't know when to let it rest.
- **It forgot the important thing.** It saved a summary every three turns, so when I shared a big life update and left early, it was never saved. I added a final save when a session ends.
- **More instructions made it worse.** The simpler the starting prompt, the better the personality. Giving it values worked better than giving it rules.

Assistants that run for years will need memory that is selective, affordable, and correctable. The hard part isn't storing more. It's keeping the right things, and letting the person see, fix, or delete what's been kept about them.
