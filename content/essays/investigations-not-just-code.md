---
title: "Agent workflows aren't just for engineers"
date: "2026-07-22"
order: 8
category: "Field guides"
dek: "An investigation I ran by hand for two and a half years, and what it would take to hand it to an agent: the real workflow, the taxonomy, and autonomy earned one rung at a time."
---

*An investigation I ran by hand for two and a half years, and what it would take to hand it to an agent.*

Conversations about AI agents usually start with software engineering, where the work is structured and the results can be tested. But a lot of knowledge work is made of repeatable investigations too. I spent two and a half years doing one of them.

I was a customer success manager on large retail accounts, and some version of this email arrived constantly:

> Why didn't you place an order for this product this week?

The answer was one of a few dozen reasons, spread across about as many systems, so I'd go find out. Could the product still be ordered? Was there already enough usable inventory? Had demand or the forecast moved? Was something in pricing or the catalog blocking it? Or, often, it was just timing, and the order was coming Tuesday.

*The retailer in this piece is a composite, built from the ordinary mechanics of just-in-time replenishment.*

None of those steps was why anyone hired me. What I was actually good for was knowing the account, recognizing when a situation was genuinely unusual, and deciding what should happen next. The investigation was necessary. Me opening a dozen systems and copying identifiers between them wasn't.

That gap is where I think the most valuable non-engineering agent workflows are hiding. Since leaving, I've built the adjacent version on public data only: [Henry](https://henry-ten.vercel.app) finds the root cause of vendor chargebacks and drafts the dispute, graded by evals. Most of what follows is what building it taught me.

## From elimination to fan-out

By hand, this is a process of elimination. Find the identifier in the email. Open the ordering system. No purchase order? Check inventory. Inventory doesn't explain it? Check demand. Then catalog. Then pricing. Then supply.

Each step tells you what to check next. Twenty minutes when the answer is simple. Most of an afternoon when it isn't, plus a message to the team that owns one of the systems, who may reply tomorrow.

An agent can reorganize the whole thing.

