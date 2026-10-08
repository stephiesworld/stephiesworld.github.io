---
title: "What making things taught me about AI agents"
date: "2026-07-22"
order: 2
category: "Field guides"
dek: "A razor factory and a dumpling line taught me the hardest problems in deploying AI agents: hidden judgment, what to automate, how to inspect, and what it costs."
---

Before I built AI workflows, I made physical things. At Harry's, I worked in global R&D, where everything we designed had to survive being manufactured at scale. At Little Bun, I spent a long time on a question that sounds trivial and isn't: what would it take to automate a genuinely good dumpling?

Agents keep running into the same problems those factories solved.

## The judgment is invisible

A dumpling looks simple. Someone folding by hand adjusts for the humidity, the dough's rest, the water in that day's meat, all without thinking. One dumpling is a dozen small decisions.

Office work hides the same thing. Take a refund request that came in after the return window closed:

<svg viewBox="0 0 700 470" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="One refund request outside the return window, broken into the seven judgments an experienced person makes before approving it, each labelled with where that knowledge lives. Three live in a record: the shipping log, the account history, and the customer's own message. Four, shown in red, live nowhere at all: the unwritten exception to the no-exceptions policy, the regional difference in how the damaged-goods rule is enforced, the knowledge of which of two disagreeing systems to trust on a given field, and the advice to log the reason in the structured field because nobody reads free text." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <defs>
    <marker id="rf" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#a7a3c4"/></marker>
  </defs>
  <style>
    .lbl{font:600 10px "IBM Plex Mono",ui-monospace,monospace;fill:#f3ece2;}
    .sm{font:400 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#a9a6b8;}
    .smb{font:600 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#f3ece2;}
    .band{font:700 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#f3ece2;}
    .no{font:600 9px "IBM Plex Mono",ui-monospace,monospace;fill:#a9a6b8;}
    .none{font:600 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#ff7a92;}
  </style>
  <text x="350" y="14" text-anchor="middle" class="band">ONE REFUND REQUEST, AT DUMPLING RESOLUTION</text>
  <rect x="130" y="26" width="440" height="30" fill="#262b4a" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="350" y="45" text-anchor="middle" class="smb">A REFUND REQUESTED OUTSIDE THE RETURN WINDOW</text>
  <line x1="350" y1="56" x2="350" y2="68" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#rf)"/>
  <text x="350" y="82" text-anchor="middle" class="lbl">THE RULE SAYS NO.</text>
  <text x="44" y="106" class="smb">WHAT THE EXPERIENCED PERSON CHECKS ANYWAY</text>
  <text x="486" y="106" class="smb">WHERE THAT LIVES</text>
  <line x1="20" y1="112" x2="692" y2="112" stroke="#8f8cab" stroke-width="1.5"/>
  <text x="24" y="136" class="no">1</text>
  <text x="44" y="136" class="sm">Was the delay ours, or the customer's?</text>
  <text x="486" y="136" class="smb">the shipping record</text>
  <line x1="20" y1="146" x2="692" y2="146" stroke="#3a3f62" stroke-width="1"/>
  <text x="24" y="170" class="no">2</text>
  <text x="44" y="170" class="sm">Third order from an account that has never returned anything</text>
  <text x="486" y="170" class="smb">the account history</text>
  <line x1="20" y1="180" x2="692" y2="180" stroke="#3a3f62" stroke-width="1"/>
  <text x="24" y="204" class="no">3</text>
  <text x="44" y="204" class="sm">"No exceptions" has an exception for a documented delivery failure</text>
  <text x="486" y="204" class="none">nowhere · unwritten</text>
  <line x1="20" y1="214" x2="692" y2="214" stroke="#3a3f62" stroke-width="1"/>
  <text x="24" y="238" class="no">4</text>
  <text x="44" y="238" class="sm">The damaged-goods rule is loose in one region, strict in another</text>
  <text x="486" y="238" class="none">nowhere · local practice</text>
  <line x1="20" y1="248" x2="692" y2="248" stroke="#3a3f62" stroke-width="1"/>
  <text x="24" y="272" class="no">5</text>
  <text x="44" y="272" class="sm">Two systems disagree on the date; one is right about that field</text>
  <text x="486" y="272" class="none">nowhere · system lore</text>
  <line x1="20" y1="282" x2="692" y2="282" stroke="#3a3f62" stroke-width="1"/>
  <text x="24" y="306" class="no">6</text>
  <text x="44" y="306" class="sm">They mentioned it was a gift · changes nothing, changes the reply</text>
  <text x="486" y="306" class="smb">the message itself</text>
  <line x1="20" y1="316" x2="692" y2="316" stroke="#3a3f62" stroke-width="1"/>
  <text x="24" y="340" class="no">7</text>
  <text x="44" y="340" class="sm">Log the reason in the structured field; nobody reads free text</text>
  <text x="486" y="340" class="none">nowhere · a colleague, once</text>
  <line x1="20" y1="350" x2="692" y2="350" stroke="#8f8cab" stroke-width="1.5"/>
  <rect x="130" y="364" width="440" height="30" fill="#262b4a" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="350" y="383" text-anchor="middle" class="smb">APPROVED · in under a minute</text>
  <line x1="20" y1="414" x2="692" y2="414" stroke="#8f8cab" stroke-width="1"/>
  <text x="20" y="434" class="none">Four of the seven are written down nowhere at all.</text>
  <text x="20" y="450" class="sm">That is the filling. A system that automates this either gets told those four, or it reads the policy, applies the rule,</text>
  <text x="20" y="464" class="sm">and says no · correctly, by the only standard it was given.</text>
</svg>

Seven judgments, four written down nowhere, made in under a minute by someone who would describe the job as "processing returns." When work looks easy, a skilled person has absorbed the complexity. Teaching it to an agent is what makes it visible again.

## Fold the pleat, or stamp the seal

Frozen dumplings got to the million-a-day line by getting rid of the pleat. A machine stamps a seal it can repeat forever, and the filling is standardized until it stops surprising the equipment.

<svg viewBox="0 0 700 440" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Two ways to automate a process that resists automation. Folding the pleat means building a system that absorbs the variation: in the kitchen, reading the dough and adjusting every unit; in software, an agent that reads context and adapts. You keep the quality that made the work worth doing, and you pay for sensing, judgment and checking on every unit forever. Stamping the seal, shown in red, means redesigning the work until the variation is gone: crimping instead of pleating and specifying the filling; a rigid form or required field in software. You keep the throughput and the margin, and you pay with the thing you were trying to make." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <defs>
    <marker id="dp" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#a7a3c4"/></marker>
  </defs>
  <style>
    .lbl{font:600 10px "IBM Plex Mono",ui-monospace,monospace;fill:#f3ece2;}
    .sm{font:400 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#a9a6b8;}
    .smb{font:600 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#f3ece2;}
    .band{font:700 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#f3ece2;}
    .cap{font:400 8px "IBM Plex Mono",ui-monospace,monospace;fill:#a9a6b8;letter-spacing:0.08em;}
  </style>
  <text x="350" y="14" text-anchor="middle" class="band">TWO WAYS TO AUTOMATE WORK THAT RESISTS IT</text>
  <rect x="210" y="26" width="280" height="36" fill="#262b4a" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="350" y="48" text-anchor="middle" class="smb">A PROCESS THAT RESISTS AUTOMATION</text>
  <line x1="300" y1="62" x2="200" y2="94" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#dp)"/>
  <line x1="400" y1="62" x2="500" y2="94" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#dp)"/>
  <rect x="20" y="96" width="310" height="44" fill="#20253f" stroke="#8f8cab" stroke-width="2"/>
  <text x="175" y="117" text-anchor="middle" class="lbl">FOLD THE PLEAT</text>
  <text x="175" y="133" text-anchor="middle" class="sm">build a system that absorbs the variation</text>
  <rect x="20" y="148" width="310" height="46" fill="#20253f" stroke="#8f8cab" stroke-width="1.2"/>
  <text x="30" y="166" class="cap">IN THE KITCHEN</text>
  <text x="30" y="182" class="smb">read the dough, adjust every single unit</text>
  <rect x="20" y="198" width="310" height="46" fill="#20253f" stroke="#8f8cab" stroke-width="1.2"/>
  <text x="30" y="216" class="cap">IN SOFTWARE</text>
  <text x="30" y="232" class="smb">an agent that reads context and adapts</text>
  <rect x="20" y="248" width="310" height="46" fill="#262b4a" stroke="#8f8cab" stroke-width="1.2"/>
  <text x="30" y="266" class="cap">YOU KEEP</text>
  <text x="30" y="282" class="smb">the quality that made it worth doing</text>
  <rect x="20" y="298" width="310" height="46" fill="#262b4a" stroke="#8f8cab" stroke-width="1.2"/>
  <text x="30" y="316" class="cap">YOU PAY</text>
  <text x="30" y="332" class="smb">sensing and judgment, per unit, forever</text>
  <rect x="370" y="96" width="310" height="44" fill="#6b2346"/>
  <text x="525" y="117" text-anchor="middle" style="font:600 10px 'IBM Plex Mono',monospace;fill:#fff;">STAMP THE SEAL</text>
  <text x="525" y="133" text-anchor="middle" style="font:400 8.5px 'IBM Plex Mono',monospace;fill:#f2c9d1;">redesign the work until variation is gone</text>
  <rect x="370" y="148" width="310" height="46" fill="#20253f" stroke="#8f8cab" stroke-width="1.2"/>
  <text x="380" y="166" class="cap">IN THE KITCHEN</text>
  <text x="380" y="182" class="smb">crimp instead of pleat; specify the filling</text>
  <rect x="370" y="198" width="310" height="46" fill="#20253f" stroke="#8f8cab" stroke-width="1.2"/>
  <text x="380" y="216" class="cap">IN SOFTWARE</text>
  <text x="380" y="232" class="smb">a rigid form, a dropdown, a required field</text>
  <rect x="370" y="248" width="310" height="46" fill="#262b4a" stroke="#8f8cab" stroke-width="1.2"/>
  <text x="380" y="266" class="cap">YOU KEEP</text>
  <text x="380" y="282" class="smb">the throughput, and the margin</text>
  <rect x="370" y="298" width="310" height="46" fill="#6b2346"/>
  <text x="380" y="316" style="font:400 8px 'IBM Plex Mono',monospace;fill:#f2c9d1;letter-spacing:0.08em;">YOU PAY</text>
  <text x="380" y="332" style="font:600 8.5px 'IBM Plex Mono',monospace;fill:#fff;">the thing you were trying to make</text>
  <line x1="8" y1="372" x2="692" y2="372" stroke="#8f8cab" stroke-width="1"/>
  <text x="8" y="392" class="smb">MOST ORGANIZATIONS TAKE THE RIGHT-HAND PATH AND NEVER RECORD THAT THEY CHOSE.</text>
  <text x="8" y="408" class="sm">It is frequently the correct call. The trouble is arriving there by default, noticing two years later that the</text>
  <text x="8" y="422" class="sm">product no longer does the thing that made it worth building, and finding no note anywhere about when that was traded away.</text>
</svg>

Companies make the same choice with AI: build an agent that handles real variation, or flatten the work into a rigid form that simple software can run. Stamping is cheaper and often right. Just know which one you chose, and what you gave up.

## Fix the line, not the operator

Treat the model, prompt, tools, and orchestration as production equipment, and each run as a unit coming off the line.

<svg viewBox="0 0 700 640" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="One agent run drawn as a production line: task, environment, and equipment feed a run of three process steps (read, reason, act); the run emits a trajectory, an output, and a state change, each inspected by its own verifier; a blocking gate either delivers the accepted unit or routes it back for rework; a failed run becomes a permanent test in the eval suite, which changes the equipment rather than the individual unit." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <defs>
    <marker id="fa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#a7a3c4"/></marker>
    <marker id="fc" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#ff7a92"/></marker>
  </defs>
  <style>
    .lbl{font:600 10px "IBM Plex Mono",ui-monospace,monospace;fill:#f3ece2;}
    .sm{font:400 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#a9a6b8;}
    .smb{font:600 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#f3ece2;}
    .band{font:700 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#f3ece2;}
  </style>
  <text x="350" y="14" text-anchor="middle" class="band">ONE RUN · from work order to accepted unit</text>
  <rect x="30"  y="26" width="210" height="48" fill="#262b4a" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="135" y="45" text-anchor="middle" class="smb">TASK</text>
  <text x="135" y="60" text-anchor="middle" class="sm">the work order</text>
  <rect x="254" y="26" width="210" height="48" fill="#262b4a" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="359" y="45" text-anchor="middle" class="smb">ENVIRONMENT</text>
  <text x="359" y="60" text-anchor="middle" class="sm">docs · data · tool state = material</text>
  <rect x="478" y="26" width="214" height="48" fill="#262b4a" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="585" y="45" text-anchor="middle" class="smb">EQUIPMENT</text>
  <text x="585" y="60" text-anchor="middle" class="sm">model · prompt · skills · harness</text>
  <line x1="135" y1="74" x2="120" y2="100" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#fa)"/>
  <line x1="359" y1="74" x2="250" y2="100" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#fa)"/>
  <line x1="585" y1="74" x2="400" y2="100" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#fa)"/>
  <rect x="30" y="100" width="440" height="122" fill="#20253f" stroke="#8f8cab" stroke-width="2"/>
  <text x="250" y="120" text-anchor="middle" class="band">THE RUN · process steps, in order</text>
  <rect x="46" y="130" width="408" height="26" fill="#262b4a" stroke="#8f8cab" stroke-width="1"/>
  <text x="56" y="147" class="smb">READ</text>
  <text x="120" y="147" class="sm">opens only what it is allowed to open</text>
  <rect x="46" y="160" width="408" height="26" fill="#262b4a" stroke="#8f8cab" stroke-width="1"/>
  <text x="56" y="177" class="smb">REASON</text>
  <text x="120" y="177" class="sm">interprets, clusters, judges · the contestable part</text>
  <rect x="46" y="190" width="408" height="26" fill="#262b4a" stroke="#8f8cab" stroke-width="1"/>
  <text x="56" y="207" class="smb">ACT</text>
  <text x="120" y="207" class="sm">writes something to the world</text>
  <line x1="250" y1="222" x2="250" y2="236" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#fa)"/>
  <rect x="30" y="236" width="440" height="42" fill="#20253f" stroke="#8f8cab" stroke-width="1.5"/>
  <text x="42" y="255" class="smb">TRAJECTORY</text>
  <text x="42" y="269" class="sm">the batch record · what it read, called, got back, changed</text>
  <line x1="250" y1="278" x2="250" y2="294" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#fa)"/>
  <rect x="30" y="294" width="440" height="44" fill="#20253f" stroke="#8f8cab" stroke-width="1.5"/>
  <text x="42" y="313" class="lbl">OUTPUT</text>
  <text x="42" y="329" class="sm">the finished unit · the brief, the ticket, the decision</text>
  <rect x="30" y="346" width="440" height="44" fill="#20253f" stroke="#8f8cab" stroke-width="1.5"/>
  <text x="42" y="365" class="lbl">STATE CHANGE</text>
  <text x="42" y="381" class="sm">what it wrote to the system of record</text>
  <rect x="486" y="236" width="180" height="42" fill="#262b4a" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="576" y="253" text-anchor="middle" class="smb">TRAJECTORY VERIFIER</text>
  <text x="576" y="268" text-anchor="middle" class="sm">made acceptably?</text>
  <line x1="486" y1="257" x2="472" y2="257" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#fa)"/>
  <rect x="486" y="294" width="180" height="44" fill="#262b4a" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="576" y="312" text-anchor="middle" class="smb">OUTPUT VERIFIER</text>
  <text x="576" y="327" text-anchor="middle" class="sm">meets specification?</text>
  <line x1="486" y1="316" x2="472" y2="316" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#fa)"/>
  <rect x="486" y="346" width="180" height="44" fill="#262b4a" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="576" y="364" text-anchor="middle" class="smb">STATE VERIFIER</text>
  <text x="576" y="379" text-anchor="middle" class="sm">world changed correctly?</text>
  <line x1="486" y1="368" x2="472" y2="368" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#fa)"/>
  <line x1="250" y1="390" x2="250" y2="414" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#fa)"/>
  <rect x="30" y="414" width="440" height="54" fill="#20253f" stroke="#8f8cab" stroke-width="2"/>
  <text x="250" y="435" text-anchor="middle" class="band">BLOCKING GATE · the andon cord</text>
  <text x="250" y="452" text-anchor="middle" class="sm">critical defect stops the line · minor defect ships</text>
  <line x1="470" y1="441" x2="486" y2="441" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#fa)"/>
  <rect x="486" y="414" width="180" height="54" fill="#20253f" stroke="#8f8cab" stroke-width="1.5"/>
  <text x="576" y="438" text-anchor="middle" class="lbl">DELIVERED</text>
  <text x="576" y="454" text-anchor="middle" class="sm">an accepted unit</text>
  <path d="M 30 441 C 8 441, 8 168, 30 168" fill="none" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#fa)"/>
  <text x="17" y="305" class="sm" transform="rotate(-90 17 305)">rework · with a reason attached</text>
  <line x1="250" y1="468" x2="250" y2="496" stroke="#ff7a92" stroke-width="1.6" marker-end="url(#fc)"/>
  <rect x="30" y="496" width="440" height="54" fill="#6b2346"/>
  <text x="250" y="520" text-anchor="middle" style="font:700 10.5px 'IBM Plex Mono',monospace;fill:#fff;">FAILED RUN → THE EVAL SUITE</text>
  <text x="250" y="537" text-anchor="middle" style="font:400 8.5px 'IBM Plex Mono',monospace;fill:#fff;">the nonconformance becomes a permanent test</text>
  <path d="M 470 523 C 688 516, 694 170, 640 78" fill="none" stroke="#ff7a92" stroke-width="1.6" marker-end="url(#fc)"/>
  <text x="686" y="300" class="sm" fill="#ff7a92" transform="rotate(90 686 300)">change the process, not the unit</text>
  <line x1="30" y1="576" x2="692" y2="576" stroke="#8f8cab" stroke-width="1"/>
  <text x="30" y="596" class="smb">WHAT MAKES IT A SYSTEM:</text>
  <text x="30" y="612" class="sm">Every arrow that returns. Rework goes back with a reason. Failures go back as tests. Neither is optional:</text>
  <text x="30" y="626" class="sm">a line with no return path is a conveyor belt pointed at your customers.</text>
</svg>

Three habits carry straight over:

- **Inspect how it was made.** A flawless-looking report can come from a run that skipped two required documents. Check what the agent read, called, and changed, not just what it wrote.
- **Stop the line on real defects.** Toyota lets any worker halt production. Agents need checks that block delivery, not a dashboard that reports bad outputs after they ship. An awkward sentence can ship; an unsupported legal conclusion can't.
- **Check the checker.** If a grader scores the same output 0.9 on Monday and 0.6 on Tuesday, the gauge is broken. Use plain code where you can. In [Henry](https://henry-ten.vercel.app), the margin math never touches the model.

## The price decides

The dumpling I most wanted to make was a better-for-you one. I could make it. I couldn't make it at the price a dumpling is allowed to cost.

Agents have the same arithmetic. A bigger model, a second model checking the first, a person reviewing everything: each improves the result and raises the cost of every run. So measure **cost per accepted output** (every retry, check, and review, divided by the outputs good enough to use) and **first-pass yield**, the share that pass on the first try. A cheap model that needs three attempts is not cheap.

## Put the person at the point of no return

Factories concentrate inspection where a mistake costs the whole run. Two questions decide where a person should review agent work: how expensive is being wrong, and can you take it back?

<svg viewBox="0 0 700 460" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A two-by-two grid placing human review by cost of being wrong against reversibility. Low cost and reversible: let it run, no gate. Low cost but irreversible: confirm anyway, one click. High cost but reversible: verify then release, with a blocking verifier and sampled human audit. High cost and irreversible, marked in red: a named human signs every time, covering money, customer commitments, writes other systems read, deletion and publication. A closing note explains that scale moves work toward the top-right corner, because the prompt is the tooling and approving a policy is the irreversible step." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <defs>
    <marker id="ha" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#a7a3c4"/></marker>
  </defs>
  <style>
    .lbl{font:600 10px "IBM Plex Mono",ui-monospace,monospace;fill:#f3ece2;}
    .sm{font:400 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#a9a6b8;}
    .smb{font:600 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#f3ece2;}
    .band{font:700 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#f3ece2;}
  </style>
  <text x="350" y="14" text-anchor="middle" class="band">WHERE TO STAND THE HUMAN</text>
  <line x1="88" y1="330" x2="88" y2="46" stroke="#8f8cab" stroke-width="1.3" marker-end="url(#ha)"/>
  <text x="74" y="190" text-anchor="middle" class="smb" transform="rotate(-90 74 190)">COST OF BEING WRONG</text>
  <line x1="100" y1="344" x2="664" y2="344" stroke="#8f8cab" stroke-width="1.3" marker-end="url(#ha)"/>
  <text x="382" y="364" text-anchor="middle" class="smb">HARDER TO TAKE BACK</text>
  <rect x="100" y="50" width="280" height="140" fill="#262b4a" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="112" y="72" class="lbl">VERIFY, THEN RELEASE</text>
  <text x="112" y="88" class="sm">expensive to get wrong · but you can fix it</text>
  <text x="112" y="112" class="smb">a triage that reorders a roadmap</text>
  <text x="112" y="128" class="smb">a brief someone will act on</text>
  <text x="112" y="144" class="smb">a draft recommendation</text>
  <text x="112" y="170" class="sm">blocking verifier + sampled human audit</text>
  <rect x="380" y="50" width="280" height="140" fill="#6b2346"/>
  <text x="392" y="72" style="font:600 10px 'IBM Plex Mono',monospace;fill:#fff;">A NAMED HUMAN SIGNS</text>
  <text x="392" y="88" style="font:400 8.5px 'IBM Plex Mono',monospace;fill:#f2c9d1;">expensive · and there is no undo</text>
  <text x="392" y="112" style="font:600 8.5px 'IBM Plex Mono',monospace;fill:#fff;">money, or a promise to a customer</text>
  <text x="392" y="128" style="font:600 8.5px 'IBM Plex Mono',monospace;fill:#fff;">a write other systems read as fact</text>
  <text x="392" y="144" style="font:600 8.5px 'IBM Plex Mono',monospace;fill:#fff;">deletion, publication, a sent email</text>
  <text x="392" y="170" style="font:400 8.5px 'IBM Plex Mono',monospace;fill:#f2c9d1;">every time · no sampling, no exceptions</text>
  <rect x="100" y="190" width="280" height="140" fill="#20253f" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="112" y="212" class="lbl">LET IT RUN</text>
  <text x="112" y="228" class="sm">cheap · and trivially fixable</text>
  <text x="112" y="252" class="smb">internal summaries and notes</text>
  <text x="112" y="268" class="smb">drafts nobody has acted on yet</text>
  <text x="112" y="284" class="smb">a ranked list a human reads next</text>
  <text x="112" y="310" class="sm">no gate · sample it for drift</text>
  <rect x="380" y="190" width="280" height="140" fill="#262b4a" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="392" y="212" class="lbl">CONFIRM ANYWAY</text>
  <text x="392" y="228" class="sm">cheap · but you cannot unsend it</text>
  <text x="392" y="252" class="smb">a comment, a minor message</text>
  <text x="392" y="268" class="smb">a status the customer can see</text>
  <text x="392" y="284" class="smb">anything that leaves the building</text>
  <text x="392" y="310" class="sm">one click, not a full review</text>
  <line x1="8" y1="390" x2="692" y2="390" stroke="#8f8cab" stroke-width="1"/>
  <text x="8" y="410" class="smb">SCALE MOVES WORK TOWARD THE TOP-RIGHT CORNER:</text>
  <text x="8" y="426" class="sm">One record is a unit. The same decision applied to forty thousand records overnight is a production run · and the prompt</text>
  <text x="8" y="440" class="sm">that made it is the tooling. Approving the policy is the irreversible step; the units are only what the tooling stamps.</text>
</svg>

Before the irreversible step, an agent can retry freely. So put the person at the last moment the work can still be undone.

## Every failure becomes a test

When a check catches a failure, that run becomes a permanent test case. Fix the process, not just the one bad output, and the test makes sure it can't quietly come back. The model matters, but the lasting advantage is the factory around it.
