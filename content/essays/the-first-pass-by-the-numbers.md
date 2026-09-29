---
title: "The first pass, by the numbers"
date: "2026-07-11"
order: 2
category: "Customer feedback, at scale"
---

When people hear "AI triages customer feedback," they tend to imagine one of two things: a toy that writes summaries nobody reads, or a machine that replaces the operations team. In practice it's a compression story, and that's easiest to see with numbers.

Suppose a company receives 10,000 pieces of feedback in a week — support tickets, sales-call transcripts, Slack threads, community posts, early-access notes, telemetry flags. The job of a first pass is turning that pile of records into a small, structured, evidence-attached set of issues that humans can judge. [Cherry](https://cherry-topaz.vercel.app), my triage tool, is built around this; the eight-stage pipeline on its homepage is this essay in diagram form.

## What the machine should and shouldn't touch

A useful first pass divides labor strictly. Ordinary software retrieves and calculates: ticket counts, customer counts, revenue on the affected accounts, dates, plan tiers, existing ticket IDs, who owns which product area. The model interprets: what the customer was trying to do, what actually went wrong, whether two complaints share a mechanism, which evidence is representative, who should own the fix. My rule is that the model should never invent what a database can answer. When a cluster says "47 reports across 29 independent accounts," those numbers came from joins; the model's contribution is the claim that those 47 reports describe the same underlying thing.

That claim is where the interesting failures live, and there are two of them, pulling in opposite directions.

**Missed duplicates** are the obvious one: "loses track of instructions in long sessions," "my configuration rules disappear," "it stops following our conventions halfway through" — five phrasings, one issue. Semantic clustering catches most of this.

**False duplication** is harder to spot. Take five complaints that all mention the product "forgetting": one is a user expecting memory that was never saved, one is an admin whose configured policy isn't applying, one is a context-length limitation, one is a genuine bug, one is a product-education gap. Bad synthesis merges them into a giant cluster called "the product forgets things" — which sounds organized and is useless, because it has five different mechanisms, five different owners, and no single fix. Good synthesis separates them by mechanism and use case. This is why the first pass needs evals and human correction, since tidy-sounding output can still be clustered wrong.

Before anything gets created, the first pass also has to **check what already exists.** Does this issue have a ticket? Did leadership already rule it an intentional tradeoff in March? Is engineering mid-investigation? A first pass that skips this step becomes a ticket-duplication machine, producing more of the noise it was built to reduce.

## The economics

Run the funnel on those 10,000 records: perhaps 1,500 contain no actionable feedback, 3,000 are near-duplicates, and the remaining substance condenses into a couple hundred candidate clusters — most merging into known issues, a few dozen genuinely new, a small number routed with high confidence, an ambiguous handful sent to human review, and a few escalated immediately. The humans deeply read the escalations, the ambiguous clusters, samples from the high-volume ones, and every low-confidence call, and they audit everything else.

<svg viewBox="0 0 680 470" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A funnel: 10,000 raw records shrink to 8,500 with substance, 5,500 after deduplication, about 180 candidate clusters, about 40 new issues, and roughly 18 items a human deeply reads — 15 ambiguous clusters plus 3 escalations." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <style>
    .fn-n{font:700 13px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .fn-nw{font:700 13px "IBM Plex Mono",ui-monospace,monospace;fill:#fff;}
    .fn-l{font:400 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#444;}
    .fn-s{font:400 9px "IBM Plex Mono",ui-monospace,monospace;fill:#888;}
  </style>
  <rect x="20" y="16" width="640" height="50" rx="5" fill="#f3f3f3" stroke="#000" stroke-width="1.2"/>
  <text x="340" y="38" text-anchor="middle" class="fn-n">10,000</text>
  <text x="340" y="54" text-anchor="middle" class="fn-l">raw records — one week, every channel</text>
  <line x1="340" y1="66" x2="340" y2="82" stroke="#000" stroke-width="1.1"/>
  <text x="354" y="78" class="fn-s">− 1,500 with nothing actionable</text>
  <rect x="70" y="82" width="540" height="50" rx="5" fill="#eceae6" stroke="#000" stroke-width="1.2"/>
  <text x="340" y="104" text-anchor="middle" class="fn-n">~8,500</text>
  <text x="340" y="120" text-anchor="middle" class="fn-l">contain something actionable</text>
  <line x1="340" y1="132" x2="340" y2="148" stroke="#000" stroke-width="1.1"/>
  <text x="354" y="144" class="fn-s">− 3,000 near-duplicates collapse</text>
  <rect x="125" y="148" width="430" height="50" rx="5" fill="#e2dfda" stroke="#000" stroke-width="1.2"/>
  <text x="340" y="170" text-anchor="middle" class="fn-n">~5,500</text>
  <text x="340" y="186" text-anchor="middle" class="fn-l">substantive, after dedupe</text>
  <line x1="340" y1="198" x2="340" y2="214" stroke="#000" stroke-width="1.1"/>
  <text x="354" y="210" class="fn-s">semantic clustering, evidence attached</text>
  <rect x="220" y="214" width="240" height="50" rx="5" fill="#d3d0ca" stroke="#000" stroke-width="1.2"/>
  <text x="340" y="236" text-anchor="middle" class="fn-n">~180</text>
  <text x="340" y="252" text-anchor="middle" class="fn-l">candidate clusters</text>
  <line x1="340" y1="264" x2="340" y2="280" stroke="#000" stroke-width="1.1"/>
  <text x="354" y="276" class="fn-s">120 attach to existing work instead</text>
  <rect x="265" y="280" width="150" height="50" rx="5" fill="#c2beb7" stroke="#000" stroke-width="1.2"/>
  <text x="340" y="302" text-anchor="middle" class="fn-n">~40</text>
  <text x="340" y="318" text-anchor="middle" class="fn-l">genuinely new issues</text>
  <line x1="340" y1="330" x2="340" y2="346" stroke="#000" stroke-width="1.1"/>
  <text x="354" y="342" class="fn-s">25 route with high confidence</text>
  <rect x="294" y="346" width="92" height="50" rx="5" fill="#B01E36" stroke="#000" stroke-width="1.2"/>
  <text x="340" y="376" text-anchor="middle" class="fn-nw">~18</text>
  <text x="400" y="368" class="fn-n" fill="#B01E36">deeply read by humans</text>
  <text x="400" y="384" class="fn-l">15 ambiguous clusters + 3 escalations</text>
  <text x="20" y="426" class="fn-s">Bar widths are compressed — drawn to true scale, the bottom rows would be invisible, which is the point.</text>
  <text x="20" y="440" class="fn-s">Everything outside the red band gets sampled and audited rather than read.</text>
</svg>

That's the trade. Human attention goes to the places where judgment changes the outcome. The team goes from reading every submission to auditing samples and hard cases, and spends its time deciding what counts as signal. The first pass compresses the analyst layer, and the judgment stays with people.

What happens to the humans' corrections after that — how they're measured and folded back in — is its own essay: [an opinion with edit access](/writing/why-the-human-stays-in-the-loop).

## The job that remains

So does the first pass replace the operations function? It automates the portion dominated by reading, tagging, and copying between systems. It also creates a harder and more interesting job: defining what quality means, building the evals that keep the machine honest, and tracking whether any of this changes what gets built. A system can do analyst-scale first-pass work all day, but someone still has to be responsible for whether it's doing it *well*, and for what happens next.
