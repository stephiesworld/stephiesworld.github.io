---
title: "Who is feedback for?"
date: "2026-07-10"
order: 1
category: "Field guides"
dek: "A feedback system succeeds or fails on the exit side: who reads the signal, what they need it for, and how it should be shaped for them."
---

Every feedback system I've seen obsesses over intake: more channels, more forms, more listening. But whether the system is useful gets decided on the other end, by **who reads it**.

So I designed [Cherry](https://cherry-topaz.vercel.app), my feedback-triage tool, around two questions for every team that uses customer feedback: *what is their goal?* and *what should the feedback look like for them?* Once I drew the whole system, most of the design decisions made themselves.

<svg viewBox="0 0 700 800" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Feedback flows from five sources into a triage core that screens, classifies, and weighs it, then out to five teams, each with its own goal and presentation; users feed the sources and receive closure; capability signals cross a permission gate into model development, whose improvements change the product and generate new signal." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <defs>
    <marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker>
    <marker id="ac" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#B01E36"/></marker>
    <marker id="am" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a8a8a"/></marker>
  </defs>
  <style>
    .lbl{font:600 10px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .sm{font:400 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#666;}
    .smb{font:600 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .cherry{fill:#B01E36;}
    .band{font:700 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
  </style>
  <!-- SOURCES -->
  <text x="340" y="16" text-anchor="middle" class="band">SIGNAL IN · every window has a tint</text>
  <g>
    <rect x="8"   y="28" width="124" height="46" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
    <text x="70" y="46" text-anchor="middle" class="smb">FIELD &amp; SALES CALLS</text>
    <text x="70" y="60" text-anchor="middle" class="sm">why buyers hesitate</text>
    <rect x="144" y="28" width="124" height="46" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
    <text x="206" y="46" text-anchor="middle" class="smb">SUPPORT TICKETS</text>
    <text x="206" y="60" text-anchor="middle" class="sm">where it hurts today</text>
    <rect x="280" y="28" width="124" height="46" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
    <text x="342" y="46" text-anchor="middle" class="smb">COMMUNITY &amp; SOCIAL</text>
    <text x="342" y="60" text-anchor="middle" class="sm">loud, self-selected</text>
    <rect x="416" y="28" width="124" height="46" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
    <text x="478" y="46" text-anchor="middle" class="smb">EARLY-ACCESS COHORTS</text>
    <text x="478" y="60" text-anchor="middle" class="sm">designed signal</text>
    <rect x="552" y="28" width="120" height="46" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
    <text x="612" y="46" text-anchor="middle" class="smb">TELEMETRY</text>
    <text x="612" y="60" text-anchor="middle" class="sm">what users do, not say</text>
  </g>
  <line x1="70"  y1="74" x2="250" y2="128" stroke="#000" stroke-width="1.2" marker-end="url(#a)"/>
  <line x1="206" y1="74" x2="300" y2="128" stroke="#000" stroke-width="1.2" marker-end="url(#a)"/>
  <line x1="342" y1="74" x2="342" y2="128" stroke="#000" stroke-width="1.2" marker-end="url(#a)"/>
  <line x1="478" y1="74" x2="386" y2="128" stroke="#000" stroke-width="1.2" marker-end="url(#a)"/>
  <line x1="612" y1="74" x2="436" y2="128" stroke="#000" stroke-width="1.2" marker-end="url(#a)"/>
  <!-- TRIAGE CORE -->
  <rect x="120" y="134" width="440" height="150" fill="#fff" stroke="#000" stroke-width="2"/>
  <text x="340" y="154" text-anchor="middle" class="band">THE TRIAGE CORE · one system of record</text>
  <rect x="136" y="166" width="408" height="30" fill="#f3f3f3" stroke="#000" stroke-width="1"/>
  <text x="146" y="185" class="smb">SCREEN</text>
  <text x="215" y="185" class="sm">real people? representative? · bots, astroturf, venting bias</text>
  <rect x="136" y="202" width="408" height="30" fill="#f3f3f3" stroke="#000" stroke-width="1"/>
  <text x="146" y="221" class="smb">CLASSIFY</text>
  <text x="215" y="221" class="sm">bug or tradeoff? one-off ticket or capability gap? use case?</text>
  <rect x="136" y="238" width="408" height="30" fill="#f3f3f3" stroke="#000" stroke-width="1"/>
  <text x="146" y="257" class="smb">WEIGH</text>
  <text x="215" y="257" class="sm">severity · reach · recency · $ at stake · no mystery number</text>
  <line x1="200" y1="284" x2="78"  y2="348" stroke="#000" stroke-width="1.2" marker-end="url(#a)"/>
  <line x1="270" y1="284" x2="212" y2="348" stroke="#000" stroke-width="1.2" marker-end="url(#a)"/>
  <line x1="340" y1="284" x2="340" y2="348" stroke="#000" stroke-width="1.2" marker-end="url(#a)"/>
  <line x1="410" y1="284" x2="468" y2="348" stroke="#000" stroke-width="1.2" marker-end="url(#a)"/>
  <line x1="480" y1="284" x2="602" y2="348" stroke="#000" stroke-width="1.2" marker-end="url(#a)"/>
  <!-- TEAMS -->
  <text x="340" y="342" text-anchor="middle" class="band" opacity="0"> </text>
  <g>
    <rect x="8" y="354" width="124" height="92" fill="#fff" stroke="#000" stroke-width="1.5"/>
    <text x="70" y="372" text-anchor="middle" class="lbl">PRODUCT</text>
    <text x="70" y="390" text-anchor="middle" class="sm">goal: what to build next</text>
    <text x="70" y="404" text-anchor="middle" class="smb">cut: ranked by user</text>
    <text x="70" y="416" text-anchor="middle" class="smb">pain, by use case</text>
    <rect x="144" y="354" width="124" height="92" fill="#fff" stroke="#B01E36" stroke-width="2"/>
    <text x="206" y="372" text-anchor="middle" class="lbl">RESEARCH / MODEL</text>
    <text x="206" y="390" text-anchor="middle" class="sm">goal: capability gaps</text>
    <text x="206" y="404" text-anchor="middle" class="smb">cut: systemic, authentic</text>
    <text x="206" y="416" text-anchor="middle" class="smb">patterns · not tickets</text>
    <rect x="280" y="354" width="124" height="92" fill="#fff" stroke="#000" stroke-width="1.5"/>
    <text x="342" y="372" text-anchor="middle" class="lbl">GTM &amp; SALES</text>
    <text x="342" y="390" text-anchor="middle" class="sm">goal: renew &amp; expand</text>
    <text x="342" y="404" text-anchor="middle" class="smb">cut: breadth, recency,</text>
    <text x="342" y="416" text-anchor="middle" class="smb">$ at stake · get ahead</text>
    <rect x="416" y="354" width="124" height="92" fill="#fff" stroke="#000" stroke-width="1.5"/>
    <text x="478" y="372" text-anchor="middle" class="lbl">SUPPORT</text>
    <text x="478" y="390" text-anchor="middle" class="sm">goal: respond now</text>
    <text x="478" y="404" text-anchor="middle" class="smb">cut: sharpest current</text>
    <text x="478" y="416" text-anchor="middle" class="smb">pain + reply drafts</text>
    <rect x="552" y="354" width="120" height="92" fill="#fff" stroke="#000" stroke-width="1.5"/>
    <text x="612" y="372" text-anchor="middle" class="lbl">LEADERSHIP</text>
    <text x="612" y="390" text-anchor="middle" class="sm">goal: strategy calls</text>
    <text x="612" y="404" text-anchor="middle" class="smb">cut: deliberate trade-</text>
    <text x="612" y="416" text-anchor="middle" class="smb">offs, cost of keeping</text>
  </g>
  <!-- MODEL DEVELOPMENT -->
  <line x1="206" y1="446" x2="206" y2="500" stroke="#B01E36" stroke-width="1.6" marker-end="url(#ac)"/>
  <rect x="192" y="470" width="14" height="14" fill="#fff" stroke="#B01E36" stroke-width="1.2"/>
  <text x="216" y="481" class="sm" fill="#B01E36">permission gate · default-deny</text>
  <rect x="96" y="506" width="220" height="58" fill="#B01E36"/>
  <text x="206" y="530" text-anchor="middle" style="font:700 10.5px 'IBM Plex Mono',monospace;fill:#fff;">MODEL DEVELOPMENT</text>
  <text x="206" y="548" text-anchor="middle" style="font:400 8.5px 'IBM Plex Mono',monospace;fill:#fff;">capability signals → training priorities</text>
  <!-- USERS loop -->
  <circle cx="512" cy="560" r="50" fill="#fff" stroke="#000" stroke-width="2"/>
  <text x="512" y="556" text-anchor="middle" class="lbl">USERS</text>
  <text x="512" y="572" text-anchor="middle" class="sm">the loop's fuel</text>
  <circle cx="600" cy="612" r="30" fill="none" stroke="#8a8a8a" stroke-width="1.3" stroke-dasharray="4 3"/>
  <text x="600" y="609" text-anchor="middle" class="sm">the silent</text>
  <text x="600" y="621" text-anchor="middle" class="sm">no voice ≠</text>
  <text x="600" y="632" text-anchor="middle" class="sm">no problem</text>
  <!-- teams -> users : you said, we did -->
  <line x1="478" y1="446" x2="500" y2="508" stroke="#000" stroke-width="1.2" marker-end="url(#a)"/>
  <text x="418" y="484" class="sm">"you said, we did"</text>
  <!-- model dev -> users : the product changes -->
  <line x1="316" y1="546" x2="458" y2="556" stroke="#B01E36" stroke-width="1.6" marker-end="url(#ac)"/>
  <text x="330" y="538" class="sm" fill="#B01E36">the product changes…</text>
  <!-- users -> sources : new signal (long return, right edge up) -->
  <path d="M 562 548 C 690 520, 694 200, 662 74" fill="none" stroke="#8a8a8a" stroke-width="1.3" stroke-dasharray="5 4" marker-end="url(#am)"/>
  <text x="694" y="300" class="sm" transform="rotate(90 694 300)">…which generates new signal</text>
  <!-- loop health -->
  <line x1="8" y1="650" x2="672" y2="650" stroke="#000" stroke-width="1"/>
  <text x="8" y="672" class="smb">LOOP HEALTH · how you know it's alive:</text>
  <text x="8" y="690" class="sm">time-to-triage (median and p90) · correction rate falling · roadmap citations at decision time · repeat submitters</text>
  <text x="8" y="716" class="sm">A funnel moves signal one way and goes quiet. A loop returns something at every edge · closure to users, priorities to builders,</text>
  <text x="8" y="730" class="sm">new signal to the top. If any return arrow goes dark, the loop is dying and the metrics above will say so before people do.</text>
</svg>

## Every source is biased

Support tickets over-represent what's broken; nobody files a ticket about a feature they love. Social media is the loudest room, and the loudest room is self-selected. Usage data shows what people *do* but never *why*. No single source tells the truth, so you need several.

## The middle has three jobs

Forwarding feedback just gives you a sorted pile. The middle has to **screen** it (is this from real, representative people?), **classify** it (a bug to fix, or a deliberate tradeoff people dislike?), and **weigh** it, with severity, reach, recency, and revenue kept as separate, visible dials. If the score is one mystery number, nobody trusts it.

## Each team needs a different view

Feedback goes to five teams doing five jobs, and the same issue means something different to each. Leadership needs its own category for deliberate choices, like pricing people dislike, where "just fix it" is the wrong instruction. In Cherry, that became one triage with a separate view for each audience.

For an AI product, one more exit matters most: feedback showing the model itself falls short should shape what it gets trained on next. That path needs a gate, because not all customer data can be used for training. If a record's permissions are unknown, it doesn't cross.

## Close the loop

A funnel becomes a loop when people hear back. Users who hear "you said, we did" keep talking. Users who hear nothing stop. And the customers who never speak up aren't happy; they're just unmeasured.

If you're building one of these, start at the exit side with the two questions. Build the plumbing after.
