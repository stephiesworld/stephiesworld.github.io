---
title: "What a dumpling taught me about AI agents"
date: "2026-07-22"
order: 9
category: "Notes"
dek: "Trying to automate a good dumpling at Little Bun taught me three things. They turned out to be the three hardest problems in deploying AI agents."
---

At Little Bun, I spent a long time on a question that sounds trivial and isn't: what would it take to automate a genuinely good dumpling?

We worked with automated manufacturing partners to bring the cost down, and I spent a lot of time with their R&D teams. Honestly, the teams we worked with in the East were stronger than the ones in the West.

It taught me three things, and years later, building AI agents, I keep running into the same three problems.

## 1. The judgment is invisible

A dumpling looks simple. The work isn't. The dough changes with humidity and how long it rested. The filling changes with the fat and water in that day's meat. Someone folding by hand adjusts for all of it without thinking: a little less filling because it's wet today, a little more pressure on this pleat because of the last one. One dumpling is a dozen small decisions. A machine has to treat each one as a separate problem in sensing, timing, and force.

Office work hides the same thing. Take a customer asking for a refund after the return window has closed.

The rule says no. The experienced person on that queue checks whether the delay was the customer's fault or a shipping failure on our side. They notice the account has never returned anything. They know the "no exceptions" policy has an unwritten exception for delivery problems. They know which of two systems to trust when they disagree about the delivery date. They see the customer mentioned it was a gift, which changes how they word the reply. Then they approve it.

