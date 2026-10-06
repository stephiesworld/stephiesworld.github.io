---
title: "An opinion with edit access"
date: "2026-07-10"
order: 3
category: "Field guides"
dek: "Why a person still reviews an AI triage, and why a correction only counts once you measure what it changed."
---

*If the model is good enough to triage feedback, why should a person still review it?* It's a fair question. The point of automating a first pass is to stop doing the first pass, and from a distance, keeping a human in the loop looks like keeping the thing you were trying to remove.

I built the correction step into [Cherry](https://cherry-topaz.vercel.app), my triage tool, from the beginning, and the longer I've worked on it, the more permanent it looks.

## The model can't know what it was never told

Say Cherry reads this: *"Checkout is terrible."* A reasonable classification: bug, route to the checkout team. But the PM reading the triage knows something no model could infer. *We redesigned checkout yesterday, on purpose, and people are reacting to the redesign.* Or: *this customer is on the mobile app; web checkout is fine.*

That context lives in the organization: in yesterday's launch, last week's decision, the tribal knowledge of who shipped what. A model can only reason over what it's given, and the freshest, most decision-relevant context is exactly what nobody has written down yet. The human in the loop is how that context gets in.

## Someone has to decide what good looks like

My favorite question about any AI system is *who decides when it's wrong?* It has to be a person. Asking the model would be circular.

Say Cherry clusters forty comments into one issue: "customers hate pricing." A PM looks at it and says no, this is three problems wearing one trench coat: a confusing pricing *page*, unexpected *fees*, and enterprise *billing*, each with its own owner and fix.

That correction also defines what better synthesis looks like, and the PM is the person qualified to define it. Over time, the system's standard of quality becomes human judgment, captured one correction at a time.

## Sarcasm, and other human sports

*"I LOVE waiting 45 minutes for support."*

A person reads that and winces. A model might file it as positive. Models have gotten remarkably good at this, but the tail of human expression is long: irony, in-jokes, industry shorthand, the customer who says "fine" in a way that means the opposite. The edge cases are where automated confidence is least deserved, so Cherry shows its *least* confident calls for review first. Human attention is scarce, and it should go where the model is shakiest.

## Trust comes from showing your work

Imagine you own a roadmap and someone hands you a priority list. Which would you rather hear?

*"The model says these are the top five issues."*

Or: *"The model proposed these five. Here's the evidence for each. I reviewed them and made two corrections."*

The second is the one a responsible decision-maker can act on, even if the two lists are identical, because judgment was visibly applied and someone put their name on it. That's what makes the output something a person will stake a quarter on.

## Measuring the correction

Without a correction step, the system is a line: feedback goes in, an answer comes out, and tomorrow's answer is exactly as good as today's. A correction step turns the line into a loop, where each improvement builds on the last.

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

Most people skip the third box, *measure*. A correction you don't measure is just an opinion with edit access.

In Cherry, an independent evaluator grades the model's original output against the human-corrected version on grounding, clustering, ranking, routing, and actionability. The layers that keep that evaluator honest are in the [eval cheat sheet](/eval-cheat-sheet.html).

I learned why this matters the embarrassing way. Early on, Cherry's quality score went *down* after I made a genuinely good correction. The measurement was the problem. Applying a correction re-ran the entire triage from scratch, so the grader was comparing two different random drafts, and the noise drowned out the signal. The fix was to apply corrections surgically: change only what the person's judgment requires and leave everything else identical, so the score moves only because of the correction. After that, the number was trustworthy. It rises when a correction genuinely helps, and a falling correction *rate* over time means the system is learning. "It gets better" became something I could measure.

## Where that leaves the human

The goal is for the model to take the repetitive first-pass work, so human attention lands where it can't be replaced: the calls that need context the model was never given, and the standards only a person can set. The system's job is to measure whether those corrections made it better, so tomorrow starts ahead of today.
