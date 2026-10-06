---
title: "Your AI agent is a factory"
date: "2026-07-22"
order: 10
category: "Field guides"
dek: "Agent reliability, run the way a factory runs quality: inspect the process, gate the defects, and price every output that gets accepted."
---

*The most useful way to think about agent reliability may come from the factory floor.*

I spent part of my career in global R&D at Harry's, where everything we designed had to survive being manufactured at scale. For the last year I've been building AI workflows, and I keep seeing the same shape.

A request comes in. A process transforms it. Tools and materials affect what happens along the way. An output comes out the other side, sometimes excellent and sometimes subtly wrong. If the work matters, "it usually works" isn't a quality strategy.

I think of every agent run as five connected things: a task, an environment, a trajectory, an output, and a set of [verifiers](/eval-cheat-sheet.html) that judge the work. The same verifier can grade live production, test a proposed change offline, compare models and prompts, or stop a bad output before it's delivered.

## The run is the product

The first shift is to treat the model, prompt, tools, and orchestration as production equipment, and each individual run as the unit being produced. The account brief, the resolved ticket, the screened candidate, the updated CRM record: that's what actually leaves the factory.

Drawn as a line, one run looks like this.

<svg viewBox="0 0 700 640" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="One agent run drawn as a production line: task, environment, and equipment feed a run of three process steps (read, reason, act); the run emits a trajectory, an output, and a state change, each inspected by its own verifier; a blocking gate either delivers the accepted unit or routes it back for rework; a failed run becomes a permanent test in the eval suite, which changes the equipment rather than the individual unit." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <defs>
    <marker id="fa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker>
    <marker id="fc" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#B01E36"/></marker>
  </defs>
  <style>
    .lbl{font:600 10px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .sm{font:400 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#666;}
    .smb{font:600 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .band{font:700 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
  </style>
  <text x="350" y="14" text-anchor="middle" class="band">ONE RUN · from work order to accepted unit</text>
  <rect x="30"  y="26" width="210" height="48" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="135" y="45" text-anchor="middle" class="smb">TASK</text>
  <text x="135" y="60" text-anchor="middle" class="sm">the work order</text>
  <rect x="254" y="26" width="210" height="48" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="359" y="45" text-anchor="middle" class="smb">ENVIRONMENT</text>
  <text x="359" y="60" text-anchor="middle" class="sm">docs · data · tool state = material</text>
  <rect x="478" y="26" width="214" height="48" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="585" y="45" text-anchor="middle" class="smb">EQUIPMENT</text>
  <text x="585" y="60" text-anchor="middle" class="sm">model · prompt · skills · harness</text>
  <line x1="135" y1="74" x2="120" y2="100" stroke="#000" stroke-width="1.2" marker-end="url(#fa)"/>
  <line x1="359" y1="74" x2="250" y2="100" stroke="#000" stroke-width="1.2" marker-end="url(#fa)"/>
  <line x1="585" y1="74" x2="400" y2="100" stroke="#000" stroke-width="1.2" marker-end="url(#fa)"/>
  <rect x="30" y="100" width="440" height="122" fill="#fff" stroke="#000" stroke-width="2"/>
  <text x="250" y="120" text-anchor="middle" class="band">THE RUN · process steps, in order</text>
  <rect x="46" y="130" width="408" height="26" fill="#f3f3f3" stroke="#000" stroke-width="1"/>
  <text x="56" y="147" class="smb">READ</text>
  <text x="120" y="147" class="sm">opens only what it is allowed to open</text>
  <rect x="46" y="160" width="408" height="26" fill="#f3f3f3" stroke="#000" stroke-width="1"/>
  <text x="56" y="177" class="smb">REASON</text>
  <text x="120" y="177" class="sm">interprets, clusters, judges · the contestable part</text>
  <rect x="46" y="190" width="408" height="26" fill="#f3f3f3" stroke="#000" stroke-width="1"/>
  <text x="56" y="207" class="smb">ACT</text>
  <text x="120" y="207" class="sm">writes something to the world</text>
  <line x1="250" y1="222" x2="250" y2="236" stroke="#000" stroke-width="1.2" marker-end="url(#fa)"/>
  <rect x="30" y="236" width="440" height="42" fill="#fff" stroke="#000" stroke-width="1.5"/>
  <text x="42" y="255" class="smb">TRAJECTORY</text>
  <text x="42" y="269" class="sm">the batch record · what it read, called, got back, changed</text>
  <line x1="250" y1="278" x2="250" y2="294" stroke="#000" stroke-width="1.2" marker-end="url(#fa)"/>
  <rect x="30" y="294" width="440" height="44" fill="#fff" stroke="#000" stroke-width="1.5"/>
  <text x="42" y="313" class="lbl">OUTPUT</text>
  <text x="42" y="329" class="sm">the finished unit · the brief, the ticket, the decision</text>
  <rect x="30" y="346" width="440" height="44" fill="#fff" stroke="#000" stroke-width="1.5"/>
  <text x="42" y="365" class="lbl">STATE CHANGE</text>
  <text x="42" y="381" class="sm">what it wrote to the system of record</text>
  <rect x="486" y="236" width="180" height="42" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="576" y="253" text-anchor="middle" class="smb">TRAJECTORY VERIFIER</text>
  <text x="576" y="268" text-anchor="middle" class="sm">made acceptably?</text>
  <line x1="486" y1="257" x2="472" y2="257" stroke="#000" stroke-width="1.2" marker-end="url(#fa)"/>
  <rect x="486" y="294" width="180" height="44" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="576" y="312" text-anchor="middle" class="smb">OUTPUT VERIFIER</text>
  <text x="576" y="327" text-anchor="middle" class="sm">meets specification?</text>
  <line x1="486" y1="316" x2="472" y2="316" stroke="#000" stroke-width="1.2" marker-end="url(#fa)"/>
  <rect x="486" y="346" width="180" height="44" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="576" y="364" text-anchor="middle" class="smb">STATE VERIFIER</text>
  <text x="576" y="379" text-anchor="middle" class="sm">world changed correctly?</text>
  <line x1="486" y1="368" x2="472" y2="368" stroke="#000" stroke-width="1.2" marker-end="url(#fa)"/>
  <line x1="250" y1="390" x2="250" y2="414" stroke="#000" stroke-width="1.2" marker-end="url(#fa)"/>
  <rect x="30" y="414" width="440" height="54" fill="#fff" stroke="#000" stroke-width="2"/>
  <text x="250" y="435" text-anchor="middle" class="band">BLOCKING GATE · the andon cord</text>
  <text x="250" y="452" text-anchor="middle" class="sm">critical defect stops the line · minor defect ships</text>
  <line x1="470" y1="441" x2="486" y2="441" stroke="#000" stroke-width="1.2" marker-end="url(#fa)"/>
  <rect x="486" y="414" width="180" height="54" fill="#fff" stroke="#000" stroke-width="1.5"/>
  <text x="576" y="438" text-anchor="middle" class="lbl">DELIVERED</text>
  <text x="576" y="454" text-anchor="middle" class="sm">an accepted unit</text>
  <path d="M 30 441 C 8 441, 8 168, 30 168" fill="none" stroke="#000" stroke-width="1.2" marker-end="url(#fa)"/>
  <text x="17" y="305" class="sm" transform="rotate(-90 17 305)">rework · with a reason attached</text>
  <line x1="250" y1="468" x2="250" y2="496" stroke="#B01E36" stroke-width="1.6" marker-end="url(#fc)"/>
  <rect x="30" y="496" width="440" height="54" fill="#B01E36"/>
  <text x="250" y="520" text-anchor="middle" style="font:700 10.5px 'IBM Plex Mono',monospace;fill:#fff;">FAILED RUN → THE EVAL SUITE</text>
  <text x="250" y="537" text-anchor="middle" style="font:400 8.5px 'IBM Plex Mono',monospace;fill:#fff;">the nonconformance becomes a permanent test</text>
  <path d="M 470 523 C 688 516, 694 170, 640 78" fill="none" stroke="#B01E36" stroke-width="1.6" marker-end="url(#fc)"/>
  <text x="686" y="300" class="sm" fill="#B01E36" transform="rotate(90 686 300)">change the process, not the unit</text>
  <line x1="30" y1="576" x2="692" y2="576" stroke="#000" stroke-width="1"/>
  <text x="30" y="596" class="smb">WHAT MAKES IT A SYSTEM:</text>
  <text x="30" y="612" class="sm">Every arrow that returns. Rework goes back with a reason. Failures go back as tests. Neither is optional:</text>
  <text x="30" y="626" class="sm">a line with no return path is a conveyor belt pointed at your customers.</text>
</svg>

This changes where you look for reliability. When a part comes off the line out of tolerance, a good manufacturing team checks the material, the work instruction, the machine calibration, the process stability, and the inspection method before anyone tells the operator to be more careful.

Agent failures deserve the same treatment. A hallucinated number might come from a weak model. It might just as easily come from stale source data, an ambiguous task, a failed retrieval, a tool returning the wrong field, a prompt that rewarded fluency over uncertainty, or a verifier that mistook confidence for correctness. "The model got it wrong" is usually as shallow a diagnosis as "the factory made a bad part."

## The trajectory is the production record

The eval systems I trust inspect the whole trajectory, not just the final output: what the agent read, which tools it called, what those tools returned, and what it changed.

Manufacturers learned long ago that final inspection isn't enough. The FDA's process-validation guidance says quality "cannot be adequately assured merely by in-process and finished-product inspection or testing." It has to be built into the process.

Say an agent produces a flawless-looking due-diligence report. A grader that only reads the output approves the structure, the prose, and the completeness. The trajectory shows the agent never opened two required documents and pulled a number from an outdated filing. The part passed dimensional inspection with the wrong alloy inside it.

Three kinds of checks answer three different questions:

- **Output verifiers:** did the thing meet the specification?
- **Trajectory verifiers:** was it made through an acceptable process?
- **State verifiers:** did the system change the outside world correctly?

For low-stakes work, the first is enough. For a hiring decision, a financial recommendation, or an agent that writes to a system of record, how the output was made is part of the product.

## Runtime gates are the andon cord

Some verifiers have to block. They stop delivery, tell the agent what's wrong, and require a revision before the work reaches anyone.

Toyota calls this *jidoka*: when something abnormal happens, the machine or the operator stops the line so the defect isn't passed downstream. A runtime gate does the same thing at the point of work, before a customer finds out the deck has no citations or the agent updated the wrong record.

The important word is **blocking**. A dashboard that reports bad outputs after delivery is a returns report. It's useful for learning and too late to stop anything.

Not every defect should stop the line. Manufacturing separates critical, major, and minor defects, and agents need the same logic. An awkward sentence can ship. An unsupported legal conclusion can't. Be careful with weighted averages here, because five strong scores can mathematically cancel one catastrophic failure. Critical attributes need hard thresholds.

## Verifiers are gauges, and gauges can be wrong

Once a verifier is a gauge, someone has to check the gauge.

Manufacturing tests measurement systems for repeatability (does the same gauge give the same result under the same conditions?) and reproducibility (does it hold across operators, instruments, and time?). Model judges need the same discipline.

If a verifier scores the same output 0.9 on Monday and 0.6 on Tuesday, the process may not have changed at all; the gauge is noisy. If a generic judge keeps approving shallow work that experts reject, the gauge is consistent and wrong. And if the agent and the verifier share a blind spot, which is likely when they're the same model family, the system can agree with itself and still be wrong.

So calibrate verifiers against expert judgment, and use deterministic checks wherever you can. "The file exists in the required folder" should be a line of code. In [Henry](https://henry-ten.vercel.app), the margin math runs in ordinary code, never in the model. "The recommendation is commercially useful" may need a model judge, and that judge should be tested against people who actually do the work.

Before optimizing an agent against a verifier, I want to know:

- Does it agree with itself across repeated judgments?
- Does it agree with qualified people, especially near the pass/fail line?
- What are its false-accept and false-reject rates?
- Can it be fooled by length, confidence, formatting, or copied rubric language?
- Does it hold up on cases it hasn't seen?

In an optimization loop, a bad gauge teaches the machine to make the wrong thing more efficiently.

## An eval suite is a control plan

A production line has to work across the real variation in materials, operators, and equipment. A test suite full of clean prompts and complete data is qualifying the line on perfect material and calling it production-ready.

Real enterprise work arrives with missing context, stale documents, ambiguous requests, permission failures, conflicting sources, and tools that time out. Design the suite around that: which failures are most severe, which are hardest to detect, where each can be caught earliest, and which checks can be code instead of judgment.

## Don't jump from the lab bench to full production

Manufacturers scale up in stages: a lab bench, a pilot batch, then a trial on the real line with real operators, materials, and speeds. The point of the line trial is to learn whether the process can make good units *repeatedly, under production conditions*.

An offline eval is a pilot batch. The mock tools are cleaner than production, the test documents are complete, permissions behave, and nobody edits a record halfway through the run. Each stage below adds more of the real world.

<svg viewBox="0 0 700 430" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A six-stage scale-up sequence shown as rows: bench test, pilot batch, line trial, controlled release, scale-up, and continued verification. Each row states the question that stage answers and what it adds, alongside a bar showing how much real production condition is present, rising from a small fraction at bench test to full at continued verification." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <style>
    .lbl{font:600 10px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .sm{font:400 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#666;}
    .smb{font:600 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .band{font:700 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .num{font:600 10px "IBM Plex Mono",ui-monospace,monospace;fill:#aaa;}
  </style>
  <text x="350" y="14" text-anchor="middle" class="band">SCALE-UP · a demo is stage one of six</text>
  <text x="8" y="36" class="smb">STAGE</text>
  <text x="180" y="36" class="smb">THE QUESTION IT ANSWERS · WHAT IT ADDS</text>
  <text x="520" y="36" class="smb">PRODUCTION REALITY</text>
  <line x1="8" y1="42" x2="692" y2="42" stroke="#000" stroke-width="1.5"/>
  <rect x="8" y="50" width="160" height="46" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="18" y="78" class="num">1</text>
  <text x="36" y="70" class="smb">BENCH TEST</text>
  <text x="36" y="84" class="sm">mock everything</text>
  <text x="180" y="70" class="smb">Can it do the task at all?</text>
  <text x="180" y="84" class="sm">clean prompts, complete data, tools that never fail</text>
  <rect x="520" y="64" width="164" height="14" fill="#ececec"/>
  <rect x="520" y="64" width="27" height="14" fill="#000"/>
  <rect x="8" y="104" width="160" height="46" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="18" y="132" class="num">2</text>
  <text x="36" y="124" class="smb">PILOT BATCH</text>
  <text x="36" y="138" class="sm">the offline suite</text>
  <text x="180" y="124" class="smb">Consistent across normal, edge, and known-failure cases?</text>
  <text x="180" y="138" class="sm">variation arrives, but you still chose all of it</text>
  <rect x="520" y="118" width="164" height="14" fill="#ececec"/>
  <rect x="520" y="118" width="55" height="14" fill="#000"/>
  <rect x="8" y="158" width="160" height="46" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="18" y="186" class="num">3</text>
  <text x="36" y="178" class="smb">LINE TRIAL</text>
  <text x="36" y="192" class="sm">real conditions</text>
  <text x="180" y="178" class="smb">Does it hold against real data, permissions, latency, concurrency?</text>
  <text x="180" y="192" class="sm">production-shaped, but nothing reaches a customer</text>
  <rect x="520" y="172" width="164" height="14" fill="#ececec"/>
  <rect x="520" y="172" width="82" height="14" fill="#000"/>
  <rect x="8" y="212" width="160" height="46" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="18" y="240" class="num">4</text>
  <text x="36" y="232" class="smb">CONTROLLED</text>
  <text x="36" y="246" class="sm">a slice of live traffic</text>
  <text x="180" y="232" class="smb">Can it take real customers with the gates on?</text>
  <text x="180" y="246" class="sm">blocking verifiers, close monitoring, a rollback path</text>
  <rect x="520" y="226" width="164" height="14" fill="#ececec"/>
  <rect x="520" y="226" width="109" height="14" fill="#000"/>
  <rect x="8" y="266" width="160" height="46" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="18" y="294" class="num">5</text>
  <text x="36" y="286" class="smb">SCALE-UP</text>
  <text x="36" y="300" class="sm">full volume</text>
  <text x="180" y="286" class="smb">Does volume degrade yield, cycle time, or review capacity?</text>
  <text x="180" y="300" class="sm">ten sequential calls is not one hundred simultaneous ones</text>
  <rect x="520" y="280" width="164" height="14" fill="#ececec"/>
  <rect x="520" y="280" width="137" height="14" fill="#000"/>
  <rect x="8" y="320" width="160" height="46" fill="#B01E36"/>
  <text x="18" y="348" style="font:600 10px 'IBM Plex Mono',monospace;fill:#e79aa8;">6</text>
  <text x="36" y="340" style="font:600 8.5px 'IBM Plex Mono',monospace;fill:#fff;">CONTINUED</text>
  <text x="36" y="354" style="font:400 8.5px 'IBM Plex Mono',monospace;fill:#f2c9d1;">forever, not once</text>
  <text x="180" y="340" class="smb">Does it stay in control as inputs, tools, and models drift?</text>
  <text x="180" y="354" class="sm">every model swap and prompt edit is a new process</text>
  <rect x="520" y="334" width="164" height="14" fill="#ececec"/>
  <rect x="520" y="334" width="164" height="14" fill="#B01E36"/>
  <line x1="8" y1="386" x2="692" y2="386" stroke="#000" stroke-width="1"/>
  <text x="8" y="406" class="sm">The demo lives at stage one. The deployment lives at stage six. Almost everything expensive hides between three and five,</text>
  <text x="8" y="420" class="sm">where the tools are real, the volume is real, and nobody has checked whether the review queue can absorb the output.</text>
</svg>

Scale exposes what small tests hide. An agent that saves one analyst time can create an impossible review queue at enterprise volume. A fast model gets slow once retries and verifier calls are counted.

The same logic applies after launch. Swapping the model, editing the system prompt, adding a tool, or changing a verifier is a process change. The bigger the change, the more of the line needs requalifying. "It passed last quarter" says little about a different process.

## The real unit cost is cost per accepted output

Most teams measure cost per run: tokens, tool calls, compute. I care more about **cost per accepted output**:

> (agent execution + tool usage + verification + retries + human review + expected cost of failures) ÷ accepted outputs

This flips decisions that look obvious. A small model can cost half as much per attempt, then need more retries, trigger more escalations, and eat more reviewer time. A larger model can be cheaper overall because more of its work is accepted the first time. And an expensive model shouldn't sit at every station just because it wins on the hardest cases.

The number I watch most is **first-pass yield**: the share of runs that clear every required gate without revision or human rework. An agent with a 95% eventual pass rate can still be operationally poor if only half its runs pass the first time. Retries are a rework loop. They use capacity, stretch cycle time, and hide instability behind a respectable final number.

Manufacturing calls the full picture the cost of quality, and it sorts spending into four buckets that are priced very differently.

<svg viewBox="0 0 700 362" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Cost of quality across four buckets, with the cost of a single defect rising in steps from left to right: prevention (design it out), appraisal (look for it), internal failure (caught before release), and external failure (caught by the customer), which is marked in red as the most expensive. An arrow underneath points leftward, noting that every dollar moved left buys more than the one before it." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <defs>
    <marker id="ql" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker>
  </defs>
  <style>
    .lbl{font:600 10px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .sm{font:400 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#666;}
    .smb{font:600 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .band{font:700 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
  </style>
  <text x="350" y="14" text-anchor="middle" class="band">COST OF QUALITY · the later you catch it, the more it costs</text>
  <text x="8" y="34" class="sm">cost of one defect, caught here ↓</text>
  <path d="M 8 104 H 178 V 86 H 348 V 62 H 518 V 34 H 688" fill="none" stroke="#000" stroke-width="1.6"/>
  <rect x="8" y="120" width="170" height="152" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="93" y="142" text-anchor="middle" class="lbl">PREVENTION</text>
  <text x="93" y="158" text-anchor="middle" class="sm">design it out</text>
  <text x="20" y="182" class="smb">task + tool contracts</text>
  <text x="20" y="198" class="smb">source controls</text>
  <text x="20" y="214" class="smb">prompt + rubric design</text>
  <text x="20" y="230" class="smb">failure-mode analysis</text>
  <text x="20" y="256" class="sm">cheapest place to spend</text>
  <rect x="178" y="120" width="170" height="152" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="263" y="142" text-anchor="middle" class="lbl">APPRAISAL</text>
  <text x="263" y="158" text-anchor="middle" class="sm">look for it</text>
  <text x="190" y="182" class="smb">verifier calls</text>
  <text x="190" y="198" class="smb">audit samples</text>
  <text x="190" y="214" class="smb">red-team tests</text>
  <text x="190" y="230" class="smb">human review</text>
  <text x="190" y="256" class="sm">buys the other three down</text>
  <rect x="348" y="120" width="170" height="152" fill="#fff" stroke="#000" stroke-width="1.5"/>
  <text x="433" y="142" text-anchor="middle" class="lbl">INTERNAL FAILURE</text>
  <text x="433" y="158" text-anchor="middle" class="sm">caught before release</text>
  <text x="360" y="182" class="smb">retries and rework</text>
  <text x="360" y="198" class="smb">diagnosis time</text>
  <text x="360" y="214" class="smb">discarded outputs</text>
  <text x="360" y="230" class="smb">late delivery</text>
  <text x="360" y="256" class="sm">the rework loop, hidden</text>
  <rect x="518" y="120" width="170" height="152" fill="#B01E36"/>
  <text x="603" y="142" text-anchor="middle" style="font:600 10px 'IBM Plex Mono',monospace;fill:#fff;">EXTERNAL FAILURE</text>
  <text x="603" y="158" text-anchor="middle" style="font:400 8.5px 'IBM Plex Mono',monospace;fill:#f2c9d1;">caught by the customer</text>
  <text x="530" y="182" style="font:600 8.5px 'IBM Plex Mono',monospace;fill:#fff;">bad decisions made</text>
  <text x="530" y="198" style="font:600 8.5px 'IBM Plex Mono',monospace;fill:#fff;">unauthorized actions</text>
  <text x="530" y="214" style="font:600 8.5px 'IBM Plex Mono',monospace;fill:#fff;">compliance incidents</text>
  <text x="530" y="230" style="font:600 8.5px 'IBM Plex Mono',monospace;fill:#fff;">trust, and earning it back</text>
  <text x="530" y="256" style="font:400 8.5px 'IBM Plex Mono',monospace;fill:#f2c9d1;">the only bucket with no cap</text>
  <text x="350" y="300" text-anchor="middle" class="sm">every dollar you move left buys more than the one before it</text>
  <line x1="688" y1="312" x2="20" y2="312" stroke="#000" stroke-width="1.3" marker-end="url(#ql)"/>
  <text x="8" y="334" class="sm">A verifier that costs cents and seconds is the cheapest thing standing</text>
  <text x="8" y="348" class="sm">between an internal failure and an external one.</text>
</svg>

Inspection is worth paying for, but running every verifier on every task is its own waste. Verifiers should have activation conditions, so the right check runs at the station where that failure can actually happen.

The dashboard I'd want shows first-pass yield, rework rate, cost per accepted output, cycle time, human minutes per unit, escape rate, and the cost and latency of each verifier. That's the view you need to find the cheapest process that reliably meets the spec.

## Put the human at the point of no return

I've argued [elsewhere](/writing/why-the-human-stays-in-the-loop) that the human belongs in the loop. The harder question is where.

Manufacturing concentrates inspection where a mistake would cost the whole run instead of one unit. You approve a first article before the run starts. You sign off on a sample before the mold is cut. A defect caught on the first article costs one part and an afternoon. The same defect caught after a full run has shipped to a large retailer costs the run, the freight, the write-off, the retailer's chargebacks, and a claims process that shows up in no unit-cost model.

Agents have the same asymmetry. Two questions decide where the human stands: **how expensive is being wrong**, and **can you take it back?**

The second one matters more than teams expect. A wrong draft can be expensive and still free to fix. A wrong email can be cheap and permanently sent.

<svg viewBox="0 0 700 460" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A two-by-two grid placing human review by cost of being wrong against reversibility. Low cost and reversible: let it run, no gate. Low cost but irreversible: confirm anyway, one click. High cost but reversible: verify then release, with a blocking verifier and sampled human audit. High cost and irreversible, marked in red: a named human signs every time, covering money, customer commitments, writes other systems read, deletion and publication. A closing note explains that scale moves work toward the top-right corner, because the prompt is the tooling and approving a policy is the irreversible step." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <defs>
    <marker id="ha" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker>
  </defs>
  <style>
    .lbl{font:600 10px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .sm{font:400 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#666;}
    .smb{font:600 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .band{font:700 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
  </style>
  <text x="350" y="14" text-anchor="middle" class="band">WHERE TO STAND THE HUMAN</text>
  <line x1="88" y1="330" x2="88" y2="46" stroke="#000" stroke-width="1.3" marker-end="url(#ha)"/>
  <text x="74" y="190" text-anchor="middle" class="smb" transform="rotate(-90 74 190)">COST OF BEING WRONG</text>
  <line x1="100" y1="344" x2="664" y2="344" stroke="#000" stroke-width="1.3" marker-end="url(#ha)"/>
  <text x="382" y="364" text-anchor="middle" class="smb">HARDER TO TAKE BACK</text>
  <rect x="100" y="50" width="280" height="140" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="112" y="72" class="lbl">VERIFY, THEN RELEASE</text>
  <text x="112" y="88" class="sm">expensive to get wrong · but you can fix it</text>
  <text x="112" y="112" class="smb">a triage that reorders a roadmap</text>
  <text x="112" y="128" class="smb">a brief someone will act on</text>
  <text x="112" y="144" class="smb">a draft recommendation</text>
  <text x="112" y="170" class="sm">blocking verifier + sampled human audit</text>
  <rect x="380" y="50" width="280" height="140" fill="#B01E36"/>
  <text x="392" y="72" style="font:600 10px 'IBM Plex Mono',monospace;fill:#fff;">A NAMED HUMAN SIGNS</text>
  <text x="392" y="88" style="font:400 8.5px 'IBM Plex Mono',monospace;fill:#f2c9d1;">expensive · and there is no undo</text>
  <text x="392" y="112" style="font:600 8.5px 'IBM Plex Mono',monospace;fill:#fff;">money, or a promise to a customer</text>
  <text x="392" y="128" style="font:600 8.5px 'IBM Plex Mono',monospace;fill:#fff;">a write other systems read as fact</text>
  <text x="392" y="144" style="font:600 8.5px 'IBM Plex Mono',monospace;fill:#fff;">deletion, publication, a sent email</text>
  <text x="392" y="170" style="font:400 8.5px 'IBM Plex Mono',monospace;fill:#f2c9d1;">every time · no sampling, no exceptions</text>
  <rect x="100" y="190" width="280" height="140" fill="#fff" stroke="#000" stroke-width="1.3"/>
  <text x="112" y="212" class="lbl">LET IT RUN</text>
  <text x="112" y="228" class="sm">cheap · and trivially fixable</text>
  <text x="112" y="252" class="smb">internal summaries and notes</text>
  <text x="112" y="268" class="smb">drafts nobody has acted on yet</text>
  <text x="112" y="284" class="smb">a ranked list a human reads next</text>
  <text x="112" y="310" class="sm">no gate · sample it for drift</text>
  <rect x="380" y="190" width="280" height="140" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="392" y="212" class="lbl">CONFIRM ANYWAY</text>
  <text x="392" y="228" class="sm">cheap · but you cannot unsend it</text>
  <text x="392" y="252" class="smb">a comment, a minor message</text>
  <text x="392" y="268" class="smb">a status the customer can see</text>
  <text x="392" y="284" class="smb">anything that leaves the building</text>
  <text x="392" y="310" class="sm">one click, not a full review</text>
  <line x1="8" y1="390" x2="692" y2="390" stroke="#000" stroke-width="1"/>
  <text x="8" y="410" class="smb">SCALE MOVES WORK TOWARD THE TOP-RIGHT CORNER:</text>
  <text x="8" y="426" class="sm">One record is a unit. The same decision applied to forty thousand records overnight is a production run · and the prompt</text>
  <text x="8" y="440" class="sm">that made it is the tooling. Approving the policy is the irreversible step; the units are only what the tooling stamps.</text>
</svg>

The irreversible actions are a short, knowable list: anything that moves money, sends a message, publishes, deletes, makes a promise to a customer, or writes to a record other systems treat as fact. Before that line, an agent can iterate freely, because a retry is just rework. After it, there's nothing left to rework.

So put the human at the last reversible moment. Reviewing every step burns the attention you need at the step that matters, and reviewing after delivery is a returns report.

One more thing teams forget: the run is the unit, but the prompt, the policy, and the rubric are the tooling. Sampling outputs while nobody signs off on a policy change is inspecting parts while the mold goes unchecked.

## Failures become corrective action

The part of this I find most useful is the loop from production back into development.

When a verifier catches a failure in a live run, that run becomes a new offline test, so the failure is reproducible. The team changes the prompt, tool, or harness. The candidate runs against the suite. If quality improves without unacceptable cost or latency, the change moves forward.

A quality system calls this corrective and preventive action, and it runs the same six steps:

1. Contain the immediate issue.
2. Record what went wrong.
3. Find the root cause.
4. Change the process, not just the bad unit.
5. Verify the change worked.
6. Watch for it coming back.

Asking an agent to redo one weak brief is a correction. Changing the system so that failure gets less likely, and adding a test so it can't quietly return, is corrective action.

## Where the analogy breaks

It breaks in a few honest places. Most agents run something closer to a make-to-order shop than a line of identical parts, so there may be no single tolerance for "good strategy." Agent behavior is probabilistic, so one passing run proves very little. Many specifications are contestable: a hole is 5.00 millimeters or it isn't, but whether a brief found the *right* commercial risk is a judgment call. And once verifier scores are used for optimization, the agent starts adapting to the gauge. Parts can't study the inspection rubric. Agents effectively can.

Digital work does make 100% inspection affordable in a way physical manufacturing rarely can. But total inspection is only as good as the verifier doing it, and checking every unit with a weak one mostly scales your confidence.

## The factory is the product

The biggest mistake in enterprise AI is grading the intelligence of the model while ignoring the reliability of the system around it. The useful questions are operational. What's the specification? Where should each failure be caught? Which defects stop delivery? What happens to a failure after it's found? The model matters, but the lasting advantage comes from defining quality, measuring it credibly, and feeding what you learn back into the process.

---

### Sources and further reading

- Toyota, ["Toyota Production System"](https://global.toyota/en/company/vision-and-philosophy/production-system/) (jidoka)
- FDA, ["Process Validation: General Principles and Practices"](https://www.fda.gov/files/drugs/published/Process-Validation--General-Principles-and-Practices.pdf)
- ASQ, ["What Is Cost of Quality?"](https://asq.org/quality-resources/cost-of-quality)
- NIST/SEMATECH, ["What Are Control Charts?"](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc31.htm) and ["Assessing Process Capability"](https://www.itl.nist.gov/div898/handbook/ppc/section4/ppc46.htm)
- NIST, [measurement repeatability and reproducibility terminology](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-d1-terminology)
