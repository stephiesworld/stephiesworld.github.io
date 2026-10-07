---
title: "The first pass, by the numbers"
date: "2026-07-11"
order: 2
category: "Field guides"
dek: "What an AI first pass does to 10,000 pieces of customer feedback, what the model should and shouldn't touch, and the job that's left for people."
---

"AI triages customer feedback" sounds like either a toy that writes summaries nobody reads or a machine that replaces the operations team. It's neither. It's compression, and the numbers show it best.

Say a company gets 10,000 pieces of feedback in a week. The job of a first pass is to turn that pile into a short list of issues, each with its evidence attached, that people can judge. That's what [Cherry](https://cherry-topaz.vercel.app), my triage tool, does.

## The model never invents what a database knows

Ordinary software handles the facts: counts, accounts, revenue, dates, ticket IDs, owners. The model handles interpretation: what the customer was trying to do and whether two complaints are the same problem. When Cherry says "47 reports across 29 accounts," the numbers come from a query. The model's only claim is that those 47 reports describe one thing.

That claim fails in two directions. **Missed duplicates:** five different phrasings of one issue. **False duplicates,** which are worse: five complaints that all say the product "forgets," with five different causes and five different owners, merged into one useless cluster. Tidy output can still be wrong, which is why the first pass needs evals and human review.

It also has to check what already exists. Is there a ticket? Did leadership already call this an intentional tradeoff? Skip that, and the first pass just makes more noise.

## The numbers

Of those 10,000 records, perhaps 1,500 have nothing actionable and 3,000 are near-duplicates. The rest condense into a couple hundred clusters. Most match known issues, a few dozen are new, and only a small set needs a person to read closely.

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

That's the trade. People stop reading every submission and start reviewing the hard cases and samples of the rest. The model compresses the reading. The judgment stays with people.

## The job that's left

The first pass automates the reading, tagging, and copying. It creates a harder job: defining what good looks like, building the evals that keep the system honest, and checking whether any of it changes what gets built. How those human corrections get measured is [its own essay](/writing/why-the-human-stays-in-the-loop).
