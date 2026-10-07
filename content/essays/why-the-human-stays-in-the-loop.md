---
title: "An opinion with edit access"
date: "2026-07-10"
order: 3
category: "Field guides"
dek: "Why a person still reviews an AI triage, and why a correction only counts once you measure what it changed."
---

If a model is good enough to triage feedback, why should a person still review it? I built a correction step into [Cherry](https://cherry-topaz.vercel.app), my triage tool, from day one, and the longer I work on it, the more permanent it looks. Three reasons.

**The model doesn't know what it was never told.** Cherry reads "Checkout is terrible" and routes it as a bug. The PM knows checkout was redesigned yesterday, on purpose, and people are reacting to the change. The most useful context is the stuff nobody has written down yet. A person is how it gets in.

**Someone has to decide what good looks like.** Cherry groups forty comments into "customers hate pricing." A PM says no: that's three problems wearing one trench coat, a confusing pricing page, surprise fees, and enterprise billing, each with its own owner. That correction defines what better looks like, and only a person can make it.

**People are strange.** "I LOVE waiting 45 minutes for support" might get filed as positive. Sarcasm, in-jokes, and the customer who says "fine" and means the opposite are where the model is shakiest. So Cherry shows its least confident calls first.

## Measure the correction

Without corrections, tomorrow's answer is exactly as good as today's. With them, the system improves, but only if you measure what each correction changed.

<svg viewBox="0 0 680 230" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Without correction: feedback to model to output, a straight line. With correction: the model proposes, a human edits, the edit is measured, and the improvement feeds back into the model's future behavior." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <defs>
    <marker id="ha" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker>
    <marker id="hc" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#B01E36"/></marker>
  </defs>
  <style>
    .hlbl{font:600 10px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .hsm{font:400 9px "IBM Plex Mono",ui-monospace,monospace;fill:#666;}
  </style>
  <text x="8" y="20" class="hsm">WITHOUT CORRECTION · a line: tomorrow is exactly as good as today</text>
  <rect x="8" y="34" width="130" height="36" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="73" y="56" text-anchor="middle" class="hlbl">FEEDBACK</text>
  <line x1="138" y1="52" x2="188" y2="52" stroke="#000" stroke-width="1.2" marker-end="url(#ha)"/>
  <rect x="190" y="34" width="130" height="36" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="255" y="56" text-anchor="middle" class="hlbl">MODEL</text>
  <line x1="320" y1="52" x2="370" y2="52" stroke="#000" stroke-width="1.2" marker-end="url(#ha)"/>
  <rect x="372" y="34" width="130" height="36" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="437" y="56" text-anchor="middle" class="hlbl">OUTPUT</text>
  <text x="8" y="118" class="hsm" fill="#B01E36">WITH CORRECTION · a loop: each fix also improves tomorrow</text>
  <rect x="8" y="132" width="118" height="36" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="67" y="154" text-anchor="middle" class="hlbl">FEEDBACK</text>
  <line x1="126" y1="150" x2="158" y2="150" stroke="#000" stroke-width="1.2" marker-end="url(#ha)"/>
  <rect x="160" y="132" width="118" height="36" fill="#fff" stroke="#000" stroke-width="1.5"/>
  <text x="219" y="149" text-anchor="middle" class="hlbl">MODEL</text>
  <text x="219" y="162" text-anchor="middle" class="hsm">proposes</text>
  <line x1="278" y1="150" x2="310" y2="150" stroke="#000" stroke-width="1.2" marker-end="url(#ha)"/>
  <rect x="312" y="132" width="118" height="36" fill="#fff" stroke="#B01E36" stroke-width="2"/>
  <text x="371" y="149" text-anchor="middle" class="hlbl">HUMAN</text>
  <text x="371" y="162" text-anchor="middle" class="hsm">edits</text>
  <line x1="430" y1="150" x2="462" y2="150" stroke="#000" stroke-width="1.2" marker-end="url(#ha)"/>
  <rect x="464" y="132" width="118" height="36" fill="#fff" stroke="#000" stroke-width="1.5"/>
  <text x="523" y="149" text-anchor="middle" class="hlbl">MEASURE</text>
  <text x="523" y="162" text-anchor="middle" class="hsm">did the edit help?</text>
  <path d="M 582 168 C 620 210, 260 226, 219 172" fill="none" stroke="#B01E36" stroke-width="1.6" marker-end="url(#hc)"/>
  <text x="400" y="216" text-anchor="middle" class="hsm" fill="#B01E36">what helped becomes tomorrow's behavior · prompts, retrieval, evals</text>
</svg>

A correction you don't measure is just an opinion with edit access.

I learned this the embarrassing way. Early on, Cherry's quality score went *down* after I made a genuinely good correction. The problem was the measurement: applying a correction re-ran the whole triage, so the grader was comparing two different random drafts. The fix was to change only what the correction required and leave everything else identical. After that, the score rose when a correction helped, and a falling correction rate meant the system was actually learning.

The goal isn't to keep people busy. It's to let the model do the repetitive first pass, so people spend their attention on the context and standards only they can supply.
