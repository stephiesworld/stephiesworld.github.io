---
title: "Your AI agent is a factory"
date: "2026-07-22"
order: 10
category: "AI & the enterprise"
---

*The most useful way to think about agent reliability may come from the factory floor.*

I spent a stretch of my career in global R&D at Harry's, where the things we designed had to survive being manufactured at scale, and I have spent the last year building AI workflows. I keep seeing the same shape.

A customer request enters. A process transforms it. Tools and materials affect what happens along the way. An output comes out the other side. Sometimes it is excellent and sometimes it is subtly wrong. If the operation matters, you need a better quality strategy than "it usually works."

I think of every agent run as five connected things: a task, an environment, a trajectory, an output, and a set of [verifiers](/eval-cheat-sheet.html) that judge the work. The same verifier can grade live production, test proposed changes offline, compare models and prompts, or stop a bad output before delivery.

## The run is the product

The first shift is to treat the model, prompt, tools, skills, and orchestration as production equipment, and the individual run as the unit being produced. A strategic account brief, a resolved support ticket, a screened candidate, or an updated CRM record is what actually leaves the factory.

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
  <text x="350" y="14" text-anchor="middle" class="band">ONE RUN — from work order to accepted unit</text>
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
  <text x="250" y="120" text-anchor="middle" class="band">THE RUN — process steps, in order</text>
  <rect x="46" y="130" width="408" height="26" fill="#f3f3f3" stroke="#000" stroke-width="1"/>
  <text x="56" y="147" class="smb">READ</text>
  <text x="120" y="147" class="sm">opens only what it is allowed to open</text>
  <rect x="46" y="160" width="408" height="26" fill="#f3f3f3" stroke="#000" stroke-width="1"/>
  <text x="56" y="177" class="smb">REASON</text>
  <text x="120" y="177" class="sm">interprets, clusters, judges — the contestable part</text>
  <rect x="46" y="190" width="408" height="26" fill="#f3f3f3" stroke="#000" stroke-width="1"/>
  <text x="56" y="207" class="smb">ACT</text>
  <text x="120" y="207" class="sm">writes something to the world</text>
  <line x1="250" y1="222" x2="250" y2="236" stroke="#000" stroke-width="1.2" marker-end="url(#fa)"/>
  <rect x="30" y="236" width="440" height="42" fill="#fff" stroke="#000" stroke-width="1.5"/>
  <text x="42" y="255" class="smb">TRAJECTORY</text>
  <text x="42" y="269" class="sm">the batch record — what it read, called, got back, changed</text>
  <line x1="250" y1="278" x2="250" y2="294" stroke="#000" stroke-width="1.2" marker-end="url(#fa)"/>
  <rect x="30" y="294" width="440" height="44" fill="#fff" stroke="#000" stroke-width="1.5"/>
  <text x="42" y="313" class="lbl">OUTPUT</text>
  <text x="42" y="329" class="sm">the finished unit — the brief, the ticket, the decision</text>
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
  <text x="250" y="435" text-anchor="middle" class="band">BLOCKING GATE — the andon cord</text>
  <text x="250" y="452" text-anchor="middle" class="sm">critical defect stops the line · minor defect ships</text>
  <line x1="470" y1="441" x2="486" y2="441" stroke="#000" stroke-width="1.2" marker-end="url(#fa)"/>
  <rect x="486" y="414" width="180" height="54" fill="#fff" stroke="#000" stroke-width="1.5"/>
  <text x="576" y="438" text-anchor="middle" class="lbl">DELIVERED</text>
  <text x="576" y="454" text-anchor="middle" class="sm">an accepted unit</text>
  <path d="M 30 441 C 8 441, 8 168, 30 168" fill="none" stroke="#000" stroke-width="1.2" marker-end="url(#fa)"/>
  <text x="17" y="305" class="sm" transform="rotate(-90 17 305)">rework — with a reason attached</text>
  <line x1="250" y1="468" x2="250" y2="496" stroke="#B01E36" stroke-width="1.6" marker-end="url(#fc)"/>
  <rect x="30" y="496" width="440" height="54" fill="#B01E36"/>
  <text x="250" y="520" text-anchor="middle" style="font:700 10.5px 'IBM Plex Mono',monospace;fill:#fff;">FAILED RUN → THE EVAL SUITE</text>
  <text x="250" y="537" text-anchor="middle" style="font:400 8.5px 'IBM Plex Mono',monospace;fill:#fff;">the nonconformance becomes a permanent test</text>
  <path d="M 470 523 C 688 516, 694 170, 640 78" fill="none" stroke="#B01E36" stroke-width="1.6" marker-end="url(#fc)"/>
  <text x="686" y="300" class="sm" fill="#B01E36" transform="rotate(90 686 300)">change the process, not the unit</text>
  <line x1="30" y1="576" x2="692" y2="576" stroke="#000" stroke-width="1"/>
  <text x="30" y="596" class="smb">WHAT MAKES IT A SYSTEM:</text>
  <text x="30" y="612" class="sm">Every arrow that returns. Rework goes back with a reason. Failures go back as tests. Neither is optional —</text>
  <text x="30" y="626" class="sm">a line with no return path is a conveyor belt pointed at your customers.</text>