<svg viewBox="0 0 700 470" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="One refund request outside the return window, broken into the seven judgments an experienced person makes before approving it, each labelled with where that knowledge lives. Three live in a record: the shipping log, the account history, and the customer's own message. Four, shown in red, live nowhere at all: the unwritten exception to the no-exceptions policy, the regional difference in how the damaged-goods rule is enforced, the knowledge of which of two disagreeing systems to trust on a given field, and the advice to log the reason in the structured field because nobody reads free text." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <defs>
    <marker id="rf" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker>
  </defs>
  <style>
    .lbl{font:600 10px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .sm{font:400 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#666;}
    .smb{font:600 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .band{font:700 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .no{font:600 9px "IBM Plex Mono",ui-monospace,monospace;fill:#aaa;}
    .none{font:600 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#B01E36;}
  </style>
  <text x="350" y="14" text-anchor="middle" class="band">ONE REFUND REQUEST, AT DUMPLING RESOLUTION</text>
  <rect x="130" y="26" width="440" height="30" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="350" y="45" text-anchor="middle" class="smb">A REFUND REQUESTED OUTSIDE THE RETURN WINDOW</text>
  <line x1="350" y1="56" x2="350" y2="68" stroke="#000" stroke-width="1.2" marker-end="url(#rf)"/>
  <text x="350" y="82" text-anchor="middle" class="lbl">THE RULE SAYS NO.</text>
  <text x="44" y="106" class="smb">WHAT THE EXPERIENCED PERSON CHECKS ANYWAY</text>
  <text x="486" y="106" class="smb">WHERE THAT LIVES</text>
  <line x1="20" y1="112" x2="692" y2="112" stroke="#000" stroke-width="1.5"/>
  <text x="24" y="136" class="no">1</text>
  <text x="44" y="136" class="sm">Was the delay ours, or the customer's?</text>
  <text x="486" y="136" class="smb">the shipping record</text>
  <line x1="20" y1="146" x2="692" y2="146" stroke="#ececec" stroke-width="1"/>
  <text x="24" y="170" class="no">2</text>
  <text x="44" y="170" class="sm">Third order from an account that has never returned anything</text>
  <text x="486" y="170" class="smb">the account history</text>
  <line x1="20" y1="180" x2="692" y2="180" stroke="#ececec" stroke-width="1"/>
  <text x="24" y="204" class="no">3</text>
  <text x="44" y="204" class="sm">"No exceptions" has an exception for a documented delivery failure</text>
  <text x="486" y="204" class="none">nowhere · unwritten</text>
  <line x1="20" y1="214" x2="692" y2="214" stroke="#ececec" stroke-width="1"/>
  <text x="24" y="238" class="no">4</text>
  <text x="44" y="238" class="sm">The damaged-goods rule is loose in one region, strict in another</text>
  <text x="486" y="238" class="none">nowhere · local practice</text>
  <line x1="20" y1="248" x2="692" y2="248" stroke="#ececec" stroke-width="1"/>
  <text x="24" y="272" class="no">5</text>
  <text x="44" y="272" class="sm">Two systems disagree on the date; one is right about that field</text>
  <text x="486" y="272" class="none">nowhere · system lore</text>
  <line x1="20" y1="282" x2="692" y2="282" stroke="#ececec" stroke-width="1"/>
  <text x="24" y="306" class="no">6</text>
  <text x="44" y="306" class="sm">They mentioned it was a gift · changes nothing, changes the reply</text>
  <text x="486" y="306" class="smb">the message itself</text>
  <line x1="20" y1="316" x2="692" y2="316" stroke="#ececec" stroke-width="1"/>
  <text x="24" y="340" class="no">7</text>
  <text x="44" y="340" class="sm">Log the reason in the structured field; nobody reads free text</text>
  <text x="486" y="340" class="none">nowhere · a colleague, once</text>
  <line x1="20" y1="350" x2="692" y2="350" stroke="#000" stroke-width="1.5"/>
  <rect x="130" y="364" width="440" height="30" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="350" y="383" text-anchor="middle" class="smb">APPROVED · in under a minute</text>
  <line x1="20" y1="414" x2="692" y2="414" stroke="#000" stroke-width="1"/>
  <text x="20" y="434" class="none">Four of the seven are written down nowhere at all.</text>
  <text x="20" y="450" class="sm">That is the filling. A system that automates this either gets told those four, or it reads the policy, applies the rule,</text>
  <text x="20" y="464" class="sm">and says no · correctly, by the only standard it was given.</text>
</svg>

Seven judgments, four of them written down nowhere, made in under a minute by someone who would describe the job as "processing returns."

When work looks easy, it's usually because a skilled person has absorbed the complexity. Trying to teach it to a machine, or an agent, is what makes that hidden judgment visible again.

## 2. You can fold the pleat, or stamp the seal

Frozen dumplings are mass-produced by the million. The way those lines got there is instructive: they got rid of the pleat. A machine stamps or crimps a seal that it can repeat forever, and the filling is standardized until it stops surprising the equipment. They changed the product until the process could be rigid.

That works, and it's usually the right call. The cost shows up on the plate, in the texture and in whether it tastes like someone made it.

<svg viewBox="0 0 700 440" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Two ways to automate a process that resists automation. Folding the pleat means building a system that absorbs the variation: in the kitchen, reading the dough and adjusting every unit; in software, an agent that reads context and adapts. You keep the quality that made the work worth doing, and you pay for sensing, judgment and checking on every unit forever. Stamping the seal, shown in red, means redesigning the work until the variation is gone: crimping instead of pleating and specifying the filling; a rigid form or required field in software. You keep the throughput and the margin, and you pay with the thing you were trying to make." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <defs>
    <marker id="dp" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker>
  </defs>
  <style>
    .lbl{font:600 10px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .sm{font:400 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#666;}
    .smb{font:600 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .band{font:700 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .cap{font:400 8px "IBM Plex Mono",ui-monospace,monospace;fill:#999;letter-spacing:0.08em;}
  </style>
  <text x="350" y="14" text-anchor="middle" class="band">TWO WAYS TO AUTOMATE WORK THAT RESISTS IT</text>
  <rect x="210" y="26" width="280" height="36" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="350" y="48" text-anchor="middle" class="smb">A PROCESS THAT RESISTS AUTOMATION</text>
  <line x1="300" y1="62" x2="200" y2="94" stroke="#000" stroke-width="1.2" marker-end="url(#dp)"/>
  <line x1="400" y1="62" x2="500" y2="94" stroke="#000" stroke-width="1.2" marker-end="url(#dp)"/>
  <rect x="20" y="96" width="310" height="44" fill="#fff" stroke="#000" stroke-width="2"/>
  <text x="175" y="117" text-anchor="middle" class="lbl">FOLD THE PLEAT</text>
  <text x="175" y="133" text-anchor="middle" class="sm">build a system that absorbs the variation</text>
  <rect x="20" y="148" width="310" height="46" fill="#fff" stroke="#000" stroke-width="1.2"/>
  <text x="30" y="166" class="cap">IN THE KITCHEN</text>
  <text x="30" y="182" class="smb">read the dough, adjust every single unit</text>
  <rect x="20" y="198" width="310" height="46" fill="#fff" stroke="#000" stroke-width="1.2"/>
  <text x="30" y="216" class="cap">IN SOFTWARE</text>
  <text x="30" y="232" class="smb">an agent that reads context and adapts</text>
  <rect x="20" y="248" width="310" height="46" fill="#f3f3f3" stroke="#000" stroke-width="1.2"/>
  <text x="30" y="266" class="cap">YOU KEEP</text>
  <text x="30" y="282" class="smb">the quality that made it worth doing</text>
  <rect x="20" y="298" width="310" height="46" fill="#f3f3f3" stroke="#000" stroke-width="1.2"/>
  <text x="30" y="316" class="cap">YOU PAY</text>
  <text x="30" y="332" class="smb">sensing and judgment, per unit, forever</text>
  <rect x="370" y="96" width="310" height="44" fill="#B01E36"/>
  <text x="525" y="117" text-anchor="middle" style="font:600 10px 'IBM Plex Mono',monospace;fill:#fff;">STAMP THE SEAL</text>
  <text x="525" y="133" text-anchor="middle" style="font:400 8.5px 'IBM Plex Mono',monospace;fill:#f2c9d1;">redesign the work until variation is gone</text>
  <rect x="370" y="148" width="310" height="46" fill="#fff" stroke="#000" stroke-width="1.2"/>
  <text x="380" y="166" class="cap">IN THE KITCHEN</text>
  <text x="380" y="182" class="smb">crimp instead of pleat; specify the filling</text>
  <rect x="370" y="198" width="310" height="46" fill="#fff" stroke="#000" stroke-width="1.2"/>
  <text x="380" y="216" class="cap">IN SOFTWARE</text>
  <text x="380" y="232" class="smb">a rigid form, a dropdown, a required field</text>
  <rect x="370" y="248" width="310" height="46" fill="#f3f3f3" stroke="#000" stroke-width="1.2"/>
  <text x="380" y="266" class="cap">YOU KEEP</text>
  <text x="380" y="282" class="smb">the throughput, and the margin</text>
  <rect x="370" y="298" width="310" height="46" fill="#B01E36"/>
  <text x="380" y="316" style="font:400 8px 'IBM Plex Mono',monospace;fill:#f2c9d1;letter-spacing:0.08em;">YOU PAY</text>
  <text x="380" y="332" style="font:600 8.5px 'IBM Plex Mono',monospace;fill:#fff;">the thing you were trying to make</text>
  <line x1="8" y1="372" x2="692" y2="372" stroke="#000" stroke-width="1"/>
  <text x="8" y="392" class="smb">MOST ORGANIZATIONS TAKE THE RIGHT-HAND PATH AND NEVER RECORD THAT THEY CHOSE.</text>
  <text x="8" y="408" class="sm">It is frequently the correct call. The trouble is arriving there by default, noticing two years later that the</text>
  <text x="8" y="422" class="sm">product no longer does the thing that made it worth building, and finding no note anywhere about when that was traded away.</text>
</svg>

Companies make the same choice with AI. You can build an agent that handles the variation in real work, or you can flatten the process into a rigid form that simple software can run. Stamping the seal is far cheaper, and often correct. Just know which one you chose, and what you gave up.

## 3. The price decides

The dumpling I most wanted to make was a better-for-you one. Better ingredients cost more per unit. But the market set the price of a dumpling a long time ago, by every other bag in the freezer aisle, none of which is trying to be good for you. I could make the product. I couldn't make it at the price a dumpling is allowed to cost.

Agents have the same arithmetic. You can always make one better: a larger model, more retrieval, a second model checking the first, a person reviewing every output. Each improves the result, and each raises the cost of every run. The frontier model is the expensive ingredient.

And the work most worth automating can afford it least. A task is worth automating because it happens a million times, and nobody ever paid much per instance for something that happens a million times. If a person clears a case in ninety seconds, an agent that costs more than ninety seconds of their time doesn't work as a product, however good it is.

There's a harder version. The quality that matters most in an agent is invisible when it works. Nobody notices the run where the agent declined to answer because its data was stale, because nothing happened. A demo shows fluency, not judgment. That was my dumpling problem too: I was trying to sell a quality you couldn't see on the plate.

## What the dumpling taught me

A cheap product can demand very sophisticated technology. Judgment is harder to automate than motion. And a system should be judged by what it does repeatedly, at a price that makes sense, when the inputs are imperfect.

*How to actually measure that reliability is [its own essay](/writing/agent-as-factory).*
