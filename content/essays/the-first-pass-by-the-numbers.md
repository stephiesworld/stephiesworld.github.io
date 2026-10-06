---
title: "The first pass, by the numbers"
date: "2026-07-11"
order: 2
category: "Field guides"
dek: "What an AI first pass does to 10,000 pieces of customer feedback, what the model should and shouldn't touch, and the job that's left for people."
---

When people hear "AI triages customer feedback," they tend to picture one of two things: a toy that writes summaries nobody reads, or a machine that replaces the operations team. In practice it's a compression story, and that's easiest to see with numbers.

Say a company receives 10,000 pieces of feedback in a week: support tickets, sales-call transcripts, Slack threads, community posts, early-access notes, telemetry flags. The job of a first pass is to turn that pile into a small, structured set of issues, each with its evidence attached, that people can judge. [Cherry](https://cherry-topaz.vercel.app), my triage tool, is built around this. The eight-stage pipeline on its homepage is this essay as a diagram.

## What the model should and shouldn't touch

A useful first pass divides the labor strictly. Ordinary software retrieves and calculates: ticket counts, customer counts, revenue on the affected accounts, dates, plan tiers, existing ticket IDs, who owns which product area. The model interprets: what the customer was trying to do, what went wrong, whether two complaints share a cause, which evidence is representative, who should own the fix.

My rule is that the model never invents what a database can answer. When a cluster says "47 reports across 29 accounts," those numbers came from queries. The model's contribution is the claim that those 47 reports describe the same underlying problem.

That claim is where the interesting failures live, and there are two, pulling in opposite directions.

**Missed duplicates** are the obvious one. "Loses track of instructions in long sessions," "my configuration rules disappear," "it stops following our conventions halfway through": five phrasings, one issue. Semantic clustering catches most of these.

**False duplicates** are harder to spot. Take five complaints that all say the product "forgets." One user expected memory that was never saved. One admin's configured policy isn't applying. One is a context-length limit. One is a real bug. One is a gap in product education. Bad synthesis merges them into one big cluster called "the product forgets things," which sounds organized and is useless: five causes, five owners, no single fix. Good synthesis separates them by cause. This is why the first pass needs evals and human correction. Tidy-sounding output can still be clustered wrong.

Before creating anything, the first pass also has to **check what already exists.** Does this issue already have a ticket? Did leadership rule it an intentional tradeoff in March? Is engineering already investigating? A first pass that skips this step becomes a ticket-duplication machine, producing more of the noise it was built to reduce.

## The economics

Run the funnel on those 10,000 records. Perhaps 1,500 contain nothing actionable and 3,000 are near-duplicates. The rest condense into a couple hundred candidate clusters. Most merge into known issues, a few dozen are genuinely new, a small number get routed with high confidence, an ambiguous handful go to human review, and a few are escalated right away. People read the escalations, the ambiguous clusters, samples from the high-volume ones, and every low-confidence call closely. They audit everything else.

<svg viewBox="0 0 680 470" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A funnel: 10,000 raw records shrink to 8,500 with substance, 5,500 after deduplication, about 180 candidate clusters, about 40 new issues, and roughly 18 items a human deeply reads · 15 ambiguous clusters plus 3 escalations." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <style>
    .fn-n{font:700 13px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .fn-nw{font:700 13px "IBM Plex Mono",ui-monospace,monospace;fill:#fff;}
    .fn-l{font:400 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#444;}
    .fn-s{font:400 9px "IBM Plex Mono",ui-monospace,monospace;fill:#888;}
  </style>
  <rect x="20" y="16" width="640" height="50" rx="5" fill="#f3f3f3" stroke="#000" stroke-width="1.2"/>
  <text x="340" y="38" text-anchor="middle" class="fn-n">10,000</text>
  <text x="340" y="54" text-anchor="middle" class="fn-l">raw records · one week, every channel</text>
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
  <text x="20" y="426" class="fn-s">Bar widths are compressed · drawn to true scale, the bottom rows would be invisible, which is the point.</text>
  <text x="20" y="440" class="fn-s">Everything outside the red band gets sampled and audited rather than read.</text>
</svg>

That's the trade. Human attention goes where judgment changes the outcome. The team stops reading every submission and starts auditing samples and hard cases, and spends its time deciding what counts as signal. The first pass compresses the analyst layer; the judgment stays with people.

What happens to people's corrections after that, and how they're measured and folded back in, is its own essay: [an opinion with edit access](/writing/why-the-human-stays-in-the-loop).

## The job that's left

So does the first pass replace the operations team? It automates the part of the job that's mostly reading, tagging, and copying between systems. It also creates a harder and more interesting job: defining what quality means, building the evals that keep the system honest, and tracking whether any of this changes what gets built. A system can do analyst-scale first-pass work all day. Someone still has to be responsible for whether it's doing it *well*, and for what happens next.