</svg>

This changes where you look for reliability. If a finished component is out of tolerance, a good manufacturing team asks whether the material was in spec, the work instruction was clear, the machine was calibrated, the process was stable, and the inspection method could reliably detect the defect, before anyone tells the operator to "be more careful."

Agent failures deserve the same treatment. A hallucinated number might come from a weak model, or just as easily from stale source data, an ambiguous task, a failed retrieval, a tool returning the wrong field, a prompt that rewarded fluency over uncertainty, or a verifier that mistook confidence for correctness. "The model got it wrong" is often as shallow a diagnosis as "the factory made a bad part."

## A trajectory is a digital production record

The eval systems I trust inspect the full trajectory as well as the final output: what the agent read, which tools it called, what those tools returned, and what it changed.

Manufacturers learned long ago that final inspection is not enough. The FDA's process-validation guidance puts it more strongly than my analogy strictly needs: quality, safety, and efficacy are designed or built into the product, and quality "cannot be adequately assured merely by in-process and finished-product inspection or testing." A polished final artifact can hide a broken one.

Say an agent produces a flawless-looking due-diligence report. A final-output grader may approve its structure, prose, and completeness. But the trajectory could reveal that the agent never opened two required documents, used a source outside the approved data room, or copied a number from an outdated filing. The report passed dimensional inspection while the wrong alloy went into the part.

Process checks and output checks answer different questions.

- Output verifiers ask: *Did the thing meet specification?*
- Trajectory verifiers ask: *Was it made through an acceptable process?*
- State verifiers ask: *Did the system change the outside world correctly?*

For low-stakes work, the first is enough. For a candidate decision, a financial recommendation, or an agent that writes to a system of record, provenance and process become part of the product.

## Runtime gates are the andon cord

Some verifiers have to block: they stop delivery, hand the agent an explanation, and require a revision before the work reaches anyone.

The manufacturing parallel is *jidoka*, one of the pillars of the Toyota Production System. Toyota describes it as automation with a human touch: when an abnormality appears, the machine or operator can stop production so defects are not passed downstream.

A runtime gate detects an abnormal condition at the point of work, before a customer discovers that a deck lacks required citations or that an agent advanced the wrong record. It stops the line and routes the unit for rework or human review.

The important word is **blocking**. A dashboard that reports bad outputs after delivery is a returns report, useful for learning and too late to stop anything.

Not every defect should stop the line. Manufacturing teams distinguish critical, major, and minor defects, and agent systems need the same risk logic. An awkward sentence can ship, but an unsupported legal conclusion should not. A weighted average alone can obscure this: five strong scores can mathematically cancel one catastrophic failure. Critical attributes need hard thresholds.