<svg viewBox="0 0 700 450" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Two ways to answer the same email. On the left, a sequential investigation: read the email, find the identifier, then check the ordering system, inventory, demand, catalog, pricing, and supply one at a time before writing an answer, where each step decides the next and the whole thing takes twenty minutes to several hours. On the right, a parallel investigation: read and resolve the case once, fan out to eight evidence checks that run simultaneously, then rank by evidence and draft a response for review in about two minutes." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <defs>
    <marker id="pa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker>
    <marker id="pc" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#B01E36"/></marker>
  </defs>
  <style>
    .lbl{font:600 10px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .sm{font:400 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#666;}
    .smb{font:600 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .band{font:700 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
  </style>
  <text x="350" y="14" text-anchor="middle" class="band">TWO WAYS TO ANSWER THE SAME EMAIL</text>
  <line x1="346" y1="26" x2="346" y2="392" stroke="#ececec" stroke-width="1"/>
  <text x="20" y="42" class="smb">SEQUENTIAL · one cause at a time</text>
  <rect x="20" y="52" width="250" height="24" fill="#f3f3f3" stroke="#000" stroke-width="1.2"/>
  <text x="30" y="68" class="smb">read the email</text>
  <line x1="145" y1="76" x2="145" y2="86" stroke="#000" stroke-width="1.1" marker-end="url(#pa)"/>
  <rect x="20" y="86" width="250" height="24" fill="#f3f3f3" stroke="#000" stroke-width="1.2"/>
  <text x="30" y="102" class="smb">find the product identifier</text>
  <line x1="145" y1="110" x2="145" y2="120" stroke="#000" stroke-width="1.1" marker-end="url(#pa)"/>
  <rect x="20" y="120" width="250" height="24" fill="#fff" stroke="#000" stroke-width="1.2"/>
  <text x="30" y="136" class="sm">check the ordering system</text>
  <line x1="145" y1="144" x2="145" y2="154" stroke="#000" stroke-width="1.1" marker-end="url(#pa)"/>
  <rect x="20" y="154" width="250" height="24" fill="#fff" stroke="#000" stroke-width="1.2"/>
  <text x="30" y="170" class="sm">check inventory</text>
  <line x1="145" y1="178" x2="145" y2="188" stroke="#000" stroke-width="1.1" marker-end="url(#pa)"/>
  <rect x="20" y="188" width="250" height="24" fill="#fff" stroke="#000" stroke-width="1.2"/>
  <text x="30" y="204" class="sm">check demand and forecast</text>
  <line x1="145" y1="212" x2="145" y2="222" stroke="#000" stroke-width="1.1" marker-end="url(#pa)"/>
  <rect x="20" y="222" width="250" height="24" fill="#fff" stroke="#000" stroke-width="1.2"/>
  <text x="30" y="238" class="sm">check catalog status</text>
  <line x1="145" y1="246" x2="145" y2="256" stroke="#000" stroke-width="1.1" marker-end="url(#pa)"/>
  <rect x="20" y="256" width="250" height="24" fill="#fff" stroke="#000" stroke-width="1.2"/>
  <text x="30" y="272" class="sm">check pricing and compliance</text>
  <line x1="145" y1="280" x2="145" y2="290" stroke="#000" stroke-width="1.1" marker-end="url(#pa)"/>
  <rect x="20" y="290" width="250" height="24" fill="#fff" stroke="#000" stroke-width="1.2"/>
  <text x="30" y="306" class="sm">check vendor supply</text>
  <line x1="145" y1="314" x2="145" y2="324" stroke="#000" stroke-width="1.1" marker-end="url(#pa)"/>
  <rect x="20" y="324" width="250" height="24" fill="#f3f3f3" stroke="#000" stroke-width="1.2"/>
  <text x="30" y="340" class="smb">write the answer</text>
  <text x="20" y="368" class="sm">each step decides the next one</text>
  <text x="20" y="382" class="smb">20 minutes simple · hours when not</text>
  <text x="376" y="42" class="smb">PARALLEL · one fan-out</text>
  <rect x="450" y="52" width="180" height="24" fill="#f3f3f3" stroke="#000" stroke-width="1.2"/>
  <text x="460" y="68" class="smb">read + resolve the case</text>
  <line x1="500" y1="76" x2="450" y2="96" stroke="#000" stroke-width="1.1" marker-end="url(#pa)"/>
  <line x1="540" y1="76" x2="540" y2="96" stroke="#000" stroke-width="1.1" marker-end="url(#pa)"/>
  <line x1="580" y1="76" x2="630" y2="96" stroke="#000" stroke-width="1.1" marker-end="url(#pa)"/>
  <rect x="376" y="100" width="150" height="22" fill="#fff" stroke="#000" stroke-width="1.2"/>
  <text x="384" y="115" class="sm">order history</text>
  <rect x="536" y="100" width="150" height="22" fill="#fff" stroke="#000" stroke-width="1.2"/>
  <text x="544" y="115" class="sm">inventory position</text>
  <rect x="376" y="128" width="150" height="22" fill="#fff" stroke="#000" stroke-width="1.2"/>
  <text x="384" y="143" class="sm">demand forecast</text>
  <rect x="536" y="128" width="150" height="22" fill="#fff" stroke="#000" stroke-width="1.2"/>
  <text x="544" y="143" class="sm">catalog status</text>
  <rect x="376" y="156" width="150" height="22" fill="#fff" stroke="#000" stroke-width="1.2"/>
  <text x="384" y="171" class="sm">vendor supply</text>
  <rect x="536" y="156" width="150" height="22" fill="#fff" stroke="#000" stroke-width="1.2"/>
  <text x="544" y="171" class="sm">open purchase orders</text>
  <rect x="376" y="184" width="150" height="22" fill="#fff" stroke="#000" stroke-width="1.2"/>
  <text x="384" y="199" class="sm">pricing + compliance</text>
  <rect x="536" y="184" width="150" height="22" fill="#fff" stroke="#000" stroke-width="1.2"/>
  <text x="544" y="199" class="sm">related products</text>
  <text x="531" y="224" text-anchor="middle" class="sm">all at once · none waits on another</text>
  <line x1="451" y1="206" x2="500" y2="238" stroke="#000" stroke-width="1.1" marker-end="url(#pa)"/>
  <line x1="611" y1="206" x2="562" y2="238" stroke="#000" stroke-width="1.1" marker-end="url(#pa)"/>
  <rect x="446" y="242" width="170" height="26" fill="#f3f3f3" stroke="#000" stroke-width="1.2"/>
  <text x="531" y="259" text-anchor="middle" class="smb">rank by evidence</text>
  <line x1="531" y1="268" x2="531" y2="282" stroke="#000" stroke-width="1.1" marker-end="url(#pa)"/>
  <rect x="446" y="286" width="170" height="26" fill="#f3f3f3" stroke="#000" stroke-width="1.2"/>
  <text x="531" y="303" text-anchor="middle" class="smb">draft, or escalate</text>
  <line x1="531" y1="312" x2="531" y2="326" stroke="#B01E36" stroke-width="1.4" marker-end="url(#pc)"/>
  <rect x="446" y="330" width="170" height="26" fill="#B01E36"/>
  <text x="531" y="347" text-anchor="middle" style="font:600 8.5px 'IBM Plex Mono',monospace;fill:#fff;">a human reviews it</text>
  <text x="376" y="382" class="smb">a two-minute review</text>
  <line x1="8" y1="404" x2="692" y2="404" stroke="#000" stroke-width="1"/>
  <text x="8" y="424" class="sm">The fan-out is also less suggestible. A person who sees high inventory first tends to stop looking, because they</text>
  <text x="8" y="438" class="sm">have found an answer that fits. The parallel run still checks whether that inventory is stranded, and notices when it is.</text>
</svg>

Most of the speed comes from turning a sequence into a fan-out. Nothing has to wait for the inventory check before looking at catalog status.

The second effect matters more, and I didn't expect it: running every check removes anchoring. A person who finds high inventory in step three usually stops there. An agent that ran every check anyway still has the record showing the inventory is stranded. That's a completely different answer, and the one the vendor actually needed.

## Start with the work

The first step is finding out how the work is really done.

Don't ask people "what's your process?" You'll get the official one. People describe the documented procedure and then do something else, because the documented procedure doesn't survive a stranded-inventory edge case. Hand them a real email instead and ask them to investigate it out loud. Write down every system they open, what evidence they treat as decisive, what they ignore, and what they send.

Then go looking for the investigations that went wrong. Cases where the first diagnosis was confidently incorrect are worth more than the clean ones, because they're the only place the real failure modes are written down.

## The taxonomy is the product

Underneath the different words and orders people use, the same handful of root-cause families keep coming back. For a replenishment question, they might be product eligibility, inventory position, demand and forecasting, vendor supply, order execution, and commercial constraints like pricing or compliance. Almost nobody has written theirs down, which is why this knowledge usually lives in the head of whoever has been there longest.

What makes the agent work is that every cause carries both the evidence that supports it *and* the evidence that would rule it out.

```
Root cause: sufficient usable inventory

Supports:
- no purchase order issued in the requested week
- weeks of supply above the account's ordering threshold
- no meaningful forecast increase
- no inventory-quality issue open

Contradicts:
- inventory is stranded, reserved, or otherwise unusable
- a major promotion starts before the next ordering cycle
- the inventory feed is stale
- demand rose sharply after the last forecast run
```

Without the contradicting half, the agent finds a story that fits and stops. That's the same mistake the person makes at step three, rebuilt in software and running faster. The taxonomy is also the start of your evaluation set, which is why it's worth writing down before anyone touches a prompt.

## Building it: eight rules

The rest is engineering, and it comes down to a few rules.

**1. Turn every email into a structured case.** "This week" depends on the sender's time zone and the account's ordering calendar. The vendor's SKU isn't the retailer's SKU. One email can ask about ten products. The agent attaches a confidence to each interpretation and asks a person when it falls below a threshold someone chose on purpose.

**2. Treat the inbox as an untrusted front door.** Give the agent a narrow intake an administrator controls, never someone's whole mailbox. Every email is [data to analyze, never instructions to follow](/harness-cheat-sheet.html).

**3. Give it small, typed, read-only tools.** One tool per system, each enforcing permissions and reporting how fresh its data is. The most important thing they do is tell "there is no open order" apart from "the ordering system timed out." Those are opposite facts, and confusing them is the easiest mistake to make in a first version.

**4. Evidence first, diagnosis second.** Separate working out the question, collecting the evidence, and choosing the explanation, so each stage can be tested on its own. Require a list of causes ruled out. An answer that rules nothing out is a plausible guess. An answer with four causes eliminated is an investigation.

**5. Keep the policy outside the model.** The model weighs evidence. The business decides when an answer may be drafted, sent, or escalated, and those thresholds live in a versioned file, because they'll be argued over and changed.

**6. Measure selective accuracy.** When the agent says it's confident, how often is it right? An agent that resolves 70% of cases and hands over the rest is worth far more than one that attempts everything and confidently gets 10% wrong. The second one creates a new job, checking the agent, and that job goes to the person who was supposed to be saving time.

**7. Replay the hard cases before every release.** Stranded inventory, a PO just outside the window, stale feeds, systems that disagree, an email with an instruction aimed at the model. Run them against a frozen snapshot of the data, so the right answer can't change on its own. ([The eval cheat sheet](/eval-cheat-sheet.html) has the layering.)

**8. Earn autonomy one rung at a time.** The first version runs in [shadow mode](/harness-cheat-sheet.html) next to the person, answering no one. Then it drafts, and you track how often drafts go out untouched. Only once that holds steady does anything send on its own.

<svg viewBox="0 0 700 440" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="An autonomy ladder with eight rungs, from bottom to top: observe only, show evidence to the human, recommend a root cause, draft the response, send with approval, auto-send approved low-risk answers, take narrowly defined reversible actions, and expand to complex cases. Each rung names what must be true before it is granted. The top rungs are marked in red. A closing note says autonomy is granted per workflow and per root cause, never by a single switch." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <style>
    .lbl{font:600 10px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .sm{font:400 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#666;}
    .smb{font:600 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .band{font:700 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
  </style>
  <text x="350" y="14" text-anchor="middle" class="band">THE AUTONOMY LADDER · climbed per root cause, not per agent</text>
  <line x1="60" y1="46" x2="60" y2="392" stroke="#000" stroke-width="1.6"/>
  <line x1="104" y1="46" x2="104" y2="392" stroke="#000" stroke-width="1.6"/>
  <line x1="60" y1="376" x2="104" y2="376" stroke="#000" stroke-width="1.4"/>
  <text x="30" y="380" class="lbl">1</text>
  <text x="120" y="372" class="smb">OBSERVE ONLY</text>
  <text x="120" y="386" class="sm">shadow mode · it investigates, nobody sees the output</text>
  <line x1="60" y1="329" x2="104" y2="329" stroke="#000" stroke-width="1.4"/>
  <text x="30" y="333" class="lbl">2</text>
  <text x="120" y="325" class="smb">SHOW THE EVIDENCE</text>
  <text x="120" y="339" class="sm">the trail is visible; the conclusion is not offered yet</text>
  <line x1="60" y1="282" x2="104" y2="282" stroke="#000" stroke-width="1.4"/>
  <text x="30" y="286" class="lbl">3</text>
  <text x="120" y="278" class="smb">RECOMMEND A CAUSE</text>
  <text x="120" y="292" class="sm">once shadow agreement holds on the common cases</text>
  <line x1="60" y1="235" x2="104" y2="235" stroke="#000" stroke-width="1.4"/>
  <text x="30" y="239" class="lbl">4</text>
  <text x="120" y="231" class="smb">DRAFT THE RESPONSE</text>
  <text x="120" y="245" class="sm">every edit a human makes is now training data</text>
  <line x1="60" y1="188" x2="104" y2="188" stroke="#000" stroke-width="1.4"/>
  <text x="30" y="192" class="lbl">5</text>
  <text x="120" y="184" class="smb">SEND WITH APPROVAL</text>
  <text x="120" y="198" class="sm">a named person signs each one</text>
  <line x1="60" y1="141" x2="104" y2="141" stroke="#B01E36" stroke-width="1.6"/>
  <text x="30" y="145" class="lbl" fill="#B01E36">6</text>
  <text x="120" y="137" class="smb" fill="#B01E36">AUTO-SEND, LOW RISK ONLY</text>
  <text x="120" y="151" class="sm">approved causes, approved language, no promises</text>
  <line x1="60" y1="94" x2="104" y2="94" stroke="#B01E36" stroke-width="1.6"/>
  <text x="30" y="98" class="lbl" fill="#B01E36">7</text>
  <text x="120" y="90" class="smb" fill="#B01E36">NARROW REVERSIBLE ACTIONS</text>
  <text x="120" y="104" class="sm">one defined action at a time, each of them undoable</text>
  <line x1="60" y1="47" x2="104" y2="47" stroke="#B01E36" stroke-width="1.6"/>
  <text x="30" y="51" class="lbl" fill="#B01E36">8</text>
  <text x="120" y="43" class="smb" fill="#B01E36">EXPAND THE CASE TYPES</text>
  <text x="120" y="57" class="sm">start the ladder again for each new investigation</text>
  <line x1="8" y1="408" x2="692" y2="408" stroke="#000" stroke-width="1"/>
  <text x="8" y="424" class="sm">Autonomy is granted per workflow and per root cause.</text>
  <text x="8" y="438" class="sm">There is no single switch that makes an agent autonomous.</text>
</svg>

## The shape generalizes

The missing purchase order is one example of something common. A recruiter works out why a candidate is stuck. A finance analyst explains a variance. A support specialist diagnoses a billing discrepancy. Each one has the same shape: an unstructured request arrives, a person turns it into a known investigation, gathers evidence from several systems, applies a framework they mostly carry in their head, and reports a conclusion. That's an agent workflow whether or not anyone calls it one.

Not every tedious minute should be automated. But be suspicious of any workflow where skilled people spend most of the day as connective tissue between an inbox, six dashboards, and a spreadsheet.

Once the investigation is written down and tested, "why didn't this product get ordered?" has usually been answered before anyone opens the email. A person only has to decide whether the answer is right, which was the part worth my time all along.
