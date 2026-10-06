---
title: "The dumpling was the stress test"
date: "2026-07-22"
order: 9
category: "Notes"
dek: "Why the cheapest food I know is the best way I've found to explain why enterprise AI agents are hard."
---

*When people picture automated manufacturing, they think of cars. I think about dumplings, and the reason is economic.*

For years I've circled a question that sounds trivial and isn't: what would it take to automate a genuinely good dumpling? It became the center of my work at Little Bun. It's also the clearest way I know to explain why enterprise AI agents are hard.

## A dumpling is a bundle of micro-decisions

On the plate, a dumpling looks simple. Small, familiar, cheap, gone in three bites.

The wrapper isn't simple. The ratio of flour to water shifts with humidity, temperature, and how long the dough rested. Knead it enough to build structure but not so much that it fights you. Roll it thin enough to feel delicate and thick enough to survive filling, folding, cooking, freezing, and a truck.

The filling isn't simple either. Meat varies in fat, moisture, and temperature. Vegetables release water. Salt changes the protein. Mix too little and it's uneven; mix too hard and it turns rubbery.

Someone making dumplings by hand handles all of this without saying any of it out loud. They feel that today's filling is wetter and use a little less. They turn the dumpling in one hand while pinching with the other, and each pleat's angle and pressure responds to the pleat before it. The pleats are doing structural work: closing a curved surface around a soft, irregular filling while taking up the extra wrapper.

Count the judgments in one dumpling. Is the wrapper centered? How much filling will this wrapper hold? How much pressure seals the seam without squeezing filling out? The maker does it in one motion. A machine has to treat it as a dozen separate problems in sensing, timing, force, and control.

## "But dumplings are already mass-produced"

They are. Frozen dumplings come off industrial lines by the million, and that's the first objection anyone informed will raise.

Look at how those lines got there. They dropped the pleat and replaced hand-folding with a stamped or crimped seal a machine can repeat forever. They standardized the filling's moisture and fat until the material stopped surprising the equipment. They reshaped the product until the process could be rigid.

That's the oldest and best move in automation, and it works. The cost shows up on the plate: in the texture of the wrapper, in how it holds, in whether it tastes like something a person made.

The same tradeoff shows up everywhere, including in AI. Redesigning the work until the variation disappears is far cheaper than building a system that handles the variation. Every time a company flattens a nuanced process into a rigid form so software can run it, it has stamped the seal instead of folding the pleat. Sometimes that's exactly right. It's worth knowing which one you chose, and what you gave up.

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

## The price is the constraint

If a robot did something this delicate to a product worth thousands of dollars, the economics would forgive a lot: expensive sensors, slow cycle times, a technician on call, the occasional manual fix.

A dumpling forgives nothing. It has to be fast, because the volume is huge. Precise, because small defects add up across thousands of units. Gentle, because the materials are soft. Hygienic, because it's food. Low-waste, because the margins are thin. And cheap enough that automating it doesn't make an everyday food cost more than people will pay.

That makes the dumpling close to a worst case for automation. Solve it and you've solved a class of problems well beyond food.

It's also where Little Bun hit a wall that had nothing to do with engineering. The dumpling I most wanted to make was a better-for-you one, and better ingredients cost more per unit. But the market settled the price of a dumpling a long time ago, set by every other bag in the freezer aisle, none of which is trying to be good for you. I could make the product. I couldn't make the arithmetic work at the price a dumpling is allowed to cost.

That taught me more than the folding did, because it moved the constraint. The real question wasn't whether it could be made. It was whether it could be made well at the price the category allows.

## A dumpling is a workflow you can eat

Enterprise workflows also look simple from the outside. We say a claim was processed or an invoice approved, the same way we say fill, fold, cook. The name hides the work.

So take one at dumpling resolution. A customer asks for a refund outside the return window.

The rule says no, but the experienced person on that queue doesn't stop there. They check whether the delay was the customer's fault or a shipping failure on our side. They notice this is the third order from an account that has never returned anything. They know the "no exceptions" policy has an unwritten exception for documented delivery problems, and that the written exception for damaged goods is enforced loosely in one region and strictly in another. They see that the order system and the fulfillment system disagree about the delivery date, and they know which one is usually right about that field. They notice the customer mentioned it was a gift, which doesn't change the procedure but does change how they word the reply. They approve it, and they log the reason in the structured field instead of free text, because a colleague once told them nobody reads free text.

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

Seven judgments, four of them written down nowhere, all made in under a minute by someone who would describe the job as "processing returns."

A dumpling hides the same kind of thing: small decisions that turn loose inputs into something that holds together downstream. Skip one and it comes apart later, in the pot or in the quarter.

## Judgment is harder to automate than motion

Traditional automation works when the environment can be made rigid: same part, same place, same angle, ten thousand times. A lot of valuable human work only works because a person absorbs context, makes small adjustments, catches exceptions, and recovers when things don't go to plan.

A dumpling maker runs a loop: look at the material, act, notice the result, adjust the next move.

A useful enterprise agent needs the same loop. Work out what kind of situation this is, gather the context that matters, choose a next step, check whether it worked, and adapt when it didn't. A script stops when an expected field is empty. An agent has to decide whether the empty field is an error, an exception, or information.

Most of that intelligence lives in [the harness](/harness-cheat-sheet.html), much as it did on the dumpling line.

## Reliability is the product

Someone eating a dumpling cares that the wrapper has the right texture and doesn't fall apart. Someone using an enterprise agent cares that it found the right record, applied the right policy, and didn't create more work.

The ingredient problem comes back almost unchanged. You can always make an agent better: a larger model, more retrieval, an extra verification pass, a second model checking the first, a person reviewing every output. Each one improves the result, and each one raises the cost of a run. The frontier model is the expensive ingredient. You can taste the difference, and often you can't charge for it.

That's awkward, because the work most worth automating is the work least able to pay for it. A task is worth automating because it happens a million times, and nobody ever paid much per instance for a task that happens a million times. If a person clears a case in ninety seconds, an agent that costs more than ninety seconds of labor per run doesn't work as a product, no matter how good its answers are. That's the freezer aisle again.

There's a harder version of this. The qualities that matter most in an agent are invisible when it's working. Fluency is obvious in a demo. Calibration mostly isn't. Nobody notices the run where the agent declined to answer because a data feed was stale, because that's the run where nothing happened. So buyers pay for what they can see, and the property that makes a system trustworthy never shows up in a demo. That was my dumpling problem too. I was trying to sell a quality you couldn't see on the plate.

*How you actually measure any of that, from what counts as a defect to what stops a bad unit from shipping, is [its own essay](/writing/agent-as-factory).*

## What automation reveals

When a process looks easy, we assume it's easy to automate. Usually it looks easy because a skilled person has absorbed the complexity. A practiced maker doesn't calculate the force across a pleat. An operations lead doesn't draw a decision tree to resolve an exception. The knowledge became physical habit and stopped being visible.

Trying to teach it to a machine makes it visible again: the unwritten policies, the sensory cues, the recovery moves, the quiet coordination that kept things running. That's the part I didn't expect to value so much, and it's the part I'd defend hardest. The goal is to understand that work well enough to build something that keeps it.

The dumpling taught me that a cheap product can demand very sophisticated technology, that judgment is harder to automate than motion, and that a system should be judged by what it does repeatedly when the inputs are imperfect.