## The verifier is a measurement system, and measurement systems can be bad

Once you see a verifier as a gauge, you have to ask who verifies the verifier.

A measurement system has to be accurate enough for the tolerance it is judging. Teams test whether the same gauge produces consistent results under the same conditions — repeatability — and whether results remain consistent across operators, instruments, locations, or time — reproducibility. NIST treats both as properties of the measurement process. Model judges need the same discipline.

If a verifier gives the same artifact a 0.9 on Monday and a 0.6 on Tuesday, the production process may not have changed; the gauge may be noisy. If a generic judge consistently approves shallow market maps that domain experts reject, the gauge may be precise but wrong. If the agent and verifier share the same blind spot — especially when they use the same model family — the system can agree with itself and still be wrong.

So verifiers need calibrating against expert judgment, with deterministic checks wherever they are possible. "The file exists in the required folder" should be a line of code. (In [Henry](https://henry-ten.vercel.app), a vendor-operations agent I built, the margin math runs in ordinary deterministic code.) "The recommendation is commercially useful" may require a model judge, but that judge should be tested against people who actually do the work.

Before optimizing an agent against a verifier, I would want to know:

- Does the verifier agree with itself across repeated judgments?
- Does it agree with qualified humans, especially near the pass/fail boundary?
- What are its false-accept and false-reject rates?
- Can it be fooled by length, confidence, formatting, or copied rubric language?
- Does its performance hold on unfamiliar cases?

In an optimization loop, a bad gauge teaches the machine to manufacture the wrong thing more efficiently.

## An eval suite is a control plan

In manufacturing, a line has to perform across the real variation of raw materials, operators, equipment conditions, and customer requirements. A task suite full of clean prompts and complete data is qualifying a line on perfect material and calling it production-ready.

Real enterprise work arrives with missing context, stale documents, ambiguous requests, permissions failures, conflicting sources, and tools that time out. Eval teams call this coverage of the task distribution. A manufacturing engineer might call it understanding the operating range of the process.

So design the suite like a control plan:

- What are the critical-to-quality attributes for each kind of work?
- Which failure modes are most severe, most likely, and hardest to detect?
- Where in the process can each failure be caught earliest?
- Which checks can be deterministic, and which require judgment?
- What production evidence should trigger tighter inspection or a new test?

## Do not jump from the lab bench to full production

Before a manufacturer commits to full-scale production, it usually learns in stages. A formulation may begin on a lab bench, move to a pilot batch, then run through the actual line using commercial equipment, trained operators, real materials, target speeds, and an approved control plan. The point of a line trial is to learn whether the process can make good units *repeatedly under production conditions*.

An offline eval is a pilot batch. Mock tools are cleaner than production tools, test documents are usually complete, permissions behave, and no one changes a record halfway through the run.

A sensible scale-up sequence, with the amount of real production conditions rising at every step:

<svg viewBox="0 0 700 430" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A six-stage scale-up sequence shown as rows: bench test, pilot batch, line trial, controlled release, scale-up, and continued verification. Each row states the question that stage answers and what it adds, alongside a bar showing how much real production condition is present, rising from a small fraction at bench test to full at continued verification." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <style>
    .lbl{font:600 10px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .sm{font:400 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#666;}
    .smb{font:600 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .band{font:700 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .num{font:600 10px "IBM Plex Mono",ui-monospace,monospace;fill:#aaa;}
  </style>
  <text x="350" y="14" text-anchor="middle" class="band">SCALE-UP — a demo is stage one of six</text>
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

Scale exposes failures that small tests conceal. An agent that saves one analyst time may create an impossible review queue at enterprise volume. A fast model may become slow once retries and verifier calls are included.

The same reasoning applies after launch. Swapping the model, editing the system prompt, adding a tool, or changing a verifier is a process change, and the larger the change, the more of the line should be requalified before rollout. "It passed last quarter" says little about a materially different production process.

## The real unit economics are cost per accepted output

Manufacturing teams care about yield, scrap, rework, inspection, downtime, throughput, and failures discovered after shipment, along with the cost of starting a unit. A cheaper input that creates more defective product ends up costing more.

Most teams reach for cost per run first (model tokens, tool calls, and compute). I care more about **cost per accepted output**:

> (agent execution + tool usage + verification + retries + human review + expected failure cost) ÷ accepted outputs

The distinction reverses model decisions that look obvious. A small model can cost half as much on the first attempt, then require more retries, trigger more escalations, and eat more reviewer time. A larger model can be cheaper at the system level because more of its work is accepted the first time. Conversely, an expensive model should not be installed at every station merely because it performs best on the hardest cases.

First-pass yield, the percentage of runs that clear every required quality gate without revision or human rework, is especially revealing. An agent with a 95% eventual pass rate can still be operationally poor if only 50% pass the first time. The retries are the digital equivalent of a rework loop: they consume capacity, lengthen cycle time, and hide instability behind a respectable final number.

Manufacturing has a name for the whole picture: cost of quality. Spending falls into four buckets, and they are not equally priced.

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
  <text x="350" y="14" text-anchor="middle" class="band">COST OF QUALITY — the later you catch it, the more it costs</text>
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

Appraisal is worth paying for, but running every possible verifier on every possible task is its own form of waste. Verifiers should have activation conditions: apply the right inspection at the station where the relevant failure can occur.

The dashboard I would want shows first-pass yield, rework rate, cost per accepted output, cycle time, human minutes per unit, escape rate, and the cost and latency of each verifier — the view needed to find the least expensive process that reliably meets the specification.

## Put the human at the point of no return

I have argued [elsewhere](/writing/why-the-human-stays-in-the-loop) that the human belongs in the loop. The harder question is where to stand them.

Manufacturing concentrates inspection at the moments where a mistake would cost the entire run instead of one unit. You approve a first article before the run starts. You sign off a sample before the tooling is cut, because a mistake found after the steel is cut for a mold is a capital loss.

The economics on either side of those moments are not close. A defect caught on the first article costs one part and an afternoon. Imagine the same defect caught after a full production run has shipped to a large retailer: it costs the run, the freight, the rework or the write-off, the retailer's chargebacks, and a claims process — slow in a way that appears in no unit-cost model.

Agents have the same asymmetry, and two questions decide where the human stands: **how expensive is being wrong**, and **can you take it back?**

The second matters more than teams expect, and it's a separate question from the first: a wrong draft can be expensive and still free to fix, while a wrong email can be cheap and permanently sent. Reversibility is what separates a rework loop from a remediation project.

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
  <text x="392" y="170" style="font:400 8.5px 'IBM Plex Mono',monospace;fill:#f2c9d1;">every time — no sampling, no exceptions</text>
  <rect x="100" y="190" width="280" height="140" fill="#fff" stroke="#000" stroke-width="1.3"/>
  <text x="112" y="212" class="lbl">LET IT RUN</text>
  <text x="112" y="228" class="sm">cheap · and trivially fixable</text>
  <text x="112" y="252" class="smb">internal summaries and notes</text>
  <text x="112" y="268" class="smb">drafts nobody has acted on yet</text>
  <text x="112" y="284" class="smb">a ranked list a human reads next</text>
  <text x="112" y="310" class="sm">no gate — sample it for drift</text>
  <rect x="380" y="190" width="280" height="140" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="392" y="212" class="lbl">CONFIRM ANYWAY</text>
  <text x="392" y="228" class="sm">cheap · but you cannot unsend it</text>
  <text x="392" y="252" class="smb">a comment, a minor message</text>
  <text x="392" y="268" class="smb">a status the customer can see</text>
  <text x="392" y="284" class="smb">anything that leaves the building</text>
  <text x="392" y="310" class="sm">one click, not a full review</text>
  <line x1="8" y1="390" x2="692" y2="390" stroke="#000" stroke-width="1"/>
  <text x="8" y="410" class="smb">SCALE MOVES WORK TOWARD THE TOP-RIGHT CORNER:</text>
  <text x="8" y="426" class="sm">One record is a unit. The same decision applied to forty thousand records overnight is a production run — and the prompt</text>
  <text x="8" y="440" class="sm">that made it is the tooling. Approving the policy is the irreversible step; the units are only what the tooling stamps.</text>
</svg>

The irreversible actions are a short and knowable list: anything that moves money, sends a message, publishes, deletes, promises something to a customer, or writes to a record other systems will read as fact. Before that line, an agent can iterate freely and cheaply, because retries are just rework; after it, there's nothing left to rework.

So put the human at the last reversible moment. Reviewing every step burns the review capacity you need at the step that matters, and reviewing after delivery is just a returns report.

Teams most often forget that while the run is the unit, the prompt, the policy, and the rubric are the tooling. Sampling the output while nobody signs off on the policy change is inspecting parts while the mold goes uninspected.

## Production failures should become corrective action

The part of this framework I find most useful is the loop from production back into development.

When a non-blocking verifier catches a failure in a live run, that run becomes a new offline evaluation, so the failure is reproducible. The team changes the prompt, skill, harness, tool, or other part of the system. The candidate runs against the suite. If quality improves without unacceptable cost or latency, the change can move forward.

This is corrective and preventive action, the same six steps a quality system would run:

1. Contain the immediate issue.
2. Record the nonconformance.
3. Investigate the root cause.
4. Change the process, not just the affected unit.
5. Verify that the change worked.
6. Monitor for recurrence.

The distinction between correction and corrective action matters. Asking an agent to redo one weak brief is correction. Changing the system so that the failure becomes less likely — and adding a test so it cannot quietly return — is corrective action.

## Where the manufacturing analogy breaks

The parallel is useful but incomplete. First, most enterprise agents run something closer to a high-mix, make-to-order operation than a line of identical widgets: every request is different, incoming information varies wildly, and the quality standard sometimes depends on context. There may be no single tolerance band for "good strategy."

Second, agent behavior is probabilistic. The same task, environment, and configuration can produce a different trajectory on the next run. Variation is part of the process itself, so a single passing run proves very little.

Third, many important specifications are contestable. A hole is 5.00 millimeters or it isn't, but whether an account brief identifies the *right* commercial risk is a judgment call. Sometimes expert disagreement is a sign that the quality standard itself is underspecified.

Fourth, the act of measuring can change the system. Once verifier feedback is used for optimization, the agent begins adapting to the gauge. This is Goodhart's law in factory clothing: when a measure becomes the target, it can stop being a good measure. Agents, unlike physical parts, can effectively study the inspection rubric.

Finally, digital work makes 100% inspection economically possible in a way physical manufacturing often cannot. But total inspection is only as good as the verifier doing it, and checking every unit with a weak one mostly scales your confidence.

## The factory is the product

The biggest mistake in enterprise AI is grading the intelligence of the model while ignoring the reliability of the system around it. The useful questions are operational: What is the specification? Where should each failure be detected? Which defects stop delivery? What happens to a failure after it is found? The model matters, but durable advantage comes from defining quality, measuring it credibly, and feeding what you learn back into the process.

---

### Sources and further reading

- Toyota, ["Toyota Production System"](https://global.toyota/en/company/vision-and-philosophy/production-system/) (jidoka)
- FDA, ["Process Validation: General Principles and Practices"](https://www.fda.gov/files/drugs/published/Process-Validation--General-Principles-and-Practices.pdf)
- ASQ, ["What Is Cost of Quality?"](https://asq.org/quality-resources/cost-of-quality)
- NIST/SEMATECH, ["What Are Control Charts?"](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc31.htm) and ["Assessing Process Capability"](https://www.itl.nist.gov/div898/handbook/ppc/section4/ppc46.htm)
- NIST, [measurement repeatability and reproducibility terminology](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-d1-terminology)
